# Backup & Restore Runbook

## Local
- Backup:  `docker compose exec -T db pg_dump -U postgres postgres > backup.sql`
- Restore: `docker compose exec -T db psql -U postgres postgres < backup.sql`

## Production (RDS)
- Enable automated snapshots; take a manual snapshot before migrations.
- Restore drill quarterly: restore snapshot to a temp instance, run proof tests.
- Object storage (uploaded docs): enable S3 versioning + lifecycle.
- Secrets: rotate DB password + Bedrock access on a schedule (Secrets Manager rotation).

## Test restore
Restore into a scratch DB, run `python -m app.scripts.test_access_control` and the eval tests.
