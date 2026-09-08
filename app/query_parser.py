"""Lightweight deterministic query parser for semantic group chat search.
Extracts attributed participants, temporal date ranges, and cleans
the semantic intent string for high-precision embedding retrieval.
"""

import re
from typing import Dict, Any, Optional, Tuple
from datetime import datetime
from app.config import PARTICIPANT_ALIASES

MONTH_MAP = {
    "october": (2025, 10), "oct": (2025, 10),
    "november": (2025, 11), "nov": (2025, 11),
    "december": (2025, 12), "dec": (2025, 12),
    "january": (2026, 1), "jan": (2026, 1),
    "february": (2026, 2), "feb": (2026, 2),
    "march": (2026, 3), "mar": (2026, 3)
}

MONTH_DAYS = {
    1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
    7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
}


def parse_query(query: str) -> Dict[str, Any]:
    """Parses raw user query into structured search parameters:
    - detected_sender: Canonical participant name if attributed
    - date_from: ISO-8601 start timestamp filter (optional)
    - date_to: ISO-8601 end timestamp filter (optional)
    - date_label: Human-readable temporal filter description
    - is_strict_sender: True if query specifically demands this person's statements
    - clean_query: Purified semantic text for embedding search
    """
    raw_query = query.strip()
    lower_query = raw_query.lower()

    detected_sender: Optional[str] = None
    is_strict_sender = False
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    date_label: Optional[str] = None

    # 1. Attributed Sender Extraction
    # Check for attribution patterns:
    # "What did Rahul say about...", "Show messages from Aman...", "Priya's suggestion..."
    for alias, canonical in sorted(PARTICIPANT_ALIASES.items(), key=lambda x: -len(x[0])):
        # Match whole word boundary for alias
        pattern = r"\b" + re.escape(alias) + r"(?:'s)?\b"
        if re.search(pattern, lower_query):
            detected_sender = canonical
            # Check if query is explicitly asking for this person's words
            if re.search(r"(?:what did|messages from|message from|by|said by|shared by|suggested by|say about|suggest for|post from)\s+" + re.escape(alias), lower_query):
                is_strict_sender = True
            elif re.search(re.escape(alias) + r"(?:'s|\s+(?:say|said|suggested|mentioned|posted|shared|recommended))", lower_query):
                is_strict_sender = True
            break

    # 2. Temporal & Date-Range Extraction
    # Pattern: "first week of <month>", "early <month>"
    match_week = re.search(r"\b(?:first|1st)\s+week\s+(?:of\s+)?([a-z]+)(?:\s+(\d{4}))?\b", lower_query)
    if match_week and match_week.group(1) in MONTH_MAP:
        month_name = match_week.group(1)
        year, month_num = MONTH_MAP[month_name]
        if match_week.group(2):
            year = int(match_week.group(2))
        date_from = f"{year:04d}-{month_num:02d}-01T00:00:00Z"
        date_to = f"{year:04d}-{month_num:02d}-07T23:59:59Z"
        date_label = f"First week of {month_name.capitalize()} {year}"

    # Pattern: "last week of <month>"
    if not date_from:
        match_last_week = re.search(r"\b(?:last)\s+week\s+(?:of\s+)?([a-z]+)(?:\s+(\d{4}))?\b", lower_query)
        if match_last_week and match_last_week.group(1) in MONTH_MAP:
            month_name = match_last_week.group(1)
            year, month_num = MONTH_MAP[month_name]
            if match_last_week.group(2):
                year = int(match_last_week.group(2))
            last_day = MONTH_DAYS[month_num]
            date_from = f"{year:04d}-{month_num:02d}-{last_day-7:02d}T00:00:00Z"
            date_to = f"{year:04d}-{month_num:02d}-{last_day:02d}T23:59:59Z"
            date_label = f"Last week of {month_name.capitalize()} {year}"

    # Pattern: "mid <month>"
    if not date_from:
        match_mid = re.search(r"\b(?:mid|middle of)\s+([a-z]+)(?:\s+(\d{4}))?\b", lower_query)
        if match_mid and match_mid.group(1) in MONTH_MAP:
            month_name = match_mid.group(1)
            year, month_num = MONTH_MAP[month_name]
            if match_mid.group(2):
                year = int(match_mid.group(2))
            date_from = f"{year:04d}-{month_num:02d}-10T00:00:00Z"
            date_to = f"{year:04d}-{month_num:02d}-20T23:59:59Z"
            date_label = f"Mid {month_name.capitalize()} {year}"

    # Pattern: "last month" (in context of chat dataset ending Mar 2026 -> February 2026)
    if not date_from and "last month" in lower_query:
        date_from = "2026-02-01T00:00:00Z"
        date_to = "2026-02-28T23:59:59Z"
        date_label = "Last month (Feb 2026)"

    # Pattern: General month mention (e.g. "in December", "December", "during January")
    if not date_from:
        for month_name, (default_year, month_num) in MONTH_MAP.items():
            pattern = r"\b(?:in\s+|during\s+|for\s+)?(" + re.escape(month_name) + r")(?:\s+(\d{4}))?\b"
            m = re.search(pattern, lower_query)
            if m:
                year = int(m.group(2)) if m.group(2) else default_year
                last_day = MONTH_DAYS[month_num]
                date_from = f"{year:04d}-{month_num:02d}-01T00:00:00Z"
                date_to = f"{year:04d}-{month_num:02d}-{last_day:02d}T23:59:59Z"
                date_label = f"{month_name.capitalize()} {year}"
                break

    # 3. Clean query and semantic intent extraction
    clean_text = raw_query
    # Remove leading attribution patterns
    clean_text = re.sub(r"^(?:what did|what was|what were|show me|find|get|tell me about|where did we)\s+", "", clean_text, flags=re.IGNORECASE)
    clean_text = re.sub(r"\b(?:say about|suggest for|talk about|recommend regarding|discuss about|think of|propose for|finally decide to|decide to)\b", "", clean_text, flags=re.IGNORECASE)
    clean_text = re.sub(r"\b(?:messages? from|from)\s+[A-Za-z]+(?:\s+[A-Za-z]+)?\b", "", clean_text, flags=re.IGNORECASE)
    clean_text = re.sub(r"\b[A-Za-z]+(?:'s)?\s+(?:suggestion|thought|budget|opinion|say|take)\b", "", clean_text, flags=re.IGNORECASE)
    # Remove temporal phrases from embedding query text
    clean_text = re.sub(r"\b(?:in|during|for|around)\s+(?:first week of|last week of|mid\s+)?(?:october|november|december|january|february|march|oct|nov|dec|jan|feb|mar)(?:\s+\d{4})?\b", "", clean_text, flags=re.IGNORECASE)
    clean_text = re.sub(r"\b(?:last month|last week|first week|this week)\b", "", clean_text, flags=re.IGNORECASE)
    clean_text = re.sub(r"[?!.,;:]+", " ", clean_text).strip()

    # 4. Semantic Intent Expansion for conversational retrieval
    expansion_terms = []
    lower_clean = (raw_query + " " + clean_text).lower()

    if any(w in lower_clean for w in ["stay", "lodging", "accommodation", "where to sleep", "sleep", "hotel", "resort", "airbnb", "apartment"]):
        expansion_terms.extend(["stay", "accommodation", "hotel", "resort", "airbnb", "apartment", "villa", "book kar dete"])

    if any(w in lower_clean for w in ["budget", "cost", "price", "expensive", "afford", "cheap", "limit", "spend"]):
        expansion_terms.extend(["budget", "cost", "price", "afford", "per head", "per night", "strict"])

    if any(w in lower_clean for w in ["decision", "decide", "finally", "finalized", "lock", "conclude", "settle"]):
        expansion_terms.extend(["finalized", "book kar dete", "lock kar diya", "order placed", "finalize karte"])

    if any(w in lower_clean for w in ["venue", "location", "place", "spot", "celebration site"]):
        expansion_terms.extend(["venue", "rooftop", "lounge", "farmhouse", "location", "grand mirage"])

    if any(w in lower_clean for w in ["food", "catering", "dinner", "lunch", "menu", "eat", "meal", "barbecue"]):
        expansion_terms.extend(["food", "catering", "biryani", "barbecue", "menu", "dinner", "charcoal"])

    if any(w in lower_clean for w in ["music", "dj", "sound", "speaker", "audio", "playlist", "songs"]):
        expansion_terms.extend(["sound system", "dj", "playlist", "speakers", "jbl", "music"])

    if any(w in lower_clean for w in ["photo", "camera", "pictures", "photobooth", "decor", "cake"]):
        expansion_terms.extend(["photo booth", "fairy lights", "cake", "decor"])

    if any(w in lower_clean for w in ["monitor", "display", "screen", "hardware", "gadget", "ultrawide", "computer"]):
        expansion_terms.extend(["ultrawide", "monitor", "display", "screen", "lg", "34-inch", "discount code"])

    if any(w in lower_clean for w in ["travel", "transport", "flight", "train", "drive", "car", "scooter", "commute"]):
        expansion_terms.extend(["flight", "tickets", "train", "scooter", "rental", "drive"])

    semantic_query = clean_text
    if expansion_terms:
        # Append distinct expansion terms to enrich semantic representation
        unique_terms = [t for t in expansion_terms if t not in clean_text.lower()]
        if unique_terms:
            semantic_query = f"{clean_text} {' '.join(unique_terms[:6])}"

    if len(clean_text.split()) < 2:
        clean_text = raw_query

    return {
        "raw_query": raw_query,
        "clean_query": clean_text,
        "semantic_query": semantic_query,
        "detected_sender": detected_sender,
        "is_strict_sender": is_strict_sender,
        "date_from": date_from,
        "date_to": date_to,
        "date_label": date_label
    }
