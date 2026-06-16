"""Extract text from an uploaded PDF, page by page."""
from pypdf import PdfReader

def load_pdf(path: str):
    reader = PdfReader(path)
    return [(i + 1, (page.extract_text() or "")) for i, page in enumerate(reader.pages)]
