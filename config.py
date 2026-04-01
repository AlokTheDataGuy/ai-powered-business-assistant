# config.py
import torch
import os
from pathlib import Path

# Auto GPU detection
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"🚀 Using device: {DEVICE.upper()} (GPU will make everything 3-10x faster)")

# Paths
BASE_DIR = Path(__file__).parent.parent
RAW_DIR = BASE_DIR / "data/raw"
VECTORSTORE_PATH = BASE_DIR / "vectorstore"
UPLOAD_DIR = RAW_DIR

# Models
EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"
LLM_MODEL = "llama3.3:8b"          # Change to "phi4:3.8b" if GPU is weak

# Chunking
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

# Limits & validation
MAX_PAGES_WARNING = 300   # Warn user if PDF has more than 500 pages