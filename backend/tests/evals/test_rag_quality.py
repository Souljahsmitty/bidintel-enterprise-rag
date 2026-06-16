"""Regression tests for RAG quality. Uses the simulated RAGAS metrics so it runs offline;
swap evaluate_rag for real RAGAS/DeepEval in production. Run: pytest backend/tests/evals"""
import json, os
from app.services.evaluation.ragas_service import evaluate_rag

DATA = os.path.join(os.path.dirname(__file__), "eval_dataset.jsonl")

def _cases():
    with open(DATA) as f:
        return [json.loads(l) for l in f if l.strip()]

def test_faithfulness_threshold():
    for case in _cases():
        ev = [{"text": case["expected_evidence"]}]
        m = evaluate_rag(case["question"], "Answer with citation [1]", ev)
        assert m["faithfulness"] >= case["min_faithfulness"], case["question"]

def test_context_recall_present():
    for case in _cases():
        ev = [{"text": case["expected_evidence"]}]
        m = evaluate_rag(case["question"], "Answer [1]", ev)
        assert 0 <= m["context_recall"] <= 1
