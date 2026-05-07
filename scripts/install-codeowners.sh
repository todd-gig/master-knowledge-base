#!/usr/bin/env bash
# install-codeowners.sh — backfill CODEOWNERS across all production repos.
#
# Usage:
#   ./scripts/install-codeowners.sh           # dry-run
#   ./scripts/install-codeowners.sh --apply   # actually write
#
# Reads master-knowledge-base/CODEOWNERS.template and copies it to
# .github/CODEOWNERS in each listed repo. Does NOT commit — leaves the
# change unstaged so a human can review per repo.

set -euo pipefail

APPLY=0
[[ "${1:-}" == "--apply" ]] && APPLY=1

MKB_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
GH_ROOT="$(cd "$MKB_ROOT/.." && pwd)"

PROD_REPOS=(
  "Carmen-Beach-Properties"
  "decision-engine"
  "gigaton"
  "gigaton-engine"
  "gigaton-ui-system"
  "intelligence-silo"
  "master-knowledge-base"
  "sales-operating-system"
  "transcript-knowledge-base"
)

for repo in "${PROD_REPOS[@]}"; do
  path="$GH_ROOT/$repo"
  if [[ ! -d "$path/.git" ]]; then
    echo "skip $repo (not a git repo at $path)"
    continue
  fi
  target="$path/.github/CODEOWNERS"
  if [[ $APPLY -eq 1 ]]; then
    mkdir -p "$path/.github"
    cp "$MKB_ROOT/CODEOWNERS.template" "$target"
    echo "✓ wrote $target"
  else
    if [[ -f "$target" ]] && diff -q "$MKB_ROOT/CODEOWNERS.template" "$target" >/dev/null 2>&1; then
      echo "[dry-run] $repo: already up to date"
    else
      echo "[dry-run] would write $target"
    fi
  fi
done

if [[ $APPLY -eq 0 ]]; then
  echo
  echo "Dry-run complete. Re-run with --apply to write files."
  echo "Each repo's diff stays unstaged so you can review and commit per repo."
fi
