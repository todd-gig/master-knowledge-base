#!/usr/bin/env bash
# install_settings_json_patterns.sh
#
# One-shot installer that adds two batches to ~/.claude/settings.json:
#
#   1. Bash permission patterns for the Gignet Phases C-G sprint
#      (~22 patterns scoped to gigaton-platform only). Removes classifier
#      friction for the rest of this sprint + ongoing ops on the fabric.
#
#   2. Phase E hook wiring for gignet-session-claim.sh + gignet-session-release.sh
#      (gives every local Claude Code session a Firestore task_registry lease
#      so multi-instance contention auto-resolves).
#
# Idempotent: safe to re-run; only adds patterns/hooks that aren't already present.
# Backs up to ~/.claude/settings.json.bak.<timestamp> before writing.
# Validates JSON before + after; aborts if either fails.
#
# After running:
#   - Open /hooks once in Claude Code OR restart the CLI so the watcher reloads
#     the new patterns. (The settings watcher only re-reads on explicit signal.)
#
# Usage:
#   bash ~/Documents/GitHub/master-knowledge-base/runbooks/install_settings_json_patterns.sh
#
# Reversible: ~/.claude/settings.json.bak.<ts> contains the pre-install version.

set -euo pipefail

SETTINGS=~/.claude/settings.json
BACKUP=~/.claude/settings.json.bak.$(date +%s)

if [ ! -f "$SETTINGS" ]; then
  echo "ABORT: $SETTINGS does not exist."
  exit 1
fi

echo "=== Pre-flight: validate current JSON ==="
python3 -c "import json; json.load(open('$SETTINGS'))" 2>&1 | head -3
echo "  OK"

echo ""
echo "=== Backup: $BACKUP ==="
cp "$SETTINGS" "$BACKUP"
echo "  done"

echo ""
echo "=== Merging new patterns + hooks ==="

python3 <<PY
import json
from pathlib import Path

p = Path("$SETTINGS")
s = json.loads(p.read_text())

# ============================================================
# BATCH 1 — Bash permission patterns for Gignet sprint
# ============================================================
new_allow = [
    "Bash(gcloud projects add-iam-policy-binding gigaton-platform *)",
    "Bash(gcloud secrets * --project=gigaton-platform)",
    "Bash(gcloud secrets * --project=gigaton-platform *)",
    "Bash(gcloud secrets add-iam-policy-binding * --project=gigaton-platform *)",
    "Bash(gcloud beta monitoring channels create *)",
    "Bash(gcloud beta monitoring channels list *)",
    "Bash(gcloud beta monitoring policies create *)",
    "Bash(gcloud beta monitoring policies list *)",
    "Bash(gcloud monitoring dashboards create *)",
    "Bash(gcloud monitoring dashboards list *)",
    "Bash(gcloud pubsub topics * --project=gigaton-platform)",
    "Bash(gcloud pubsub topics * --project=gigaton-platform *)",
    "Bash(gcloud pubsub subscriptions * --project=gigaton-platform)",
    "Bash(gcloud pubsub subscriptions * --project=gigaton-platform *)",
    "Bash(gcloud functions deploy * --project=gigaton-platform *)",
    "Bash(gcloud functions list --project=gigaton-platform *)",
    "Bash(gcloud iam service-accounts create * --project=gigaton-platform *)",
    "Bash(gcloud iam service-accounts add-iam-policy-binding * --project=gigaton-platform *)",
    "Bash(gcloud pubsub topics add-iam-policy-binding * --project=gigaton-platform *)",
    "Bash(gcloud firestore * --project=gigaton-platform *)",
    "Bash(gcloud services enable * --project=gigaton-platform)",
    "Bash(gcloud beta run domain-mappings * --project=gigaton-platform *)",
    # Phase E hook script execution permissions:
    "Bash(~/.claude/hooks/gignet-session-claim.sh *)",
    "Bash(~/.claude/hooks/gignet-session-release.sh *)",
]

current_allow = s.setdefault("permissions", {}).setdefault("allow", [])
added_perms = []
for pattern in new_allow:
    if pattern not in current_allow:
        current_allow.append(pattern)
        added_perms.append(pattern)

print(f"permissions.allow: added {len(added_perms)} new patterns (skipped {len(new_allow) - len(added_perms)} already present)")
for pattern in added_perms:
    print(f"  + {pattern}")

# ============================================================
# BATCH 2 — Phase E hook wiring
# ============================================================
hooks = s.setdefault("hooks", {})

claim_hook = {
    "type": "command",
    "command": "~/.claude/hooks/gignet-session-claim.sh",
    "timeout": 5,
    "async": True,
}

ups_list = hooks.setdefault("UserPromptSubmit", [])
if not ups_list:
    ups_list.append({"hooks": []})
ups_inner = ups_list[0].setdefault("hooks", [])
if not any(h.get("command", "").endswith("gignet-session-claim.sh") for h in ups_inner):
    ups_inner.append(claim_hook)
    print("hooks.UserPromptSubmit: added gignet-session-claim.sh")
else:
    print("hooks.UserPromptSubmit: gignet-session-claim.sh already present, skipped")

release_hook = {
    "type": "command",
    "command": "~/.claude/hooks/gignet-session-release.sh",
    "timeout": 5,
    "async": True,
}

stop_list = hooks.setdefault("Stop", [])
if not stop_list:
    stop_list.append({"hooks": []})
stop_inner = stop_list[0].setdefault("hooks", [])
if not any(h.get("command", "").endswith("gignet-session-release.sh") for h in stop_inner):
    stop_inner.append(release_hook)
    print("hooks.Stop: added gignet-session-release.sh")
else:
    print("hooks.Stop: gignet-session-release.sh already present, skipped")

p.write_text(json.dumps(s, indent=2) + "\n")
print("")
print(f"wrote {p}")
PY

echo ""
echo "=== Post-flight: re-validate JSON ==="
python3 -c "import json; json.load(open('$SETTINGS'))" 2>&1 | head -3
echo "  OK"

echo ""
echo "=== Diff summary (first 60 lines) ==="
diff -u "$BACKUP" "$SETTINGS" | head -60 || true

echo ""
echo "=== DONE ==="
echo ""
echo "Next steps:"
echo "  1. Open /hooks once in Claude Code OR restart the CLI so the watcher"
echo "     reloads the new permissions + hooks."
echo ""
echo "  2. (Optional but recommended) Install gignet-coordination on system"
echo "     python3 so the claim/release hooks actually claim tasks:"
echo "       cd ~/Documents/GitHub/gignet-local-node && python3.11 -m pip install -e ."
echo "     If you don't have python3.11+ as default, the hooks gracefully no-op"
echo "     + log; you can wrap them in a venv launcher later."
echo ""
echo "  3. Verify the hooks fire on next session start:"
echo "       ls -la ~/.gignet/active-claim-*.json 2>/dev/null || echo '(no active claim yet)'"
echo ""
echo "Backup is at: $BACKUP"
echo "To revert: cp '$BACKUP' '$SETTINGS'  &&  restart Claude Code"
