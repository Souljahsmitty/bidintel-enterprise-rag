import os, tempfile, json
from uuid import uuid4
from fastapi import APIRouter, UploadFile, File, Form
from ..database import get_conn
from ..services.pdf_loader import load_pdf
from ..services import store, audit_service, document_versioning_service
router = APIRouter()
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), '..', 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload(file: UploadFile = File(...), title: str = Form("Untitled"),
                 tenant_id: str = Form("demo"), access_groups: str = Form("[]")):
    groups = json.loads(access_groups) if access_groups else []
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        raw = await file.read(); tmp.write(raw); path = tmp.name
    pages = load_pdf(path)
    doc_id = uuid4()
    with open(os.path.join(UPLOAD_DIR, str(doc_id) + '.pdf'), 'wb') as fh:
        fh.write(raw)
    with get_conn() as c, c.cursor() as cur:
        cur.execute("""INSERT INTO documents (id,tenant_id,title,filename,doc_type,access_groups,created_at)
                       VALUES (%s,%s,%s,%s,%s,%s, now())""",
                    (doc_id, tenant_id, title, file.filename, "RFP", groups))
        document_versioning_service.register_version(cur, doc_id, tenant_id, raw)
        inserted = store.ingest_pages(cur, doc_id, tenant_id, pages, groups)
        audit_service.log(cur, tenant_id, "system", "embed", query=file.filename)
    return {"document_id": str(doc_id), "chunks_inserted": inserted, "embedded": True,
            "pipeline": ["loaded", "cleaned", "chunked", "embedded", "stored"]}
