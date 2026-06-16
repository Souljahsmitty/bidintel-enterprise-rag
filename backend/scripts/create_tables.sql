-- BidIntel schema. Run after: CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS tenants (
  id UUID PRIMARY KEY,
  name TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS documents (
  id UUID PRIMARY KEY,
  tenant_id UUID,
  title TEXT,
  filename TEXT,
  doc_type TEXT,
  access_groups TEXT[],
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS chunks (
  id UUID PRIMARY KEY,
  document_id UUID REFERENCES documents(id),
  tenant_id UUID,
  page_number INT,
  chunk_text TEXT,
  embedding vector(384),          -- meaning vector (all-MiniLM-L6-v2)
  search_vector tsvector,         -- keyword index (BM25-style)
  access_groups TEXT[]
);

CREATE TABLE IF NOT EXISTS audit_logs (
  id BIGSERIAL PRIMARY KEY,
  tenant_id UUID, user_id TEXT, action TEXT, query TEXT,
  doc_ids INT[], chunk_ids INT[], eval NUMERIC, guardrail TEXT,
  ts TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS proposal_scores (
  id UUID PRIMARY KEY, tenant_id UUID, opportunity TEXT,
  relevance INT, compliance INT, evidence INT, risk INT,
  final_score INT, ts TIMESTAMPTZ DEFAULT now()
);

-- evaluator / feedback / review tables (reliability loop)
CREATE TABLE IF NOT EXISTS evaluation_results (
  id BIGSERIAL PRIMARY KEY, answer_id UUID, verdict TEXT,
  faithfulness NUMERIC, context_recall NUMERIC, ts TIMESTAMPTZ DEFAULT now()
);
CREATE TABLE IF NOT EXISTS human_feedback (
  id BIGSERIAL PRIMARY KEY, answer_id UUID, user_id TEXT,
  verdict TEXT, note TEXT, ts TIMESTAMPTZ DEFAULT now()
);
CREATE TABLE IF NOT EXISTS review_queue (
  id BIGSERIAL PRIMARY KEY, answer_id UUID, reason TEXT,
  status TEXT DEFAULT 'open', ts TIMESTAMPTZ DEFAULT now()
);

-- indexes
CREATE INDEX IF NOT EXISTS chunks_embedding_hnsw
  ON chunks USING hnsw (embedding vector_cosine_ops);
CREATE INDEX IF NOT EXISTS chunks_search_gin
  ON chunks USING gin (search_vector);

-- keep search_vector in sync with chunk_text
CREATE OR REPLACE FUNCTION chunks_tsv_trigger() RETURNS trigger AS $$
BEGIN
  NEW.search_vector := to_tsvector('english', COALESCE(NEW.chunk_text,''));
  RETURN NEW;
END $$ LANGUAGE plpgsql;
DROP TRIGGER IF EXISTS chunks_tsv ON chunks;
CREATE TRIGGER chunks_tsv BEFORE INSERT OR UPDATE ON chunks
  FOR EACH ROW EXECUTE FUNCTION chunks_tsv_trigger();
