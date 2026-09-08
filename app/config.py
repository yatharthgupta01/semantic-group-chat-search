from pathlib import Path
import os

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Data directory and paths
DATA_DIR = BASE_DIR / "data"
MESSAGES_FILE = DATA_DIR / "messages.jsonl"
INDEX_METADATA_FILE = DATA_DIR / "messages_index.json"
EMBEDDINGS_FILE = DATA_DIR / "embeddings.npy"
EVALUATION_QUERIES_FILE = DATA_DIR / "evaluation_queries.json"

# Frontend directory
FRONTEND_DIR = BASE_DIR / "frontend"

# Model Configuration
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
EMBEDDING_DIM = 384
BATCH_SIZE = 64

# Search and Context Configuration
DEFAULT_TOP_K = 10
CONTEXT_WINDOW_BEFORE = 3
CONTEXT_WINDOW_AFTER = 2

# Scoring weights
SENDER_BOOST = 0.25
TEMPORAL_BOOST = 0.20
LEXICAL_BOOST = 0.15

# Known participants for attributed search
PARTICIPANTS = [
    "Rahul Sharma",
    "Priya Patel",
    "Aman Verma",
    "Sneha Reddy",
    "Vikram Malhotra",
    "Neha Gupta",
    "Rohan Mehta",
    "Ananya Iyer",
    "Kabir Das",
]

# Aliases mapping to canonical participant names
PARTICIPANT_ALIASES = {
    "rahul": "Rahul Sharma",
    "rahul sharma": "Rahul Sharma",
    "priya": "Priya Patel",
    "priya patel": "Priya Patel",
    "aman": "Aman Verma",
    "aman verma": "Aman Verma",
    "sneha": "Sneha Reddy",
    "sneha reddy": "Sneha Reddy",
    "vikram": "Vikram Malhotra",
    "vikram malhotra": "Vikram Malhotra",
    "vicky": "Vikram Malhotra",
    "neha": "Neha Gupta",
    "neha gupta": "Neha Gupta",
    "rohan": "Rohan Mehta",
    "rohan mehta": "Rohan Mehta",
    "ananya": "Ananya Iyer",
    "ananya iyer": "Ananya Iyer",
    "kabir": "Kabir Das",
    "kabir das": "Kabir Das",
}
