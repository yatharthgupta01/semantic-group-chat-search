"""Vector Retrieval Engine.
Provides high-performance in-memory vector search over normalized embeddings
with candidate filtering and metadata lookups.
"""

from typing import List, Dict, Any, Optional, Tuple
import json
from pathlib import Path
import numpy as np

from app.config import (
    MESSAGES_FILE,
    INDEX_METADATA_FILE,
    EMBEDDINGS_FILE
)


class VectorIndex:
    """In-memory search index managing precomputed embeddings and message metadata."""

    def __init__(self):
        self.embeddings: Optional[np.ndarray] = None
        self.messages: List[Dict[str, Any]] = []
        self.id_to_idx: Dict[str, int] = {}
        self.sender_indices: Dict[str, List[int]] = {}
        self.conversation_indices: Dict[str, List[int]] = {}
        self.is_loaded: bool = False

    def load(self, force_reload: bool = False) -> None:
        """Loads index metadata and embeddings into memory."""
        if self.is_loaded and not force_reload:
            return

        if not INDEX_METADATA_FILE.exists() or not EMBEDDINGS_FILE.exists():
            from scripts.build_index import build_index
            build_index()

        with open(INDEX_METADATA_FILE, "r", encoding="utf-8") as f:
            meta = json.load(f)

        self.messages = meta["messages"]
        self.id_to_idx = meta["id_to_idx"]
        self.sender_indices = meta["sender_indices"]
        self.conversation_indices = meta["conversation_indices"]
        self.embeddings = np.load(EMBEDDINGS_FILE)

        # Verify dimensionality
        assert len(self.messages) == self.embeddings.shape[0], (
            f"Mismatch between messages ({len(self.messages)}) and embeddings ({self.embeddings.shape[0]})"
        )
        self.is_loaded = True

    def get_total_count(self) -> int:
        return len(self.messages)

    def get_message(self, idx: int) -> Optional[Dict[str, Any]]:
        if 0 <= idx < len(self.messages):
            return self.messages[idx]
        return None

    def get_message_by_id(self, msg_id: str) -> Optional[Dict[str, Any]]:
        idx = self.id_to_idx.get(msg_id)
        if idx is not None:
            return self.messages[idx]
        return None

    def search_similarities(
        self,
        query_vector: np.ndarray
    ) -> np.ndarray:
        """Computes cosine similarities for all messages against the query vector.
        Since vectors are L2-normalized, cosine similarity is the inner product.
        """
        if not self.is_loaded:
            self.load()

        # Dot product against (N, D) yields (N,) similarities in [-1, 1]
        sims = np.dot(self.embeddings, query_vector)
        return sims


# Singleton index instance
_GLOBAL_INDEX: Optional[VectorIndex] = None


def get_index() -> VectorIndex:
    """Lazy loader for global vector index."""
    global _GLOBAL_INDEX
    if _GLOBAL_INDEX is None:
        _GLOBAL_INDEX = VectorIndex()
        _GLOBAL_INDEX.load()
    return _GLOBAL_INDEX
