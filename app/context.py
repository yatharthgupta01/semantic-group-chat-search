"""Conversation Context Expansion Module.
Expands surrounding conversation context for retrieved group chat messages
within the same conversation thread to provide complete conversational context.
"""

from typing import List, Dict, Any, Optional
from app.config import CONTEXT_WINDOW_BEFORE, CONTEXT_WINDOW_AFTER
from app.retrieval import get_index


def expand_context(
    message_id: str,
    before: int = CONTEXT_WINDOW_BEFORE,
    after: int = CONTEXT_WINDOW_AFTER
) -> List[Dict[str, Any]]:
    """Retrieves surrounding messages within the same conversation thread.
    
    Args:
        message_id: ID of the central retrieved message.
        before: Number of preceding messages to include.
        after: Number of succeeding messages to include.
        
    Returns:
        Chronologically ordered list of message dictionaries with 'is_match' flag.
    """
    index = get_index()
    target_idx = index.id_to_idx.get(message_id)
    if target_idx is None:
        return []

    target_msg = index.messages[target_idx]
    conv_id = target_msg["conversation_id"]

    # Retrieve all indices for this conversation thread
    thread_indices = index.conversation_indices.get(conv_id, [target_idx])

    # Find the position of target_msg in the thread
    try:
        pos_in_thread = thread_indices.index(target_idx)
    except ValueError:
        pos_in_thread = 0

    # Calculate window bounds
    start_pos = max(0, pos_in_thread - before)
    end_pos = min(len(thread_indices), pos_in_thread + after + 1)

    selected_indices = thread_indices[start_pos:end_pos]

    context_messages = []
    for idx in selected_indices:
        msg = index.messages[idx]
        context_messages.append({
            "id": msg["id"],
            "sender": msg["sender"],
            "timestamp": msg["timestamp"],
            "text": msg["text"],
            "forwarded": msg.get("forwarded", False),
            "reply_to": msg.get("reply_to"),
            "is_match": (msg["id"] == message_id)
        })

    return context_messages
