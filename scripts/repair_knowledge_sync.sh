#!/usr/bin/env bash
# repair_knowledge_sync.sh — Move sync.py out of ~/Documents (TCC-restricted)
# and update the com.knowledge.sync launchd plist.
#
# Root cause: launchd_err.log shows
#   can't open file '/Users/admin/Documents/knowledge-sync/sync.py':
#   [Errno 1] Operation not permitted
# macOS TCC blocks launchd's Python from reading user's ~/Documents folder
# without Full Disk Access. Moving the script out of ~/Documents avoids the
# permission gate without requiring System Settings clicks.

set -euo pipefail

SRC="$HOME/Documents/knowledge-sync/sync.py"
DEST_DIR="$HOME/.knowledge_sync/bin"
DEST="$DEST_DIR/sync.py"
PLIST="$HOME/Library/LaunchAgents/com.knowledge.sync.plist"
LABEL="com.knowledge.sync"

if [[ ! -f "$SRC" ]]; then
  echo "ERROR: sync.py not found at $SRC" >&2
  exit 1
fi

mkdir -p "$DEST_DIR"
cp -p "$SRC" "$DEST"
echo "Copied sync.py → $DEST"

# Update plist if it exists — patch ProgramArguments in place
if [[ -f "$PLIST" ]]; then
  /usr/bin/plutil -replace ProgramArguments -json "[\"/usr/bin/python3\", \"$DEST\"]" "$PLIST"
  echo "Patched $PLIST ProgramArguments → python3 $DEST"
  launchctl unload "$PLIST" 2>/dev/null || true
  launchctl load   "$PLIST"
  echo "Reloaded $LABEL"
else
  echo "WARN: $PLIST not found — sync.py copied but launchd job not patched." >&2
fi

# Verify next run by tailing the log
LOG_DIR="$HOME/.knowledge_sync"
echo
echo "Logs to watch:"
echo "  $LOG_DIR/launchd_err.log"
echo "  $LOG_DIR/sync.log"
echo
echo "Trigger manually:"
echo "  launchctl kickstart -k gui/\$UID/$LABEL"
