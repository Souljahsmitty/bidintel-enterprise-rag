# Hiring-Manager Demo Script (8-12 min)

1. Open README + architecture diagram (30s).
2. `bash scripts/start_local.sh` (one command).
3. Open the frontend (login -> dashboard).
4. Open Swagger (/docs) - show endpoints.
5. Seed documents (5 mock federal docs).
6. Hybrid proof: ask "What is the SOC monitoring requirement?" -> cited answer.
7. Access-control proof: `python -m app.scripts.test_access_control` -> proposal_writer blocked from HR.
8. Show the Response Quality trust panel (faithfulness, citation support, coverage, risk).
9. Click Helpful/Not Helpful -> user_feedback row.
10. Show evaluation_runs / evaluation_scores / request_logs rows in pgAdmin.
11. Explain AWS/IAM mapping (roles, least privilege).
12. Show CI workflow + GitHub repo.

Pitch line: "BidIntel is an enterprise-style hybrid RAG platform with retrieval, RRF fusion,
reranking, context assembly, citations, evaluation scoring, RBAC, feedback, and CI/CD."
