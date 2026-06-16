"""Normalise raw PDF text before chunking."""
import re

def clean(text: str) -> str:
    text = re.sub(r"-\n", "", text)      # join words broken across lines
    text = re.sub(r"\s+", " ", text)     # collapse whitespace
    return text.strip()
