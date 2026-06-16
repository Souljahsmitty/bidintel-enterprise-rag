from app.services.confidence_gate_service import answer_from_trusted_evidence, trusted_kb_confidence
from app.services.query_cache_service import normalize_question, question_hash


def test_question_hash_normalizes_common_variations():
    assert normalize_question(" What is the SOC monitoring requirement? ") == "what is the soc monitoring requirement"
    assert question_hash("What is the SOC monitoring requirement?") == question_hash(
        "what is the soc monitoring requirement"
    )


def test_confidence_gate_allows_strong_trusted_evidence():
    evidence = [{
        "text": "The contractor shall provide 24/7 SOC monitoring services. FedRAMP Moderate authorization is required.",
        "rerank": 5.6,
        "rrf": 0.033,
    }]
    gate = trusted_kb_confidence("What is the SOC monitoring requirement?", evidence)
    assert gate["decision"] == "trusted_kb_direct"
    assert gate["score"] >= gate["threshold"]


def test_trusted_answer_cites_first_evidence_chunk():
    answer = answer_from_trusted_evidence("What is required?", [{"text": "Provide 24/7 SOC monitoring."}])
    assert "Provide 24/7 SOC monitoring." in answer
    assert "[1]" in answer
