"""Tests for semantic vector retrieval, sender filtering, and temporal range filtering."""

import pytest
from app.retrieval import get_index
from app.search import search_messages


def test_index_loaded():
    """Verify vector index is loaded and message count matches."""
    index = get_index()
    assert index.is_loaded
    assert index.get_total_count() == 4250
    assert index.embeddings.shape == (4250, 384)


def test_semantic_retrieval():
    """Verify semantic search retrieves relevant accommodation discussion."""
    res = search_messages("Where did we finally decide to stay for the trip?", limit=5)
    assert res["total_hits"] > 0
    top_hit = res["results"][0]
    # Should retrieve the Airbnb decision message
    assert "Airbnb" in top_hit["text"] or "apartment" in top_hit["text"]
    assert top_hit["score"] > 0.65


def test_sender_filtering():
    """Verify attributed search strictly boosts or filters target author."""
    res = search_messages("What did Rahul say about the budget?", limit=5)
    assert res["total_hits"] > 0
    top_hit = res["results"][0]
    assert top_hit["sender"] == "Rahul Sharma"
    assert "budget" in top_hit["text"].lower()


def test_temporal_filtering():
    """Verify temporal query isolates discussions within requested month."""
    res = search_messages("What did we discuss about the event in December?", limit=5)
    assert res["total_hits"] > 0
    for r in res["results"]:
        # Timestamps should fall within December 2025
        assert "-12-" in r["timestamp"]
