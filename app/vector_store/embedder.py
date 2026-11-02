import numpy as np
import re
from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import normalize

class PropertyEmbedder:
    """
    Computes dense vector representations for property descriptions and queries
    as specified in SRS FR-1.2.
    Uses TF-IDF + Latent Semantic Analysis (Truncated SVD) with L2 normalization,
    providing deterministic, lightning-fast (<1ms) vector embeddings without external API limits.
    """
    def __init__(self, embedding_dim: int = 128):
        self.embedding_dim = embedding_dim
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            max_features=5000,
            token_pattern=r"(?u)\b\w[\w-]*\b"
        )
        self.svd = TruncatedSVD(n_components=self.embedding_dim, random_state=42)
        self.is_fitted = False

    def clean_text(self, text: str) -> str:
        text = text.lower()
        # Keep alphanumeric, currency symbols, and hyphens
        text = re.sub(r'[^a-z0-9\s₹\-\.]', ' ', text)
        return " ".join(text.split())

    def fit(self, texts: List[str]):
        cleaned = [self.clean_text(t) for t in texts]
        tfidf_matrix = self.vectorizer.fit_transform(cleaned)
        
        # Ensure n_components does not exceed min(n_samples, n_features)
        n_components = min(self.embedding_dim, tfidf_matrix.shape[0], tfidf_matrix.shape[1] - 1)
        if n_components < 2:
            n_components = min(tfidf_matrix.shape[0], tfidf_matrix.shape[1])
        
        self.svd = TruncatedSVD(n_components=max(1, n_components), random_state=42)
        self.svd.fit(tfidf_matrix)
        self.is_fitted = True

    def transform(self, texts: List[str]) -> np.ndarray:
        if not self.is_fitted:
            self.fit(texts)
        cleaned = [self.clean_text(t) for t in texts]
        tfidf_matrix = self.vectorizer.transform(cleaned)
        dense_vectors = self.svd.transform(tfidf_matrix)
        # Normalize to unit length for exact cosine similarity
        normed = normalize(dense_vectors, norm='l2', axis=1)
        return normed.astype(np.float32)

    def embed_query(self, query: str) -> np.ndarray:
        return self.transform([query])[0]

