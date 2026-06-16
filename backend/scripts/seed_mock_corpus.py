"""Insert 5 mock federal-bidding documents + chunks so reviewers have predictable data.
Run: python -m app.scripts.seed_mock_corpus"""
from uuid import uuid4
from app.database import get_conn
from app.services.embedding_service import embed
from app.services.tenant_service import DEMO_TENANT_ID

DOCS = [
 ("DHS Cyber Modernization RFP", "proposal",
  "The contractor shall provide 24/7 SOC monitoring services. FedRAMP Moderate authorization is required."),
 ("SOC Past Performance", "past_performance",
  "Delivered 24/7 SOC monitoring and reduced mean time to respond by 40% for a federal agency."),
 ("Compliance Controls Policy", "compliance",
  "The contractor shall comply with NIST SP 800-171 and provide monthly metrics reporting."),
 ("Pricing Realism Note", "pricing",
  "Labor rates align to GSA MAS ceilings; pricing realism documented for cleared analysts."),
 ("HR Payroll Restricted", "hr",
  "Employee payroll records and salary bands. Restricted to HR role only."),
]

def main():
    with get_conn() as c, c.cursor() as cur:
        cur.execute("INSERT INTO tenants (id,name) VALUES (%s,%s) ON CONFLICT DO NOTHING",
                    (DEMO_TENANT_ID, "demo"))
        filenames = [title + ".txt" for title, _, _ in DOCS]
        try:
            cur.execute("""DELETE FROM query_answer_cache WHERE tenant_id=%s""", (DEMO_TENANT_ID,))
        except Exception:
            pass
        cur.execute("""DELETE FROM chunks
                       WHERE tenant_id=%s AND document_id IN (
                         SELECT id FROM documents WHERE tenant_id=%s AND filename = ANY(%s)
                       )""", (DEMO_TENANT_ID, DEMO_TENANT_ID, filenames))
        try:
            cur.execute("""DELETE FROM document_versions
                           WHERE document_id IN (
                             SELECT id FROM documents WHERE tenant_id=%s AND filename = ANY(%s)
                           )""", (DEMO_TENANT_ID, filenames))
        except Exception:
            pass
        cur.execute("""DELETE FROM documents WHERE tenant_id=%s AND filename = ANY(%s)""",
                    (DEMO_TENANT_ID, filenames))
        n_docs = n_chunks = 0
        for title, group, text in DOCS:
            doc_id = uuid4()
            cur.execute("""INSERT INTO documents (id,tenant_id,title,filename,doc_type,access_groups,created_at)
                           VALUES (%s,%s,%s,%s,%s,%s, now())""",
                        (doc_id, DEMO_TENANT_ID, title, title + ".txt", group, [group]))
            vec = embed([text])[0]
            cur.execute("""INSERT INTO chunks (id,document_id,tenant_id,page_number,chunk_text,embedding,access_groups,is_active)
                           VALUES (%s,%s,%s,%s,%s,%s,%s,true)""",
                        (uuid4(), doc_id, DEMO_TENANT_ID, 1, text, vec, [group]))
            n_docs += 1; n_chunks += 1
        print(f"seeded {n_docs} documents and {n_chunks} chunks")

if __name__ == "__main__":
    main()
