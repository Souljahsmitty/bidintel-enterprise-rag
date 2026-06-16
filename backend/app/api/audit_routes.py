"""GET /audit-logs — recent audit rows for the Audit screen."""
from fastapi import APIRouter
from ..database import get_conn
router = APIRouter()

@router.get("/audit-logs")
def audit_logs(tenant_id: str = "demo", limit: int = 25):
    try:
        with get_conn() as c, c.cursor() as cur:
            cur.execute("""SELECT ts, user_id, action, query, eval, guardrail
                           FROM audit_logs WHERE tenant_id=%s ORDER BY ts DESC LIMIT %s""",(tenant_id,limit))
            rows=[{"ts":str(t),"user":u,"action":a,"query":q,"eval":float(e) if e else None,"guardrail":g}
                  for t,u,a,q,e,g in cur.fetchall()]
        return {"events":rows}
    except Exception as e:
        return {"events":[],"error":str(e)}
