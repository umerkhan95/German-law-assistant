"""CommonLII Supreme Court crawler pipeline.

Orchestrates the full flow: listing → case pages → PDF text → JSON output.
Single responsibility: coordinate the pipeline stages with crash resilience.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
from pathlib import Path
from typing import Optional

from .case_page import CaseMetadata, extract_case_metadata
from .errors import CrawlError
from .listing import CaseLink, crawl_all_years, crawl_listing_page
from .pdf_extract import download_and_extract

logger = logging.getLogger(__name__)

DEFAULT_OUTPUT_DIR = Path(
    os.environ.get("COMMONLII_OUTPUT_DIR", "data/commonlii")
)

# Save checkpoint every N cases
CHECKPOINT_INTERVAL = 25


async def crawl_recent(
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    limit: int | None = None,
) -> list[dict]:
    """Crawl the recent decisions page and extract all judgments.

    Raises CrawlError if the listing page cannot be crawled.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Stage 1: Get case links from listing page
    logger.info("Stage 1: Crawling recent decisions listing...")
    case_links = await crawl_listing_page()
    logger.info("Found %d case links", len(case_links))

    if limit:
        case_links = case_links[:limit]
        logger.info("Limited to %d cases", limit)

    # Stage 2+3: For each case, get metadata and extract PDF text
    results = await _process_cases(case_links, output_dir)

    # Save final results
    _save_results(results, output_dir / "recent_results.jsonl")
    _save_summary(results, output_dir / "recent_summary.json")
    return results


async def crawl_full(
    start_year: int = 2002,
    end_year: int | None = None,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    limit_per_year: int | None = None,
) -> list[dict]:
    """Crawl all years for comprehensive coverage.

    Raises CrawlError if ALL years fail.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Stage 1: Get all case links across years
    logger.info("Stage 1: Crawling years %d-%s...", start_year, end_year or "current")
    case_links = await crawl_all_years(start_year, end_year)
    logger.info("Found %d total case links", len(case_links))

    if limit_per_year:
        by_year: dict[Optional[int], list[CaseLink]] = {}
        for link in case_links:
            by_year.setdefault(link.year, []).append(link)

        limited = []
        for year, year_cases in by_year.items():
            taken = year_cases[:limit_per_year]
            limited.extend(taken)
            if len(year_cases) > limit_per_year:
                logger.info(
                    "Year %s: limited %d → %d cases",
                    year or "unknown", len(year_cases), len(taken),
                )
        case_links = limited

    # Stage 2+3: Process all cases
    results = await _process_cases(case_links, output_dir)

    # Save final results
    _save_results(results, output_dir / "full_results.jsonl")
    _save_summary(results, output_dir / "full_summary.json")
    return results


async def _process_cases(
    case_links: list[CaseLink],
    output_dir: Path,
) -> list[dict]:
    """Process a list of case links: extract metadata + PDF text.

    - Per-case try/except so one failure doesn't kill the batch
    - Checkpoint saves every CHECKPOINT_INTERVAL cases
    - Tracks seen URLs to avoid duplicates within a run
    """
    from crawl4ai import AsyncWebCrawler, BrowserConfig

    results: list[dict] = []
    seen_urls: set[str] = set()
    pdf_dir = output_dir / "pdfs"
    pdf_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_path = output_dir / "checkpoint.jsonl"

    browser_config = BrowserConfig(
        headless=True,
        extra_args=["--ignore-certificate-errors"],
        enable_stealth=True,
    )

    failed_count = 0
    async with AsyncWebCrawler(config=browser_config) as crawler:
        for idx, link in enumerate(case_links):
            # Deduplicate within run
            if link.url in seen_urls:
                logger.debug("Skipping duplicate URL: %s", link.url)
                continue
            seen_urls.add(link.url)

            try:
                result = await _process_single_case(link, crawler, pdf_dir)
                results.append(result)

                if result["text"]:
                    logger.info(
                        "[%d/%d] OK: %s — %d chars",
                        idx + 1, len(case_links),
                        result.get("citation") or result.get("case_number") or "?",
                        result["text_length"],
                    )
                else:
                    logger.warning(
                        "[%d/%d] EMPTY: %s — no text extracted",
                        idx + 1, len(case_links),
                        result.get("citation") or link.url,
                    )

            except Exception as e:
                failed_count += 1
                logger.error(
                    "[%d/%d] FAILED: %s: %s",
                    idx + 1, len(case_links), link.url, e,
                    exc_info=True,
                )
                results.append({
                    "page_url": link.url,
                    "title": link.title,
                    "citation": link.citation,
                    "text": "",
                    "text_length": 0,
                    "error": str(e),
                    "source": "commonlii",
                    "court": "supreme_court",
                })

            # Checkpoint save
            if len(results) % CHECKPOINT_INTERVAL == 0 and results:
                _save_results(results, checkpoint_path)
                logger.info("Checkpoint: %d results saved", len(results))

    with_text = sum(1 for r in results if r["text"])
    logger.info(
        "Processed %d cases: %d with text, %d empty, %d failed",
        len(results), with_text, len(results) - with_text - failed_count, failed_count,
    )
    return results


async def _process_single_case(
    link: CaseLink,
    crawler: AsyncWebCrawler,
    pdf_dir: Path,
) -> dict:
    """Process a single case: metadata extraction + PDF text extraction."""
    # Stage 2: Get metadata + PDF URL from case page
    metadata = await extract_case_metadata(link.url, crawler=crawler)

    if metadata is None:
        return {
            "page_url": link.url,
            "title": link.title,
            "citation": link.citation,
            "text": "",
            "text_length": 0,
            "error": "metadata_extraction_failed",
            "source": "commonlii",
            "court": "supreme_court",
        }

    # Stage 3: Download and extract PDF text
    text = ""
    if metadata.pdf_url:
        text = await download_and_extract(metadata.pdf_url, pdf_dir)
    else:
        logger.warning("No PDF URL for %s", link.url)

    return {
        **metadata.model_dump(),
        "text": text,
        "text_length": len(text),
        "source": "commonlii",
        "court": "supreme_court",
    }


def _save_results(results: list[dict], path: Path) -> None:
    """Save results as line-delimited JSON (JSONL) for append safety."""
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(path, "w") as f:
            for result in results:
                f.write(json.dumps(result, ensure_ascii=False) + "\n")
        logger.info("Saved %d results to %s", len(results), path)
    except (OSError, TypeError) as e:
        logger.error("Failed to save results to %s: %s", path, e)
        raise


def _save_summary(results: list[dict], path: Path) -> None:
    """Save a summary of the crawl run (without full text)."""
    with_text = sum(1 for r in results if r.get("text"))
    errors = sum(1 for r in results if r.get("error"))
    summary = {
        "total_cases": len(results),
        "with_text": with_text,
        "empty_text": len(results) - with_text,
        "errors": errors,
        "cases": [
            {
                "citation": r.get("citation"),
                "case_number": r.get("case_number"),
                "date_judgment": r.get("date_judgment"),
                "text_length": r.get("text_length", 0),
                "error": r.get("error"),
            }
            for r in results
        ],
    }
    try:
        with open(path, "w") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
    except (OSError, TypeError) as e:
        logger.error("Failed to save summary to %s: %s", path, e)


async def main():
    """CLI entry point."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
    )

    import argparse

    parser = argparse.ArgumentParser(description="CommonLII Supreme Court Crawler")
    parser.add_argument("--mode", choices=["recent", "full"], default="recent")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--output", type=str, default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--start-year", type=int, default=2002)
    parser.add_argument("--end-year", type=int, default=None)
    args = parser.parse_args()

    output_dir = Path(args.output)

    if args.mode == "recent":
        results = await crawl_recent(output_dir, limit=args.limit)
    else:
        results = await crawl_full(
            args.start_year, args.end_year, output_dir,
            limit_per_year=args.limit,
        )

    with_text = sum(1 for r in results if r["text"])
    errors = sum(1 for r in results if r.get("error"))
    logger.info("Done: %d cases, %d with text, %d errors", len(results), with_text, errors)


if __name__ == "__main__":
    asyncio.run(main())
