# config.py
import torch
from pathlib import Path

# Auto GPU detection
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"🚀 Using device: {DEVICE.upper()}")

# Paths
BASE_DIR = Path(__file__).parent
RAW_DIR = BASE_DIR / "data/raw"
VECTORSTORE_PATH = BASE_DIR / "vectorstore"

# Models
EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"
LLM_MODEL = "llama3.1:8b"

# Chunking
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

# 🔥 NEW: Safe batch size for your RTX 3050 (4 GB)
BATCH_SIZE = 512          # Lower = more stable on laptop GPU

# Limits
MAX_PAGES_WARNING = 500