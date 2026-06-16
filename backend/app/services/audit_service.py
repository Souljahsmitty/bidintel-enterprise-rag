"""Every route logs here before returning. Immutable audit trail."""

def log(cur, tenant_id, user_id, action, query=None, doc_ids=None,
        chunk_ids=None, eval=None, guardrail="OK"):
    cur.execute(
        """INSERT INTO audit_logs
           (tenant_id,user_id,action,query,doc_ids,chunk_ids,eval,guardrail,ts)
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s, now())""",
        (tenant_id, user_id, action, query, doc_ids, chunk_ids, eval, guardrail),
    )
