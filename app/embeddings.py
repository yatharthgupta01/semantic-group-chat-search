"""Local Multilingual Embedding Engine.
Uses sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 to produce
dense 384-dimensional semantic embeddings optimized for English and Hinglish code-mixed text.
"""

from typing import List, Union
import numpy as np
from sentence_transformers import SentenceTransformer
from app.config import MODEL_NAME, BATCH_SIZE

_EMBEDDING_MODEL = None


def get_embedding_model() -> SentenceTransformer:
    """Lazy loader singleton for the SentenceTransformer model."""
    global _EMBEDDING_MODEL
    if _EMBEDDING_MODEL is None:
        # Load local cached model
        _EMBEDDING_MODEL = SentenceTransformer(MODEL_NAME)
    return _EMBEDDING_MODEL


def encode_texts(
    texts: List[str],
    batch_size: int = BATCH_SIZE,
    show_progress: bool = False
) -> np.ndarray:
    """Encodes a list of text strings into normalized L2 float32 vectors.
    
    Args:
        texts: List of message strings to embed.
        batch_size: Batch size for model inference.
        show_progress: Whether to display progress bars.
        
    Returns:
        np.ndarray of shape (len(texts), 384) with float32 values.
    """
    if not texts:
        return np.zeros((0, 384), dtype=np.float32)

    model = get_embedding_model()
    # Normalize embeddings enables exact cosine similarity via fast inner dot product
    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=show_progress,
        normalize_embeddings=True,
        convert_to_numpy=True
    )
    return embeddings.astype(np.float32)


def encode_query(query: str) -> np.ndarray:
    """Encodes a single search query into a normalized L2 float32 vector.
    
    Args:
        query: User input query string.
        
    Returns:
        1D np.ndarray of shape (384,) with float32 values.
    """
    model = get_embedding_model()
    emb = model.encode(query.strip(), normalize_embeddings=True, convert_to_numpy=True)
    return emb.astype(np.float32)
