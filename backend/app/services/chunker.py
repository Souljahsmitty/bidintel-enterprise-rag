"""Split cleaned text into overlapping, searchable evidence blocks."""

def chunk(text: str, size: int = 800, overlap: int = 120):
    out, i = [], 0
    while i < len(text):
        out.append(text[i:i + size])
        i += size - overlap
    return [c for c in out if c.strip()]
