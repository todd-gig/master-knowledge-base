#!/usr/bin/env bash
# deploy_19.sh — daily manual deploy trigger (19:00 CT cutoff).
#
# Usage:
#   ./scripts/deploy_19.sh           # run all production services
#   ./scripts/deploy_19.sh <svc>     # run one service (hot fix path)
#   ./scripts/deploy_19.sh --check   # pre-flight only, no deploy
#
# Refuses to run if:
#   - any production repo has a dirty working tree
#   - it's already past 20:00 CT (use morning instead)
#   - the previous day's entry in deploy-log.jsonl is not green
#
# Logs every run as one line in master-knowledge-base/deploy-log.jsonl.
#
# STATUS: SKELETON — fill in service-specific build/deploy logic on Day 3-4.

set -euo pipefail

MKB_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
GH_ROOT="$(cd "$MKB_ROOT/.." && pwd)"
LOG="$MKB_ROOT/deploy-log.jsonl"

# Order matters: backend services before things that depend on them.
SERVICES=(
  "decision-engine"
  "intelligence-silo"
  "gigaton-engine"
  "sales-operating-system"
  "gigaton"
  "Carmen-Beach-Properties"
)

ts() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }
ct_hour() { TZ=America/Chicago date +%H; }

log_event() {
  local kind="$1" svc="${2:-_all}" status="${3:-info}" msg="${4:-}"
  jq -n \
    --arg ts "$(ts)" \
    --arg kind "$kind" \
    --arg svc "$svc" \
    --arg status "$status" \
    --arg msg "$msg" \
    '{ts:$ts, kind:$kind, svc:$svc, status:$status, msg:$msg}' \
    >> "$LOG"
}

preflight() {
  local h
  h="$(ct_hour)"
  if (( 10#$h >= 20 )); then
    echo "✗ It's already past 20:00 CT. Skip today; deploy tomorrow morning instead."
    log_event preflight _all blocked "past 20:00 CT"
    exit 2
  fi

  for s in "${SERVICES[@]}"; do
    if [[ -d "$GH_ROOT/$s/.git" ]]; then
      if ! git -C "$GH_ROOT/$s" diff --quiet --ignore-submodules HEAD; then
        echo "✗ $s has a dirty working tree."
        log_event preflight "$s" blocked "dirty tree"
        exit 3
      fi
    fi
  done

  if [[ -f "$LOG" ]]; then
    last_status="$(tail -200 "$LOG" | jq -r 'select(.kind=="run_end") | .status' | tail -1)"
    if [[ -n "$last_status" && "$last_status" != "ok" ]]; then
      echo "✗ Previous deploy didn't end green ($last_status). Resolve before redeploying."
      log_event preflight _all blocked "previous run not green"
      exit 4
    fi
  fi

  echo "✓ pre-flight clean"
  log_event preflight _all ok ""
}

deploy_one() {
  local svc="$1"
  echo "→ deploying $svc"
  log_event deploy_start "$svc" running ""

  # Each repo will gain a Makefile with `make deploy` on Day 3.
  # For now this is a placeholder dispatch.
  if [[ -f "$GH_ROOT/$svc/Makefile" ]] && grep -q '^deploy:' "$GH_ROOT/$svc/Makefile"; then
    if ( cd "$GH_ROOT/$svc" && make deploy ); then
      log_event deploy_end "$svc" ok ""
      echo "✓ $svc"
    else
      log_event deploy_end "$svc" failed "make deploy returned non-zero"
      echo "✗ $svc — auto-rolling back"
      # TODO: gcloud run services update-traffic <svc> --to-revisions=<prev>=100
      return 1
    fi
  else
    echo "  (skipped — no Makefile deploy target yet — Day 3 work)"
    log_event deploy_end "$svc" skipped "no make deploy target"
  fi
}

main() {
  if [[ "${1:-}" == "--check" ]]; then
    preflight
    exit 0
  fi

  log_event run_start _all running "trigger=manual"
  preflight

  if [[ -n "${1:-}" ]]; then
    deploy_one "$1"
  else
    failed=()
    for s in "${SERVICES[@]}"; do
      deploy_one "$s" || failed+=("$s")
    done
    if (( ${#failed[@]} )); then
      log_event run_end _all failed "services: ${failed[*]}"
      exit 1
    fi
  fi

  log_event run_end _all ok ""
  echo "✓ all green"
}

main "$@"
