"""Download CommonLII PDFs and extract judgment text.

Single responsibility: PDF URL → full judgment text string.
Uses PyMuPDF (fitz) for text extraction. Falls back to pdfplumber
for complex layouts where PyMuPDF yields sparse results.
"""

from __future__ import annotations

import logging
import re
import tempfile
import time
from pathlib import Path
from urllib.parse import unquote, urlparse

import fitz  # PyMuPDF
import httpx
import pdfplumber

logger = logging.getLogger(__name__)

# Browser-like headers required by CommonLII
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "application/pdf,*/*",
}

# If PyMuPDF extracts fewer chars per page than this, try pdfplumber
MIN_CHARS_PER_PAGE = 100

# Retry settings for PDF downloads
MAX_RETRIES = 3
RETRY_BACKOFF = 2  # seconds, doubles each retry


def _safe_filename(url: str) -> str:
    """Derive a safe filename from a URL."""
    parsed = urlparse(url)
    name = Path(unquote(parsed.path)).name
    # Sanitize: keep only safe chars
    name = re.sub(r"[^A-Za-z0-9._-]", "_", name)
    if not name.endswith(".pdf"):
        name += ".pdf"
    return name


def extract_text_pymupdf(pdf_path: str | Path) -> tuple[str, int]:
    """Extract text from PDF using PyMuPDF. Returns (text, page_count)."""
    try:
        with fitz.open(str(pdf_path)) as doc:
            pages = [page.get_text() for page in doc]
            return "\n\n".join(pages), len(pages)
    except Exception as e:
        logger.error("PyMuPDF failed on %s: %s", pdf_path, e)
        return "", 0


def extract_text_pdfplumber(pdf_path: str | Path) -> str:
    """Extract text from PDF using pdfplumber (better for complex layouts)."""
    try:
        pages = []
        with pdfplumber.open(str(pdf_path)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    pages.append(text)
        return "\n\n".join(pages)
    except Exception as e:
        logger.error("pdfplumber failed on %s: %s", pdf_path, e)
        return ""


def extract_text_from_pdf(pdf_path: str | Path) -> str:
    """Extract text from a local PDF file. Tries PyMuPDF first, falls back to pdfplumber.

    Returns empty string only if both extractors fail.
    """
    path = Path(pdf_path)
    if not path.exists():
        logger.error("PDF not found: %s", path)
        return ""

    # Try PyMuPDF first (faster)
    text, page_count = extract_text_pymupdf(path)

    # Check quality — if too little text per page, try pdfplumber
    chars_per_page = len(text) / max(page_count, 1)
    if chars_per_page < MIN_CHARS_PER_PAGE:
        logger.info(
            "PyMuPDF: %.0f chars/page (<%d), trying pdfplumber: %s",
            chars_per_page, MIN_CHARS_PER_PAGE, path.name,
        )
        plumber_text = extract_text_pdfplumber(path)
        if len(plumber_text) > len(text):
            text = plumber_text

    if not text.strip():
        logger.warning(
            "No text extracted from %s — possible scanned/image PDF (%d pages)",
            path.name, page_count,
        )

    return text.strip()


async def download_pdf(
    url: str,
    output_dir: str | Path | None = None,
    max_retries: int = MAX_RETRIES,
) -> Path | None:
    """Download a PDF from CommonLII with retry logic.

    Returns Path to downloaded file, or None on failure.
    """
    if output_dir is None:
        output_dir = Path(tempfile.mkdtemp(prefix="commonlii_"))
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

    filename = _safe_filename(url)
    output_path = output_dir / filename

    last_error = None
    for attempt in range(1, max_retries + 1):
        try:
            async with httpx.AsyncClient(
                verify=False, follow_redirects=True,
                timeout=httpx.Timeout(connect=10.0, read=60.0, write=10.0, pool=10.0),
            ) as client:
                response = await client.get(url, headers=HEADERS)
                response.raise_for_status()

                if b"%PDF" not in response.content[:10]:
                    logger.error("Not a PDF (%d bytes): %s", len(response.content), url)
                    return None

                output_path.write_bytes(response.content)
                logger.info("Downloaded %s (%d bytes)", filename, len(response.content))
                return output_path

        except (httpx.HTTPError, httpx.TimeoutException) as e:
            last_error = e
            if attempt < max_retries:
                wait = RETRY_BACKOFF ** attempt
                logger.warning(
                    "Download attempt %d/%d failed for %s: %s (retrying in %ds)",
                    attempt, max_retries, url, e, wait,
                )
                time.sleep(wait)

    logger.error("Download failed after %d attempts for %s: %s", max_retries, url, last_error)
    return None


async def download_and_extract(url: str, output_dir: str | Path | None = None) -> str:
    """Download a PDF and extract its text in one step.

    Returns extracted text. Empty string on failure.
    """
    pdf_path = await download_pdf(url, output_dir)
    if pdf_path is None:
        return ""

    text = extract_text_from_pdf(pdf_path)
    logger.info("Extracted %d chars from %s", len(text), pdf_path.name)
    return text
