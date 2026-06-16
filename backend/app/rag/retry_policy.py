"""Conditional routing for the answer pipeline (LangGraph-style)."""
from ..config import MAX_RAG_RETRIES

def route(state: dict) -> str:
    if state.get("verdict") == "PASS":
        return "final_response"
    if state.get("retries", 0) < MAX_RAG_RETRIES:
        return "retry"
    return "human_review"
