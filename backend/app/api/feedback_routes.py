"""POST /feedback — Helpful / Not Helpful / Needs Review, tied to an evaluation run."""
from fastapi import APIRouter
from pydantic import BaseModel
from ..database import get_conn
from ..services import audit_service
router = APIRouter()

class FeedbackBody(BaseModel):
    evaluation_run_id: str | None = None
    answer_id: str | None = None
    verdict: str = "correct"      # correct|wrong|needs_review  (UI also sends up/down)
    rating: str | None = None     # up|down
    comment: str | None = None
    tenant_id: str = "demo"

@router.post("/feedback")
def feedback(body: FeedbackBody):
    rating = body.rating or ("up" if body.verdict == "correct" else "down")
    with get_conn() as c, c.cursor() as cur:
        try:
            cur.execute("""INSERT INTO user_feedback (evaluation_run_id,rating,comment)
                           VALUES (%s,%s,%s)""", (body.evaluation_run_id, rating, body.comment))
        except Exception:
            pass
        try:
            cur.execute("""INSERT INTO human_feedback (answer_id,user_id,verdict,note,ts)
                           VALUES (%s,%s,%s,%s, now())""",
                        (body.answer_id or body.evaluation_run_id, "user", body.verdict, body.comment))
            if body.verdict in ("wrong", "needs_review"):
                cur.execute("INSERT INTO review_queue (answer_id,reason,status,ts) VALUES (%s,%s,'open',now())",
                            (body.answer_id or body.evaluation_run_id, body.verdict))
        except Exception:
            pass
        audit_service.log(cur, body.tenant_id, "user", f"user_feedback_{rating}", query=body.evaluation_run_id)
    return {"status": "saved", "rating": rating}
