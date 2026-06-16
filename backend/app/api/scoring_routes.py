from fastapi import APIRouter
from pydantic import BaseModel
from ..database import get_conn
from ..services.proposal_scoring_service import score_proposal
from ..services import audit_service
from ..services.tenant_service import normalize_tenant_id
router = APIRouter()

class ScoreBody(BaseModel):
    opportunity_id: str
    tenant_id: str = "demo"

@router.post("/score-proposal")
def score(body: ScoreBody):
    tenant_id = normalize_tenant_id(body.tenant_id)
    with get_conn() as c, c.cursor() as cur:
        result = score_proposal(cur, tenant_id, body.opportunity_id)
        audit_service.log(cur, tenant_id, "user", "score-proposal",
                          query=body.opportunity_id, eval=result["final_score"] / 100)
    return result
