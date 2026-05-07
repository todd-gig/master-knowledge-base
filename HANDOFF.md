---
title: Handoff — Continuing the 10-Day Revenue Plan in a Fresh Conversation
created: 2026-05-07
revised: 2026-05-07 (afternoon — after state-of-union verification)
from-session: 50de4461-2c6c-414b-8aa0-86339f0be672 → continuation session
audience: Claude in VS Code, cold start
read-order: STATE_OF_UNION_2026-05-07.md → PLAN_10_DAY_2026-05-07.md → this file
---

# Paste this entire file (or open it as context) at the start of a new conversation

## Who I am and what I'm doing

I'm todd.cx@turtleisland.solutions / todd@gigaton.ai. I'm executing a 10-day plan to put a process foundation, daily deployment automation, and knowledge distribution layer around ~18 active GitHub repos. The plan lives at `/Users/admin/Documents/GitHub/master-knowledge-base/PLAN_10_DAY_2026-05-07.md` — read it first.

## Locked decisions (do not re-ask)

1. **GCP owner of record:** `todd@gigaton.ai`. `todd.cx@turtleisland.solutions` is IAM Viewer only.
2. **Domain strategy:** per-service custom domains (`api/app/decide/sales/sie/docs.gigaton.ai`, plus `carmenbeach.com` + `admin.carmenbeach.com`).
3. **Docs site:** Cloud Run + mkdocs-material container. Same deploy pipeline as everything else.
4. **Daily deploy:** **manual trigger at or by 19:00 CT.** Must complete green before any other work proceeds the next day. No cron. Past 20:00 CT = skip, deploy in the morning.
5. **CODEOWNERS:** `@todd-gig` + `@bella-byte` (bella@gigaton.ai) on every production repo. New repos auto-provision CODEOWNERS via `scripts/init-repo.sh`.

## What's already done (Day 0)

Files in `/Users/admin/Documents/GitHub/master-knowledge-base/`:

- `PLAN_10_DAY_2026-05-07.md` — full 10-day plan with locked decisions section.
- `SERVICES.md` — scaffolded registry. Cells marked `_fill_` need gcloud query output.
- `PROCESS.md` — branching, PR rules, 19:00 CT deploy ritual, rollback, incident response.
- `PRINCIPLES.md` — 10 non-negotiables.
- `CODEOWNERS.template` — defaults for all repos.
- `scripts/init-repo.sh` — provisions governance files on any repo.
- `scripts/install-codeowners.sh` — backfills CODEOWNERS to 9 production repos. Dry-run by default; pass `--apply` to write. Leaves changes unstaged for per-repo review.
- `scripts/deploy_19.sh` — manual deploy trigger skeleton. Pre-flight checks (clean tree, time-of-day, previous run green), then runs `make deploy` per service. Service `make deploy` targets are Day-3 work.

None of these are committed yet. The parent repo at `/Users/admin/Documents/GitHub` has the dirty sweep branch in play; commit per-file once the sweep-branch triage is done.

## P0 blockers (clear before Day 2)

1. **`gcloud auth login` (interactive).** Auth expired. Cannot enumerate Cloud Run live state until user re-logs.
2. **SIE rebase stuck.** `~/Documents/Claude/Projects/CxGuy-2.0/sovereign-influence-engine` has `interactive rebase in progress; onto fcb4b34`. Recommend `git rebase --abort`, then plan the merge as a normal PR. **SIE cannot deploy until clean.**
3. **Sweep branch at PARENT monorepo.** `~/Documents/GitHub/.git` is on `wip/sweep-2026-04-28-1619` with 12 dirty submodules + 5 untracked dirs (`Gigaton-UI-Platform`, `playa-del-carmen`, `admin-turtleisland`, `bella-byte`, `toddcx-turtleisland`). Per-submodule triage required.
4. **OAuth client_secret on Desktop.** `/Users/admin/Desktop/client_secret_372047156871-*.json` — move to Secret Manager + rotate.

## Confirmations (no longer questions)

- **Bella's GitHub username:** `bella-byte` (confirmed via merge commit on Gigaton-UI-Platform).
- **GH CLI auth:** `todd-gig` active.
- **gcloud account configured:** `todd@gigaton.ai` (token just expired).

## Repo map — CORRECTED (read STATE_OF_UNION for full reconciliation)

**SHIPPED on Cloud Run:** `Carmen-Beach-Properties` (web+admin, plus Cloud SQL + staging/prod CI/CD merged 2026-05-07), `gigaton-engine`, `gigaton`, `gigaton-ui-system` (npm), `decision-engine`, `sales-operating-system`. SIE operator-api gateway live (`/sie-pending`, `/sie-decide`, `/sie-audit` skills work).

**ACTIVE — was wrongly flagged deprecated:** `Gigaton-UI-Platform` is the **most active repo** (337 commits/60d, commit today, has its own CI workflows including a daily janitor for sweep branches). It's untracked at the parent monorepo level and lives next to it. **Do NOT delete — this is the live multi-tenant product surface.**

**In progress:** `intelligence-silo` (NOT its own git — tracked subdir of parent monorepo; cloudbuild ready, env not wired), `transcript-knowledge-base` (4h cron live, 70 commits/60d), `braintrust-knowledge-base`, `playa-del-carmen`.

**Stale / archive candidates:** `gigaton-ui-platform` (lowercase, the OLD one — distinct from `Gigaton-UI-Platform`), `liquifex` (research), 5 stale POC repos.

## SIE local clone — IMPORTANT

Lives at `/Users/admin/Documents/Claude/Projects/CxGuy-2.0/sovereign-influence-engine` — NOT in `~/Documents/GitHub/`. 11 services, 951 tests passing per Phase A+B+C commit. Currently mid-rebase. The L1–L4 architecture is documented at `/Users/admin/Documents/Claude/Projects/CxGuy-2.0/SIE_Operational_State_And_Completion_Plan_2026-04-22.md`.

## How to proceed in a fresh conversation

Open VS Code in `/Users/admin/Documents/GitHub`. Start a new Claude Code conversation. Paste the prompt below to bootstrap, or open this file as context.

### Bootstrap prompt to paste:

> Continue the 10-day execution plan documented in `master-knowledge-base/PLAN_10_DAY_2026-05-07.md`. Read `master-knowledge-base/HANDOFF.md` first for current state and locked decisions. Day 1 scaffolds are written but not committed and the gcloud-output cells in `SERVICES.md` are unfilled. The two blockers before Day 2 are: (1) confirm Bella's GitHub username, (2) sweep-branch triage of `wip/sweep-2026-04-28-1619`. Pick up from there.

## Day-1 commands the user still needs to run

```bash
# 1. Auth + inventory (paste output back to Claude to fill SERVICES.md)
gcloud config set account todd@gigaton.ai
gcloud run services list --platform=managed \
  --format="table(metadata.name,status.url,status.latestReadyRevisionName,metadata.labels.commit-sha)"
gcloud run domain-mappings list --region=us-central1
gcloud secrets list

# 2. Dry-run CODEOWNERS backfill, review, then apply
cd /Users/admin/Documents/GitHub
./master-knowledge-base/scripts/install-codeowners.sh
./master-knowledge-base/scripts/install-codeowners.sh --apply

# 3. Sanity-check the deploy preflight (won't deploy; just runs the gates)
./master-knowledge-base/scripts/deploy_19.sh --check
```

## Day-by-day (next steps)

- **Day 1 (Thu 5/8):** sweep-branch triage; fill `SERVICES.md` from gcloud; commit governance files.
- **Day 2 (Fri 5/9):** roll out CODEOWNERS, branch protection on `main`, shared deploy workflow.
- **Day 3 (Sat 5/10):** standardize `make deploy` across backends; wire intelligence-silo env/secrets/volume.
- **Day 4 (Sun 5/11):** standardize `make deploy` across frontends; finish `deploy_19.sh` to <15 min full-stack.
- **Day 5 (Mon 5/12):** SIE ↔ decision-engine ↔ silo end-to-end with certificate chain visible in `/sie-audit`.
- **Day 6 (Tue 5/13):** memory unification; TI Memory v3 folded into governance spine.
- **Day 7 (Wed 5/14):** onboarding bundle + role guides + `START_HERE.md`.
- **Day 8 (Thu 5/15):** docs.gigaton.ai live on Cloud Run.
- **Day 9 (Fri 5/16):** `POLICY.md` enforced as YAML in decision-engine 7-gate.
- **Day 10 (Sat 5/17):** archive stale repos, full audit, retro.

## Tools the new Claude will need

Default Claude Code tools cover most of this. Confirm these are available in the new session:

- **Bash, Read, Write, Edit, Grep, Glob** — core file ops.
- **TodoWrite** — task tracking.
- **`gh` CLI** via Bash — GitHub PR/branch protection ops.
- **`gcloud` CLI** via Bash — Cloud Run inspection (user has already auth'd).
- The SIE skills (`/sie-pending`, `/sie-decide`, `/sie-audit`) for Day 5+.

If skills/tools are missing, search via ToolSearch with `select:<name>` or keyword queries.

## Memory references

The user's auto-memory at `/Users/admin/.claude/projects/-Users-admin-Documents-GitHub/memory/MEMORY.md` already contains:
- `project_transcript_kb.md` — transcript ingestion pipeline.
- `feedback_never_lose_knowledge.md` — confirm durable backup before deleting anything.
- `project_intelligence_silo.md` — Society of Minds architecture context.

Read those if the new conversation needs deeper background on a specific repo.

## What NOT to do

- Don't touch the sweep branch's dirty submodules without explicit per-submodule confirmation.
- Don't re-ask the 5 locked decisions above.
- Don't commit anything to `main` without a PR (CODEOWNERS rule once installed).
- Don't deploy outside the 19:00 CT window without the user explicitly overriding.
- Don't fold Desktop bundles into repos without confirming the destination repo with the user — there are duplicate-named bundles and the right destination isn't always obvious.
