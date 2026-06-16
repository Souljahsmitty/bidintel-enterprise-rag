"""GET /compliance/{opportunity_id} — requirements extracted from the RFP.
Reads 'shall' statements from the stored chunks; falls back to a demo set so the
screen always renders (clearly a fallback)."""
from fastapi import APIRouter
from ..database import get_conn
router = APIRouter()

DEMO = [
    {"id":"R-01","section":"C.3.1","text":"The contractor shall provide 24/7 SOC monitoring services.",
     "owner":"Tech Lead","risk":"High","status":"Open"},
    {"id":"R-02","section":"C.3.2","text":"Offeror must hold or obtain FedRAMP Moderate authorization.",
     "owner":"Contracts","risk":"High","status":"Open"},
    {"id":"R-03","section":"C.3.4","text":"The contractor shall staff cleared (Secret) analysts.",
     "owner":"Staffing","risk":"Med","status":"In progress"},
]

@router.get("/compliance/{opportunity_id}")
def compliance(opportunity_id: str, tenant_id: str = "demo"):
    try:
        with get_conn() as c, c.cursor() as cur:
            cur.execute(
                """SELECT id, page_number, chunk_text FROM chunks
                   WHERE tenant_id=%s AND chunk_text ILIKE '%%shall%%' LIMIT 25""",
                (tenant_id,))
            rows = cur.fetchall()
        reqs = [{"id":f"R-{i+1:02d}","section":f"p{r[1]}","text":r[2][:160],
                 "owner":"Unassigned","risk":"Med","status":"Open"} for i,r in enumerate(rows)]
        return {"opportunity_id":opportunity_id,"requirements":reqs or DEMO,"source":"chunks" if reqs else "demo"}
    except Exception:
        return {"opportunity_id":opportunity_id,"requirements":DEMO,"source":"demo"}
