"""Extract metadata and PDF URL from a CommonLII case page.

Single responsibility: case page HTML → CaseMetadata (title, citation, date, PDF URL).
Does NOT download the PDF — that's pdf_extract.py's job.
"""

from __future__ import annotations

import logging
import re
from html import unescape
from typing import Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from pydantic import BaseModel
from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CacheMode,
    CrawlerRunConfig,
)

logger = logging.getLogger(__name__)


class CaseMetadata(BaseModel):
    """Metadata extracted from a CommonLII case page."""

    page_url: str
    title: str
    citation: Optional[str] = None
    alt_citations: list[str] = []
    date_judgment: Optional[str] = None
    year: Optional[int] = None
    case_number: Optional[str] = None
    pdf_url: Optional[str] = None


def _parse_title(h2_text: str) -> dict:
    """Parse the h2 title into structured fields.

    Example: 'Aamir Afzal v. S. Akmal [2024] PKSC 242; 2024 SCP 240 (19 July 2024)'
    """
    # Decode HTML entities and normalize whitespace
    text = unescape(h2_text).strip()
    text = re.sub(r"\s+", " ", text)

    result: dict = {
        "title": text,
        "citation": None,
        "alt_citations": [],
        "date": None,
        "year": None,
        "case_number": None,
    }

    # Primary citation: [2024] PKSC 242
    primary = re.search(r"\[(\d{4})\]\s+PKSC\s+(\d+)", text)
    if primary:
        result["citation"] = primary.group(0)
        result["year"] = int(primary.group(1))
        result["case_number"] = f"PKSC-{primary.group(1)}-{primary.group(2)}"

    # Alternative citations: 2024 SCP 240, 2024 SCMR 123, etc.
    alt_pattern = r"\b(\d{4}\s+(?:SCP|SCMR|PLD|CLC|PCrLJ|PTD|PLC|CLD|YLR|MLD)\s+\d+)\b"
    result["alt_citations"] = re.findall(alt_pattern, text)

    # Date patterns — handle multiple formats:
    # (19 July 2024), (19th July 2024), (July 19, 2024), (19-07-2024)
    date_patterns = [
        r"\((\d{1,2}(?:st|nd|rd|th)?\s+\w+\s+\d{4})\)",  # 19 July 2024 / 19th July 2024
        r"\((\w+\s+\d{1,2},?\s+\d{4})\)",                  # July 19, 2024
        r"\((\d{1,2}[-/]\d{1,2}[-/]\d{4})\)",               # 19-07-2024 / 19/07/2024
    ]
    for pattern in date_patterns:
        date_match = re.search(pattern, text)
        if date_match:
            result["date"] = date_match.group(1)
            break

    return result


def _extract_from_html(html: str, page_url: str) -> CaseMetadata | None:
    """Extract metadata from raw case page HTML using BeautifulSoup."""
    if not html or len(html) < 100:
        logger.error("Empty/short HTML from %s (%d chars)", page_url, len(html) if html else 0)
        return None

    # Detect non-case pages (captcha, rate limit, error pages)
    html_lower = html.lower()
    if "captcha" in html_lower or "rate limit" in html_lower or "<title>410 gone</title>" in html_lower:
        logger.error("Received non-case page (captcha/error) from %s", page_url)
        return None

    soup = BeautifulSoup(html, "lxml")

    # Extract h2 title
    h2 = soup.find("h2")
    if not h2:
        logger.error("No <h2> tag found on %s", page_url)
        return None

    h2_text = h2.get_text(strip=True)
    parsed = _parse_title(h2_text)

    # Extract PDF URL from <object data="...pdf">
    pdf_url = None
    obj = soup.find("object", attrs={"data": re.compile(r"\.pdf$")})
    if obj:
        pdf_path = obj.get("data", "")
        pdf_url = urljoin(page_url, pdf_path)

    # Also check for <a href="...pdf"> download link as fallback
    if not pdf_url:
        pdf_link = soup.find("a", href=re.compile(r"\.pdf$"))
        if pdf_link:
            pdf_url = urljoin(page_url, pdf_link.get("href", ""))

    return CaseMetadata(
        page_url=page_url,
        title=parsed["title"],
        citation=parsed.get("citation"),
        alt_citations=parsed.get("alt_citations", []),
        date_judgment=parsed.get("date"),
        year=parsed.get("year"),
        case_number=parsed.get("case_number"),
        pdf_url=pdf_url,
    )


async def extract_case_metadata(
    url: str,
    crawler: AsyncWebCrawler | None = None,
) -> CaseMetadata | None:
    """Crawl a single case page and extract metadata + PDF URL.

    Returns None if the page cannot be crawled or parsed.
    """
    crawl_config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS, magic=True)

    try:
        if crawler is not None:
            result = await crawler.arun(url=url, config=crawl_config)
        else:
            browser_config = BrowserConfig(
                headless=True,
                extra_args=["--ignore-certificate-errors"],
                enable_stealth=True,
            )
            async with AsyncWebCrawler(config=browser_config) as c:
                result = await c.arun(url=url, config=crawl_config)
    except Exception as e:
        logger.error("Browser error crawling %s: %s", url, e)
        return None

    if not result.success:
        logger.error("Crawl failed for %s: %s", url, result.error_message)
        return None

    return _extract_from_html(result.html, url)
