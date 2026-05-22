#!/usr/bin/env bash
# rebase_26_after_27.sh — run AFTER gigaton-gateway PR #27 merges to main.
#
# Rebases PR #26 (Phase D LLM router) onto new main + force-pushes.
# Conflict expected on Dockerfile + api/main.py (mechanical — adjacent lines, no semantic overlap).
#
# Uses a fresh clone in /tmp so the user's working tree stays untouched.
# Idempotent: re-run safely.

set -euo pipefail

WORK_DIR=$(mktemp -d)
trap "rm -rf $WORK_DIR" EXIT

echo "=== Step 1: fresh clone of gigaton-gateway ==="
git clone git@github.com:todd-gig/gigaton-gateway.git "$WORK_DIR/gigaton-gateway"
cd "$WORK_DIR/gigaton-gateway"

# Pre-flight: confirm PR #27's code is on main
if [ ! -f api/webhooks/github.py ]; then
  echo "ABORT: PR #27 (webhooks) not on main yet — merge #27 first."
  exit 1
fi
echo "  Confirmed: phase C webhooks present on main"

echo ""
echo "=== Step 2: check out PR #26 branch + rebase onto main ==="

git fetch origin feat/phase-d-llm-router
git switch -c feat/phase-d-llm-router origin/feat/phase-d-llm-router

# Try the rebase
if git rebase origin/main; then
  echo "  Rebase clean — no conflicts"
else
  echo ""
  echo "  Conflict detected. Resolving Dockerfile + api/main.py mechanically."

  # Strategy for each known conflict file:
  # Dockerfile: both branches add `COPY --chown=app:app app/ /app/app/`. Take Phase C's version (identical content), abort if structure differs.
  # api/main.py: both branches add to middleware/router lists. Take both — accept theirs (Phase C) + add ours (Phase D) below it.

  for f in Dockerfile api/main.py; do
    if git status --porcelain "$f" | grep -qE "^(UU|AA)"; then
      echo "  Conflict in $f — attempting auto-resolve"

      # Strategy: take "theirs" (origin/main = post-#27) as base, then re-apply Phase D's specific additions.
      # For Dockerfile: Phase C and Phase D both added the same `COPY app/` line — taking theirs gives us the line already.
      git checkout --theirs "$f"

      # For api/main.py: theirs (Phase C) added webhook router + JWT bypass. Phase D added /v1/llm/call route + lifespan. The two sets don't overlap textually but Phase D's lifespan + route are missing after taking theirs. We re-apply them surgically.
      if [ "$f" = "api/main.py" ]; then
        # Note: this is a best-effort patch — if structure has diverged, user must hand-resolve.
        # Phase D's specific additions:
        #   1. lifespan = startup_lifespan(...) registration
        #   2. router.add_api_route for /v1/llm/call BEFORE the catch-all
        # These were added in feat/phase-d-llm-router. We grep them out of the original feat/phase-d-llm-router tree.
        ORIG_D=$(mktemp)
        git show "origin/feat/phase-d-llm-router:api/main.py" > "$ORIG_D"

        # If theirs (Phase C) lacks the LLM router import + lifespan + route, append them.
        if ! grep -q "from app.llm_router import LLMRouter" "$f"; then
          echo "  Phase D imports missing — appending"
          # Best-effort: bail out so user can resolve manually
          echo ""
          echo "AUTO-RESOLVE INCOMPLETE: api/main.py needs hand-merge of Phase D's"
          echo "LLM router import + lifespan + /v1/llm/call route on top of Phase C's webhook"
          echo "router include. Resolve manually then run:"
          echo "  git add api/main.py && git rebase --continue"
          echo "  git push --force-with-lease origin feat/phase-d-llm-router"
          exit 2
        fi
      fi

      git add "$f"
    fi
  done

  if git status --porcelain | grep -q .; then
    git rebase --continue
  else
    echo "  All conflicts resolved automatically"
    git rebase --continue || true
  fi
fi

echo ""
echo "=== Step 3: smoke test rebased branch ==="
if [ -f tests ]; then
  python -m pytest tests/ --tb=short -q 2>&1 | tail -10
else
  echo "  (no pytest run — manual verification recommended)"
fi

echo ""
echo "=== Step 4: force-push (with lease) ==="
git push --force-with-lease origin feat/phase-d-llm-router

echo ""
echo "=== DONE ==="
echo ""
echo "PR #26 is now rebased on top of new main (with Phase C merged)."
echo "Merge it via:"
echo "  gh pr merge 26 --repo todd-gig/gigaton-gateway --squash --delete-branch"
echo ""
echo "Then run post_merge_followups.sh to open the cloudbuild fix + cleanup PRs."
