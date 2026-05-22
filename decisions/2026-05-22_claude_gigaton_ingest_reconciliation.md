---
adr_id: 2026-05-22-claude_gigaton_ingest_reconciliation
title: Reconcile claude_gigaton_ingest package (v2.0.0) against live production reality
status: ACCEPTED
date: 2026-05-22
accepted_at: 2026-05-22
accepted_by: todd@gigaton.ai
authors:
  - Claude (architecture intelligence pass)
reviewers:
  - todd@gigaton.ai
serves: foundational_goal_gigaton_engineered_brand_experience
supersedes: none
superseded_by: none
related:
  - "[[master_project_plan]]"
  - "[[repo_registry]]"
  - "docs/architecture/CODEBASE_MAP.md"
---

> **ACCEPTED 2026-05-22 by todd@gigaton.ai.** All six binary approval gates (treat-as-kickoff-brief, keep Penrose, keep PPIM schema, keep UAE routing, commit, archive) confirmed. Gate #5 (pick next §4 gap) deferred to a follow-up conversation.


# ADR — Reconcile `claude_gigaton_ingest` v2.0.0 against live production reality

## Context

User dropped `~/Downloads/claude_gigaton_ingest/` (manifest v2.0.0, package "claude_gigaton_standalone_project_v2") into the session and instructed:

> "Before making any code changes, perform a full architecture intelligence pass. … If existing code conflicts with project knowledge, stop and report the conflict before changing code. Do not create duplicate services, schemas, routes, dashboards, auth logic, billing logic, or agent systems."

The package contains:
- 2 prompts (system + startup) telling Claude to behave as a "standalone execution brain".
- 3 context briefs (Gigaton overview, April-9 meeting summary, memory registry summary).
- 1 architecture sketch (6 layers).
- 4 PRDs (Decision Engine, Brand Engine, Client Namespace System, Platform UI).
- 4 JSON schemas (client_namespace, decision_record, asset_metadata, task).
- 3 playbooks (access, deployment, repo-read-first).
- 1 master backlog (P0–P4) with weights JSON + execution state machine JSON.
- 2 governance docs (policy, source provenance).
- 2 repo-integration docs (instructions, expected structure).
- 1 dashboard scaffold (Control Plane UI spec).
- Source-grounding doc citing the April 9, 2026 meeting and Gigaton Company Summary.

The package's load-order README explicitly states: *"Claude must not assume the current codebase is blank. Before changing code, Claude must inspect the existing repo, identify current architecture, map constraints, then implement additive improvements that preserve working functionality."*

## Problem

The ingest package was authored against the **April 9, 2026 meeting state**. The codebase has since shipped enormous work:

- **9 platform engines LIVE** on Cloud Run (decision-engine, gigaton-engine, intelligence-silo, sales-OS, gigaton-gateway, UAE, HME, persona-engine, ppeme) plus mimi-whatsapp + connector-api + 2 Cloud Functions.
- **Penrose 8-metric falsification scoreboard LIVE** in decision-engine.
- **Doctrine layer codified** — Constitution v1.0.0 RATIFIED 2026-05-21; 7 non-neg + 15 principles + 8 ethos + 19 frameworks + 23 axioms + nightly Drift Sentinel sweep.
- **Gignet orchestrator fabric LIVE** — Phases A–G all shipped 2026-05-20.
- **Operator Onboarding v1 chat-first 10-stage workflow LIVE** — `/wizard` deprecated → `/chat?onboarding=*`.
- **Stage-8 credential collection LIVE** 2026-05-22 — 15 provider probes + Pattern A storage.
- **38 PRs merged across 2-day sprint 2026-05-20→21**; another 13-PR sprint in flight 2026-05-22.
- **10 of 10 net-new concepts** from the Apr-9 Standalone Bundle ALL LANDED on main 2026-05-20 — including Client Namespace System, Decision Execution Engine, First Principles Variable Registry, EO System, Memory Lifecycle State Machine, Axiom Registry, Portable System Prompt Contract.

The ingest package's P0–P3 backlog asks for ~80% of the above to be built. Treating the package as a literal execution brief would produce duplicate systems, replace richer production schemas with thinner ones, and replace the Penrose scoreboard with a weighted-sum scalar.

## Conflicts surfaced

### C1 — Decision scoring formula (HIGH)
- Package: `priority_score = 0.30·roi + 0.20·speed + 0.20·reuse + 0.15·dep_unblock + 0.15·risk_adj_confidence`.
- Production: Penrose 8-metric falsification scoreboard + Trust×Value×Authority matrix + Axiom Registry.
- These are not interchangeable. Penrose answers "which decisions are now falsified by outcomes?"; the package formula answers "which action has the best static ROI score?".
- **Risk if naively applied:** erase ~6 months of doctrine work.

### C2 — Decision record schema (HIGH)
- Package: 8 fields.
- Production: PPIM signature + multi-axis JSONB tags + execution provenance + Penrose hooks + axiom violations + sign-off matrix routing.
- The package schema is a strict subset; migrating to it is a regression.

### C3 — Approval thresholds (MEDIUM)
- Package: single scalar `auto_execute_max_risk: 0.25` + blocking categories.
- Production: UAE sign-off matrix routes by *category × persona* with AX-010 enforcement; not a scalar.

### C4 — "Build Google sign-in / messenger UI / approvals queue / task generation / namespace generator" (HIGH)
- All of these are LIVE in production.
- Following the P0–P3 literally would create parallel systems.

### C5 — "Access fragmentation is the #1 blocker" (LOW)
- Was true on April 9. Now ~90% resolved: gh CLI authenticated, Drive OAuth LIVE, gcloud canonical account standing, entity + repo registries exist.
- Remaining: GoDaddy DNS for `api.gigaton.ai`, OpenAI key paste, settings.json hook wiring.

### C6 — Expected repo structure (LOW)
- Package proposes a single monorepo `/apps + /packages + /docs + …`.
- Production is polyrepo (9 engines = 9 repos).
- Package itself says "this is a target, not a mandate." No real conflict.

## Decision

**Treat `claude_gigaton_ingest` v2.0.0 as a foundational kickoff brief, not an execution mandate.**

Specifically:

1. **Keep the package's *doctrinal* contributions** — they align with what's already canonical:
   - The governance policy authority hierarchy (foundational doctrine → user → repo → memory → package → inference) is consistent with [[master_project_plan]] §6. Adopt verbatim where missing.
   - The source-provenance confidence levels (0.95/0.85/0.70/0.50/<0.50) are useful and additive. Adopt.
   - The decision-record template fields *that don't already exist* (rationale prose, validation_plan list, options array) can be added as **optional auxiliary fields** to the production schema. Do not replace the canonical PPIM-signed schema.

2. **Reject the *re-implementation* asks** for systems that already exist (P0 #1–4, P1 #1–5, P2 #1–5, P3 #1–2, P3 #5, Control Plane UI 8 of 9 pages). For each, add a `superseded_by` pointer in the package and stop.

3. **Keep, but downgrade, the *scoring formula* (C1) and *risk threshold* (C3) asks** — they may be useful as auxiliary scalars feeding into the existing Penrose + UAE matrix. They are NOT replacements.

4. **Accept the genuinely missing items as the active gap list:**
   - Stripe / billing / payment processing (no production code yet).
   - Liquifax productization package (canonical TBD; broken-remote local clone).
   - Local tourism SMB package (not started).
   - Upwork package (not started).
   - Proposal generator (not started).
   - Production storage flip for Decision Execution Engine + EO System (Cloud SQL provisioned 2026-05-21; in-memory v0 still serves).
   - Cross-engine event-driven storage/retrieval (sprint 2026-05-22 in flight, 13 PRs across 5 repos — S1–S16).
   - mimi-whatsapp gateway aggregator registration (S4 gap).
   - GoDaddy DNS for `api.gigaton.ai`.
   - OPENAI_API_KEY mount (operator paste pending).
   - 8 registry-drift items logged in [[master_project_plan]] §3.6.

5. **File this ADR + `docs/architecture/CODEBASE_MAP.md` as the audit artifacts.** Update `MEMORY.md` index with a one-line pointer.

## Consequences

- **Positive.** No duplicate auth/billing/agent/dashboard/schema systems get built. The Penrose scoreboard and PPIM-signed decision schema survive. The 10 net-new concepts already merged on 2026-05-20 stay canonical. The 38-PR sprint of 2026-05-20→21 is not undone.
- **Negative.** The ingest package is partly stale; future onboarding of new contributors via the package may mislead them. Mitigation: place a `SUPERSEDED_BY_CODEBASE_MAP.md` stub at the package root + commit the package into `master-knowledge-base/archive/` so it is preserved but flagged.
- **Neutral.** The package's governance + provenance contributions get adopted. Net-additive.

## Implementation plan (file-level)

> **No code is changed by this ADR.** All changes here are documentation. Code changes (genuine gaps in §4 of this ADR) are separate ADRs / PRs / runbooks.

**Files created in this audit (already on disk, not yet committed):**

1. `/Users/admin/Documents/GitHub/master-knowledge-base/docs/architecture/CODEBASE_MAP.md` — the canonical codebase map.
2. `/Users/admin/Documents/GitHub/master-knowledge-base/decisions/2026-05-22_claude_gigaton_ingest_reconciliation.md` — this ADR.

**Files proposed (NOT created yet — awaiting user approval):**

3. `~/.claude/projects/-Users-admin/memory/ingest_package_v2_reconciliation_2026_05_22.md` — memory pointer + one-line MEMORY.md index entry.
4. `~/Downloads/claude_gigaton_ingest/SUPERSEDED_BY_CODEBASE_MAP.md` — stub at package root pointing readers to CODEBASE_MAP.md + this ADR.
5. `master-knowledge-base/archive/claude_gigaton_ingest_v2_2026-04-09/` — archived copy of the package (preserved, not deleted).
6. Per-package-PRD redirect stubs (4 files) added inline to the package, each citing the production engine that supersedes it.

**No engine code, schema migration, route, or auth change is proposed by this ADR.**

## Approval gates

- [ ] User confirms "treat ingest package as kickoff brief, not execution mandate" (this decision).
- [ ] User confirms keeping Penrose scoreboard as canonical decision-scoring (C1).
- [ ] User confirms keeping PPIM-signed decision schema (C2).
- [ ] User confirms keeping UAE category-based approval routing (C3).
- [ ] User confirms which of the §4 genuine gaps to prioritize next (Stripe? Local SMB? Liquifax canonical? storage flip?).
- [ ] User approves committing CODEBASE_MAP.md + this ADR to `master-knowledge-base`.
- [ ] User approves archiving the package into `master-knowledge-base/archive/`.

## Rollback

This ADR is documentation. If rejected, delete the two created files; no production state changes.
