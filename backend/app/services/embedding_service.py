"""Turn text into meaning vectors using a free local model (no cloud cost).
Production swap: call Bedrock Titan Embeddings with the same return shape."""
from functools import lru_cache

@lru_cache(maxsize=1)
def _model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("all-MiniLM-L6-v2")

def embed(texts):
    return _model().encode(list(texts), normalize_embeddings=True).tolist()
