"""Tests for CommonLII crawler pipeline.

Unit tests (no network) test parsing logic.
Integration tests (marked with comments) test live crawling.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.pipelines.commonlii.case_page import CaseMetadata, _extract_from_html, _parse_title
from src.pipelines.commonlii.errors import CrawlError
from src.pipelines.commonlii.listing import CaseLink, _parse_case_link
from src.pipelines.commonlii.pdf_extract import _safe_filename


# ── Unit Tests (no network) ─────────────────────────────────────────


def test_parse_case_link_absolute():
    item = {"url": "/pk/cases/PKSC/2024/312.html", "title": "Test [2024] PKSC 312 (1 Jan 2024)"}
    result = _parse_case_link(item)
    assert result is not None
    assert result.url == "https://www.commonlii.org/pk/cases/PKSC/2024/312.html"
    assert result.year == 2024
    assert result.citation == "[2024] PKSC 312"


def test_parse_case_link_relative():
    item = {"url": "2024/312.html", "title": "Test [2024] PKSC 312 (1 Jan 2024)"}
    result = _parse_case_link(item)
    assert result is not None
    assert "commonlii.org" in result.url
    assert result.url.endswith("2024/312.html")


def test_parse_case_link_empty_discarded():
    assert _parse_case_link({"url": "", "title": ""}) is None
    assert _parse_case_link({"url": "test.html", "title": ""}) is None


def test_parse_title_standard():
    p = _parse_title("Aamir v. Akmal [2024] PKSC 242; 2024 SCP 240 (19 July 2024)")
    assert p["citation"] == "[2024] PKSC 242"
    assert p["case_number"] == "PKSC-2024-242"
    assert "2024 SCP 240" in p["alt_citations"]
    assert p["date"] == "19 July 2024"


def test_parse_title_ordinal_date():
    p = _parse_title("Test [2020] PKSC 100 (19th July 2020)")
    assert p["date"] == "19th July 2020"


def test_parse_title_numeric_date():
    p = _parse_title("Test [2018] PKSC 50 (15-07-2018)")
    assert p["date"] == "15-07-2018"


def test_parse_title_no_citation():
    p = _parse_title("Some case title with no standard citation")
    assert p["citation"] is None
    assert p["case_number"] is None


def test_extract_from_html_full():
    html = (
        '<h2 class="make-database">'
        "Aamir v. Akmal [2024] PKSC 242; 2024 SCP 240 (19 July 2024)"
        "</h2>"
        '<object data="/pk/cases/PKSC/2024/242.pdf" type="application/pdf"></object>'
    )
    m = _extract_from_html(html, "http://www.commonlii.org/pk/cases/PKSC/2024/242.html")
    assert m is not None
    assert m.citation == "[2024] PKSC 242"
    assert m.pdf_url == "http://www.commonlii.org/pk/cases/PKSC/2024/242.pdf"
    assert m.date_judgment == "19 July 2024"


def test_extract_from_html_entities():
    html = '<h2>Smith &amp; Jones v. State [2023] PKSC 100 (1st March 2023)</h2><object data="100.pdf"></object>'
    m = _extract_from_html(html, "http://www.commonlii.org/pk/cases/PKSC/2023/100.html")
    assert m is not None
    assert "&amp;" not in m.title
    assert "Smith & Jones" in m.title
    assert m.pdf_url == "http://www.commonlii.org/pk/cases/PKSC/2023/100.pdf"


def test_extract_from_html_error_page():
    m = _extract_from_html("<title>410 Gone</title><h1>Gone</h1>", "http://test.com")
    assert m is None


def test_extract_from_html_empty():
    m = _extract_from_html("", "http://test.com")
    assert m is None


def test_extract_from_html_no_h2():
    m = _extract_from_html("<html><body><p>No heading here</p></body></html>", "http://test.com")
    assert m is None


def test_pydantic_model_serialization():
    meta = CaseMetadata(
        page_url="http://test.com",
        title="Test",
        citation="[2024] PKSC 1",
    )
    data = meta.model_dump()
    assert isinstance(data, dict)
    assert data["citation"] == "[2024] PKSC 1"
    assert data["alt_citations"] == []


def test_safe_filename():
    assert _safe_filename("http://commonlii.org/pk/cases/PKSC/2024/242.pdf") == "242.pdf"
    assert _safe_filename("http://bad.com/../../etc/passwd") == "passwd.pdf"
    assert ".." not in _safe_filename("http://bad.com/%2E%2E/test.pdf")


def test_crawl_error():
    try:
        raise CrawlError("test error")
    except CrawlError as e:
        assert str(e) == "test error"


def test_case_link_is_pydantic():
    link = CaseLink(url="http://test.com", title="Test")
    assert link.year is None
    data = link.model_dump()
    assert isinstance(data, dict)


# ── Integration Tests (require network) ─────────────────────────────


async def _test_live_listing():
    """Test live crawl of listing page."""
    from src.pipelines.commonlii.listing import crawl_listing_page

    cases = await crawl_listing_page()
    assert len(cases) > 100, f"Expected 2000+ cases, got {len(cases)}"
    assert cases[0].url.startswith("https://")
    assert cases[0].citation is not None
    return cases


async def _test_live_case_metadata(case_url: str):
    """Test live case page metadata extraction."""
    from src.pipelines.commonlii.case_page import extract_case_metadata

    meta = await extract_case_metadata(case_url)
    assert meta is not None, f"Metadata extraction returned None for {case_url}"
    assert meta.pdf_url is not None, "No PDF URL found"
    assert meta.citation is not None, "No citation found"
    return meta


async def _test_live_pdf_extraction(pdf_url: str):
    """Test live PDF download + text extraction."""
    from src.pipelines.commonlii.pdf_extract import download_and_extract

    text = await download_and_extract(pdf_url)
    assert len(text) > 100, f"Too little text: {len(text)} chars"
    return text


async def _test_live_pipeline():
    """Test 3-case end-to-end pipeline."""
    from src.pipelines.commonlii.pipeline import crawl_recent

    results = await crawl_recent(output_dir=Path("/tmp/commonlii_test"), limit=3)
    assert len(results) == 3
    with_text = sum(1 for r in results if r["text"])
    assert with_text >= 2, f"Expected 2+ cases with text, got {with_text}"
    return results


async def run_integration_tests():
    """Run all integration tests."""
    import logging
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    print("=== Integration Test: Listing ===")
    cases = await _test_live_listing()
    print(f"  PASS: {len(cases)} cases found")

    print("\n=== Integration Test: Case Metadata ===")
    meta = await _test_live_case_metadata(cases[0].url)
    print(f"  PASS: {meta.citation} → {meta.pdf_url}")

    print("\n=== Integration Test: PDF Extraction ===")
    text = await _test_live_pdf_extraction(meta.pdf_url)
    print(f"  PASS: {len(text)} chars extracted")

    print("\n=== Integration Test: Pipeline (3 cases) ===")
    results = await _test_live_pipeline()
    print(f"  PASS: {len(results)} results")

    print("\n" + "=" * 50)
    print("ALL INTEGRATION TESTS PASSED")


if __name__ == "__main__":
    # Run unit tests
    print("=== Unit Tests ===")
    for name, func in sorted(globals().items()):
        if name.startswith("test_") and callable(func):
            func()
            print(f"  {name}: PASS")

    print("\n=== Running Integration Tests ===")
    asyncio.run(run_integration_tests())
