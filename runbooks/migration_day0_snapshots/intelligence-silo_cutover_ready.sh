#!/usr/bin/env bash
# intelligence-silo cutover script — Day 2 (after DE soak passes)
# Authored: 2026-05-25 by parallel-prep migration session
# State BEFORE running:
#   parallel intelligence-silo service LIVE in gigaton-platform at
#     https://intelligence-silo-825651647756.us-central1.run.app
#   DB: gigaton-platform:us-central1:intelligence-silo-pg (data restored 2026-05-25T20:50Z)
#   gigaton-experiences-prod-v2 bucket exists in gigaton-platform (empty — source was also empty)
#   gigaton-silo-index bucket exists in gigaton-platform
#   ALL oauth-drive-* secrets mirrored from carmen → gigaton-platform with intel-silo-runtime SA access
#   google-drive-oauth-client mirrored Day 0
#
# CRITICAL pre-step (user manual): add the new Cloud Run URL as authorized OAuth redirect URI
#   in Google Cloud Console → APIs & Services → Credentials → Web client used for Drive.
#   New URI base: https://intelligence-silo-825651647756.us-central1.run.app/v1/oauth/drive/callback
#   (verify exact callback path in intel-silo source: app/oauth/drive_router.py or similar)
#
# Rollback: revert gateway INTELLIGENCE_SILO_URL + decision-engine INTELLIGENCE_SILO_URL.

set -euo pipefail

NEW_URL="https://intelligence-silo-825651647756.us-central1.run.app"
OLD_URL="https://intelligence-silo-rjmcrtvuzq-uc.a.run.app"
TS=$(date -u +%Y%m%dT%H%M%SZ)

echo "=== Step 1: delta-resync intelligence_silo DB ==="
gcloud sql export sql intelligence-silo-pg \
  "gs://gigaton-migration-staging/intelligence-silo-pg-cutover-${TS}.sql.gz" \
  --database=intelligence_silo \
  --project=carmen-beach-properties

gcloud sql databases delete intelligence_silo --instance=intelligence-silo-pg --project=gigaton-platform --quiet
gcloud sql databases create intelligence_silo --instance=intelligence-silo-pg --project=gigaton-platform

gcloud sql import sql intelligence-silo-pg \
  "gs://gigaton-migration-staging/intelligence-silo-pg-cutover-${TS}.sql.gz" \
  --database=intelligence_silo \
  --project=gigaton-platform --quiet

echo "=== Step 2: re-sync gigaton-experiences-prod (in case data appeared in carmen) ==="
gcloud storage cp -r gs://gigaton-experiences-prod/* gs://gigaton-experiences-prod-v2/ --project=gigaton-platform 2>/dev/null || echo "source bucket empty — skipping"

echo "=== Step 3: pre-flip smoke ==="
ID_TOKEN=$(gcloud auth print-identity-token)
curl -fsS -H "Authorization: Bearer $ID_TOKEN" "$NEW_URL/health" >/dev/null && echo "  /health green"

echo "=== Step 4: flip gateway INTELLIGENCE_SILO_URL ==="
gcloud run services update gigaton-gateway --project=gigaton-platform --region=us-central1 \
  --update-env-vars=INTELLIGENCE_SILO_URL=$NEW_URL

echo "=== Step 5: flip decision-engine INTELLIGENCE_SILO_URL ==="
# decision-engine was deployed Day 1 in gigaton-platform — update its env to use the new silo URL too
gcloud run services update decision-engine --project=gigaton-platform --region=us-central1 \
  --update-env-vars=INTELLIGENCE_SILO_URL=$NEW_URL

echo "=== Step 6: end-to-end OAuth roundtrip test ==="
echo "Manually visit https://gigaton-platform.web.app/connectors/google-drive and verify the Drive OAuth flow completes."

echo "=== Step 7: 30-min soak ==="
echo "  gcloud logging tail 'resource.type=cloud_run_revision AND resource.labels.service_name=intelligence-silo' --project=gigaton-platform"

echo "=== Rollback ==="
echo "  gcloud run services update gigaton-gateway --project=gigaton-platform --region=us-central1 --update-env-vars=INTELLIGENCE_SILO_URL=$OLD_URL"
echo "  gcloud run services update decision-engine --project=gigaton-platform --region=us-central1 --update-env-vars=INTELLIGENCE_SILO_URL=$OLD_URL"
