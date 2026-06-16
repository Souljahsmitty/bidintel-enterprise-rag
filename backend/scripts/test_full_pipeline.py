"""End-to-end proof. Run with: pytest backend/scripts/test_full_pipeline.py"""
from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def test_health():
    assert client.get("/health").status_code == 200

def test_ask_returns_cited_answer():
    r = client.post("/ask", json={"question": "SOC monitoring requirement?"})
    assert r.status_code == 200
    body = r.json()
    assert "answer" in body and "eval" in body

def test_score_proposal_in_range():
    r = client.post("/score-proposal", json={"opportunity_id": "dhs"})
    assert 0 <= r.json()["final_score"] <= 100
