#!/usr/bin/env bash
# new_test_operator.sh — Bootstrap a clean test operator for browser smoke testing
#
# WHY THIS SCRIPT EXISTS:
#   The chat-first onboarding workflow assumes an operator namespace exists
#   in UAE.client_namespaces. Pre-existing operators (carmen-beach, liquefex,
#   ti-solutions, incontekst, gigaton) all have real data — testing
#   onboarding flows on them pollutes that data and changes their nav-tier
#   state visible to real users.
#
#   This script provisions an ISOLATED test operator namespace with a
#   throwaway slug so you can:
#     - Demo the chat-first flow from blank-slate without affecting prod data
#     - Exercise stages 0-9 with synthetic actions
#     - Reset by deleting the namespace + re-running the script
#
# PPIM signature:
#   ppim_interaction: every demo / test session starts from a known clean state
#   ppim_economics: ~$0 (one row in UAE Postgres, deleted on cleanup)
#   ppim_predictability: HIGH — fully reproducible operator state
#   ppim_brand_dimension: demo coherence
#
# Cross-references:
#   - master-knowledge-base/manifests/onboarding_v1.yaml (the workflow this exercises)
#   - ~/.claude/projects/-Users-admin/memory/onboarding_workflow_v1_completion_verified_2026_05_22.md
#     (the verification chain this enables)
#
# Usage:
#   ./new_test_operator.sh <slug>           # blank operator, lands at Stage 0
#   ./new_test_operator.sh <slug> seeded    # (future) pre-completes stages 0-3 for later-stage demos
#   ./new_test_operator.sh --cleanup <slug> # tear down a test operator
#
# Examples:
#   ./new_test_operator.sh gigaton-demo
#   ./new_test_operator.sh smoke-$(date +%Y%m%d)
#   ./new_test_operator.sh --cleanup gigaton-demo

set -euo pipefail

UAE_URL="${UAE_URL:-https://user-access-engine-sqatlxhlza-uc.a.run.app}"
GATEWAY_URL="${GATEWAY_URL:-https://gigaton-gateway-sqatlxhlza-uc.a.run.app}"
ADMIN_TOKEN_SECRET="${ADMIN_TOKEN_SECRET:-uae-admin-token}"
ADMIN_TOKEN_PROJECT="${ADMIN_TOKEN_PROJECT:-gigaton-platform}"

# Reserved slugs we won't let you accidentally use
RESERVED_SLUGS="gigaton carmen-beach liquefex ti-solutions incontekst"

usage() {
  sed -n '2,30p' "$0" | sed 's/^# \?//'
  exit 1
}

[[ $# -lt 1 ]] && usage

# --cleanup mode
if [[ "$1" == "--cleanup" ]]; then
  [[ $# -lt 2 ]] && { echo "ERROR: --cleanup requires a slug"; exit 1; }
  SLUG="$2"
  echo "===> Cleaning up test operator: $SLUG"
  TOKEN=$(gcloud auth print-identity-token)
  ADMIN_HEADER=""
  if gcloud secrets describe "$ADMIN_TOKEN_SECRET" --project="$ADMIN_TOKEN_PROJECT" >/dev/null 2>&1; then
    ADMIN_TOKEN=$(gcloud secrets versions access latest --secret="$ADMIN_TOKEN_SECRET" --project="$ADMIN_TOKEN_PROJECT")
    ADMIN_HEADER="-H X-Admin-Token:$ADMIN_TOKEN"
  fi
  curl -sS -X DELETE "$UAE_URL/v1/namespaces/$SLUG" \
    -H "Authorization: Bearer $TOKEN" \
    $ADMIN_HEADER \
    -w "\nHTTP %{http_code}\n"
  echo "Done."
  exit 0
fi

SLUG="$1"
PRESET="${2:-fresh}"

# Validate slug — alphanumeric + dash, no spaces, lowercase
if [[ ! "$SLUG" =~ ^[a-z0-9][a-z0-9-]{2,63}$ ]]; then
  echo "ERROR: slug must be lowercase alphanumeric+dash, 3-64 chars"
  echo "       got: '$SLUG'"
  exit 1
fi

# Refuse to overwrite a real operator
for reserved in $RESERVED_SLUGS; do
  if [[ "$SLUG" == "$reserved" ]]; then
    echo "ERROR: '$SLUG' is a reserved real-operator slug. Use a test prefix."
    echo "       suggestion: smoke-$SLUG or test-$SLUG or $SLUG-demo"
    exit 1
  fi
done

# Validate preset
if [[ "$PRESET" != "fresh" && "$PRESET" != "seeded" ]]; then
  echo "ERROR: preset must be 'fresh' or 'seeded' (got '$PRESET')"
  exit 1
fi

echo "===> Bootstrapping test operator '$SLUG' (preset=$PRESET)"

# ─────────────────────────────────────────────────────────────────────
# 1. Refresh gcloud auth (will no-op if already authed)
# ─────────────────────────────────────────────────────────────────────
TOKEN=$(gcloud auth print-identity-token 2>/dev/null || true)
if [[ -z "$TOKEN" ]]; then
  echo "ERROR: gcloud auth not active. Run: gcloud auth login"
  exit 1
fi

# ─────────────────────────────────────────────────────────────────────
# 2. Resolve admin token (if provisioned)
# ─────────────────────────────────────────────────────────────────────
ADMIN_HEADER=""
if gcloud secrets describe "$ADMIN_TOKEN_SECRET" --project="$ADMIN_TOKEN_PROJECT" >/dev/null 2>&1; then
  echo "===> Found admin-token secret; using it"
  ADMIN_TOKEN=$(gcloud secrets versions access latest --secret="$ADMIN_TOKEN_SECRET" --project="$ADMIN_TOKEN_PROJECT")
  ADMIN_HEADER="-H X-Admin-Token:$ADMIN_TOKEN"
else
  echo "===> No admin-token secret found (fail-open mode per UAE PR #30); proceeding without"
fi

# ─────────────────────────────────────────────────────────────────────
# 3. Check if namespace already exists
# ─────────────────────────────────────────────────────────────────────
EXISTING=$(curl -sS -o /dev/null -w "%{http_code}" \
  "$UAE_URL/v1/namespaces/$SLUG" \
  -H "Authorization: Bearer $TOKEN" \
  $ADMIN_HEADER)

if [[ "$EXISTING" == "200" ]]; then
  echo "ERROR: namespace '$SLUG' already exists. Use --cleanup first, or pick a different slug."
  exit 1
fi

# ─────────────────────────────────────────────────────────────────────
# 4. Create the namespace
# ─────────────────────────────────────────────────────────────────────
echo "===> Creating namespace '$SLUG' in UAE"

# Generate a parent_entity_id UUIDv5 from the slug (deterministic so re-runs
# produce the same UUID if the namespace was deleted + recreated)
PARENT_ENTITY_ID=$(python3 -c "
import uuid
ns = uuid.uuid5(uuid.NAMESPACE_DNS, 'test-operators.gigaton.ai')
print(uuid.uuid5(ns, '$SLUG'))
")

CREATE_RESP=$(curl -sS -X POST "$UAE_URL/v1/namespaces" \
  -H "Authorization: Bearer $TOKEN" \
  $ADMIN_HEADER \
  -H "Content-Type: application/json" \
  -d "{
    \"namespace_id\": \"$SLUG\",
    \"parent_entity_id\": \"$PARENT_ENTITY_ID\",
    \"display_name\": \"Test Operator: $SLUG\",
    \"business_goals\": [],
    \"workflows\": [],
    \"stakeholders\": [],
    \"integrations\": [],
    \"decision_preferences\": {},
    \"memory_filter\": {},
    \"retrieval_policy\": {},
    \"governance_overlays\": {},
    \"first_principle_variable_overrides\": {},
    \"multi_axis_tags\": [
      \"environment:test\",
      \"created_by:new_test_operator.sh\",
      \"created_at:$(date -u +%Y-%m-%dT%H:%M:%SZ)\"
    ],
    \"lifecycle_state\": \"active\"
  }")

echo "$CREATE_RESP" | python3 -m json.tool || { echo "FAIL: namespace creation"; echo "$CREATE_RESP"; exit 1; }

# ─────────────────────────────────────────────────────────────────────
# 5. Seeded preset — pre-complete stages 0-3 (future enhancement)
# ─────────────────────────────────────────────────────────────────────
if [[ "$PRESET" == "seeded" ]]; then
  echo "===> Seeded preset not yet implemented — namespace created blank."
  echo "     TODO: walk through stages 0-3 via gateway /v1/onboarding/intent"
  echo "           with synthetic form-submissions to land an operator at Stage 4."
fi

# ─────────────────────────────────────────────────────────────────────
# 6. Verify against gateway
# ─────────────────────────────────────────────────────────────────────
echo ""
echo "===> Verifying via gateway state endpoint"
GATEWAY_STATE=$(curl -sS "$GATEWAY_URL/v1/onboarding/state?operator_id=$SLUG" \
  -H "Authorization: Bearer $TOKEN")
echo "$GATEWAY_STATE" | python3 -m json.tool

# ─────────────────────────────────────────────────────────────────────
# 7. Print test instructions
# ─────────────────────────────────────────────────────────────────────
cat <<EOF

═══════════════════════════════════════════════════════════════════════
✅ Test operator '$SLUG' provisioned
═══════════════════════════════════════════════════════════════════════

Browser test (FE):
  1. Open https://gigaton-platform.web.app/ in an incognito Chrome window
  2. Sign in (note: chat-first onboarding currently inherits the @gigaton.ai
     auth check — you may need to authenticate as a known operator account;
     true multi-operator FE auth is a follow-on)
  3. The FE currently keys on its own auth-context operator_id resolution;
     to force this test operator, append ?operator_id=$SLUG to URLs
  4. Navigate to: https://gigaton-platform.web.app/chat?operator_id=$SLUG&onboarding=stage-0
  5. Verify: only chat circle lit; Stage 0 affordance renders; side panel
     shows "Stage 1 of 10 — Trust & Scope"

CLI test (curl):
  # State
  curl "$GATEWAY_URL/v1/onboarding/state?operator_id=$SLUG" \\
    -H "Authorization: Bearer \$(gcloud auth print-identity-token)" | python3 -m json.tool

  # Intent (Stage 0 declare-legal-entity)
  curl -X POST "$GATEWAY_URL/v1/onboarding/intent" \\
    -H "Authorization: Bearer \$(gcloud auth print-identity-token)" \\
    -H "Content-Type: application/json" \\
    -d '{
      "operator_id": "$SLUG",
      "stage_id": "stage-0-trust-scope",
      "action_id": "declare-legal-entity",
      "reply_kind": "form_submission",
      "payload": {"form_data": {"legal_name": "Demo Inc"}}
    }' | python3 -m json.tool

Cleanup when done:
  $0 --cleanup $SLUG

═══════════════════════════════════════════════════════════════════════
EOF
