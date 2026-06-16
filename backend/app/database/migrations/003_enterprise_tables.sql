-- Enterprise hardening tables. Run AFTER create_tables.sql.
CREATE TABLE IF NOT EXISTS roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT UNIQUE NOT NULL
);
CREATE TABLE IF NOT EXISTS user_roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    tenant_id UUID NOT NULL,
    role_id UUID NOT NULL REFERENCES roles(id)
);
CREATE TABLE IF NOT EXISTS document_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL REFERENCES documents(id),
    version_number INT NOT NULL,
    file_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT now()
);
CREATE TABLE IF NOT EXISTS evaluation_runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    tenant_id UUID,
    created_at TIMESTAMP DEFAULT now()
);
CREATE TABLE IF NOT EXISTS evaluation_scores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    evaluation_run_id UUID REFERENCES evaluation_runs(id),
    faithfulness FLOAT, answer_relevance FLOAT,
    context_precision FLOAT, context_recall FLOAT,
    citation_accuracy FLOAT, response_quality FLOAT
);
CREATE TABLE IF NOT EXISTS citation_checks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    evaluation_run_id UUID REFERENCES evaluation_runs(id),
    claim TEXT, citation TEXT, supported BOOLEAN, reason TEXT
);
CREATE TABLE IF NOT EXISTS user_feedback (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    evaluation_run_id UUID,
    rating TEXT, comment TEXT, created_at TIMESTAMP DEFAULT now()
);
CREATE TABLE IF NOT EXISTS request_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID, endpoint TEXT, latency_ms INT,
    input_tokens INT, output_tokens INT, estimated_cost FLOAT,
    created_at TIMESTAMP DEFAULT now()
);
CREATE TABLE IF NOT EXISTS query_answer_cache (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL,
    role TEXT NOT NULL,
    question_hash TEXT NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    citations JSONB DEFAULT '[]'::jsonb,
    evidence JSONB DEFAULT '[]'::jsonb,
    metrics JSONB DEFAULT '{}'::jsonb,
    quality JSONB DEFAULT '{}'::jsonb,
    source TEXT NOT NULL,
    confidence FLOAT DEFAULT 0,
    hit_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),
    UNIQUE (tenant_id, role, question_hash)
);
CREATE INDEX IF NOT EXISTS query_answer_cache_lookup
    ON query_answer_cache (tenant_id, role, question_hash);
-- document versioning columns on chunks
ALTER TABLE chunks ADD COLUMN IF NOT EXISTS document_version_id UUID;
ALTER TABLE chunks ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT true;
