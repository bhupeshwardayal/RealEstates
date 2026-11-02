import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'real_estates.db'}")

# Vector store configuration
VECTOR_INDEX_DIR = BASE_DIR / "data" / "vector_index"
VECTOR_INDEX_DIR.mkdir(parents=True, exist_ok=True)
FAISS_INDEX_PATH = VECTOR_INDEX_DIR / "property_faiss.index"
METADATA_PATH = VECTOR_INDEX_DIR / "property_metadata.json"

# App settings
DEFAULT_TOP_K = 4
MAX_SEARCH_RESULTS = 10
HALLUCINATION_GUARD_STRICT = True

