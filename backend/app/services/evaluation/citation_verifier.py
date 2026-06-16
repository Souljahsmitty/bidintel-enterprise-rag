"""Citation verification: check that each cited chunk actually supports the claim.
Deterministic local check (word overlap) so it runs with no external LLM. A production
build swaps in an LLM judge with the same output shape."""

def _supported(claim: str, evidence: str) -> bool:
    cw = {w for w in claim.lower().split() if len(w) > 3}
    ew = {w for w in evidence.lower().split() if len(w) > 3}
    if not cw:
        return True
    overlap = len(cw & ew) / len(cw)
    return overlap >= 0.25

def verify_citations(answer: str, citations: list) -> dict:
    checks = []
    for c in citations:
        claim = f"marker {c.get('marker')}"
        ev = c.get("text", "")
        ok = _supported(answer, ev)
        checks.append({"claim": claim, "citation": f"doc {c.get('document_id')} p{c.get('page')}",
                       "supported": ok, "reason": "evidence overlaps the answer" if ok else "weak overlap"})
    supported = sum(1 for c in checks if c["supported"])
    accuracy = supported / len(checks) if checks else 0.0
    return {"citation_accuracy": round(accuracy, 2),
            "unsupported_claims": len(checks) - supported, "checks": checks}
