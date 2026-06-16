"""RAGAS/DeepEval-style metrics. SIMULATED locally with deterministic heuristics so the
eval pipeline runs offline. Production swaps in real RAGAS/DeepEval with the same keys."""

def evaluate_rag(question: str, answer: str, evidence: list) -> dict:
    has_cite = "[" in answer and "]" in answer
    ev_text = " ".join(e.get("text", "") for e in evidence).lower()
    qw = {w for w in question.lower().split() if len(w) > 3}
    recall = round(min(1.0, (len(qw & set(ev_text.split())) / len(qw)) if qw else 0.7) , 2)
    return {
        "faithfulness": 0.92 if has_cite else 0.5,
        "answer_relevance": 0.88,
        "context_precision": 0.80,
        "context_recall": max(0.6, recall),
    }
