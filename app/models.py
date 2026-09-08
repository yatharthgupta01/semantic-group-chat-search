"""Pydantic schemas and models for the FastAPI Semantic Search backend."""

from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class SearchRequest(BaseModel):
    query: str = Field(..., description="The search query text (semantic, attributed, or temporal).")
    sender: Optional[str] = Field(None, description="Optional explicit participant name filter.")
    person: Optional[str] = Field(None, description="Alias for sender filter.")
    date_from: Optional[str] = Field(None, description="Optional ISO timestamp start filter.")
    date_to: Optional[str] = Field(None, description="Optional ISO timestamp end filter.")
    top_k: Optional[int] = Field(10, ge=1, le=50, description="Maximum number of search results to return.")

    @field_validator("query")
    @classmethod
    def query_not_blank(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Query string cannot be empty or whitespace only.")
        return v.strip()


class ContextMessage(BaseModel):
    id: str
    sender: str
    timestamp: str
    text: str
    is_match: bool = False
    forwarded: bool = False
    reply_to: Optional[str] = None


class SearchResultItem(BaseModel):
    id: str
    sender: str
    timestamp: str
    text: str
    score: float
    match_reason: str
    conversation_id: str
    forwarded: bool = False
    reply_to: Optional[str] = None
    context: List[ContextMessage] = []


class ParsedFilters(BaseModel):
    clean_query: str
    detected_sender: Optional[str] = None
    is_strict_sender: bool = False
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    date_label: Optional[str] = None


class SearchResponse(BaseModel):
    query: str
    parsed_filters: ParsedFilters
    total_hits: int
    results: List[SearchResultItem]


class HealthResponse(BaseModel):
    status: str
    version: str
    model: str
    indexed_messages: int
    data_date_range: Optional[str] = None
