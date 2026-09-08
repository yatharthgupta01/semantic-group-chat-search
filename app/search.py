"""Semantic Search Pipeline.
Coordinates query parsing, multilingual embeddings, vector similarity search,
metadata filtering/boosting, re-ranking, and conversational context expansion.
"""

from typing import List, Dict, Any, Optional
import re
import numpy as np
from app.config import (
    DEFAULT_TOP_K,
    SENDER_BOOST,
    TEMPORAL_BOOST,
    LEXICAL_BOOST
)
from app.embeddings import encode_query
from app.query_parser import parse_query
from app.retrieval import get_index
from app.context import expand_context


def search_messages(
    query: str,
    limit: int = DEFAULT_TOP_K,
    sender_filter: Optional[str] = None,
    date_from_filter: Optional[str] = None,
    date_to_filter: Optional[str] = None
) -> Dict[str, Any]:
    """Executes multi-stage semantic group chat search.
    
    Args:
        query: User search query string.
        limit: Maximum number of results to return.
        sender_filter: Optional explicit override for sender.
        date_from_filter: Optional explicit start timestamp filter.
        date_to_filter: Optional explicit end timestamp filter.
        
    Returns:
        Structured search response containing parsed metadata, count, and results.
    """
    index = get_index()
    parsed = parse_query(query)

    target_sender = sender_filter or parsed["detected_sender"]
    is_strict_sender = parsed["is_strict_sender"] or (sender_filter is not None)
    target_date_from = date_from_filter or parsed["date_from"]
    target_date_to = date_to_filter or parsed["date_to"]
    clean_query = parsed["clean_query"]
    raw_query = parsed["raw_query"]
    semantic_query = parsed.get("semantic_query", clean_query)

    # Compute query embedding (blend semantic intent with raw query)
    emb_semantic = encode_query(semantic_query)
    emb_raw = encode_query(raw_query)
    query_vec = 0.70 * emb_semantic + 0.30 * emb_raw
    query_vec = query_vec / (np.linalg.norm(query_vec) + 1e-9)

    # Calculate raw cosine similarities across all 4,250 messages
    base_sims = index.search_similarities(query_vec)

    # Score adjustments and candidate filtering
    num_messages = len(index.messages)
    final_scores = np.copy(base_sims)
    match_reasons = [[] for _ in range(num_messages)]

    # Query tokens for selective lexical boosting (filter out noisy conversational stop words)
    STOPWORDS = {
        "what", "when", "where", "which", "about", "from", "with", "this",
        "that", "there", "their", "have", "will", "would", "could", "should",
        "some", "them", "then", "into", "onto", "trip", "chat", "guys", "yaar",
        "bhai", "karein", "hain", "kuch", "kya", "the", "and", "for", "say", "said",
        "rahul", "priya", "aman", "sneha", "vikram", "neha", "rohan", "ananya", "kabir"
    }
    query_tokens = [w.lower() for w in re.findall(r"\b[a-zA-Z0-9_-]+\b", clean_query) if len(w) > 3 and w.lower() not in STOPWORDS]

    is_decision_query = any(w in raw_query.lower() for w in ["decide", "decision", "final", "finally", "finalized", "conclude", "settle", "lock"])
    decision_markers = ["book kar dete", "finalized", "lock kar diya", "finalize karte", "order placed"]

    for i in range(num_messages):
        msg = index.messages[i]
        msg_text = msg["text"].lower()
        msg_sender = msg["sender"]
        msg_time = msg["timestamp"]

        # Base semantic similarity tag
        sim_val = base_sims[i]
        match_reasons[i].append(f"Semantic similarity: {sim_val:.2f}")

        # Attributed filter / boost
        if target_sender:
            if msg_sender.lower() == target_sender.lower():
                final_scores[i] += SENDER_BOOST
                match_reasons[i].append(f"Author match: {target_sender}")
            elif is_strict_sender:
                # Heavy penalty if user specifically asked for this person's words
                final_scores[i] -= 1.0

        # Temporal filter / boost
        if target_date_from and target_date_to:
            if target_date_from <= msg_time <= target_date_to:
                final_scores[i] += TEMPORAL_BOOST
                label = parsed.get("date_label") or f"{target_date_from[:10]} to {target_date_to[:10]}"
                match_reasons[i].append(f"Within {label}")
            else:
                # Penalize messages outside requested time range
                final_scores[i] -= 0.60

        # Decision point boost if query asks for decisions/conclusions
        if is_decision_query and any(marker in msg_text for marker in decision_markers):
            final_scores[i] += 0.22
            match_reasons[i].append("Actionable decision milestone")

        # Selective lexical boost for distinctive keywords
        for tok in query_tokens:
            if tok in msg_text:
                final_scores[i] += (LEXICAL_BOOST / len(query_tokens))
                match_reasons[i].append(f"Contains keyword '{tok}'")
                break

    # Re-rank by final score
    top_indices = np.argsort(final_scores)[::-1][:limit]

    results = []
    for idx in top_indices:
        score = float(final_scores[idx])
        # Skip results with negative or heavily penalized scores
        if score < 0.10:
            continue

        msg = index.messages[idx]
        reason_str = " • ".join(match_reasons[idx])
        context = expand_context(msg["id"])

        results.append({
            "id": msg["id"],
            "sender": msg["sender"],
            "timestamp": msg["timestamp"],
            "text": msg["text"],
            "conversation_id": msg["conversation_id"],
            "reply_to": msg.get("reply_to"),
            "forwarded": msg.get("forwarded", False),
            "score": round(max(0.0, min(1.0, (score + 1.0) / 2.0)), 4),
            "raw_score": round(score, 4),
            "match_reason": reason_str,
            "context": context
        })

    return {
        "query": query,
        "parsed_filters": {
            "clean_query": clean_query,
            "detected_sender": target_sender,
            "is_strict_sender": is_strict_sender,
            "date_from": target_date_from,
            "date_to": target_date_to,
            "date_label": parsed["date_label"]
        },
        "total_hits": len(results),
        "results": results
    }
