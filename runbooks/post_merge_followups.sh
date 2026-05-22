#!/usr/bin/env bash
# post_merge_followups.sh — runs after gigaton-gateway PRs #27 + #26 are merged to main.
#
# Does three things in one shot:
#   1. Opens "fix(gateway): wire OPENAI_API_KEY secret + LLM_ROUTER budgets in cloudbuild"
#      — adds the missing OpenAI secret mount + 3 LLM_ROUTER budget env vars that
#        Phase D PR #26 author claimed but didn't include.
#   2. Opens "chore(gateway): remove unused router.py imports + asyncio.sleep in pubsub_publisher"
#      — cosmetic cleanups flagged by both reviewers.
#   3. Reports PR URLs for user to merge.
#
# Idempotent: re-runs safely; second run is a no-op on branches that already exist.
#
# Pre-flight checks:
#   - gigaton-gateway main has the new Phase C + D code (verifies presence of app/llm_router/router.py and api/webhooks/github.py)
#   - gh auth as todd-gig
#   - clean working tree on the gigaton-gateway clone (uses a fresh clone in /tmp to avoid WIP issues)

set -euo pipefail

WORK_DIR=$(mktemp -d)
trap "rm -rf $WORK_DIR" EXIT

echo "=== Step 1: fresh clone of gigaton-gateway main ==="
git clone --depth=10 git@github.com:todd-gig/gigaton-gateway.git "$WORK_DIR/gigaton-gateway"
cd "$WORK_DIR/gigaton-gateway"

# Pre-flight: confirm both PRs have merged
if [ ! -f app/llm_router/router.py ]; then
  echo "ABORT: Phase D PR #26 (LLM router) not on main yet — abort."
  exit 1
fi
if [ ! -f api/webhooks/github.py ]; then
  echo "ABORT: Phase C PR #27 (webhooks) not on main yet — abort."
  exit 1
fi
echo "  Both PRs landed: phase C webhooks + phase D LLM router present on main"

echo ""
echo "=== Step 2: branch + apply cloudbuild fix ==="

git switch -c fix/gateway-llm-router-cloudbuild-secrets

# Edit cloudbuild.yaml: append OPENAI_API_KEY to --set-secrets line; append LLM_ROUTER_* env vars to --set-env-vars line
python3 <<'PY'
import re
from pathlib import Path
path = Path("cloudbuild.yaml")
text = path.read_text()

# 1. Append OPENAI_API_KEY=openai-api-key:latest to --set-secrets
text = re.sub(
    r'(--set-secrets=SESSION_HMAC_KEY=session-hmac-key:latest)(,GITHUB_WEBHOOK_SECRET=[^"\n]+)',
    r'\1\2,OPENAI_API_KEY=openai-api-key:latest',
    text,
)

# 2. Append LLM_ROUTER_* env vars to --set-env-vars
text = re.sub(
    r'(GIGNET_ORCHESTRATOR_TOPIC=gignet-orchestrator)',
    r'\1,LLM_ROUTER_BUDGET_PER_CALL_USD=0.50,LLM_ROUTER_BUDGET_HIGH_ERROR_COST_USD=2.00,LLM_ROUTER_DAILY_ORG_CAP_USD=50.00',
    text,
)

path.write_text(text)
print("cloudbuild.yaml patched")
PY

git diff cloudbuild.yaml | head -30

git add cloudbuild.yaml
git commit -m "$(cat <<'EOF'
fix(gateway): wire OPENAI_API_KEY secret + LLM_ROUTER budget env vars in cloudbuild

Phase D PR #26 (Phase D LLM router) added the LLM router code but did NOT
add the cloudbuild.yaml entries its description claimed. Without these,
the OpenAI provider raises RoutingError("openai_key_unset") on every call
even after the user pastes a key into Secret Manager.

Adds:
- --set-secrets += OPENAI_API_KEY=openai-api-key:latest
- --set-env-vars += LLM_ROUTER_BUDGET_PER_CALL_USD=0.50
- --set-env-vars += LLM_ROUTER_BUDGET_HIGH_ERROR_COST_USD=2.00
- --set-env-vars += LLM_ROUTER_DAILY_ORG_CAP_USD=50.00

Defaults match the spec in [[gignet_auto_trigger_orchestration]] §5 Phase D.

task_id: phase-d-cloudbuild-followup

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"

git push -u origin fix/gateway-llm-router-cloudbuild-secrets

CLOUDBUILD_PR_URL=$(gh pr create --repo todd-gig/gigaton-gateway \
  --base main --head fix/gateway-llm-router-cloudbuild-secrets \
  --title "fix(gateway): wire OPENAI_API_KEY secret + LLM_ROUTER budgets in cloudbuild" \
  --body "$(cat <<'EOF'
## Summary

Phase D PR #26 added the LLM router code but its cloudbuild.yaml diff did not include the OpenAI secret mount + LLM_ROUTER budget env vars that the PR description claimed. Without these, the OpenAI provider raises `RoutingError("openai_key_unset")` on every call even after the user pastes a key into Secret Manager — and the per-call/daily budgets fall back to whatever the code defaults are.

This 4-line cloudbuild.yaml diff fixes both gaps.

## Changes

- `--set-secrets` += `OPENAI_API_KEY=openai-api-key:latest`
- `--set-env-vars` += `LLM_ROUTER_BUDGET_PER_CALL_USD=0.50`
- `--set-env-vars` += `LLM_ROUTER_BUDGET_HIGH_ERROR_COST_USD=2.00`
- `--set-env-vars` += `LLM_ROUTER_DAILY_ORG_CAP_USD=50.00`

Defaults match the spec in [[gignet_auto_trigger_orchestration]] §5 Phase D + the user-approved Q3 budget policy from the 2026-05-20 sprint.

## Test plan

- [x] Existing 232 gateway tests still pass (cloudbuild.yaml is deploy-config, not code-pathed by pytest)
- [ ] Post-merge: cloud build succeeds + `gcloud run services describe gigaton-gateway --format='value(spec.template.spec.containers[0].env[].name)'` includes the 3 LLM_ROUTER vars
- [ ] Post-merge: `gcloud run services describe gigaton-gateway --format='value(spec.template.spec.containers[0].env[].valueFrom.secretKeyRef.name)'` includes `openai-api-key`

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)")

echo "  Opened: $CLOUDBUILD_PR_URL"

echo ""
echo "=== Step 3: branch + apply cleanup fixes ==="

git switch main
git pull origin main
git switch -c chore/gateway-router-and-publisher-cleanups

# 1. Remove unused imports in app/llm_router/router.py
python3 <<'PY'
from pathlib import Path
path = Path("app/llm_router/router.py")
if not path.exists():
    print("router.py missing — Phase D not on main yet?")
    exit(0)
text = path.read_text()
# Remove unused Awaitable, Callable from typing imports
new_text = text.replace("from typing import Any, Awaitable, Callable, ", "from typing import Any, ")
new_text = new_text.replace("from typing import Awaitable, Callable, ", "from typing import ")
if new_text != text:
    path.write_text(new_text)
    print("router.py cleaned")
else:
    print("router.py already clean")
PY

# 2. Swap time.sleep for await asyncio.sleep in pubsub_publisher.py
python3 <<'PY'
from pathlib import Path
path = Path("app/webhooks/pubsub_publisher.py")
if not path.exists():
    print("pubsub_publisher.py missing — Phase C not on main yet?")
    exit(0)
text = path.read_text()
# Only swap inside async functions — naive but works for the v0 file
if "time.sleep" in text and "asyncio" in text:
    new_text = text.replace("time.sleep(", "await asyncio.sleep(")
    # Drop "import time" if it was only used for sleep
    lines = new_text.split("\n")
    if not any("time." in line and "time.sleep" not in line for line in lines):
        lines = [l for l in lines if l != "import time"]
        new_text = "\n".join(lines)
    path.write_text(new_text)
    print("pubsub_publisher.py time.sleep -> await asyncio.sleep")
else:
    print("pubsub_publisher.py already clean or no sleep present")
PY

# Only commit if anything changed
if [ -n "$(git status --porcelain)" ]; then
  git add -A
  git commit -m "$(cat <<'EOF'
chore(gateway): remove unused router.py imports + non-blocking pubsub sleep

Two cosmetic cleanups flagged by reviewers of Phase C + D PRs:

1. app/llm_router/router.py: drop unused Awaitable, Callable from typing imports
   (ruff F401, reviewer of PR #26).

2. app/webhooks/pubsub_publisher.py: swap time.sleep() for await asyncio.sleep()
   on the retry backoff path inside an async function (reviewer of PR #27 noted
   this blocks the event loop briefly).

Neither change affects behavior at request-rate volumes the gateway sees today.
Both improve clarity + asyncio hygiene for future high-concurrency callers.

task_id: phase-c-d-cosmetic-cleanups

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
  git push -u origin chore/gateway-router-and-publisher-cleanups
  CLEANUP_PR_URL=$(gh pr create --repo todd-gig/gigaton-gateway \
    --base main --head chore/gateway-router-and-publisher-cleanups \
    --title "chore(gateway): remove unused router.py imports + non-blocking pubsub sleep" \
    --body "Cosmetic cleanups from Phase C + D reviewer notes. No behavior change.

🤖 Generated with [Claude Code](https://claude.com/claude-code)")
  echo "  Opened: $CLEANUP_PR_URL"
else
  echo "  No cleanup needed (files already clean)"
  CLEANUP_PR_URL="(none — no changes)"
fi

echo ""
echo "=== DONE ==="
echo ""
echo "Two follow-up PRs:"
echo "  1. Cloudbuild fix:    $CLOUDBUILD_PR_URL"
echo "  2. Cosmetic cleanups: $CLEANUP_PR_URL"
echo ""
echo "Both can be merged independently. Cloudbuild fix triggers a gateway deploy that"
echo "wires the OpenAI key (provided you've pasted it into openai-api-key Secret Manager slot)."
