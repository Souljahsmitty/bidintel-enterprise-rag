"""Reciprocal Rank Fusion: merge two ranked lists by rank position only."""

def rrf(bm25_rows, vector_rows, k=60, top=20):
    scores, texts = {}, {}
    for rank, row in enumerate(bm25_rows):
        scores[row[0]] = scores.get(row[0], 0) + 1 / (k + rank); texts[row[0]] = row[1]
    for rank, row in enumerate(vector_rows):
        scores[row[0]] = scores.get(row[0], 0) + 1 / (k + rank); texts[row[0]] = row[1]
    fused = sorted(scores.items(), key=lambda x: -x[1])[:top]
    return [{"id": cid, "text": texts[cid], "rrf": s} for cid, s in fused]
