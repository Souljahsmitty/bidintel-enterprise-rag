#!/usr/bin/env bash
# Reviewer demo: prove the RAG pipeline works end-to-end in ~1 minute.
set -e
BASE="${1:-http://localhost:8000}"
echo "== 1. health =="; curl -s "$BASE/health"; echo
echo "== 2. seed 5 mock federal documents =="
docker compose exec -T backend env PYTHONPATH=. python scripts/seed_mock_corpus.py
echo "== 3. ask a grounded question (cache/trusted KB/LLM routing + evaluation) =="
curl -s -X POST "$BASE/ask" -H 'content-type: application/json' \
  -d '{"question":"What is the SOC monitoring requirement?","tenant_id":"demo","role":"proposal_writer"}' \
  | python3 -m json.tool
echo "== 4. RBAC proof: a proposal writer is blocked from HR =="
docker compose exec -T backend env PYTHONPATH=. python scripts/test_access_control.py
echo "Done. You just saw: cache/trusted-KB/LLM routing -> cited answer -> response-quality score, plus RBAC."
