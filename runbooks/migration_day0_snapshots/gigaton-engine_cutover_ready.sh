#!/usr/bin/env bash
# gigaton-engine cutover script — Day 3
# Authored: 2026-05-25 by parallel-prep migration session
# State BEFORE running:
#   parallel gigaton-engine service LIVE in gigaton-platform at
#     https://gigaton-engine-825651647756.us-central1.run.app
#   No DB binding (gigaton-engine doesn't use a DB in current deploy — verified Day 0 snapshot).
#   New gigaton-engine-pg in gigaton-platform was post-provisioned (sql user + db + secret created)
#   but is unused — reserved for future schema. Per MIG-2, gigaton-platform instance is canonical.
#
# This is the SAFEST cutover of the 4 — no data, no OAuth, no external deps.

set -euo pipefail

NEW_URL="https://gigaton-engine-825651647756.us-central1.run.app"
OLD_URL="https://gigaton-engine-rjmcrtvuzq-uc.a.run.app"

echo "=== Step 1: pre-flip smoke ==="
ID_TOKEN=$(gcloud auth print-identity-token)
curl -fsS -H "Authorization: Bearer $ID_TOKEN" "$NEW_URL/health" && echo

echo "=== Step 2: flip gateway GIGATON_ENGINE_URL ==="
gcloud run services update gigaton-gateway --project=gigaton-platform --region=us-central1 \
  --update-env-vars=GIGATON_ENGINE_URL=$NEW_URL

echo "=== Step 3: smoke through gateway ==="
curl -fsS "https://gigaton-platform.web.app/v1/gigaton-engine/health" -w "\nHTTP %{http_code}\n"

echo "=== Step 4: 30-min soak ==="
echo "  gcloud logging tail 'resource.type=cloud_run_revision AND resource.labels.service_name=gigaton-engine' --project=gigaton-platform"

echo "=== Rollback ==="
echo "  gcloud run services update gigaton-gateway --project=gigaton-platform --region=us-central1 --update-env-vars=GIGATON_ENGINE_URL=$OLD_URL"
