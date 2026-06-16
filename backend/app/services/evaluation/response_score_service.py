"""Response Quality Score: combine metrics into ONE user-facing trust number + reasons.
Formula (from the enterprise spec):
  Faithfulness 30% + Citation Accuracy 25% + Answer Relevance 20%
  + Context Precision 15% + Context Recall 10%."""

WEIGHTS = {"faithfulness": .30, "citation_accuracy": .25, "answer_relevance": .20,
           "context_precision": .15, "context_recall": .10}

def _band(x): return "Strong" if x >= 0.8 else ("Medium" if x >= 0.6 else "Weak")

def response_quality(metrics: dict) -> dict:
    score = sum(metrics.get(k, 0) * w for k, w in WEIGHTS.items())
    pct = round(score * 100)
    risk = "Low" if score >= 0.8 else ("Medium" if score >= 0.6 else "High")
    return {
        "response_quality": pct,
        "citation_support": _band(metrics.get("citation_accuracy", 0)),
        "evidence_coverage": _band(metrics.get("context_recall", 0)),
        "hallucination_risk": risk,
        "sources_used": metrics.get("sources_used", 0),
        "reason": f"Faithfulness {_band(metrics.get('faithfulness',0))}, "
                  f"citations {_band(metrics.get('citation_accuracy',0))}, "
                  f"coverage {_band(metrics.get('context_recall',0))}.",
    }
