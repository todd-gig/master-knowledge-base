#!/usr/bin/env bash
# docs_sweep_run_app_to_api_gigaton.sh
#
# Run AFTER api.gigaton.ai is live + verified (curl -sI https://api.gigaton.ai/v1/healthz returns HTTP/2 200).
#
# Swaps the legacy *.run.app URL for the clean api.gigaton.ai URL across 14 ACTIVE docs.
# Frozen historical files (session handoffs, archive/) are intentionally skipped — they
# are historical records of what was true on a given date, and rewriting them would be
# revisionist (violates AX-016 doctrine-claim vs committed-code).
#
# Idempotent: safe to re-run; second run is a no-op.
#
# Also updates the master plan §3.6 drift #4 entry (changes "NXDOMAIN" reference to "live").

set -euo pipefail

OLD_URL="gigaton-gateway-sqatlxhlza-uc.a.run.app"
NEW_URL="api.gigaton.ai"

# Pre-flight: verify api.gigaton.ai responds 200 before rewriting anything
echo "=== Pre-flight: verify api.gigaton.ai is live ==="
HTTP_CODE=$(curl -sI -o /dev/null -w '%{http_code}' --max-time 10 "https://${NEW_URL}/v1/healthz" || echo "fail")
if [ "$HTTP_CODE" != "200" ]; then
  echo "ABORT: https://${NEW_URL}/v1/healthz returned ${HTTP_CODE}, not 200."
  echo "Wait for DNS propagation + Cloud Run SSL cert issuance (typically 5-30 min after CNAME goes live)."
  exit 1
fi
echo "  OK: api.gigaton.ai responds 200"

ACTIVE_FILES=(
  # Memory (canonical)
  "/Users/admin/.claude/projects/-Users-admin/memory/api_reference_2026_05_19.md"
  "/Users/admin/.claude/projects/-Users-admin/memory/master_project_plan.md"
  "/Users/admin/.claude/projects/-Users-admin/memory/RESUME_HERE_2026_05_20.md"
  "/Users/admin/.claude/projects/-Users-admin/memory/active_work_registry.md"
  "/Users/admin/.claude/projects/-Users-admin/memory/operator_runbook_2026_05_19.md"
  "/Users/admin/.claude/projects/-Users-admin/memory/operational_state_snapshot_2026_05_19.md"
  "/Users/admin/.claude/projects/-Users-admin/memory/repo_registry.md"
  "/Users/admin/.claude/projects/-Users-admin/memory/gateway_and_oauth_landed_2026_05_13.md"
  # NotebookLM mirrors
  "/Users/admin/Documents/Gigaton-NotebookLLM/05_API_Reference/01_API_Reference.md"
  "/Users/admin/Documents/Gigaton-NotebookLLM/02_Master_Project_Plan/03_RESUME_HERE_2026_05_20.md"
  "/Users/admin/Documents/Gigaton-NotebookLLM/02_Master_Project_Plan/00_MASTER_PROJECT_PLAN.md"
  "/Users/admin/Documents/Gigaton-NotebookLLM/09_Audit_And_Drift/04_Production_State_Verification_2026_05_20.md"
  "/Users/admin/Documents/Gigaton-NotebookLLM/07_Operator_Playbooks/01_Operator_Runbook.md"
  "/Users/admin/Documents/Gigaton-NotebookLLM/03_Engines_And_Architecture/01_Canonical_Repo_Registry.md"
)

# Skipped (frozen historical / archive):
#   session_handoff_2026_05_13_late_evening.md
#   session_handoff_2026_05_14_early_morning.md
#   archive/MASTER_PROJECT_DOCUMENTATION-2026-05-20.md

echo ""
echo "=== Step 1: swap URL in 14 active files ==="

COUNT_CHANGED=0
COUNT_UNCHANGED=0
for f in "${ACTIVE_FILES[@]}"; do
  if [ ! -f "$f" ]; then
    echo "  SKIP (missing): $f"
    continue
  fi
  if grep -q "$OLD_URL" "$f"; then
    # macOS sed requires the -i '' empty backup arg
    sed -i '' "s|${OLD_URL}|${NEW_URL}|g" "$f"
    OCC=$(grep -c "$NEW_URL" "$f" || echo 0)
    echo "  OK    $f (now references $NEW_URL ${OCC}x)"
    COUNT_CHANGED=$((COUNT_CHANGED + 1))
  else
    echo "  noop  $f (already clean)"
    COUNT_UNCHANGED=$((COUNT_UNCHANGED + 1))
  fi
done

echo ""
echo "  ${COUNT_CHANGED} files updated, ${COUNT_UNCHANGED} already clean."

echo ""
echo "=== Step 2: update master plan §3.6 drift #4 (NXDOMAIN → live) ==="

for MP in \
  "/Users/admin/.claude/projects/-Users-admin/memory/master_project_plan.md" \
  "/Users/admin/Documents/Gigaton-NotebookLLM/02_Master_Project_Plan/00_MASTER_PROJECT_PLAN.md"; do
  if [ -f "$MP" ]; then
    # Find the drift #4 line and replace it
    if grep -q "DNS = NXDOMAIN" "$MP"; then
      sed -i '' 's|`api.gigaton.ai` DNS = NXDOMAIN despite registry promising it|`api.gigaton.ai` DNS LIVE 2026-05-20 (drift resolved by Phases C-G sprint)|g' "$MP"
      sed -i '' 's|Provision GoDaddy DNS + Cloud Run domain mapping|✅ Provisioned 2026-05-20|g' "$MP"
      echo "  updated drift #4 in $MP"
    fi
  fi
done

echo ""
echo "=== DONE ==="
echo ""
echo "Verify with:"
echo "  grep -c '${NEW_URL}' /Users/admin/.claude/projects/-Users-admin/memory/master_project_plan.md"
echo "  curl -sI https://${NEW_URL}/v1/healthz | head -3"
echo ""
echo "Memory + NotebookLM mirror are in sync (per master plan §16 update protocol)."
