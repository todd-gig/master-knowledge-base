#!/usr/bin/env bash
# ingest_mkb_to_silo.sh — Push MKB content into intelligence-silo as
# operator_id=gigaton with the taxonomy documented in LEARNING_LOOP.md.
#
# Required env:
#   SILO_URL    Base URL of intel-silo (e.g. https://intelligence-silo-xxx.run.app)
#   SILO_TOKEN  Bearer token (Cloud Run authenticated invoker)
#
# Optional env:
#   MKB_ROOT     Defaults to the dir containing this script's parent
#   SILO_INGEST  Path to intel-silo checkout (for scripts/ingest_docs.py).
#                Defaults to ~/Documents/GitHub/intelligence-silo
#   DRY_RUN      Set to 1 to skip the actual POST
#
# Exits non-zero if any sub-ingest fails. Designed to be idempotent — the
# silo's /memory/ingest dedups by content sha256.

set -euo pipefail

MKB_ROOT="${MKB_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
SILO_INGEST="${SILO_INGEST:-$HOME/Documents/GitHub/intelligence-silo}"
INGEST_PY="$SILO_INGEST/scripts/ingest_docs.py"

if [[ ! -f "$INGEST_PY" ]]; then
  echo "ERROR: intel-silo ingest script not found at $INGEST_PY" >&2
  echo "Set SILO_INGEST to your intelligence-silo checkout." >&2
  exit 1
fi

if [[ -z "${SILO_URL:-}" ]]; then
  echo "ERROR: SILO_URL not set." >&2
  exit 1
fi

# Auto-derive SILO_TOKEN from gcloud identity if not provided. Works for both
# interactive runs and launchd (inherits the user's gcloud config). Requires
# the caller to have roles/run.invoker on the silo Cloud Run service.
if [[ -z "${SILO_TOKEN:-}" ]]; then
  if command -v gcloud >/dev/null 2>&1; then
    SILO_TOKEN="$(gcloud auth print-identity-token --audiences="$SILO_URL" 2>/dev/null || true)"
    if [[ -n "$SILO_TOKEN" ]]; then
      export SILO_TOKEN
      echo "Derived SILO_TOKEN from gcloud (audience=$SILO_URL)."
    else
      echo "WARN: gcloud auth print-identity-token failed; ingest_docs.py will run unauthenticated." >&2
    fi
  fi
fi

DRY_FLAG=""
if [[ "${DRY_RUN:-0}" == "1" ]]; then
  DRY_FLAG="--dry-run"
fi

OPERATOR=gigaton
AUTHOR="todd@gigaton.ai"
SUMMARY=()

ingest() {
  local category="$1"; shift
  local label="$1"; shift
  local roots=("$@")
  echo
  echo "=== Ingesting $label (category=$category) ==="
  python3 "$INGEST_PY" \
    "${roots[@]}" \
    --category "$category" \
    --author "$AUTHOR" \
    --operator-id "$OPERATOR" \
    --silo-url "$SILO_URL" \
    $DRY_FLAG || {
      SUMMARY+=("FAIL  $label")
      return 1
    }
  SUMMARY+=("OK    $label")
}

cd "$MKB_ROOT"

ingest foundational "Foundational doctrine" \
  CONSTITUTION.md PRINCIPLES.md LEARNING_LOOP.md MASTER_PROJECT_PLAN.md

[[ -d decisions ]]                  && ingest doctrine        "Decision packs"            decisions/
[[ -d decision-execution-engine ]]  && ingest doctrine        "Decision execution engine" decision-execution-engine/
[[ -d for-the-group ]]              && ingest doctrine        "For-the-group frameworks"  for-the-group/
[[ -d manifests ]]                  && ingest capability      "Onboarding & capability manifests" manifests/
[[ -d runbooks ]]                   && ingest runbook         "Operational runbooks"      runbooks/
[[ -d knowledge-extracts ]]         && ingest extract         "Knowledge extracts"        knowledge-extracts/
[[ -d memory-snapshots ]]           && ingest session-memory  "Promoted auto-memory"      memory-snapshots/
[[ -d claude-systems/v3.2 ]]        && ingest operating-system "Claude OS v3.2"           claude-systems/v3.2/
[[ -d brand-knowledge-library ]]    && ingest extract         "Brand knowledge library"   brand-knowledge-library/

echo
echo "=== Ingest summary ==="
printf '%s\n' "${SUMMARY[@]}"

# Fail the run if any ingest failed
for line in "${SUMMARY[@]}"; do
  [[ "$line" == FAIL* ]] && exit 2
done
