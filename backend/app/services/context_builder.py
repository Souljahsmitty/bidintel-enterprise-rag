"""Assemble the grounded prompt. Raw retrieval never goes straight to the model."""

def build_context(question, evidence):
    blocks = "\n".join(
        f'[{i+1}] (doc {e.get("doc")} p{e.get("page")}) {e["text"]}'
        for i, e in enumerate(evidence)
    )
    return (
        "You are BidIntel. Answer ONLY from the evidence below. "
        "Cite every claim like [n]. If evidence is missing, say so.\n\n"
        f"QUESTION: {question}\n\nEVIDENCE:\n{blocks}"
    )
