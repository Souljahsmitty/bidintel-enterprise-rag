"""Vector (meaning) search via pgvector cosine distance. Same tenant + role enforcement."""
from .embedding_service import embed
from ..security.rbac import sql_filter

def vector_search(cur, tenant_id, query, role="proposal_writer", k=20):
    qvec = embed([query])[0]
    clause, params = sql_filter(role)
    cur.execute(f"""
        SELECT id, chunk_text, 1 - (embedding <=> %s::vector) AS score
        FROM chunks
        WHERE tenant_id = %s AND COALESCE(is_active, true) = true {clause}
        ORDER BY embedding <=> %s::vector LIMIT %s
    """, [qvec, tenant_id, *params, qvec, k])
    return cur.fetchall()
