#!/usr/bin/env bash
# install_launchagents.sh — Copy MKB launchd plists into ~/Library/LaunchAgents
# and load them. Safe to re-run.
#
# Skips com.gigaton.mkb-ingest unless SILO_URL is set in the env or the plist
# was hand-edited (so we don't load a broken job).

set -euo pipefail

SRC="$(cd "$(dirname "$0")/launchagents" && pwd)"
DEST="$HOME/Library/LaunchAgents"
mkdir -p "$DEST"

JOBS=(
  com.gigaton.mkb-gcs-backup
  com.gigaton.mkb-ingest
  com.gigaton.auto-memory-promote
  com.gigaton.knowledge-extracts-refresh
)

for job in "${JOBS[@]}"; do
  src_plist="$SRC/${job}.plist"
  dst_plist="$DEST/${job}.plist"
  if [[ ! -f "$src_plist" ]]; then
    echo "WARN: missing $src_plist, skipping"
    continue
  fi

  # mkb-ingest needs a configured SILO_URL — skip if still placeholder
  if [[ "$job" == "com.gigaton.mkb-ingest" ]]; then
    if grep -q '<key>SILO_TOKEN</key>\s*<string></string>' "$src_plist" 2>/dev/null \
       && [[ -z "${SILO_TOKEN:-}" ]]; then
      echo "SKIP $job — SILO_TOKEN not set (edit $src_plist or export SILO_TOKEN)"
      continue
    fi
  fi

  cp "$src_plist" "$dst_plist"
  launchctl unload "$dst_plist" 2>/dev/null || true
  launchctl load   "$dst_plist"
  echo "Loaded $job"
done

echo
echo "Verify with: launchctl list | grep gigaton"
echo "Logs:        ~/.knowledge_sync/*.log"
