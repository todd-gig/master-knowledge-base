#!/usr/bin/env bash
# deploy_19.sh — daily manual deploy trigger (19:00 CT cutoff).
#
# Usage:
#   ./scripts/deploy_19.sh                 # run all production services
#   ./scripts/deploy_19.sh <svc>           # run one service (hot fix path)
#   ./scripts/deploy_19.sh --check         # pre-flight only, no deploy
#   ./scripts/deploy_19.sh --list          # print services + deploy mechanism
#
# Refuses to run if:
#   - it's already past 20:00 CT (use morning instead)
#   - the previous day's entry in deploy-log.jsonl is not green
#
# Logs every run as one line in master-knowledge-base/deploy-log.jsonl.

set -uo pipefail

MKB_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
GH_ROOT="$(cd "$MKB_ROOT/.." && pwd)"
SIE_ROOT="/Users/admin/Documents/Claude/Projects/CxGuy-2.0/sovereign-influence-engine"
LOG="$MKB_ROOT/deploy-log.jsonl"
GCP_PROJECT="carmen-beach-properties"

# Service registry: order = deploy sequence (backends first, frontends last).
# Each entry: "svc_id|repo_path|deploy_mechanism"
# deploy_mechanism: cloudbuild | sie_daily | gh_workflow | firebase_auto_verify
SERVICES=(
  "decision-engine|$GH_ROOT/decision-engine|cloudbuild"
  "gigaton-engine|$GH_ROOT/gigaton-engine|cloudbuild"
  "sales-operating-system|$GH_ROOT/sales-operating-system|cloudbuild"
  "intelligence-silo|$GH_ROOT/intelligence-silo|cloudbuild"
  "sovereign-influence-engine|$SIE_ROOT|sie_daily"
  # DESCOPED 2026-05-08 until 2026-05-13 (Wed) — Carmen Beach needs:
  # 6 GH secrets + Cloud SQL instance + Secret Manager entries + gh-deploy SA
  # before deploy-prod.yml workflow can succeed. See:
  # decisions/2026-05-08_carmen_beach_descope.md for the prereq checklist.
  # "Carmen-Beach-Properties|$GH_ROOT/Carmen-Beach-Properties|gh_workflow"
  "Gigaton-UI-Platform|$GH_ROOT/Gigaton-UI-Platform|firebase_auto_verify"
)

ts() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }
ct_hour() { TZ=America/Chicago date +%H; }

log_event() {
  local kind="$1" svc="${2:-_all}" status="${3:-info}" msg="${4:-}"
  if command -v jq >/dev/null 2>&1; then
    jq -nc \
      --arg ts "$(ts)" --arg kind "$kind" --arg svc "$svc" \
      --arg status "$status" --arg msg "$msg" \
      '{ts:$ts, kind:$kind, svc:$svc, status:$status, msg:$msg}' \
      >> "$LOG"
  else
    printf '{"ts":"%s","kind":"%s","svc":"%s","status":"%s","msg":"%s"}\n' \
      "$(ts)" "$kind" "$svc" "$status" "$msg" >> "$LOG"
  fi
}

list_services() {
  printf "%-30s %-15s %s\n" "SERVICE" "MECHANISM" "PATH"
  for entry in "${SERVICES[@]}"; do
    IFS='|' read -r svc path mech <<< "$entry"
    printf "%-30s %-15s %s\n" "$svc" "$mech" "$path"
  done
}

preflight() {
  local h
  h="$(ct_hour)"
  if (( 10#$h >= 20 )); then
    echo "✗ It's already past 20:00 CT. Skip today; deploy tomorrow morning instead." >&2
    log_event preflight _all blocked "past 20:00 CT"
    return 2
  fi

  if ! gcloud auth print-identity-token >/dev/null 2>&1; then
    echo "✗ gcloud not authenticated. Run: gcloud auth login" >&2
    log_event preflight _all blocked "gcloud not authed"
    return 3
  fi

  if [[ -f "$LOG" ]] && command -v jq >/dev/null 2>&1; then
    local last_status
    last_status="$(tail -200 "$LOG" 2>/dev/null | jq -r 'select(.kind=="run_end") | .status' 2>/dev/null | tail -1)"
    if [[ -n "$last_status" && "$last_status" != "ok" && "$last_status" != "skipped" ]]; then
      echo "✗ Previous deploy didn't end clean ($last_status). Resolve before redeploying." >&2
      log_event preflight _all blocked "previous run not green"
      return 4
    fi
  fi

  # Governance verification: refuse to deploy if canonical docs are missing or stale.
  # publish_governance.sh emits its own manifest into deploy-log.jsonl.
  if [[ -x "$MKB_ROOT/scripts/publish_governance.sh" ]]; then
    if ! "$MKB_ROOT/scripts/publish_governance.sh" >&2; then
      echo "✗ governance verification failed — see deploy-log.jsonl" >&2
      log_event preflight _all blocked "governance verification failed"
      return 5
    fi
  fi

  echo "✓ pre-flight clean (CT hour=$h, gcloud=ok, prev=ok, governance=ok)"
  log_event preflight _all ok ""
  return 0
}

deploy_cloudbuild() {
  local svc="$1" path="$2"
  if [[ ! -f "$path/cloudbuild.yaml" ]]; then
    echo "  ✗ $svc: no cloudbuild.yaml at $path" >&2
    log_event deploy_end "$svc" failed "no cloudbuild.yaml"
    return 1
  fi
  # cloudbuild.yamls reference $COMMIT_SHA which Cloud Build only auto-populates
  # when triggered from a git source (Cloud Source Repositories / GitHub trigger).
  # When invoked from a local tarball via `gcloud builds submit`, COMMIT_SHA is
  # empty unless we pass it explicitly.
  local sha
  sha=$(git -C "$path" rev-parse HEAD 2>/dev/null || echo "manual-$(date +%s)")
  echo "  → cloudbuild submit for $svc (sha=${sha:0:12})"
  ( cd "$path" && gcloud builds submit \
      --config=cloudbuild.yaml \
      --project="$GCP_PROJECT" \
      --substitutions="COMMIT_SHA=$sha" \
      --quiet )
}

deploy_sie_daily() {
  local svc="$1" path="$2"
  if [[ ! -x "$path/daily_deploy.sh" ]]; then
    echo "  ✗ $svc: $path/daily_deploy.sh not executable or missing" >&2
    log_event deploy_end "$svc" failed "daily_deploy.sh missing"
    return 1
  fi
  echo "  → SIE daily_deploy.sh"
  ( cd "$path" && bash daily_deploy.sh )
}

deploy_gh_workflow() {
  local svc="$1" path="$2"
  # Carmen-Beach-Properties — fires the deploy-prod.yml workflow.
  echo "  → gh workflow run deploy-prod.yml ($svc)"
  ( cd "$path" && gh workflow run deploy-prod.yml )
}

deploy_firebase_auto_verify() {
  local svc="$1"
  # Gigaton-UI-Platform auto-deploys to Firebase Hosting on every merge to main.
  # Don't redeploy from here — just verify the last CI run on main was green.
  local last
  last="$(gh run list --repo bella-byte/Gigaton-UI-Platform --branch main --workflow=firebase-hosting-merge.yml --limit=1 --json conclusion --jq '.[0].conclusion' 2>/dev/null)"
  if [[ "$last" == "success" ]]; then
    echo "  ✓ $svc: last Firebase merge deploy = success (no action needed)"
    log_event deploy_end "$svc" skipped "auto-deployed via Firebase, last=success"
    return 0
  else
    echo "  ⚠ $svc: last Firebase merge deploy = ${last:-unknown}. Investigate." >&2
    log_event deploy_end "$svc" failed "Firebase last=$last"
    return 1
  fi
}

deploy_one() {
  local svc_filter="$1" entry svc path mech
  local found=0
  for entry in "${SERVICES[@]}"; do
    IFS='|' read -r svc path mech <<< "$entry"
    if [[ "$svc" == "$svc_filter" ]]; then
      found=1
      echo "→ deploying $svc (mechanism=$mech)"
      log_event deploy_start "$svc" running ""
      case "$mech" in
        cloudbuild)             deploy_cloudbuild "$svc" "$path" ;;
        sie_daily)              deploy_sie_daily "$svc" "$path" ;;
        gh_workflow)            deploy_gh_workflow "$svc" "$path" ;;
        firebase_auto_verify)   deploy_firebase_auto_verify "$svc" ;;
        *) echo "  ✗ unknown mechanism: $mech" >&2; return 1 ;;
      esac
      local rc=$?
      if (( rc == 0 )); then
        log_event deploy_end "$svc" ok ""
        echo "✓ $svc"
      else
        log_event deploy_end "$svc" failed "deploy returned $rc"
        echo "✗ $svc — exit $rc" >&2
        return 1
      fi
    fi
  done
  if (( found == 0 )); then
    echo "✗ unknown service: $svc_filter (use --list to see available)" >&2
    return 1
  fi
}

main() {
  case "${1:-}" in
    --list)
      list_services
      exit 0
      ;;
    --check)
      preflight; exit $?
      ;;
  esac

  log_event run_start _all running "trigger=manual user=$(whoami)"

  if ! preflight; then
    log_event run_end _all failed "preflight blocked"
    exit 1
  fi

  if [[ -n "${1:-}" ]]; then
    if deploy_one "$1"; then
      log_event run_end _all ok "single-service: $1"
      echo "✓ done"
    else
      log_event run_end _all failed "single-service $1 failed"
      exit 1
    fi
    exit 0
  fi

  failed=()
  for entry in "${SERVICES[@]}"; do
    IFS='|' read -r svc _ _ <<< "$entry"
    deploy_one "$svc" || failed+=("$svc")
  done

  if (( ${#failed[@]} )); then
    log_event run_end _all failed "services: ${failed[*]}"
    echo "✗ failed services: ${failed[*]}" >&2
    exit 1
  fi

  log_event run_end _all ok ""
  echo "✓ all green"
}

main "$@"
