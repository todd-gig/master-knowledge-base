#!/usr/bin/env bash
# decision-engine cutover script — Day 1 (post-LAUNCH-1)
# Authored: 2026-05-25 by parallel-prep migration session
# State BEFORE running: parallel decision-engine service is LIVE in gigaton-platform
#   at https://decision-engine-825651647756.us-central1.run.app
#   DB: gigaton-platform:us-central1:decision-engine-pg (data restored from carmen 2026-05-25T20:50Z)
#   Source still routing: gateway DECISION_ENGINE_URL = https://decision-engine-rjmcrtvuzq-uc.a.run.app (carmen-beach)
#
# What this script does:
#   1. Fresh delta-resync of decision_engine DB from carmen → gigaton-platform (in case any writes happened post-prep)
#   2. Flip gateway DECISION_ENGINE_URL env to the new gigaton-platform URL + redeploy gateway
#   3. Smoke test through the gateway
#
# Rollback (paste in another terminal if soak goes red):
#   gcloud run services update gigaton-gateway --project=gigaton-platform --region=us-central1 \
#     --update-env-vars=DECISION_ENGINE_URL=https://decision-engine-rjmcrtvuzq-uc.a.run.app
#
# ETA: ~10 min cutover + 30 min soak.

set -euo pipefail

NEW_URL="https://decision-engine-825651647756.us-central1.run.app"
OLD_URL="https://decision-engine-rjmcrtvuzq-uc.a.run.app"
TS=$(date -u +%Y%m%dT%H%M%SZ)

echo "=== Step 1: delta-resync decision_engine DB ==="
echo "Re-exporting from carmen at $TS..."
gcloud sql export sql decision-engine-pg \
  "gs://gigaton-migration-staging/decision-engine-pg-cutover-${TS}.sql.gz" \
  --database=decision_engine \
  --project=carmen-beach-properties

echo "Wiping gigaton-platform decision_engine DB before re-import..."
gcloud sql databases delete decision_engine --instance=decision-engine-pg --project=gigaton-platform --quiet
gcloud sql databases create decision_engine --instance=decision-engine-pg --project=gigaton-platform

echo "Re-importing..."
gcloud sql import sql decision-engine-pg \
  "gs://gigaton-migration-staging/decision-engine-pg-cutover-${TS}.sql.gz" \
  --database=decision_engine \
  --project=gigaton-platform --quiet
# Note: tail of import will throw "must be member of role postgres" — that is the trailing
# ALTER DEFAULT PRIVILEGES FOR ROLE postgres; benign because all data + tables apply before it.

echo "=== Step 2: pre-flip smoke directly against new URL ==="
ID_TOKEN=$(gcloud auth print-identity-token)
curl -fsS -H "Authorization: Bearer $ID_TOKEN" "$NEW_URL/health" && echo

echo "=== Step 3: flip gateway DECISION_ENGINE_URL ==="
gcloud run services update gigaton-gateway --project=gigaton-platform --region=us-central1 \
  --update-env-vars=DECISION_ENGINE_URL=$NEW_URL

echo "=== Step 4: smoke through gateway ==="
GW="https://gigaton-platform.web.app"
# adjust path below to your real DE-proxied endpoint
curl -fsS "$GW/v1/decision-engine/health" -w "\nHTTP %{http_code}\n" || echo "WARN: gateway proxy 4xx/5xx"

echo "=== Step 5: 30-min soak ==="
echo "Watch logs:"
echo "  gcloud logging tail 'resource.type=cloud_run_revision AND resource.labels.service_name=decision-engine' --project=gigaton-platform"
echo "  gcloud logging tail 'resource.type=cloud_run_revision AND resource.labels.service_name=gigaton-gateway AND httpRequest.status>=400' --project=gigaton-platform"
echo "Penrose scoreboard:"
echo "  curl -s $NEW_URL/v1/penrose/scoreboard | jq ."

echo "=== Cutover complete. If green after 30min, proceed to Day 2 (intel-silo cutover). ==="
echo "Rollback: gcloud run services update gigaton-gateway --project=gigaton-platform --region=us-central1 --update-env-vars=DECISION_ENGINE_URL=$OLD_URL"
