"""BM25-style keyword search via Postgres full-text. Enforces tenant + role access
groups in SQL so restricted chunks never reach the model."""
from ..security.rbac import sql_filter

def bm25_search(cur, tenant_id, query, role="proposal_writer", k=20):
    clause, params = sql_filter(role)
    cur.execute(f"""
        SELECT id, chunk_text,
               ts_rank(search_vector, plainto_tsquery('english', %s)) AS score
        FROM chunks
        WHERE tenant_id = %s
          AND COALESCE(is_active, true) = true
          AND search_vector @@ plainto_tsquery('english', %s)
          {clause}
        ORDER BY score DESC LIMIT %s
    """, [query, tenant_id, query, *params, k])
    return cur.fetchall()
