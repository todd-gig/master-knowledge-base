#!/usr/bin/env bash
# init-repo.sh — provision a new repo with our standard governance files.
#
# Usage:
#   ./scripts/init-repo.sh <repo-path>
#
# Idempotent: re-running on an existing repo updates the governance files
# in place without touching application code.

set -euo pipefail

REPO_PATH="${1:?usage: $0 <repo-path>}"
MKB_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

if [[ ! -d "$REPO_PATH/.git" ]]; then
  echo "error: $REPO_PATH is not a git repo" >&2
  exit 1
fi

cd "$REPO_PATH"

mkdir -p .github

# 1. CODEOWNERS — copy from master-knowledge-base template.
cp "$MKB_ROOT/CODEOWNERS.template" .github/CODEOWNERS
echo "✓ wrote .github/CODEOWNERS"

# 2. PR template if missing.
if [[ ! -f .github/pull_request_template.md ]]; then
  cat > .github/pull_request_template.md <<'EOF'
## What changed

## Why

## Rollback plan
<one sentence>

## Risk
- [ ] low
- [ ] medium
- [ ] high

## Linked issue / decision
EOF
  echo "✓ wrote .github/pull_request_template.md"
fi

# 3. Branch protection reminder.
cat <<EOF

Next steps for $REPO_PATH:
  1. git add .github/ && git commit -m "chore: add governance files (CODEOWNERS, PR template)"
  2. Push to origin.
  3. On GitHub, enable branch protection on 'main':
     - Require PR before merging
     - Require review from CODEOWNERS
     - Require status checks (cloudbuild + tests)
     - Restrict force-push
EOF
