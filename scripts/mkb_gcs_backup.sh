#!/usr/bin/env bash
# mkb_gcs_backup.sh — Nightly off-GitHub bundle of MKB into GCS.
# Belt-and-suspenders against the "only backup is the GitHub remote" risk.
#
# Required env:
#   GCS_BUCKET   e.g. gs://gigaton-mkb-backup
# Optional env:
#   MKB_ROOT     Defaults to the script's parent's parent
#   RETAIN_DAYS  Days of bundles to keep (default 90)

set -euo pipefail

MKB_ROOT="${MKB_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
BUCKET="${GCS_BUCKET:?GCS_BUCKET must be set, e.g. gs://gigaton-mkb-backup}"
RETAIN_DAYS="${RETAIN_DAYS:-90}"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
BUNDLE="/tmp/mkb-${STAMP}.bundle"
ARCHIVE="/tmp/mkb-worktree-${STAMP}.tar.gz"

cd "$MKB_ROOT"

# 1. Git bundle of every ref — fully restorable git history
git bundle create "$BUNDLE" --all

# 2. Tar of the working tree (minus .git, node_modules, .pytest_cache)
tar --exclude='.git' --exclude='node_modules' --exclude='.pytest_cache' \
    --exclude='.claude/worktrees' \
    -czf "$ARCHIVE" -C "$MKB_ROOT" .

# 3. Upload both with date-partitioned paths
gcloud storage cp "$BUNDLE"   "${BUCKET}/bundles/mkb-${STAMP}.bundle"
gcloud storage cp "$ARCHIVE"  "${BUCKET}/worktree/mkb-${STAMP}.tar.gz"

# 4. Prune old bundles — gsutil-style age filter via list+sort
CUTOFF=$(date -u -v-${RETAIN_DAYS}d +%Y%m%d 2>/dev/null || date -u -d "${RETAIN_DAYS} days ago" +%Y%m%d)
echo "Pruning bundles older than ${CUTOFF}…"
gcloud storage ls "${BUCKET}/bundles/" 2>/dev/null \
  | awk -F/ -v cutoff="$CUTOFF" '
      {
        f=$NF
        if (match(f, /mkb-([0-9]{8})T/, m)) {
          if (m[1] < cutoff) print $0
        }
      }' \
  | xargs -r -n1 gcloud storage rm

rm -f "$BUNDLE" "$ARCHIVE"
echo "MKB backup complete: ${BUCKET}/bundles/mkb-${STAMP}.bundle"
