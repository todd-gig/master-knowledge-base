---
name: gigaton-codebase-map
description: Canonical map of every repo, engine, route, schema, auth boundary, integration, and deployment surface in the Gigaton ecosystem. Produced from a full architecture intelligence pass on 2026-05-22.
type: reference
established: 2026-05-22
status: active
sources:
  - "[[repo_registry]]"
  - "[[master_project_plan]]"
  - "[[entity_ecosystem_registry]]"
  - "[[active_work_registry]]"
  - "Cloud Run audit 2026-05-21"
  - "claude_gigaton_ingest package (Downloads, 2026-04-09 vintage)"
---

# Gigaton Codebase Map

> **Purpose.** Single read-first artifact for any agent or human about to touch the codebase. Pairs with [[repo_registry]] (where things live on disk) and [[master_project_plan]] (why they exist). This file answers: *what currently exists, what is partial, what is missing, and what would duplicate if naively rebuilt.*
>
> **Last verified.** 2026-05-22 against Cloud Run + GitHub + on-disk repo state.

---

## 1. Ecosystem at a glance

- **9 platform engines** LIVE on Cloud Run across 2 GCP projects (`gigaton-platform`, `carmen-beach-properties`).
- **2 frontends** LIVE (`gigaton-ui-system` on Firebase Hosting; `Carmen-Beach-Properties` root on App Hosting).
- **2 net-new services** active (`mimi-whatsapp`, `connector-api`) — both in `carmen-beach-properties` GCP project.
- **2 auxiliary Cloud Functions** active (`gignet-activity-emitter`, `orchestrator-trigger-fan-out`).
- **8 Cloud SQL instances** RUNNABLE across both projects.
- **38 PRs** merged across 2-day sprint 2026-05-20→21. Sprint 2026-05-22 in flight (13 PRs across 5 repos for storage/retrieval path-to-100%).

---

## 2. Layer-by-layer map

### 2.1 Identity + Access (UAE)

| Concern | Implementation | Location | Status |
|---|---|---|---|
| Google OAuth | gigaton-ui-system gated to `@gigaton.ai` for privileged routes | `gigaton-ui-system/src/auth/*`, `/oauth/callback` | LIVE |
| RBAC + roles | user-access-engine (UAE) `00024-vcp` | `user-access-engine/app/auth/`, `user-access-engine/migrations/` | LIVE |
| Capabilities catalog | UAE `/v1/capabilities` | UAE | LIVE — `UAE_REQUIRE_CAPABILITIES=true` strict flip DEFERRED to wk 2026-05-25 |
| Sign-off matrix | UAE `/v1/signoff` + FE `/founder/signoff` | UAE + gigaton-ui-system | LIVE — AX-010 enforcement DEFERRED |
| Client namespaces (multi-tenant boundary) | UAE owns `client_namespaces` table per Decision A.1 | UAE migration pending | SEEDED — 4 canonical namespaces 2026-05-21 |
| Admin gate | POST `/v1/namespaces` requires `uae-admin-token` | UAE PR #34 MERGED | LIVE soft-gate |

### 2.2 Data + Memory

| Concern | Implementation | Location | Status |
|---|---|---|---|
| Google Drive ingest | intelligence-silo OAuth multi-account + `documentation_bundles` | `intelligence-silo/app/drive/`, `intelligence-silo/migrations/` | v0 LIVE; v1 multi-source ingest spec [[documentation_ingest_feature_spec]] |
| Memory store (per-user) | Firestore `users/{uid}/activity` + `users/{uid}/memory/*` | `gigaton-platform` Firestore | LIVE |
| Memory store (canonical) | `/Users/admin/.claude/projects/-Users-admin/memory/` — 244 files Lifecycle-tagged | local + `master-knowledge-base` mirror | LIVE — Memory Lifecycle State Machine LIVE |
| Source Registry | intelligence-silo `/v1/sources` + provenance | `intelligence-silo/app/sources/` | LIVE |
| Knowledge bases (markdown) | master-knowledge-base + braintrust-knowledge-base + transcript-knowledge-base + MD Files | `/Users/admin/Documents/GitHub/*` | LIVE |
| NotebookLM canonical folder | `/Users/admin/Documents/Gigaton-NotebookLLM/` — 29 .md in 9 subfolders | local | LIVE — see [[gigaton_notebookllm_canonical_folder]] |
| Variable registry (50 seed vars) | persona-engine `/v1/variables` | persona-engine Postgres | LIVE |

### 2.3 Intelligence

| Concern | Implementation | Location | Status |
|---|---|---|---|
| Decision engine | decision-engine `00034-t2s` | `decision-engine/engine/` | LIVE |
| Penrose 8-metric falsification scoreboard | decision-engine `/v1/penrose/scoreboard` | `decision-engine/engine/penrose/` | LIVE — 8/8 metrics responsive (decision_velocity null pending real execute() flow) |
| Decision Execution Engine | decision-engine `/v1/decisions/.../executions` | decision-engine | LIVE (in-memory v0; Cloud SQL approved per A.3 — provisioned 2026-05-21) |
| Doctrine + Trust/Value/Authority matrix | decision-engine `drift_sentinel/GIGATON_CANONICAL_FIRST_PRINCIPLES.md` + `axioms.yaml` (23 axioms) | decision-engine | LIVE — Constitution v1.0.0 RATIFIED |
| Drift Sentinel | recursive scanner walking codebase + GitHub + Drive + ClickUp + Downloads | decision-engine | LIVE — nightly Cloud Scheduler `sweep-executions-daily` (verified fired 2026-05-21T09:00Z) |
| Society of Minds / EO System | intelligence-silo `/v1/eo` | intelligence-silo | LIVE (in-memory v0; Cloud SQL provisioned 2026-05-21) |
| LLM router (multi-model) | gigaton-gateway `app/llm_router/` + POST `/v1/llm/call` | gigaton-gateway `00036-vxh` (incl ade445f) | LIVE — Anthropic + Gemini via Vertex AI work; OPENAI_API_KEY mount NOT live (operator paste pending) |
| BFT Master Calculator (Framework 5.19) | ppeme `00015-zz7` | ppeme | LIVE |
| Experience Engineering Equation | ppeme `engine/experience_engineering/` | ppeme | LIVE |
| Codification proposals | decision-engine + intelligence-silo | `/founder/proposals` + `/owner/proposals` | LIVE |
| Calibration (Framework 5.7 Learning Loop) | decision-engine `engine/ovs_calibration/` | decision-engine | LIVE — nightly variance recompute 2026-05-15 |

### 2.4 Execution + Orchestration

| Concern | Implementation | Location | Status |
|---|---|---|---|
| Task registry | Firestore `task_registry` (collection) | `gigaton-platform` Firestore | LIVE |
| Gignet orchestrator topic | Pub/Sub `projects/gigaton-platform/topics/gignet-orchestrator` + 2 subs | `gigaton-platform` | LIVE — Phase A |
| Trigger fan-out | Cloud Function `orchestrator-trigger-fan-out` `00002-guy` | `gigaton-platform` | LIVE — Phase B |
| External-source adapters (4) | `/webhooks/github`, `/webhooks/cloudbuild`, `/webhooks/twilio` on gateway + `gignet-activity-emitter` CF `00003-cav` | gigaton-gateway + CF | LIVE — Phase C |
| LLM router + telemetry | gateway `app/llm_router/`; Firestore `llm_call_cost` | gigaton-gateway | LIVE — Phase D |
| gignet-local-node (MCP peer) | v0.3.0 on main — Pub/Sub subscriber + heartbeat + FastAPI `localhost:7878` dashboard | `/Users/admin/Documents/GitHub/gignet-local-node` | LIVE — Phase E (hook wiring in settings.json PENDING) |
| Drift axioms AX-021/022/023 | decision-engine PR #62 MERGED | decision-engine | LIVE — Phase F |
| Monitoring dashboard + alerts | Cloud Monitoring "Gignet Orchestrator Fabric" + 3 alert policies → todd@gigaton.ai | `gigaton-platform` | LIVE — Phase G |
| Approval queue | UAE `/v1/signoff` + HME owner endpoints + FE `/founder/signoff`, `/owner/proposals` | UAE + HME + gigaton-ui-system | LIVE |

### 2.5 Productization layer

| Concern | Implementation | Location | Status |
|---|---|---|---|
| Brand engine | brand-knowledge-library + decision-engine brand_voice category | `master-knowledge-base/brand-knowledge-library/` + Variable Registry | PARTIAL — no dedicated engine; lives across SIE + variable registry |
| Interaction management (PPIM) | ppeme + HME Framework 5.18 Learning Loop | ppeme + HME | LIVE |
| Sovereign Influence Engine (SIE) | sovereign-influence-engine | `/Users/admin/Documents/Claude/Projects/CxGuy-2.0/` (`master` branch) | LIVE — Source Registry FE deployed |
| Proposal generator | NOT YET — gap | n/a | MISSING |
| Client onboarding generator | Operator Onboarding v1 chat-first 10-stage workflow | `master-knowledge-base/manifests/onboarding_v1.yaml` + gateway 3 endpoints + gigaton-ui-system `/chat?onboarding=*` | LIVE (shipped 2026-05-20) |
| Stage-8 credential collection | PR #41 gateway + gigaton-ui-system PR #33 + Carmen-Beach-Properties PR #35 — 15 first-class provider probes + Pattern A storage | gateway + ui-system + connector-api | LIVE 2026-05-22 |
| Billing / payment hooks | gateway budget cap only (no Stripe wiring yet) | gigaton-gateway | MISSING — net new |

### 2.6 Control plane UI (gigaton-ui-system)

React + Vite + TypeScript SPA at `https://gigaton-platform.web.app`. Routes:

| Persona | Route | Status |
|---|---|---|
| All | `/` (login), `/dashboard`, `/chat`, `/oauth/callback` | LIVE |
| All | `/wizard` → DEPRECATED → redirects to `/chat?onboarding=stage-0` | LIVE — deprecated 2026-05-20 |
| All | `/connectors` (10 cards) + `/connectors/whatsapp` + `/connectors/documentation` + `/connectors/github-pat` + `/connectors/airbnb-ical` + `/connectors/ga4` + `/onboarding/tech-stack?action=credentials` | LIVE for shipped connectors |
| All | `/sources` (Source Registry view) | LIVE |
| Founder | `/founder`, `/founder/doctrine`, `/founder/drift`, `/founder/proposals`, `/founder/signoff` | LIVE |
| Owner | `/owner`, `/owner/coverage`, `/owner/proposals`, `/owner/recruitment` | LIVE |
| Admin | `/admin` (Bella) | LIVE |
| Cross | `/calibration`, `/overrides`, `/platform`, `/brand-icon-lists`, `/brand-voice-dictionary` | LIVE |

### 2.7 Carmen Beach vertical (the first operator-specific deployment)

- Repo: `Carmen-Beach-Properties` (pnpm monorepo).
- Layout: `apps/web` (Next.js, hosts `/platform/*`), `apps/admin` collapsing into `apps/web` per Option C, `packages/{ai,auth,automation,leads,pricing,…}`, `services/whatsapp` (mimi-whatsapp), `apps/connector-api`.
- Live URL: `https://playadelcarmen.homes/` (root = basic real estate site; **do not overwrite**); `/platform` reserved for the Next.js Option C build.
- Status: **Phase 3 partial; Phase 4 BLOCKER per 2026-05-12 pre-flight.**

---

## 3. Inventory of completed vs partial vs missing vs duplicate-risk

### 3.1 COMPLETED (do not rebuild)

- Identity + Access (UAE + Google OAuth + RBAC + sign-off matrix + capabilities catalog).
- Decision Engine + Penrose 8-metric scoreboard + Decision Execution Engine.
- Doctrine layer (Constitution v1.0.0 RATIFIED, 7 non-neg + 15 principles + 8 ethos + 19 frameworks + 23 axioms + Drift Sentinel nightly sweep).
- 10 net-new concepts from the Apr-9 Standalone Bundle — ALL LANDED on main 2026-05-20.
- Gignet orchestrator fabric Phases A–G — ALL LIVE.
- Operator Onboarding v1 chat-first 10-stage workflow including Stage-8 credential collection.
- Multi-tenant boundary (client_namespaces, 4 canonical seeded; multi-axis JSONB tags on data).
- LLM router + cost telemetry + second-opinion gate + codification trigger.
- Drive OAuth + Source Registry + provenance.
- Calibration loop (nightly variance recompute).
- Control plane UI: dashboard, chat, approvals queue, decision records, client namespaces viewer (via `/platform`), access/connectivity status (via `/connectors`), settings.

### 3.2 PARTIAL (extend, do not duplicate)

- **Brand engine** — present across SIE + brand-knowledge-library + Variable Registry. No single dedicated "brand engine" service. Decision needed: consolidate vs leave distributed.
- **Carmen Beach productization** — phase 3 partial, phase 4 blocked.
- **`api.gigaton.ai` DNS** — NXDOMAIN; pending GoDaddy DNS + Cloud Run domain mapping.
- **OPENAI_API_KEY mount** — operator paste pending; Anthropic + Gemini work meanwhile.
- **mimi-whatsapp gateway aggregator registration** — service deployed `00005-t5k` but not in gateway `health_aggregator.py` yet (S4 gap).
- **GCP project drift** — 4 platform engines (decision-engine, gigaton-engine, intelligence-silo, sales-OS) misplaced in `carmen-beach-properties`; 3-phase migration plan logged in [[gcp_project_organization_target_2026]].
- **Registry drift** — 8 items logged in [[master_project_plan]] §3.6.

### 3.3 MISSING (genuine gaps; net-new builds)

- **Stripe / billing / payment processing** — only budget cap exists at gateway. No paying-customer flow.
- **Liquifax productization package** — repo present in `Liquefex` org but canonical TBD; broken-remote local clone is anomaly #3 in [[repo_registry]].
- **Local tourism SMB package** — not started.
- **Upwork package** — not started.
- **Proposal generator** — not started.
- **`gignet-orchestrator-fn` + `gignet-coordination`** — exist on GitHub but missing from `repo_registry.md` (drift item #1).
- **Production storage for Decision Execution Engine + EO System** — Cloud SQL provisioned 2026-05-21 but in-memory v0 still serves; migration not yet flipped.
- **Cross-engine event-driven storage/retrieval** — sprint 2026-05-22 in flight (13 PRs S1–S16).

### 3.4 DUPLICATE-RISK (DO NOT BUILD; the ingest package asks for these but they already exist)

| Ingest Package Ask | Already Exists As | Action |
|---|---|---|
| Google sign-in / user mgmt | UAE + gigaton-ui-system `/oauth/callback` | EXTEND existing — never create parallel auth |
| User/tenant model | UAE + `client_namespaces` (UAE-owned per Decision A.1) | EXTEND UAE migration |
| Central messenger UI + message persistence | gigaton-ui-system `/chat` + ChatOnboardingOrchestrator + HME event types | EXTEND existing |
| Approval queue | UAE sign-off + HME owner endpoints + FE `/founder/signoff` | EXTEND |
| Decision scoring service | decision-engine + Penrose scoreboard | **CONFLICT** — see §4.1 |
| Decision record schema | decision-engine (richer than ingest schema) | **CONFLICT** — see §4.2 |
| Approval gates | UAE + HME + AX-010 | EXTEND |
| Task generation | Firestore `task_registry` + Pub/Sub `gignet-orchestrator` | EXTEND |
| Human review workflow | Owner v0.5 HME endpoints + FE | EXTEND |
| Client intake schema | UAE-owned `client_namespaces` schema; 4 seeded | EXTEND |
| Namespace generator | A.1 v1 namespace flow proven end-to-end 2026-05-21 | EXTEND |
| Brand brief generator | SIE + brand-knowledge-library + Variable Registry | EXTEND OR CONSOLIDATE (decision needed) |
| Interaction guide generator | ppeme + HME Framework 5.18 + EEE | EXTEND |
| Asset metadata enforcement | intelligence-silo Source Registry + provenance + multi-axis JSONB tags | EXTEND |
| Control Plane UI pages (8/9) | gigaton-ui-system has them all except payment/billing | EXTEND |

### 3.5 CONTRADICTION-RISK (codebase conflicts with ingest package; require ADR)

See `decisions/2026-05-22_claude_gigaton_ingest_reconciliation.md` for the formal record.

---

## 4. Specific contradictions surfaced by the ingest package

### 4.1 Decision scoring formula

- **Ingest package** (`04_specs/PRD_DECISION_ENGINE.md` + `08_execution/decision_scoring_weights.json`):
  `priority_score = 0.30·roi + 0.20·speed + 0.20·reuse + 0.15·dep_unblock + 0.15·risk_adj_confidence` (0–100 scale, single scalar).
- **Production reality** (decision-engine `00034-t2s`): **Penrose 8-metric falsification scoreboard** + Trust×Value×Authority matrix + Axiom Registry + Decision Execution Engine. Not a single weighted-sum; a falsification regime.
- **They are not the same thing.** The ingest formula asks "what's the highest-ROI action?"; Penrose asks "which decisions are now falsified by outcomes?". Replacing one with the other would erase ~6 months of doctrine work.
- **Recommendation:** keep Penrose. The ingest formula can be *added* as a single auxiliary scalar inside the decision-engine if the user wants one — but it is not a substitute and must not replace the scoreboard.

### 4.2 Decision record schema

- **Ingest package** (`05_schemas/decision_record.schema.json`): 8 fields — `decision_id`, `objective`, `options`, `selected_option`, `score`, `approval_required`, `status`, `rationale`.
- **Production reality**: decision-engine carries PPIM signature (`ppim_interaction`, `ppim_economics`, `ppim_predictability`, `ppim_brand_dimension`), multi-axis JSONB tags (industry/sub-vertical/geo/regime/segment/lifecycle/provenance/modality), execution provenance, Penrose hooks, axiom violations, sign-off matrix routing.
- **Migrating to the ingest schema would regress every field above.** The ingest schema is a subset; treat it as such.

### 4.3 Approval thresholds

- **Ingest package**: `auto_execute_max_risk: 0.25`, `human_review_min_risk: 0.26`, blocking categories `auth/billing/payments/production_deploy/data_deletion/client_commitment`.
- **Production reality**: UAE sign-off matrix routes by *category × persona* (todd@/matt@/both), gated by AX-010, with HME owner-UI endpoints; not a single scalar threshold.
- **Recommendation:** keep UAE category-based routing. If the user wants a numeric risk gate added, treat it as a *secondary* signal feeding into the matrix.

### 4.4 Expected repo structure

- **Ingest package** (`10_repo_integration/EXPECTED_REPO_STRUCTURE.md`): single monorepo `/apps`, `/packages`, `/docs`, `/database/migrations`, `/scripts`.
- **Production reality**: polyrepo — 9 engines as separate Cloud Run services + separate GitHub repos; the package explicitly states "this is a target, not a mandate; adapt to the actual repo." No conflict if read carefully.

### 4.5 P0 (account/access inventory) blocker

- **Ingest package** treats access fragmentation as the #1 blocker.
- **Production reality**: gh CLI authenticated to `todd-gig`; Drive OAuth LIVE; gcloud canonical `todd@gigaton.ai`; entity registry + repo registry exist. **This blocker is already 90% resolved.** Remaining: GoDaddy DNS for `api.gigaton.ai`, OpenAI key paste, settings.json hook wiring.

---

## 5. Source authority hierarchy (when this map disagrees with another file)

Per [[master_project_plan]] §6 and [[governance_policy]] (ingest):

1. **Foundational doctrine** — `decision-engine/drift_sentinel/GIGATON_CANONICAL_FIRST_PRINCIPLES.md` + `axioms.yaml` + `CONSTITUTION.md`.
2. **User explicit instruction** — direct, in-conversation.
3. **Current repo reality** — `git log` + `gcloud run revisions list` + live `/v1/healthz`.
4. **Memory canonical files** — [[master_project_plan]], [[repo_registry]], [[entity_ecosystem_registry]], this map.
5. **Package specifications** — including the claude_gigaton_ingest package.
6. **Claude inference** — last resort.

If this map says X is LIVE but `gcloud run revisions list` disagrees, trust gcloud and update this map.

---

## 6. How to use this map

- **Before creating any new service / route / schema / dashboard / auth flow / billing logic**, search this map first.
- **Before accepting a spec from an external doc** (ingest packages, PRDs, ChatGPT exports), reconcile against §3.4 and §3.5 here.
- **Before claiming a P0/P1/P2/P3 item from the ingest backlog**, verify it isn't already LIVE in §3.1.
- **Before editing a repo**, follow the [[repo_registry]] preamble (`cd <path> && git remote -v && git rev-parse --show-toplevel && pwd`).
- **Before deploying**, follow `master-knowledge-base/runbooks/empty_secret_slot_deploy_failure.md` and the gateway cascade lessons from 2026-05-21.

---

## 7. Cross-references

- [[master_project_plan]] — unified spine (operating rules, Waves 0–7, Gignet affiliate network).
- [[repo_registry]] — disk path + remote + Cloud Run service per repo.
- [[entity_ecosystem_registry]] — 5 entities, relationships, key contacts.
- [[active_work_registry]] — what is in-flight right now.
- [[gcp_project_organization_target_2026]] — 3-phase migration plan for misplaced platform engines.
- [[universal_connector_hub_architecture]] — the *what* of the product.
- [[foundational_modular_replication_via_input_substitution]] — the *how* of scale.
- `decisions/2026-05-22_claude_gigaton_ingest_reconciliation.md` — the ADR for this audit.
