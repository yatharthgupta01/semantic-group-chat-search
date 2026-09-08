"""Tests for conversational context expansion and thread boundaries."""

import pytest
from app.context import expand_context
from app.retrieval import get_index


def test_context_expansion_window():
    """Verify context expansion retrieves [-3, +2] surrounding messages."""
    index = get_index()
    # Pick a message in the middle of a conversation thread
    target_msg = index.messages[10]
    ctx = expand_context(target_msg["id"], before=3, after=2)

    assert len(ctx) >= 1
    assert len(ctx) <= 6

    # Verify chronological ordering
    timestamps = [c["timestamp"] for c in ctx]
    assert timestamps == sorted(timestamps)

    # Exactly one message must be marked as the match
    match_items = [c for c in ctx if c["is_match"]]
    assert len(match_items) == 1
    assert match_items[0]["id"] == target_msg["id"]


def test_context_expansion_thread_boundary():
    """Verify context respects start of thread boundary."""
    index = get_index()
    first_msg = index.messages[0]
    ctx = expand_context(first_msg["id"], before=3, after=2)

    assert len(ctx) >= 1
    assert ctx[0]["id"] == first_msg["id"]
    assert ctx[0]["is_match"] is True


def test_context_expansion_invalid_id():
    """Verify querying context for a non-existent ID returns empty list gracefully."""
    ctx = expand_context("msg_nonexistent_99999")
    assert ctx == []
