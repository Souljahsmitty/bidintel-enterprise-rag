"""GET /dashboard — aggregate counts for the home screen cards."""
from fastapi import APIRouter
from ..database import get_conn
router = APIRouter()

@router.get("/dashboard")
def dashboard(tenant_id: str = "demo"):
    out = {"documents":0,"chunks":0,"scores":0,"recent":[]}
    try:
        with get_conn() as c, c.cursor() as cur:
            cur.execute("SELECT count(*) FROM documents WHERE tenant_id=%s",(tenant_id,)); out["documents"]=cur.fetchone()[0]
            cur.execute("SELECT count(*) FROM chunks WHERE tenant_id=%s",(tenant_id,)); out["chunks"]=cur.fetchone()[0]
            cur.execute("SELECT count(*) FROM proposal_scores WHERE tenant_id=%s",(tenant_id,)); out["scores"]=cur.fetchone()[0]
            cur.execute("SELECT action, ts FROM audit_logs WHERE tenant_id=%s ORDER BY ts DESC LIMIT 5",(tenant_id,))
            out["recent"]=[{"action":a,"ts":str(t)} for a,t in cur.fetchall()]
    except Exception as e:
        out["error"]=str(e)
    return out
