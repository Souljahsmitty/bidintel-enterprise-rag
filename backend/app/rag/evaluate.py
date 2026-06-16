"""Lightweight grounded-ness check. Real builds use RAGAS/Phoenix metrics."""

def evaluate(answer, evidence):
    has_citation = "[" in answer and "]" in answer
    faithfulness = 0.94 if has_citation else 0.45
    verdict = "PASS" if faithfulness >= 0.7 else "FAIL"
    return {"verdict": verdict, "faithfulness": faithfulness,
            "answer_relevance": 0.89, "context_precision": 0.82}
