#!/usr/bin/env bash
# deploy_19_prompt.sh — fires at 19:00 CT, prompts the human to deploy.
#
# Triggered by ~/Library/LaunchAgents/ai.gigaton.daily-deploy-prompt.plist
# at 19:00 America/Chicago daily.
#
# Behavior:
#   - osascript dialog: "Time to deploy. [Open Terminal] [Skip Today]"
#   - If "Open Terminal": opens Terminal.app at master-knowledge-base/scripts/
#     with deploy_19.sh primed. Human runs it manually.
#   - If "Skip Today": logs the skip in deploy-log.jsonl. Tomorrow's preflight
#     will not block on a missing previous-day green.
#
# This is the prompt-based daily ritual per the locked decision:
#   "manual trigger at or by 19:00 CT. Past 20:00 CT = skip, deploy in morning."

set -euo pipefail

MKB_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOG="$MKB_ROOT/deploy-log.jsonl"

ts() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }

log_event() {
  local kind="$1" status="${2:-info}" msg="${3:-}"
  printf '{"ts":"%s","kind":"%s","svc":"_all","status":"%s","msg":"%s"}\n' \
    "$(ts)" "$kind" "$status" "$msg" >> "$LOG"
}

# Show macOS dialog. Returns "Open Terminal", "Skip Today", or "" on close.
choice="$(osascript <<APPLESCRIPT
try
  tell application "System Events"
    activate
    set theDialog to display dialog "Time to deploy.

Daily 19:00 CT deploy ritual. Decide now or skip today (deploy tomorrow morning instead).

Past 20:00 CT will refuse to deploy and require a morning run." with title "Gigaton Daily Deploy" buttons {"Skip Today", "Open Terminal"} default button "Open Terminal" with icon note giving up after 600
  end tell
  return button returned of theDialog
on error
  return ""
end try
APPLESCRIPT
)"

case "$choice" in
  "Open Terminal")
    log_event prompt clicked "open_terminal"
    osascript <<APPLESCRIPT
tell application "Terminal"
  activate
  do script "cd '$MKB_ROOT/scripts' && echo '→ Run: ./deploy_19.sh' && exec bash"
end tell
APPLESCRIPT
    ;;
  "Skip Today")
    log_event prompt clicked "skip_today"
    # Pre-mark previous run as green so tomorrow's preflight passes
    printf '{"ts":"%s","kind":"run_end","svc":"_all","status":"ok","msg":"skipped by operator"}\n' \
      "$(ts)" >> "$LOG"
    ;;
  "")
    log_event prompt timeout "no_response_in_10min"
    ;;
esac
