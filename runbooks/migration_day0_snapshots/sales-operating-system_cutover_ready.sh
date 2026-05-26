#!/usr/bin/env bash
# sales-operating-system cutover script — Day 4
# Authored: 2026-05-25 by parallel-prep migration session
#
# State BEFORE running:
#   parallel sales-operating-system service LIVE in gigaton-platform at
#     https://sales-operating-system-825651647756.us-central1.run.app
#   STILL running SQLite ephemeral mode (DATABASE_PATH=/data/sales_os.db, no volume mount,
#     no DATABASE_URL set) — same posture as the current carmen-beach service.
#   The new sales-os-pg Cloud SQL was provisioned (user + db + secret created) but is UNUSED.
#   DECISION_ENGINE_URL in the new sales-OS service env is already pointed at the new
#     gigaton-platform decision-engine (https://decision-engine-825651647756.us-central1.run.app).
#
# CRITICAL DECISION FOR OPERATOR BEFORE CUTOVER — read DECISIONS.md or:
#   sales-OS lifespan (app/main.py:30) hard-wires init_global_db(SQLite path), bypassing the
#   asyncpg path in app/database.py. To actually USE sales-os-pg Postgres, the lifespan must
#   be rewired to use the asyncpg engine. That is a code change, not an env-flip.
#   For NOW, this cutover preserves the current SQLite-ephemeral posture in the new project.
#   Future PR: rewire lifespan + run alembic 001_initial_schema.py via Cloud Run job.

set -euo pipefail

NEW_URL="https://sales-operating-system-825651647756.us-central1.run.app"
OLD_URL="https://sales-operating-system-rjmcrtvuzq-uc.a.run.app"

echo "=== Step 1: pre-flip smoke ==="
ID_TOKEN=$(gcloud auth print-identity-token)
curl -fsS -H "Authorization: Bearer $ID_TOKEN" "$NEW_URL/health" && echo

echo "=== Step 2: flip gateway SALES_OPERATING_SYSTEM_URL ==="
gcloud run services update gigaton-gateway --project=gigaton-platform --region=us-central1 \
  --update-env-vars=SALES_OPERATING_SYSTEM_URL=$NEW_URL

echo "=== Step 3: smoke through gateway ==="
curl -fsS "https://gigaton-platform.web.app/v1/sales-os/health" -w "\nHTTP %{http_code}\n" || \
curl -fsS "https://gigaton-platform.web.app/v1/sales-operating-system/health" -w "\nHTTP %{http_code}\n" || \
echo "WARN: route name unclear; verify gateway aggregator route mapping"

echo "=== Step 4: 30-min soak ==="
echo "  gcloud logging tail 'resource.type=cloud_run_revision AND resource.labels.service_name=sales-operating-system' --project=gigaton-platform"

echo "=== Rollback ==="
echo "  gcloud run services update gigaton-gateway --project=gigaton-platform --region=us-central1 --update-env-vars=SALES_OPERATING_SYSTEM_URL=$OLD_URL"

echo "=== FOLLOW-UP — PostgresMigration PR (separate session) ==="
echo "  1. Modify app/main.py lifespan to use app.database.engine + Base.metadata.create_all instead of init_global_db"
echo "  2. Deploy with DATABASE_URL pointed at gigaton-platform:us-central1:sales-os-pg"
echo "  3. Run alembic upgrade head (one-shot Cloud Run job or inline at startup)"
echo "  4. Run scripts/seed_from_xlsx.py if catalog seed needed"
