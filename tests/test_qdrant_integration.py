"""End-to-end test: extract → embed → ingest → search against real judgments.

Uses in-memory Qdrant (no server needed).
Requires VOYAGE_API_KEY in .env for embedding.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.extractors.criminal.pipeline import extract_criminal_judgment
from src.qdrant.collections import (
    create_collection,
    get_client,
    get_collection_info,
)
from src.qdrant.ingestion import ingest_judgment
from src.qdrant.search import (
    build_filter,
    format_results,
    search_dense,
    search_hybrid,
    search_sparse,
)

SAMPLES_PATH = Path(__file__).parent.parent / "data" / "evaluation" / "criminal_samples.json"


def run_integration_test():
    print("=" * 70)
    print("Qdrant Integration Test: Extract → Embed → Ingest → Search")
    print("=" * 70)

    # ── Step 1: Load samples ──
    with open(SAMPLES_PATH) as f:
        samples = json.load(f)
    print(f"\n1. Loaded {len(samples)} judgment samples")

    # ── Step 2: Create in-memory Qdrant collection ──
    client = get_client()
    create_collection(client)
    info = get_collection_info(client)
    print(f"2. Collection created: {info}")

    # ── Step 3: Extract + Ingest each judgment ──
    print(f"\n3. Extracting and ingesting {len(samples)} judgments...")
    point_ids = []

    for idx, sample in enumerate(samples):
        case_id = sample["case_id"]
        text = sample["text"]
        print(f"\n   [{idx+1}/{len(samples)}] {case_id} ({len(text):,} chars)")

        # Run Tier A only (skip LLM to keep test fast and free)
        result = extract_criminal_judgment(text, skip_llm=True)
        payload = result.to_qdrant_payload()
        print(f"   Tier A: {len(payload)} payload fields")

        # Ingest into Qdrant
        case_number = payload.get("case_number", case_id)
        pid = ingest_judgment(
            client=client,
            text=text,
            payload=payload,
            case_number=case_number,
            source_url=f"test://{case_id}",
        )
        point_ids.append(pid)
        print(f"   Ingested: {pid[:12]}...")

    info = get_collection_info(client)
    print(f"\n   Collection after ingestion: {info}")
    assert info["points_count"] == len(samples), (
        f"Expected {len(samples)} points, got {info['points_count']}"
    )

    # ── Step 4: Test dense search ──
    print("\n4. Dense (semantic) search tests:")

    test_queries = [
        "murder conviction section 302 PPC",
        "bail application in criminal case",
        "contempt of court proceedings",
    ]

    for query in test_queries:
        results = search_dense(client, query, limit=3)
        formatted = format_results(results)
        print(f"\n   Query: \"{query}\"")
        for r in formatted:
            print(f"     {r['score']:.4f}  {r['case_number']}")
        # Check that results are returned
        assert len(results) > 0, f"No results for: {query}"

    # ── Step 5: Test sparse search ──
    print("\n5. Sparse (keyword) search tests:")

    sparse_queries = [
        "section 302 section 34 PPC",
        "SCMR 2019",
        "suo motu",
    ]

    for query in sparse_queries:
        results = search_sparse(client, query, limit=3)
        formatted = format_results(results)
        print(f"\n   Query: \"{query}\"")
        for r in formatted:
            print(f"     {r['score']:.4f}  {r['case_number']}")

    # ── Step 6: Test hybrid search ──
    print("\n6. Hybrid (dense + sparse fused) search tests:")

    hybrid_queries = [
        "murder appeal eyewitness testimony section 302 PPC",
        "criminal miscellaneous application bail",
    ]

    for query in hybrid_queries:
        results = search_hybrid(client, query, limit=3)
        formatted = format_results(results)
        print(f"\n   Query: \"{query}\"")
        for r in formatted:
            print(f"     {r['score']:.4f}  {r['case_number']}")
        assert len(results) > 0, f"No hybrid results for: {query}"

    # ── Step 7: Test filtered search ──
    print("\n7. Filtered search tests:")

    filt = build_filter(court_level="supreme_court")
    results = search_dense(client, "murder case", limit=5, filters=filt)
    formatted = format_results(results)
    print(f"\n   Query: \"murder case\" + filter: court_level=supreme_court")
    for r in formatted:
        print(f"     {r['score']:.4f}  {r['case_number']} ({r['court_level']})")
        assert r["court_level"] == "supreme_court", (
            f"Filter failed: got {r['court_level']}"
        )

    # ── Step 8: Test idempotent re-ingestion ──
    print("\n8. Idempotent re-ingestion test:")
    sample = samples[0]
    result = extract_criminal_judgment(sample["text"], skip_llm=True)
    payload = result.to_qdrant_payload()
    pid = ingest_judgment(
        client=client,
        text=sample["text"],
        payload=payload,
        case_number=payload.get("case_number", sample["case_id"]),
        source_url=f"test://{sample['case_id']}",
    )
    info = get_collection_info(client)
    print(f"   Re-ingested {sample['case_id']}, points_count still: {info['points_count']}")
    assert info["points_count"] == len(samples), "Re-ingestion should not duplicate points"

    # ── Done ──
    print("\n" + "=" * 70)
    print("ALL INTEGRATION TESTS PASSED")
    print("=" * 70)


if __name__ == "__main__":
    run_integration_test()
