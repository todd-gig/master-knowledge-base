---
title: State of Union — Verified Ground Truth Snapshot
created: 2026-05-07
window-analyzed: code stack 60d (since 2026-03-08), Desktop/Downloads 20d (since 2026-04-17)
supersedes: claims in active_work_registry.md (2026-05-06) and HANDOFF.md (2026-05-07 morning)
purpose: single source of truth before executing the 10-day revenue plan
---

# Verified production state

## Live on Cloud Run (project `carmen-beach-properties`, region `us-central1`)

> **Note:** Live URLs and revisions could not be re-verified this session — `gcloud` auth expired (needs `gcloud auth login` from user). All claims below are from repo state + commit history, not from a live API call.

| Repo | Service(s) | Last shipped | Status (from repo) |
|---|---|---|---|
| `Carmen-Beach-Properties` | carmen-web, carmen-admin | 2026-05-07 (PR #4: Prisma + Cloud SQL + staging/prod pipeline merged today) | SHIPPED with staging+prod GH Actions wired |
| `decision-engine` | FastAPI 9-stage pipeline | 2026-05-05 (master architecture doc) | SHIPPED, cloudbuild.yaml live |
| `sales-operating-system` | FastAPI catalog + agent runtime | 2026-05-05 (Cloud Run hardening) | SHIPPED, 63 tests, `/health` live |
| `gigaton-engine` | Pricing/margin + DAG | 2026-04-07 (healthcheck added) | SHIPPED, cloudbuild.yaml live |
| `gigaton-ui-system` | React component lib (npm) | 2026-04-07 | SHIPPED to npm |
| `gigaton` | Operator dashboard | 2026-04-07 | SHIPPED |
| **`Gigaton-UI-Platform`** | Multi-tenant onboarding + chat | **2026-05-07 (commit "auth", same day)** | **ACTIVE — 337 commits in 60 days. Registry was wrong: this is NOT deprecated.** |
| `transcript-knowledge-base` | 4h cron ingestion | 2026-04-11 | LIVE — 70 commits in 60d, GitHub Actions cron active |

## SIE (sovereign-influence-engine) — operator-api gateway live

- **Local clone path:** `/Users/admin/Documents/Claude/Projects/CxGuy-2.0/sovereign-influence-engine` (NOT in `~/Documents/GitHub/`)
- **Latest commits**: G2.7 chunk-based connector work (PR #34 = decision_logic_pack absorption merged), all on `master` (NOT `main`)
- **11 services** per Phase A+B+C commit (8535006): operator-api, action-orchestrator-service, decision-engine-service, memory-service, entity-resolution-service, ontology-service, symbol-engine-service, calibration-service, feedback-service, interface-service, feed-ingestion-service. **951 tests passing per commit msg.**
- **Operational status doc**: `/Users/admin/Documents/Claude/Projects/CxGuy-2.0/SIE_Operational_State_And_Completion_Plan_2026-04-22.md` (35KB) — L1–L4 architecture canonical reference. **L1 LIVE. L2 partial. L3 LIVE but missing 7-gate, bias detection, exception engine, gap analysis. L4 STUBBED — schedule_meeting/send_message/update_entity return stub responses.**
- **Existing automation**: `daily_deploy.sh` + `~/Library/LaunchAgents/ai.gigaton.sie-deploy.plist` already exist. Day-4 work in old plan was duplicating this.

# Verified in-progress state

| Repo / artifact | Reality |
|---|---|
| `intelligence-silo` | Last commit 2026-04-09. Has cloudbuild.yaml + Dockerfile but env/secrets/volume not wired. **Lives inside parent monorepo**, not its own `.git`. |
| `master-knowledge-base` | Last commit 2026-04-09 (a junk `.DS_Store` sync). 7 uncommitted Day-0 governance files from morning session. CLAUDE.md modified. |
| `MD Files` | 2026-05-07 on branch `chore/intelligence-engine-superseded` — intelligence-engine code now absorbed into `decision-engine`. |
| `Carmen-Beach-Properties` Phase 2 | Sprints 1-8 merged via PR #3 (2026-05-05). Phase 3 partially done — Cloud SQL + staging/prod pipeline merged today. **Registry claim "Phase 3 NOT STARTED" is wrong.** |
| Sweep branch `wip/sweep-2026-04-28-1619` | At PARENT monorepo `/Users/admin/Documents/GitHub/.git`. 12 dirty submodules. Plus 5 untracked dirs: `Gigaton-UI-Platform/`, `playa-del-carmen/`, `admin-turtleisland/`, `bella-byte/`, `toddcx-turtleisland/`. |

# Critical blockers (P0 — must clear before/during Day 1)

1. **SIE is in a stuck interactive rebase.** `git status` reports `interactive rebase in progress; onto fcb4b34`. Phase A+B+C (commit 8535006) is the patch being rebased. Files in conflict: `infra/gcp/cloud_run.tf`, `infra/gcp/database.tf`, `infra/docker/docker-compose.yml`, `services/decision-engine-service/...`. **Either resolve and continue or abort. SIE cannot deploy until clean.** Recommend: `cd ~/Documents/Claude/Projects/CxGuy-2.0/sovereign-influence-engine && git rebase --abort` to recover the original work, then plan the merge as a non-rebase PR.

2. **`gcloud` auth expired.** Cannot enumerate Cloud Run / Secret Manager / Cloud SQL state without re-login. **User must run** `gcloud auth login` (interactive) before Day-1 inventory completes.

3. **Parent monorepo on sweep branch** with 12 dirty submodules + 5 untracked dirs. `Gigaton-UI-Platform` (the most active product surface) is untracked at parent level. Decide per-submodule: land, branch off, or revert. **No further submodule changes until this is settled.**

4. **Sensitive credential file on Desktop.** `/Users/admin/Desktop/client_secret_372047156871-*.json` is a Google OAuth client secret sitting in plaintext on Desktop. Move to `gcloud secrets create` or local keychain immediately; rotate if exposed.

# Reconciled errors in prior registry / handoff

| Prior claim | Reality | Source |
|---|---|---|
| `Gigaton-UI-Platform` is **archived/deprecated** (registry, HANDOFF) | **Most active repo: 337 commits in 60 days, commit today, has CI workflows including `daily janitor for wip/sweep`, Firebase deploys, Bella's fork active.** This is the live multi-tenant product surface. | `git log Gigaton-UI-Platform` |
| Sweep branch is at master-knowledge-base parent (HANDOFF) | Sweep branch is at `/Users/admin/Documents/GitHub/.git` (parent of all repos). master-knowledge-base is a clean submodule. | `git -C intelligence-silo status` |
| `~/Documents/GitHub/intelligence-silo` is its own git repo | **It is NOT.** It's a tracked subdirectory of the parent monorepo. Same for `admin-turtleisland`, `bella-byte`, `toddcx-turtleisland`. | `ls -la intelligence-silo/.git` returns nonexistent |
| Carmen Beach Phase 3 NOT STARTED (registry) | Phase 3 partially done: Cloud SQL + staging/prod pipeline + Prisma migrations merged 2026-05-07 in PR #4. | Carmen Beach `git log` |
| Carmen Beach on branch `add-chatgpt-snippets-carmen` (registry) | Currently on `main`. PR #3 (sprints 1-8) and PR #4 (migration pipeline) both merged. | Carmen Beach `git status` |
| Bella's GitHub username unknown (HANDOFF blocker #1) | **Confirmed `bella-byte`** (visible in merge commit "Merge branch 'main' of https://github.com/bella-byte/Gigaton-UI-Platform"). | Gigaton-UI-Platform `git log` |
| Sales OS bridge to Gigaton Engine confirmed wired (registry) | Bridge code exists; runtime integration not verified live. | Repo state only |

# Desktop / Downloads inventory (20-day window)

## Bundles already on the radar (in old plan)
- `claude_brand_interaction_system`, `claude_decision_logic_pack` (already its own repo), `claude_gigaton_standalone_project`, `claude_sovereign_influence_md_package`, `gigaton_enterprise_onboarding_v2`, `gigaton_sie_first_production_bundle_v1`, `TI_Memory_Network_Claude_Bundle_v3` (also in Downloads)

## Bundles missed by old plan (revenue-relevant)
- **`fiduciary-risk-audit-deck.pptx` + email-sequence.html + landing-page.html + one-pager.pdf** (in CxGuy-2.0/) — outbound campaign assets ready to fire. Targets fiduciaries (LiquiFex's domain) with SIE proof points.
- **`gignet_usage_billing_dashboard_claude_bundle`** — billing control surface bundle. **README states: "Every GigNet user must have a Dashboard page that is the user's actual usage + billing control surface."** This is the monetization plumbing — entitlements, invoices, usage cards, upgrade actions. **Not in old plan. Revenue-critical.**
- `Qwen2.5-7B-Instruct-Q4_K_M.gguf` (4GB+ in Downloads) — local SLM for intelligence-silo Society of Minds.
- `Sovereign_Influence_Engine.pdf` + `Architecting_Agency__The_Sovereign_Influence_Engine.mp4` — SIE narrative assets.
- `gigaton_v3_execution`, `claude_v3_part1`, `claude_v3_part2` — v3 execution bundle (governance + config).
- `claude_acquisition_prospect_memory_bundle_v1` — prospect memory for the SIE/SalesOS pipeline.

## Desktop dirs that ARE git repos (orphan clones)
- `/Users/admin/Desktop/gigaton-platform-ui` — appears to be a UI clone outside `~/Documents/GitHub`. Investigate.
- `/Users/admin/Desktop/gigaton_repo_audit/` contains clones of `Gigaton-UI-Platform` and `Liquefex-fluidity-presentations` — looks like an audit working copy.

# Revenue paths identified (new — not in old plan)

| Path | Time-to-cash | Status | What's missing |
|---|---|---|---|
| **Carmen Beach property bookings** | 0–3 days once domains live | Code is shipped Phase 2; infra is shipped today | Custom domain (`playadelcarmen.homes`), live property data seed, payment processor go-live |
| **SIE Fiduciary Risk Audit campaign** | 1–7 days | Deck + landing + email + one-pager all written 2026-04-22 | Landing-page hosting, email list, SIE rebase fix to demo |
| **Sales OS internal-then-external** | 7–14 days | Cloud Run live, 214-item catalog, 63 tests | Pricing layer (entitlements + Stripe), customer #1 commitment |
| **Gigaton-UI-Platform billing dashboard** | 5–10 days | Bundle exists, target repo is most active | Implementation in `Gigaton-UI-Platform`, entitlements schema, Stripe webhooks |
| **Carmen Beach affiliate tier program** | 3–5 days | 3-tier ladder coded (`feat/sprints-additive-2026-05-06`) | First 3-5 affiliates onboarded, payout test |
| **Ti Solutions internal SalesOS** | already revenue | Active dialer + ClickUp + HubSpot stack | SalesOS bridge wired into Ti's deal flow (existing revenue, not net-new) |

# Decisions still pending from user

1. **Which revenue path is Day 1 priority?** Recommend dual-track: (A) Carmen Beach domain go-live + first booking, (B) Fiduciary audit campaign launch (lowest infra burden — landing page on Vercel, email via existing Gmail).
2. **SIE rebase: continue or abort?** Recommend abort + plan the merge as a normal PR; the rebase is touching 40+ files and is fragile.
3. **Sweep-branch triage cadence:** all-at-once on Day 1, or roll into Day 2 process work? Recommend all-at-once Day 1 — every dirty submodule blocks the deploy ritual.
4. **Stripe / payment processor account:** owned by which entity (Gigaton, Carmen Beach LLC, Ti Solutions)? Determines accounting + 1099/W-9 chain for affiliates.
5. **Should `Gigaton-UI-Platform` move into `~/Documents/GitHub/` parent monorepo as a tracked subdir, or stay separate?** It's currently untracked at parent. Recommend: keep separate since it has its own active CI and Bella's collab; just remove from "untracked" noise by adding to parent `.gitignore`.
