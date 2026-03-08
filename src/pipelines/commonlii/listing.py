"""Crawl CommonLII listing pages and extract case URLs.

Single responsibility: listing page HTML → list of CaseLink models.
Uses JsonCssExtractionStrategy for structured extraction of all case links.
"""

from __future__ import annotations

import json
import logging
import re
from datetime import date

from pydantic import BaseModel
from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CacheMode,
    CrawlerRunConfig,
)
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

from .constants import BASE_URL, SC_BASE_PATH, SC_RECENT_URL
from .errors import CrawlError

logger = logging.getLogger(__name__)

# CSS schema for extracting case links from listing pages
LISTING_SCHEMA = {
    "name": "case_links",
    "baseSelector": "li.make-database",
    "fields": [
        {
            "name": "url",
            "selector": "a",
            "type": "attribute",
            "attribute": "href",
        },
        {
            "name": "title",
            "selector": "a",
            "type": "text",
        },
    ],
}


class CaseLink(BaseModel):
    """A single case link extracted from a listing page."""

    url: str
    title: str
    year: int | None = None
    citation: str | None = None


def _parse_case_link(item: dict, base_path: str = SC_BASE_PATH) -> CaseLink | None:
    """Parse a raw extracted item into a CaseLink."""
    url = item.get("url", "").strip()
    title = item.get("title", "").strip()

    if not url or not title:
        return None

    # Make URL absolute
    if url.startswith("/"):
        url = BASE_URL + url
    elif not url.startswith("http"):
        url = f"{BASE_URL}{base_path}/{url}"

    # Extract year from URL pattern like 2024/312.html
    year_match = re.search(r"/(\d{4})/\d+\.html", url)
    year = int(year_match.group(1)) if year_match else None

    # Extract citation like [2024] PKSC 312
    citation_match = re.search(r"\[(\d{4})\]\s+PKSC\s+\d+", title)
    citation = citation_match.group(0) if citation_match else None

    return CaseLink(url=url, title=title, year=year, citation=citation)


async def _crawl_single_listing(
    crawler: AsyncWebCrawler,
    url: str,
    crawl_config: CrawlerRunConfig,
    base_path: str = SC_BASE_PATH,
) -> list[CaseLink]:
    """Crawl one listing page and parse results. Shared by both public functions."""
    result = await crawler.arun(url=url, config=crawl_config)

    if not result.success:
        raise CrawlError(f"Failed to crawl {url}: {result.error_message}")

    try:
        raw_items = json.loads(result.extracted_content) if result.extracted_content else []
    except json.JSONDecodeError as e:
        raise CrawlError(f"Malformed JSON from {url}: {e}") from e

    cases = []
    discarded = 0
    for item in raw_items:
        case = _parse_case_link(item, base_path)
        if case is not None:
            cases.append(case)
        else:
            discarded += 1

    if discarded > 0 and len(cases) == 0:
        raise CrawlError(
            f"All {discarded} items discarded from {url} — CSS schema may be broken"
        )
    if discarded > len(raw_items) * 0.5:
        logger.warning("%d/%d items discarded from %s", discarded, len(raw_items), url)

    logger.info("Parsed %d case links from %s (%d discarded)", len(cases), url, discarded)
    return cases


async def crawl_listing_page(url: str = SC_RECENT_URL) -> list[CaseLink]:
    """Crawl a CommonLII listing page and extract all case links.

    Raises CrawlError if the page cannot be crawled or parsed.
    """
    extraction_strategy = JsonCssExtractionStrategy(schema=LISTING_SCHEMA)

    browser_config = BrowserConfig(
        headless=True,
        extra_args=["--ignore-certificate-errors"],
        enable_stealth=True,
    )

    crawl_config = CrawlerRunConfig(
        extraction_strategy=extraction_strategy,
        cache_mode=CacheMode.BYPASS,
        magic=True,
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        return await _crawl_single_listing(crawler, url, crawl_config)


async def crawl_all_years(
    start_year: int = 2002,
    end_year: int | None = None,
) -> list[CaseLink]:
    """Crawl year-by-year index pages for comprehensive coverage.

    Raises CrawlError if ALL years fail (site likely down).
    Logs warnings for individual year failures.
    """
    if end_year is None:
        end_year = date.today().year

    all_cases: list[CaseLink] = []
    failed_years: list[int] = []
    total_years = end_year - start_year + 1

    browser_config = BrowserConfig(
        headless=True,
        extra_args=["--ignore-certificate-errors"],
        enable_stealth=True,
    )

    extraction_strategy = JsonCssExtractionStrategy(schema=LISTING_SCHEMA)
    crawl_config = CrawlerRunConfig(
        extraction_strategy=extraction_strategy,
        cache_mode=CacheMode.BYPASS,
        magic=True,
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        for year in range(start_year, end_year + 1):
            url = f"{BASE_URL}{SC_BASE_PATH}/{year}/"
            logger.info("Crawling year %d: %s", year, url)

            try:
                year_cases = await _crawl_single_listing(crawler, url, crawl_config)
                all_cases.extend(year_cases)
                logger.info("Year %d: %d cases", year, len(year_cases))
            except CrawlError as e:
                logger.error("Year %d failed: %s", year, e)
                failed_years.append(year)

    if len(failed_years) == total_years:
        raise CrawlError(
            f"All {total_years} years failed ({start_year}-{end_year}). Site may be down."
        )
    if failed_years:
        logger.warning(
            "%d/%d years failed: %s", len(failed_years), total_years, failed_years
        )

    logger.info("Total cases across all years: %d", len(all_cases))
    return all_cases
