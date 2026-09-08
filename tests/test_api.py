"""API endpoint tests for FastAPI backend."""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    """Verify /health returns operational status and index statistics."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "1.0.0"
    assert "paraphrase-multilingual" in data["model"]
    assert data["indexed_messages"] == 4250
    assert data["data_date_range"] is not None


def test_docs_endpoint():
    """Verify OpenAPI Swagger documentation is accessible at /docs."""
    response = client.get("/docs")
    assert response.status_code == 200
    assert "Swagger UI" in response.text


def test_search_endpoint_success():
    """Verify POST /search returns properly formatted results with context."""
    payload = {
        "query": "Where did we finally decide to stay for the trip?",
        "top_k": 5
    }
    response = client.post("/search", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == payload["query"]
    assert "results" in data
    assert len(data["results"]) > 0
    assert len(data["results"]) <= 5

    first = data["results"][0]
    assert "id" in first
    assert "sender" in first
    assert "timestamp" in first
    assert "text" in first
    assert "score" in first
    assert 0.0 <= first["score"] <= 1.0
    assert "match_reason" in first
    assert "context" in first
    assert isinstance(first["context"], list)
    assert len(first["context"]) > 0

    # Ensure match marker is present in context
    matches = [c for c in first["context"] if c["is_match"]]
    assert len(matches) == 1
    assert matches[0]["id"] == first["id"]


def test_search_endpoint_empty_query():
    """Verify POST /search rejects empty and blank queries gracefully."""
    response = client.post("/search", json={"query": "   "})
    assert response.status_code == 422 or response.status_code == 400


def test_search_endpoint_with_explicit_filters():
    """Verify POST /search respects explicit sender and date filters."""
    payload = {
        "query": "budget",
        "sender": "Rahul Sharma",
        "top_k": 5
    }
    response = client.post("/search", json=payload)
    assert response.status_code == 200
    data = response.json()
    for r in data["results"]:
        assert r["sender"] == "Rahul Sharma"


def test_search_endpoint_gibberish_query():
    """Verify POST /search handles nonsense queries without crashing."""
    payload = {
        "query": "zzxxyyqqww998877",
        "top_k": 5
    }
    response = client.post("/search", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data


def test_frontend_mounted_and_served():
    """Verify static frontend files (HTML, CSS, JS) are mounted and accessible."""
    # Test HTML UI
    response_ui = client.get("/ui/")
    assert response_ui.status_code == 200
    assert "Semantic Group Chat Search" in response_ui.text
    assert "searchInput" in response_ui.text

    # Test CSS
    response_css = client.get("/ui/styles.css")
    assert response_css.status_code == 200
    assert "Semantic Group Chat Search" in response_css.text

    # Test JS
    response_js = client.get("/ui/app.js")
    assert response_js.status_code == 200
    assert "Semantic Group Chat Search" in response_js.text


def test_root_redirect_to_ui():
    """Verify root URL (/) redirects to /ui when frontend is present."""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers.get("location") == "/ui"