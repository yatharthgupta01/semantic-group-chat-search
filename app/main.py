"""FastAPI Backend Application for Semantic Group Chat Search.
Provides GET /health, POST /search, and auto-generated interactive OpenAPI /docs.
"""

from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse

from app.config import MODEL_NAME, FRONTEND_DIR
from app.models import SearchRequest, SearchResponse, HealthResponse
from app.retrieval import get_index
from app.search import search_messages


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Warm up index and embedding model on application startup."""
    index = get_index()
    index.load()
    yield


app = FastAPI(
    title="Semantic Group Chat Search API",
    description=(
        "Production-grade semantic search engine over synthetic multilingual/Hinglish "
        "group chat exports. Features dense vector similarity, attributed sender detection, "
        "temporal filtering, and conversational context expansion."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Enable CORS for local web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/health",
    response_model=HealthResponse,
    summary="System Health & Index Status",
    tags=["System"]
)
async def health_check():
    """Returns the operational health, active embedding model, and index statistics."""
    try:
        index = get_index()
        total_msgs = index.get_total_count()
        date_range = None
        if total_msgs > 0:
            first_time = index.messages[0]["timestamp"][:10]
            last_time = index.messages[-1]["timestamp"][:10]
            date_range = f"{first_time} to {last_time}"

        return HealthResponse(
            status="healthy",
            version="1.0.0",
            model=MODEL_NAME,
            indexed_messages=total_msgs,
            data_date_range=date_range
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Index initialization error: {str(e)}"
        )


@app.post(
    "/search",
    response_model=SearchResponse,
    summary="Execute Semantic Group Chat Search",
    tags=["Search"]
)
async def search_endpoint(request: SearchRequest):
    """Searches messages using semantic similarity, attribution, and temporal filters.

    - **query**: User input query string (required)
    - **sender** / **person**: Optional participant filter
    - **date_from**: Optional start date ISO timestamp
    - **date_to**: Optional end date ISO timestamp
    - **top_k**: Maximum results to retrieve (default: 10)
    """
    clean_query = request.query.strip()
    if not clean_query:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Search query cannot be empty or whitespace only."
        )

    sender_filter = request.sender or request.person
    limit = request.top_k or 10

    try:
        res = search_messages(
            query=clean_query,
            limit=limit,
            sender_filter=sender_filter,
            date_from_filter=request.date_from,
            date_to_filter=request.date_to
        )
        return SearchResponse(**res)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search pipeline failed: {str(e)}"
        )


@app.get(
    "/search",
    response_model=SearchResponse,
    summary="GET Search (Convenience)",
    tags=["Search"]
)
async def search_get_endpoint(
    q: str = Query(..., description="Query string"),
    sender: str = Query(None, description="Optional sender filter"),
    date_from: str = Query(None, description="Optional start date"),
    date_to: str = Query(None, description="Optional end date"),
    top_k: int = Query(10, ge=1, le=50, description="Number of results")
):
    """Convenience GET endpoint for browser address-bar search tests."""
    req = SearchRequest(
        query=q,
        sender=sender,
        date_from=date_from,
        date_to=date_to,
        top_k=top_k
    )
    return await search_endpoint(req)


# Mount static frontend directory if available
if FRONTEND_DIR.exists():
    app.mount("/ui", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")


@app.get("/", include_in_schema=False)
async def root_redirect():
    """Redirect root to UI if available, otherwise to /docs."""
    if FRONTEND_DIR.exists() and (FRONTEND_DIR / "index.html").exists():
        return RedirectResponse(url="/ui")
    return RedirectResponse(url="/docs")
