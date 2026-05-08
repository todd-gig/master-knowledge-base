---
title: At-risk WIP inventory — preserve before any cleanup
created: 2026-05-08
purpose: nothing-is-lost audit; any of these locations contains uncommitted work
---

# Why this matters

Several work-in-progress states live across the local environment that aren't on any remote. If a `git reset --hard`, worktree removal, or accidental delete hits these, the work is lost. This doc lists every at-risk location + how to recover.

# Locations holding uncommitted work

## 1. Parent monorepo `~/Documents/GitHub/.git`

**Branch:** `wip/sweep-2026-04-28-1619`
**Tip commit:** `9591176`
**State:** 12 modified submodule pointers + intelligence-silo direct-tracked changes + 4 untracked dirs.

### Modified submodule pointers (the parent's view of submodule SHAs)

```
M  Carmen-Beach-Properties
M  "MD Files"
?  braintrust-knowledge-base
M  claude_decision_logic_pack
M  decision-engine
m  gigaton
m  gigaton-engine
m  gigaton-ui-system
M  master-knowledge-base
M  sales-operating-system
M  transcript-knowledge-base
```

These represent the PARENT's view of where each submodule was. The submodules themselves have their own `.git` and may have moved past these SHAs. Recovery: if the parent's view diverges from submodule reality, `git submodule update --remote` resyncs.

### intelligence-silo direct-tracked changes (NOT a submodule — lives in parent's tracking)

```
M  intelligence-silo/CLAUDE.md
M  intelligence-silo/Dockerfile
M  intelligence-silo/config/silo.yaml
M  intelligence-silo/core/api.py
M  intelligence-silo/core/bridge/__init__.py
M  intelligence-silo/core/bridge/connector.py
M  intelligence-silo/core/memory/__init__.py
M  intelligence-silo/core/memory/semantic.py
M  intelligence-silo/core/node.py
M  intelligence-silo/core/vault/backup.py
?  intelligence-silo/.dockerignore
```

Real code, uncommitted. **Recovery if lost:** none — these are not on any remote. Snapshot before any reset.

### Untracked dirs at parent level

```
?  Gigaton-UI-Platform/        (the active product surface — has its own .git)
?  admin-turtleisland/         (admin documents — own .git)
?  bella-byte/                 (bella's working dir — own .git)
?  intelligence-silo/.dockerignore
```

These are entire directories that the parent has never tracked. Each has its own `.git` so the work inside is preserved per-subdir, but the parent doesn't reference them.

## 2. Master-knowledge-base uncommitted (after PR #1 split)

**Branch:** `feat/governance-2026-05-07` (PR #1 open)
**State:** 3 modified + 14 untracked files NOT included in PR #1.

```
M  CLAUDE.md                            (Doctrine alignment section — prior session)
M  knowledge-extracts/sales-os-catalog.md   (auto-regenerated)
M  scripts/deploy_19.sh                 (publish_governance.sh integration — recent)
?? DESKTOP_AUDIT_2026-05-07.md
?? MASTER_INVENTORY_2026-05-07.md
?? POLICY.md
?? PROCESS.md
?? SERVICES.md
?? TRANSCRIPT_KB_STATUS_2026-05-07.md
?? config/                              (whole dir)
?? deploy-log.jsonl                     (runtime artifact — should be .gitignored)
?? docs-site/                           (whole dir)
?? docs/                                (whole dir)
?? scripts/9pm_commit.sh
?? scripts/github-multiaccount/         (whole dir)
?? scripts/morning_brief.sh
?? scripts/publish_governance.sh        (the script deploy_19.sh now requires)
```

**Note:** `scripts/publish_governance.sh` is REQUIRED by `deploy_19.sh` preflight (added to the script today). If this file is lost, tonight's deploy fails preflight. **High-priority for preservation.**

**Recovery if lost:** the deploy_19.sh modification (publish_governance integration) and publish_governance.sh itself can be recreated from the deploy-log.jsonl manifest output, but the easiest path is to commit them now.

## 3. Rerank worktree (PR #120 closed)

**Path:** `~/Documents/GitHub/Gigaton-UI-Platform/.worktrees/rerank`
**Branch:** `feat/learning-dashboard-rerank-ab` (tip `fd512ab`)
**State:** PR closed, tree has only `.cxguy-active-agent` untracked file.

The branch tip (`fd512ab`) IS pushed to origin (it's still on `origin/feat/learning-dashboard-rerank-ab`). **Local removal would not lose the commit history** — only the working-tree state would go.

**Recovery:** `git worktree add .worktrees/rerank feat/learning-dashboard-rerank-ab` recreates from origin.

## 4. SIE local clone

**Path:** `~/Documents/Claude/Projects/CxGuy-2.0/sovereign-influence-engine`
**Branch:** `feat/phase-a-b-c-integration` (tip `453b3d0`)
**State:** clean. Both this branch and master are pushed to origin. **Nothing at risk here.**

# Recovery primitives

## Stash all sweep-branch dirty state

```bash
cd ~/Documents/GitHub
# clear any stale lock first if needed:
[ -f .git/index.lock ] && rm .git/index.lock
git stash push --include-untracked --message "snapshot 2026-05-08-pre-deploy"
git stash list  # verify
```

After this, `git stash apply` recovers without losing the stash; `git stash pop` recovers and removes the stash.

## Snapshot intelligence-silo work into a wip branch on the parent

```bash
cd ~/Documents/GitHub
git checkout -b wip/intelligence-silo-snapshot-2026-05-08
git add intelligence-silo/
git commit -m "wip: intelligence-silo work-in-progress snapshot 2026-05-08"
git push origin wip/intelligence-silo-snapshot-2026-05-08
git checkout wip/sweep-2026-04-28-1619  # return to original branch
```

This preserves the work in a remote branch you can resume from any machine.

## Master-knowledge-base — split-decision

The 14 untracked files were intentionally left out of PR #1 because they're not from this session. **Either:**
- Identify their original author/session and ask them to commit
- Commit them to a separate `wip/mkb-untracked-2026-05-08` branch with a README explaining provenance is unclear
- Leave alone; they sit untracked indefinitely

`scripts/publish_governance.sh` is the **exception** — it's required by deploy_19.sh, must be committed before the next clean working tree event.

# Quick-action one-liners (you run when ready)

```bash
# 1. Preserve sweep-branch dirty state via stash:
cd ~/Documents/GitHub && git stash push --include-untracked -m "snapshot pre-deploy 2026-05-08"

# 2. Commit publish_governance.sh + deploy_19.sh edit to mkb feat-branch:
cd ~/Documents/GitHub/master-knowledge-base
git add scripts/publish_governance.sh scripts/deploy_19.sh
git commit -m "feat(governance): publish_governance.sh + deploy_19.sh integration"
git push origin feat/governance-2026-05-07  # updates PR #1

# 3. (Optional) Snapshot intelligence-silo work into wip branch:
cd ~/Documents/GitHub
git checkout -b wip/intelligence-silo-snapshot-2026-05-08
git add intelligence-silo/
git commit -m "wip: intelligence-silo snapshot 2026-05-08"
git push origin wip/intelligence-silo-snapshot-2026-05-08
git checkout wip/sweep-2026-04-28-1619
```
