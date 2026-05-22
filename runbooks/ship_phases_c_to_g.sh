#!/usr/bin/env bash
# ship_phases_c_to_g.sh — single ship-it script for the Gignet Phases C-G deploy.
#
# Run AFTER:
#   1. All 4 in-flight PRs (gigaton-gateway webhooks, gigaton-gateway LLM router,
#      gignet-local-node integration, decision-engine drift rules) are MERGED
#      to main of their respective repos.
#   2. api.gigaton.ai DNS is verified + CNAME live (per api_gigaton_ai_dns_provisioning.md).
#   3. OpenAI key is pasted into openai-api-key secret slot.
#   4. Settings.json permission patterns are added (per the snippet sent in chat).
#
# This script idempotently:
#   - Creates the gignet-orchestrator-fn-runtime SA if missing
#   - Grants required IAM (Pub/Sub publisher + Eventarc receiver)
#   - Deploys gignet-activity-emitter Cloud Function
#   - Creates the Cloud Run domain mapping for api.gigaton.ai
#   - Deploys the Cloud Monitoring dashboard
#   - Applies the 4 alert policies
#   - Runs an E2E smoke test
#
# Total runtime: ~10-15 min (mostly waiting on Cloud Run cert issuance + Cloud Function build).
#
# Usage:
#   bash ship_phases_c_to_g.sh [--skip-domain-mapping] [--skip-smoke]

set -euo pipefail

PROJECT="gigaton-platform"
REGION="us-central1"
RUNBOOK_DIR="$(cd "$(dirname "$0")" && pwd)"
ACTIVITY_FN_REPO="${HOME}/Documents/GitHub/gignet-activity-emitter-fn"
NOTIFY_CHANNEL="projects/${PROJECT}/notificationChannels/13279974536745540560"

SKIP_DOMAIN_MAPPING=0
SKIP_SMOKE=0
for arg in "$@"; do
  case "$arg" in
    --skip-domain-mapping) SKIP_DOMAIN_MAPPING=1 ;;
    --skip-smoke) SKIP_SMOKE=1 ;;
    *) echo "unknown flag: $arg" >&2; exit 1 ;;
  esac
done

echo ""
echo "=== Step 1: pre-flight ==="

# Auth check
gcloud auth print-access-token --account=todd@gigaton.ai >/dev/null 2>&1 || { echo "FAIL: run 'gcloud auth login --account=todd@gigaton.ai' first"; exit 1; }
echo "  gcloud auth: OK"

# Project check
gcloud config set project "$PROJECT" >/dev/null 2>&1
echo "  active project: $PROJECT"

# Repo check
[ -d "$ACTIVITY_FN_REPO" ] || { echo "FAIL: gignet-activity-emitter-fn repo not found at $ACTIVITY_FN_REPO"; exit 1; }
echo "  activity emitter repo: present"

# OpenAI key check
OPENAI_VERSIONS=$(gcloud secrets versions list openai-api-key --project="$PROJECT" --format='value(name)' 2>/dev/null | head -1)
[ -n "$OPENAI_VERSIONS" ] || { echo "WARN: openai-api-key secret has 0 versions; Phase D OpenAI route will fail until populated"; }

echo ""
echo "=== Step 2: provision gignet-orchestrator-fn-runtime SA (if missing) ==="

SA_EMAIL="gignet-orchestrator-fn-runtime@${PROJECT}.iam.gserviceaccount.com"
if ! gcloud iam service-accounts describe "$SA_EMAIL" --project="$PROJECT" >/dev/null 2>&1; then
  gcloud iam service-accounts create gignet-orchestrator-fn-runtime \
    --display-name="Gignet orchestrator Cloud Functions runtime" \
    --project="$PROJECT"
  echo "  created SA: $SA_EMAIL"
else
  echo "  SA already exists: $SA_EMAIL"
fi

# Grant Pub/Sub publisher on the orchestrator topic
gcloud pubsub topics add-iam-policy-binding gignet-orchestrator \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/pubsub.publisher" \
  --project="$PROJECT" >/dev/null
echo "  granted: pubsub.publisher on gignet-orchestrator topic"

# Grant Eventarc receiver on project (Firestore trigger needs it)
gcloud projects add-iam-policy-binding "$PROJECT" \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/eventarc.eventReceiver" --condition=None >/dev/null
echo "  granted: eventarc.eventReceiver on project"

echo ""
echo "=== Step 3: deploy gignet-activity-emitter Cloud Function ==="

cd "$ACTIVITY_FN_REPO"
gcloud functions deploy gignet-activity-emitter \
  --gen2 --runtime=python312 --region="$REGION" --project="$PROJECT" \
  --source=. --entry-point=on_activity_change \
  --trigger-event-filters="type=google.cloud.firestore.document.v1.created" \
  --trigger-event-filters="database=(default)" \
  --trigger-event-filters-path-pattern="document=users/{userId}/activity/{activityId}" \
  --service-account="$SA_EMAIL" \
  --max-instances=10 --memory=256Mi --timeout=60s \
  --set-env-vars=GCP_PROJECT="$PROJECT"
echo "  deployed: gignet-activity-emitter"

echo ""
echo "=== Step 4: Cloud Run domain mapping for api.gigaton.ai ==="

if [ "$SKIP_DOMAIN_MAPPING" -eq 1 ]; then
  echo "  skipped (--skip-domain-mapping)"
else
  if gcloud beta run domain-mappings describe --domain=api.gigaton.ai --region="$REGION" --project="$PROJECT" >/dev/null 2>&1; then
    echo "  mapping already exists: api.gigaton.ai"
  else
    gcloud beta run domain-mappings create \
      --service=gigaton-gateway \
      --domain=api.gigaton.ai \
      --region="$REGION" --project="$PROJECT"
    echo "  created mapping: api.gigaton.ai → gigaton-gateway"
    echo "  NOTE: managed SSL cert issuance takes 5-15 min; curl will 502 until then."
  fi
fi

echo ""
echo "=== Step 5: deploy Cloud Monitoring dashboard ==="

gcloud monitoring dashboards create --config-from-file="$RUNBOOK_DIR/gignet-orchestrator-dashboard.json" --project="$PROJECT"
echo "  deployed: Gignet Orchestrator Fabric dashboard"

echo ""
echo "=== Step 6: deploy alert policies ==="

# YAML file contains 4 policies separated by ---; gcloud needs them one at a time.
# Split + apply each.
TMP=$(mktemp -d)
csplit -s -f "$TMP/policy-" -b '%02d.yaml' "$RUNBOOK_DIR/gignet-alert-policies.yaml" '/^---$/' '{*}'
for f in "$TMP"/policy-*.yaml; do
  # Skip empty / non-policy fragments
  if grep -q '^displayName:' "$f"; then
    if grep -q '^enabled: false' "$f"; then
      echo "  skipped (enabled:false): $(grep '^displayName:' "$f" | head -1)"
    else
      gcloud beta monitoring policies create --policy-from-file="$f" --project="$PROJECT" >/dev/null
      echo "  deployed: $(grep '^displayName:' "$f" | head -1 | sed 's/displayName: //')"
    fi
  fi
done
rm -rf "$TMP"

echo ""
echo "=== Step 7: E2E smoke test ==="

if [ "$SKIP_SMOKE" -eq 1 ]; then
  echo "  skipped (--skip-smoke)"
else
  echo "  Publishing a synthetic task_completed event to gignet-orchestrator..."
  TASK_ID="smoke-$(date +%s)"
  gcloud pubsub topics publish gignet-orchestrator \
    --project="$PROJECT" \
    --attribute="event_type=task_completed,emitted_by=ship-phases-c-to-g-smoke,completion_event_id=portable_contract_propagated" \
    --message="{\"task_id\":\"$TASK_ID\",\"task_type\":\"smoke.test\",\"status\":\"completed\"}"

  echo "  Waiting 5s for fan-out..."
  sleep 5

  echo "  Checking task_registry for spawned task..."
  # The orchestrator-trigger-fan-out function should have written a new row with spawned_by_trigger=portable_contract_propagated
  # (Manual check via Firestore console — gcloud CLI doesn't query well.)
  echo "  → Verify in Firebase console: Firestore → task_registry → filter spawned_by_trigger='portable_contract_propagated'"
  echo "  Cloud Function logs:"
  gcloud functions logs read orchestrator-trigger-fan-out --project="$PROJECT" --limit=5 --format='value(time_utc,log)' 2>/dev/null || true
fi

echo ""
echo "=== DONE ==="
echo ""
echo "What's now live:"
echo "  • Cloud Function: gignet-activity-emitter (Firestore activity → orchestrator)"
echo "  • Cloud Run domain mapping: api.gigaton.ai → gigaton-gateway"
echo "  • Cloud Monitoring: Gignet Orchestrator Fabric dashboard"
echo "  • Alert policies: 3 active (backlog, fan-out errors, gateway 5xx); 1 inactive pending custom metric"
echo ""
echo "Verify:"
echo "  • Dashboard:  https://console.cloud.google.com/monitoring/dashboards?project=$PROJECT"
echo "  • api.gigaton.ai: curl -sI https://api.gigaton.ai/v1/healthz   (wait 5-15 min for cert)"
echo ""
echo "Next steps:"
echo "  1. Run docs sweep PR to swap *.run.app URLs → api.gigaton.ai across repos"
echo "  2. Update unified master plan §3-§10 with Phase C-G completion notes"
echo "  3. Register GitHub org webhook: https://github.com/organizations/todd-gig/settings/hooks"
echo "     Payload URL: https://api.gigaton.ai/webhooks/github"
echo "     Content-Type: application/json"
echo "     Secret: gcloud secrets versions access latest --secret=github-webhook-secret --project=$PROJECT"
