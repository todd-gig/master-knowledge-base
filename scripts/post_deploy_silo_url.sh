#!/usr/bin/env bash
# post_deploy_silo_url.sh — wire intelligence-silo URL into Firebase Functions config.
#
# Run AFTER the silo's first deploy (tonight via deploy_19.sh) succeeds.
# This finishes the chat "Gigaton (local)" provider wiring described in
# decisions/2026-05-08_carmen_beach_descope.md and the callGigatonSilo()
# code path in Gigaton-UI-Platform/functions/src/providers.ts.
#
# What it does:
#   1. Reads the current intelligence-silo Cloud Run URL
#   2. Calls /health on it to confirm the service is up
#   3. Sets Firebase Functions secret GIGATON_SILO_URL to that URL
#   4. (Optional) deploys functions so the secret is picked up
#
# This is idempotent — safe to re-run.

set -euo pipefail

PROJECT="carmen-beach-properties"
REGION="us-central1"
FIREBASE_PROJECT="gigaton-platform"

echo "→ fetching intelligence-silo URL"
SILO_URL=$(gcloud run services describe intelligence-silo \
  --region="$REGION" --project="$PROJECT" \
  --format='value(status.url)' 2>/dev/null)

if [[ -z "$SILO_URL" ]]; then
  echo "✗ intelligence-silo not deployed yet. Run deploy_19.sh intelligence-silo first."
  exit 1
fi

echo "  URL: $SILO_URL"

echo "→ /health smoke test"
HTTP=$(curl -s -o /dev/null -w "%{http_code}" "${SILO_URL}/health")
if [[ "$HTTP" != "200" ]]; then
  echo "✗ /health returned $HTTP — service not ready"
  exit 2
fi
echo "  ✓ /health = 200"

echo "→ setting Firebase Functions secret GIGATON_SILO_URL"
# `firebase functions:secrets:set` expects stdin or a file. Pipe the URL.
echo -n "$SILO_URL" | firebase functions:secrets:set GIGATON_SILO_URL \
  --project="$FIREBASE_PROJECT" \
  --data-file=- 2>&1 | tail -5

echo
echo "→ verify secret is set"
firebase functions:secrets:access GIGATON_SILO_URL \
  --project="$FIREBASE_PROJECT" 2>&1 | head -3

echo
echo "✓ GIGATON_SILO_URL = $SILO_URL"
echo
echo "Next: redeploy functions to pick up the new secret:"
echo "  cd ~/Documents/GitHub/Gigaton-UI-Platform"
echo "  firebase deploy --only functions --project=$FIREBASE_PROJECT"
echo
echo "After functions deploy, the chat 'Gigaton (local)' provider routes to:"
echo "  $SILO_URL"
echo "via callGigatonSilo() in functions/src/providers.ts."
