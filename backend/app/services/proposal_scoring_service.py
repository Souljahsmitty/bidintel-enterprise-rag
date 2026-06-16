"""Score a proposal against retrieved evidence. Transparent + weighted.

NOTE: This is a SIMPLIFIED/PLACEHOLDER scorer for the tutorial. The factor values
below are illustrative. A production version computes each sub-score from retrieved
evidence. It is intentionally simple so beginners can see the shape of the output."""
WEIGHTS = {"relevance": .30, "compliance": .25, "evidence": .25, "risk": .20}

def score_proposal(cur, tenant_id, opportunity):
    # Each sub-score is backed by retrieval in a full build; demo values shown.
    factors = {"relevance": 84, "compliance": 78, "evidence": 88, "risk": 100 - 34}
    final = round(sum(factors[k] * WEIGHTS[k] for k in factors))
    return {
        "final_score": final, "factors": factors,
        "recommendation": "BID" if final >= 70 else "NO-BID",
    }
