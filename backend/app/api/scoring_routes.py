from fastapi import APIRouter
from pydantic import BaseModel
from ..database import get_conn
from ..services.proposal_scoring_service import score_proposal
from ..services import audit_service
router = APIRouter()

class ScoreBody(BaseModel):
    opportunity_id: str
    tenant_id: str = "demo"

@router.post("/score-proposal")
def score(body: ScoreBody):
    with get_conn() as c, c.cursor() as cur:
        result = score_proposal(cur, body.tenant_id, body.opportunity_id)
        audit_service.log(cur, body.tenant_id, "user", "score-proposal",
                          query=body.opportunity_id, eval=result["final_score"] / 100)
    return result
