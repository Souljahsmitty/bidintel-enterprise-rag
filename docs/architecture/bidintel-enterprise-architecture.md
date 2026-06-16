# BidIntel Enterprise Architecture

See `bidintel-enterprise-architecture.mmd` (Mermaid). Flow: React UI -> FastAPI routes ->
model-efficiency harness (exact cache -> trusted KB -> confidence gate -> LLM fallback) ->
RBAC-filtered hybrid retrieval (BM25 + vector -> RRF -> rerank) -> citations -> evaluation
(citation verify, RAGAS metrics, response quality, Phoenix trace) -> PostgreSQL/pgvector.
When confidence is high, `/ask` can return a cited trusted-KB answer without calling the LLM.
When confidence is low, it builds context and falls back to the Bedrock/Claude interface.
Observability logs latency + token/cost estimates per request.
Production maps the same code onto ECR/ECS/RDS/Bedrock/Cognito/Secrets/CloudWatch.
