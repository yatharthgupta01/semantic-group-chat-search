"""Index builder script.
Encodes all messages in data/messages.jsonl into dense semantic embeddings and
builds fast lookup metadata indexes for retrieval and context expansion.
"""

import json
import time
import sys
from pathlib import Path

# Add project root to sys.path for direct script execution
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
from app.config import (
    MESSAGES_FILE,
    EMBEDDINGS_FILE,
    INDEX_METADATA_FILE,
    DATA_DIR,
    MODEL_NAME
)
from app.embeddings import encode_texts


def build_index():
    print(f"Starting index build from {MESSAGES_FILE}...")
    start_time = time.time()

    if not MESSAGES_FILE.exists():
        raise FileNotFoundError(f"Missing {MESSAGES_FILE}. Run scripts/generate_dataset.py first.")

    messages = []
    with open(MESSAGES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                messages.append(json.loads(line))

    total = len(messages)
    print(f"Loaded {total} messages. Extracting text for embedding...")

    texts = [m["text"] for m in messages]

    print(f"Encoding {total} texts with {MODEL_NAME}...")
    embeddings = encode_texts(texts, batch_size=64, show_progress=True)

    print(f"Saving embeddings matrix of shape {embeddings.shape} to {EMBEDDINGS_FILE}...")
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    np.save(EMBEDDINGS_FILE, embeddings)

    # Build metadata lookup indexes
    id_to_idx = {m["id"]: i for i, m in enumerate(messages)}
    sender_indices = {}
    conversation_indices = {}

    for idx, m in enumerate(messages):
        s = m["sender"]
        if s not in sender_indices:
            sender_indices[s] = []
        sender_indices[s].append(idx)

        c = m["conversation_id"]
        if c not in conversation_indices:
            conversation_indices[c] = []
        conversation_indices[c].append(idx)

    index_metadata = {
        "model_name": MODEL_NAME,
        "total_messages": total,
        "embedding_dim": int(embeddings.shape[1]),
        "messages": messages,
        "id_to_idx": id_to_idx,
        "sender_indices": sender_indices,
        "conversation_indices": conversation_indices,
        "indexed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }

    print(f"Saving index metadata to {INDEX_METADATA_FILE}...")
    with open(INDEX_METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(index_metadata, f, ensure_ascii=False)

    elapsed = time.time() - start_time
    print(f"Indexing complete in {elapsed:.2f} seconds!")
    print(f"Total messages indexed: {total}")
    print(f"Embeddings saved to: {EMBEDDINGS_FILE}")
    print(f"Metadata saved to: {INDEX_METADATA_FILE}")


if __name__ == "__main__":
    build_index()
