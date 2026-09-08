"""Tests for query understanding and parser logic."""

import pytest
from app.query_parser import parse_query


def test_sender_extraction():
    """Verify participant name and aliases are detected."""
    res1 = parse_query("What did Rahul say about the budget?")
    assert res1["detected_sender"] == "Rahul Sharma"
    assert res1["is_strict_sender"] is True

    res2 = parse_query("Show messages from Priya regarding venue")
    assert res2["detected_sender"] == "Priya Patel"
    assert res2["is_strict_sender"] is True

    res3 = parse_query("Aman's thoughts on Airbnb")
    assert res3["detected_sender"] == "Aman Verma"


def test_temporal_extraction():
    """Verify month and date-range extraction."""
    res_dec = parse_query("What did we discuss in December?")
    assert res_dec["date_from"] == "2025-12-01T00:00:00Z"
    assert res_dec["date_to"] == "2025-12-31T23:59:59Z"

    res_jan_week = parse_query("What happened in first week of January?")
    assert res_jan_week["date_from"] == "2026-01-01T00:00:00Z"
    assert res_jan_week["date_to"] == "2026-01-07T23:59:59Z"


def test_clean_query_cleanup():
    """Verify query syntax is cleaned for semantic embedding."""
    res = parse_query("What did Rahul say about the budget?")
    assert "rahul" not in res["clean_query"].lower()
    assert "budget" in res["clean_query"].lower()
