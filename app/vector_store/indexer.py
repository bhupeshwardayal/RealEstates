import os
import json
import faiss
import numpy as np
from typing import List, Dict, Any, Tuple
from app.config import FAISS_INDEX_PATH, METADATA_PATH, DEFAULT_TOP_K
from app.vector_store.embedder import PropertyEmbedder
from app.database.db import SessionLocal, Property

class PropertyVectorIndex:
    """
    Manages FAISS vector indexing and similarity retrieval
    as specified in SRS FR-1.3 and FR-3.1.
    """
    def __init__(self):
        self.index = None
        self.embedder = PropertyEmbedder(embedding_dim=64)
        self.property_metadata: List[Dict[str, Any]] = []
        self.property_id_to_idx: Dict[int, int] = {}
        self.load_or_build()

    def build_from_db(self):
        from app.database.db import init_db
        init_db()
        db = SessionLocal()
        try:
            properties = db.query(Property).all()
            if not properties:
                print("No properties in database to index.")
                return

            context_chunks = [p.to_context_chunk() for p in properties]
            self.embedder.fit(context_chunks)
            vectors = self.embedder.transform(context_chunks)

            # Dimensionality of dense vectors
            d = vectors.shape[1]
            # Use IndexFlatIP (Inner Product) on normalized vectors for exact Cosine Similarity
            self.index = faiss.IndexFlatIP(d)
            self.index.add(vectors)

            # Save metadata
            self.property_metadata = [p.to_dict() for p in properties]
            self.property_id_to_idx = {p.property_id: i for i, p in enumerate(properties)}

            self.save()
            print(f"Indexed {len(properties)} properties into FAISS with dimension {d}.")
        finally:
            db.close()

    def save(self):
        if self.index is not None:
            faiss.write_index(self.index, str(FAISS_INDEX_PATH))
            with open(METADATA_PATH, "w", encoding="utf-8") as f:
                json.dump({
                    "metadata": self.property_metadata,
                    "id_map": self.property_id_to_idx
                }, f, indent=2)

    def load_or_build(self):
        from app.database.db import init_db
        init_db()
        if FAISS_INDEX_PATH.exists() and METADATA_PATH.exists():
            try:
                self.index = faiss.read_index(str(FAISS_INDEX_PATH))
                with open(METADATA_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.property_metadata = data.get("metadata", [])
                    self.property_id_to_idx = {int(k): v for k, v in data.get("id_map", {}).items()}
                # Fit embedder on stored context texts
                db = SessionLocal()
                try:
                    props = db.query(Property).all()
                    if props:
                        self.embedder.fit([p.to_context_chunk() for p in props])
                finally:
                    db.close()
                print(f"Loaded FAISS index containing {self.index.ntotal} vectors.")
                return
            except Exception as e:
                print(f"Failed to load existing index: {e}. Rebuilding...")
        self.build_from_db()

    def search(self, query: str, top_k: int = DEFAULT_TOP_K) -> List[Dict[str, Any]]:
        """
        FR-3.1 Semantic Search Retrieval:
        Returns top-K relevant properties with cosine similarity confidence score.
        """
        if self.index is None or self.index.ntotal == 0:
            self.build_from_db()

        if self.index is None or self.index.ntotal == 0:
            return []

        query_vector = self.embedder.embed_query(query).reshape(1, -1)
        k = min(top_k, self.index.ntotal)
        scores, indices = self.index.search(query_vector, k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx != -1 and idx < len(self.property_metadata):
                prop_info = dict(self.property_metadata[idx])
                # Convert cosine similarity (-1 to 1) into percentage confidence (60% to 99.8%)
                confidence = float(np.clip((score + 1.0) / 2.0, 0.0, 1.0) * 100)
                prop_info["similarity_score"] = round(float(score), 4)
                prop_info["match_confidence"] = round(confidence, 1)
                results.append(prop_info)

        return results

# Global singleton
vector_index = PropertyVectorIndex()
