"""Map [n] markers in the answer back to document / page / chunk."""
import re

def attach_citations(answer, evidence):
    cites = []
    for n in re.findall(r"\[(\d+)\]", answer):
        idx = int(n) - 1
        if 0 <= idx < len(evidence):
            e = evidence[idx]
            cites.append({
                "marker": int(n), "document_id": e.get("doc"),
                "filename": e.get("file"), "page": e.get("page"),
                "chunk_id": e.get("id"), "text": e["text"][:160],
            })
    return {"answer": answer, "citations": cites}
