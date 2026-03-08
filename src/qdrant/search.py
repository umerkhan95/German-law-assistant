"""Search pk_judgments collection with dense, sparse, or hybrid queries.

Single responsibility: convert a search query into Qdrant search calls
and return ranked results.
"""

from __future__ import annotations

import logging
from typing import Any, Optional

from qdrant_client import QdrantClient, models

from .collections import COLLECTION_NAME
from .embeddings import embed_query
from .ingestion import _build_sparse_vector

logger = logging.getLogger(__name__)


def search_dense(
    client: QdrantClient,
    query: str,
    limit: int = 10,
    filters: Optional[models.Filter] = None,
    score_threshold: Optional[float] = None,
) -> list[models.ScoredPoint]:
    """Semantic search using dense (Voyage) vectors only."""
    query_vector = embed_query(query)

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        using="dense",
        limit=limit,
        query_filter=filters,
        score_threshold=score_threshold,
    ).points

    logger.info("Dense search: %d results for '%s'", len(results), query[:80])
    return results


def search_sparse(
    client: QdrantClient,
    query: str,
    limit: int = 10,
    filters: Optional[models.Filter] = None,
) -> list[models.ScoredPoint]:
    """Keyword search using sparse (BM25) vectors. Best for exact citations."""
    sparse_vector = _build_sparse_vector(query)
    if sparse_vector is None:
        logger.warning("No extractable tokens for sparse search: '%s'", query[:80])
        return []

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=sparse_vector,
        using="sparse",
        limit=limit,
        query_filter=filters,
    ).points

    logger.info("Sparse search: %d results for '%s'", len(results), query[:80])
    return results


def search_hybrid(
    client: QdrantClient,
    query: str,
    limit: int = 10,
    filters: Optional[models.Filter] = None,
    dense_limit: int = 20,
    sparse_limit: int = 20,
) -> list[models.ScoredPoint]:
    """Hybrid search: fuse dense + sparse results via Reciprocal Rank Fusion.

    Prefetches from both vector spaces, then fuses with RRF for final ranking.
    This combines semantic understanding with exact keyword/citation matching.
    """
    query_dense = embed_query(query)
    query_sparse = _build_sparse_vector(query)

    prefetches = [
        models.Prefetch(
            query=query_dense,
            using="dense",
            limit=dense_limit,
            filter=filters,
        ),
    ]

    if query_sparse is not None:
        prefetches.append(
            models.Prefetch(
                query=query_sparse,
                using="sparse",
                limit=sparse_limit,
                filter=filters,
            ),
        )

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        prefetch=prefetches,
        query=models.FusionQuery(fusion=models.Fusion.RRF),
        limit=limit,
    ).points

    logger.info("Hybrid search: %d results for '%s'", len(results), query[:80])
    return results


def build_filter(**kwargs: Any) -> models.Filter:
    """Build a Qdrant filter from keyword arguments.

    Example:
        build_filter(court_level="supreme_court", case_type="appeal")
    """
    conditions = []
    for key, value in kwargs.items():
        if value is None:
            continue
        if isinstance(value, list):
            conditions.append(
                models.FieldCondition(
                    key=key,
                    match=models.MatchAny(any=value),
                )
            )
        else:
            conditions.append(
                models.FieldCondition(
                    key=key,
                    match=models.MatchValue(value=value),
                )
            )

    return models.Filter(must=conditions)


def format_results(results: list[models.ScoredPoint]) -> list[dict]:
    """Convert Qdrant ScoredPoint list to simple dicts for display."""
    formatted = []
    for r in results:
        entry = {
            "id": r.id,
            "score": round(r.score, 4) if r.score else 0,
            "case_number": r.payload.get("case_number") if r.payload else None,
            "case_title": r.payload.get("case_title") if r.payload else None,
            "court_level": r.payload.get("court_level") if r.payload else None,
            "case_type": r.payload.get("case_type") if r.payload else None,
            "date_judgment": r.payload.get("date_judgment") if r.payload else None,
            "judgment_type": r.payload.get("judgment_type") if r.payload else None,
        }
        formatted.append(entry)
    return formatted
