#!/usr/bin/env bash
set -e
echo "[1/6] checking Docker..."; docker info >/dev/null 2>&1 || { echo "Start Docker Desktop first."; exit 1; }
echo "[2/6] starting containers..."; docker compose up --build -d
echo "[3/6] waiting for Postgres..."; sleep 8
echo "[4/6] applying schema + enterprise migration..."
docker compose exec -T db psql -U postgres -d postgres -f - < backend/scripts/create_tables.sql || true
docker compose exec -T db psql -U postgres -d postgres -f - < backend/app/database/migrations/003_enterprise_tables.sql || true
echo "[5/6] seeding sample documents..."
docker compose exec -T backend python scripts/seed_mock_corpus.py || true
echo "[6/6] ready:"
echo "  Frontend : http://localhost:5173"
echo "  Swagger  : http://localhost:8000/docs"
echo "  Health   : http://localhost:8000/health"
echo "Proof: docker compose exec -T backend python scripts/test_access_control.py"
