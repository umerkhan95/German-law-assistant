"""Ingest extracted criminal judgments into Qdrant pk_judgments collection.

Single responsibility: take a CriminalExtractionResult + raw text → embed → upsert.
Handles both dense (Voyage) and sparse (BM25) vectors.
"""

from __future__ import annotations

import hashlib
import logging
import re
import uuid
from collections import Counter
from typing import Optional

from qdrant_client import QdrantClient, models

from .collections import COLLECTION_NAME
from .embeddings import embed_batch, embed_document

logger = logging.getLogger(__name__)


def _make_point_id(case_number: str, source_url: str) -> str:
    """Generate a deterministic UUID point ID from case identifiers.

    Qdrant accepts either unsigned int or UUID string IDs.
    Uses UUID3 (MD5-based) so re-ingesting the same case overwrites.
    """
    key = f"{case_number}|{source_url}".strip()
    return str(uuid.uuid3(uuid.NAMESPACE_URL, key))


def _build_sparse_vector(text: str) -> Optional[models.SparseVector]:
    """Build a simple term-frequency sparse vector for BM25-style matching.

    Extracts legal terms, citation patterns, and section numbers.
    Qdrant's sparse vector uses {indices: [...], values: [...]}.
    We hash each token to an index and use TF as value.
    """
    text_lower = text.lower()

    # Extract meaningful tokens: words 3+ chars, legal citations, section numbers
    tokens = re.findall(r"\b[a-z]{3,}\b", text_lower)

    # Also extract PPC/CrPC section references as compound tokens
    section_refs = re.findall(
        r"section\s+\d+[a-z]?(?:\s*[-/]\s*\d+[a-z]?)?",
        text_lower,
    )
    tokens.extend(section_refs)

    # Extract citation patterns (PLD, SCMR, etc.)
    citations = re.findall(
        r"\b(?:pld|scmr|clc|pcrlj|ptd|plc|cld|ylr|mld)\s+\d{4}\b",
        text_lower,
    )
    tokens.extend(citations)

    if not tokens:
        return None

    # Count term frequencies
    tf = Counter(tokens)

    # Hash tokens to integer indices (deterministic)
    indices = []
    values = []
    for token, count in tf.items():
        idx = int(hashlib.md5(token.encode()).hexdigest()[:8], 16)
        indices.append(idx)
        values.append(float(count))

    return models.SparseVector(indices=indices, values=values)


def ingest_judgment(
    client: QdrantClient,
    text: str,
    payload: dict,
    case_number: str,
    source_url: str = "",
) -> str:
    """Embed and upsert a single judgment into pk_judgments.

    Args:
        client: Qdrant client.
        text: Full judgment text (used for embedding).
        payload: Flat dict from CriminalExtractionResult.to_qdrant_payload().
        case_number: Case number for deduplication.
        source_url: Source URL for deduplication.

    Returns:
        The point ID that was upserted.
    """
    point_id = _make_point_id(case_number, source_url)

    # Dense embedding via Voyage
    dense_vector = embed_document(text)

    # Sparse vector for BM25-style keyword matching
    vectors: dict = {"dense": dense_vector}
    sparse_vector = _build_sparse_vector(text)
    if sparse_vector is not None:
        vectors["sparse"] = sparse_vector

    point = models.PointStruct(
        id=point_id,
        vector=vectors,
        payload=payload,
    )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[point],
    )

    logger.info(
        "Upserted judgment %s (id=%s, payload_fields=%d)",
        case_number,
        point_id[:12],
        len(payload),
    )
    return point_id


def ingest_batch(
    client: QdrantClient,
    items: list[dict],
) -> list[str]:
    """Ingest a batch of judgments.

    Each item must have:
        - "text": full judgment text
        - "payload": dict from to_qdrant_payload()
        - "case_number": str
        - "source_url": str (optional)

    Returns:
        List of upserted point IDs.
    """
    if not items:
        return []

    texts = [item["text"] for item in items]
    logger.info("Embedding %d judgments in batch...", len(texts))
    dense_vectors = embed_batch(texts, input_type="document")

    points = []
    point_ids = []

    for idx, item in enumerate(items):
        case_number = item["case_number"]
        source_url = item.get("source_url", "")
        point_id = _make_point_id(case_number, source_url)
        point_ids.append(point_id)

        vectors: dict = {"dense": dense_vectors[idx]}
        sparse_vector = _build_sparse_vector(item["text"])
        if sparse_vector is not None:
            vectors["sparse"] = sparse_vector

        point = models.PointStruct(
            id=point_id,
            vector=vectors,
            payload=item["payload"],
        )
        points.append(point)

    # Upsert in chunks of 100 (Qdrant recommended batch size)
    batch_size = 100
    for i in range(0, len(points), batch_size):
        batch = points[i : i + batch_size]
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=batch,
        )
        logger.info(
            "Upserted batch %d-%d / %d",
            i + 1,
            i + len(batch),
            len(points),
        )

    logger.info("Ingested %d judgments total", len(points))
    return point_ids
