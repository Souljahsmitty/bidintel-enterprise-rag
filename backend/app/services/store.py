"""Ingestion writer: chunk + embed + insert rows. search_vector fills via trigger."""
from uuid import uuid4
from .text_cleaner import clean
from .chunker import chunk
from .embedding_service import embed

def ingest_pages(cur, doc_id, tenant_id, pages, access_groups):
    inserted = 0
    for page_no, text in pages:
        for ck in chunk(clean(text)):
            vec = embed([ck])[0]
            cur.execute(
                """INSERT INTO chunks
                   (id,document_id,tenant_id,page_number,chunk_text,embedding,access_groups)
                   VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                (uuid4(), doc_id, tenant_id, page_no, ck, vec, access_groups),
            )
            inserted += 1
    return inserted
