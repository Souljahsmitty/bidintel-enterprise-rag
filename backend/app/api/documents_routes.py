"""GET /documents (inventory) and GET /documents/{id}/download (original file).
Uploaded files are saved under app/uploads/<document_id> so a reviewer can open the
source PDF alongside the cited answer."""
import os
from fastapi import APIRouter
from fastapi.responses import FileResponse, JSONResponse
from ..database import get_conn
from ..services.tenant_service import normalize_tenant_id
router = APIRouter()
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads")

@router.get("/documents")
def list_documents(tenant_id: str = "demo"):
    tenant_id = normalize_tenant_id(tenant_id)
    try:
        with get_conn() as c, c.cursor() as cur:
            cur.execute("""SELECT d.id, d.title, d.filename, d.doc_type, d.access_groups,
                                  d.created_at, count(ch.id)
                           FROM documents d LEFT JOIN chunks ch ON ch.document_id = d.id
                           WHERE d.tenant_id = %s
                           GROUP BY d.id ORDER BY d.created_at DESC LIMIT 100""", (tenant_id,))
            rows = cur.fetchall()
        docs = [{"id": str(r[0]), "title": r[1], "filename": r[2], "type": r[3],
                 "access_groups": r[4], "created_at": str(r[5]), "chunks": r[6]} for r in rows]
        return {"documents": docs}
    except Exception as e:
        return {"documents": [], "error": str(e)}

@router.get("/documents/{document_id}/download")
def download(document_id: str):
    for ext in (".pdf", ".txt", ""):
        path = os.path.join(UPLOAD_DIR, document_id + ext)
        if os.path.exists(path):
            return FileResponse(path, filename=os.path.basename(path))
    return JSONResponse({"error": "file not found (was it uploaded via /upload?)"}, status_code=404)
