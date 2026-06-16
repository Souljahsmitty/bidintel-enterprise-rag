# BidIntel Enterprise Architecture

See `bidintel-enterprise-architecture.mmd` (Mermaid). Flow: React UI -> FastAPI routes ->
RBAC-filtered hybrid retrieval (BM25 + vector -> RRF -> rerank) -> context builder ->
(mock) Bedrock -> citations -> evaluation (citation verify, RAGAS metrics, response quality,
Phoenix trace) -> PostgreSQL/pgvector. Observability logs latency + cost per request.
Production maps the same code onto ECR/ECS/RDS/Bedrock/Cognito/Secrets/CloudWatch.
