"""Cross-encoder reranker: read (question, chunk) together and score true relevance.
Production swap: a hosted reranker with the same interface."""
from functools import lru_cache

@lru_cache(maxsize=1)
def _ce():
    from sentence_transformers import CrossEncoder
    return CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank(question, chunks, top=4):
    if not chunks:
        return []
    pairs = [(question, c["text"]) for c in chunks]
    for c, s in zip(chunks, _ce().predict(pairs)):
        c["rerank"] = float(s)
    return sorted(chunks, key=lambda c: -c["rerank"])[:top]
