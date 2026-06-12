---
name: feedback-verify-production-state-before-planning
description: "Before writing any \"what's missing / what to build\" plan, verify production state with gcloud + gh. Memory can be 24-48h stale; trusting it produces obsolete plans that waste a sprint of effort."
metadata: 
  node_type: memory
  type: feedback
  established: 2026-05-22
  origin_incident: "2026-05-22 storage flip plan written based on stale memory; while writing, parallel sprint S1-S16 shipped both engines to Cloud SQL (decision-engine rev 00037-86d + intelligence-silo rev 00036-flc deployed within minutes of each other), making the plan obsolete before it could execute."
  originSessionId: 2eb8068b-17a6-4456-b364-07fcd24b12a2
promoted_from: feedback_verify_production_state_before_planning.md
promoted_at: 2026-06-02T20:13:25Z
---

# Verify production state BEFORE writing a plan that claims something is missing

**Rule.** Before writing a "what's missing / what to build" plan for the Gigaton ecosystem, verify production state by running:

- `gcloud run services list --format='value(name,latestReadyRevisionName)'` (both projects)
- `gh pr list --repo <relevant-repo> --state all --limit 10` (each repo the plan touches)
- `gcloud sql instances list --format='value(name,state)'` (both projects)

**Why.** Memory in `/Users/admin/.claude/projects/-Users-admin/memory/` is a snapshot, not a live oracle. Sibling agents and parallel sessions ship work continuously — on 2026-05-22 a 13-PR sprint landed across 5 repos in 24 hours. Memory frequently lags reality by 24-48 hours. A plan written against stale memory claims things are missing that have already shipped.

**Past incident (2026-05-22).** I wrote a detailed file-level "storage flip plan" for DEE + EO based on memory claiming both engines were "in-memory v0; Cloud SQL provisioned but not yet flipped." Verification just before execution showed:
- decision-engine had Alembic adoption (PR #78) MERGED 2026-05-21 and follow-on baselines (PR #80) MERGED 2026-05-22 — rev `00037-86d` LIVE on Cloud SQL.
- intelligence-silo had Cloud SQL wiring (PR #27) MERGED 2026-05-20 and boot-gate migrations (PR #34) MERGED 2026-05-21 — rev `00036-flc` LIVE on Cloud SQL. They deliberately chose RAW SQL boot-gate over Alembic — a different architecture than my plan proposed, but equivalent outcome.
- Wasted: ~30 min writing a detailed file-level plan that was obsolete on arrival.

**How to apply.**

1. **Before any plan that claims X is missing** — run the gcloud/gh verification commands above. Diff against memory.
2. **Look for agent worktrees** — `git worktree list` in any major repo. If there are locked worktrees on adjacent branches, sibling agents are actively shipping work; double-check before claiming anything is missing.
3. **Check current branch state** — `git status` + `git log --oneline -10 main..HEAD`. If you're on a feature branch with uncommitted work, that work is someone else's; do NOT touch it.
4. **Memory says "X is planned / approved but not shipped"** — treat that as "X was planned at the time of writing; check now." Especially for items dated within the last 7 days.
5. **Write plans defensively** — if uncertain, start the plan with "verified production state on YYYY-MM-DD HH:MMZ: X live, Y missing" so future readers know the snapshot date.

Related:
- [[repo_registry]] — the canonical "where things live" file, which is itself updated after production audits.
- [[master_project_plan]] §3 — current production reality, updated 2026-05-20+.
- `docs/architecture/CODEBASE_MAP.md` — the post-2026-05-22 audit map; itself superseded items as work ships.
