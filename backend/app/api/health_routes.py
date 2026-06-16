from fastapi import APIRouter
from ..database import get_conn
router = APIRouter()

@router.get("/health")
def health():
    try:
        with get_conn() as c, c.cursor() as cur:
            cur.execute("SELECT 1")
        return {"status": "ok", "db": "connected"}
    except Exception as e:
        return {"status": "degraded", "db": str(e)}
