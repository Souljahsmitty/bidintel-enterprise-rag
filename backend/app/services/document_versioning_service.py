"""Document versioning: hash an upload, create a version row if the file changed,
and mark old chunks inactive so retrieval only uses the latest version."""
import hashlib
from uuid import uuid4

def file_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def register_version(cur, document_id, tenant_id, data: bytes):
    h = file_hash(data)
    cur.execute("SELECT COALESCE(MAX(version_number),0) FROM document_versions WHERE document_id=%s",
                (document_id,))
    last = cur.fetchone()[0]
    cur.execute("SELECT 1 FROM document_versions WHERE document_id=%s AND file_hash=%s",
                (document_id, h))
    if cur.fetchone():
        return None  # unchanged file, no new version
    version_id = uuid4()
    cur.execute("""INSERT INTO document_versions (id, document_id, version_number, file_hash)
                   VALUES (%s,%s,%s,%s)""", (version_id, document_id, last + 1, h))
    # mark previous chunks of this document inactive
    cur.execute("UPDATE chunks SET is_active=false WHERE document_id=%s", (document_id,))
    return version_id
