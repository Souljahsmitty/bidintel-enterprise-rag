"""Decide when trusted local evidence is strong enough to skip the LLM."""
import re
from ..config import TRUSTED_KB_CONFIDENCE_THRESHOLD


def _tokens(text: str) -> set[str]:
    out = set()
    for w in re.findall(r"[a-z0-9]+", text.lower()):
        if len(w) < 3:
            continue
        out.add(w)
        if w.endswith("ment"):
            out.add(w[:-4])
        if w.endswith("ed"):
            out.add(w[:-2])
        if w.endswith("s"):
            out.add(w[:-1])
    return out


def trusted_kb_confidence(question: str, evidence: list) -> dict:
    if not evidence:
        return {"score": 0.0, "decision": "llm_fallback", "reason": "no evidence retrieved"}
    top = evidence[0]
    qw = _tokens(question)
    ew = _tokens(top.get("text", ""))
    overlap = len(qw & ew) / len(qw) if qw else 0.0
    rerank = float(top.get("rerank", 0.0) or 0.0)
    rrf = float(top.get("rrf", 0.0) or 0.0)
    # Normalize local reranker/rrf signals into a bounded production-style gate.
    score = min(1.0, round((overlap * 0.55) + (min(rerank, 6.0) / 6.0 * 0.35) + (min(rrf, 0.04) / 0.04 * 0.10), 3))
    strong = score >= TRUSTED_KB_CONFIDENCE_THRESHOLD
    return {
        "score": score,
        "decision": "trusted_kb_direct" if strong else "llm_fallback",
        "reason": "top trusted chunk passed confidence gate" if strong else "retrieved evidence below confidence threshold",
        "threshold": TRUSTED_KB_CONFIDENCE_THRESHOLD,
    }


def answer_from_trusted_evidence(question: str, evidence: list) -> str:
    if not evidence:
        return "I do not have enough trusted evidence to answer that."
    text = evidence[0].get("text", "").strip()
    if not text:
        return "I do not have enough trusted evidence to answer that."
    return f"Based on the trusted knowledge base: {text} [1]"
