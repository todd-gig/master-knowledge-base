---
title: Inventory of last-6-months Gigaton work — what's deployed/wired/live vs. not
date: 2026-05-25
horizon: 2025-11-25 → 2026-05-25
authority: investigation snapshot, read-only
constraint: per MIG-CANCEL (decisions log 2026-05-25), carmen-beach engines stay live as primary; gigaton-platform mirror = warm DR; no migration cutover
goal: identify every shipped feature NOT yet in state {deployed + wired + live + generating value}
---

# Inventory + Undeployed/Unwired Punch List — 2026-05-25

## A. Per-engine state matrix (6mo)

Legend: STATE column ∈ {FULL = deployed+wired+called+value, WIRED = deployed+routed+UI-stub, PARTIAL = deployed-not-wired-or-UI-orphan, ORPHAN = deployed-no-FE-no-route, SPECCED = design only, BACKEND-ONLY = no FE consumer}.

| Engine | Last-6mo features shipped (net of lint/typo) | Deployed rev | Gateway wired? | FE calls? | Value today? | STATE |
|---|---|---|---|---|---|---|
| **gigaton-gateway** (gigaton-platform) | LLM router (Phase D, multi-model+cost+second-opinion gate), `/v1/review/` HME route, mimi `/v1/messaging/*`, `/v1/documentation/*` + `/v1/oauth/drive/*`, OPENAI_API_KEY mount, CORS for `gigaton-platform.web.app`, namespace middleware (UAE-backed httpx + bypass list), AX-024 preflight, register-provider-credentials action | gigaton-gateway-00041-s5p | n/a (is the gateway) | yes | yes — 11/11 aggregate ok | FULL |
| **user-access-engine** | client_namespaces (Concept 7 / §A.1), workflow_overlays + scope contract (Stage 0), `/v1/access/check` cross-engine, scope-contract + legal-entity endpoints, 6 documentation + 4 directed-workflow capability seeds, namespace REST, soft admin-token gate now STRICT (SEC-2), boot-time alembic gate | uae-00028-6wr (strict) | yes (/v1/auth, /v1/oauth, /v1/orgs, /v1/personas, /v1/access/check, /v1/invites, /v1/onboarding/{manifest,state,intent}, /v1/signoff/) | yes | yes | FULL |
| **human-management-engine** | L7 review records + 4 endpoints (Bella's queue), Value of Human Contribution Matrix (Concept 4), directed-workflow backend persistence + initiative auto-emission, 10-stage onboarding event_type enum extension, org-process-readiness + assignment-readiness aggregators (Stages 6+7), `IndustryCatalogSubmitted` event (Stage 5 self-healing), 4-operator empirical matrix tests, BFT-snapshot consumer | hme-00031-mv7 | yes (/v1/events, /v1/users, /v1/initiatives, /v1/supervisor, /v1/coaching, /v1/tasks, /v1/reports, /v1/review) | yes (admin review queue live a5e8ff3 2026-05-25) | yes | FULL |
| **decision-engine** | Alembic adoption (S2) + chains 0002–0006, migration 004 industry_catalogs APPLIED tonight, Stage 5 self-healing endpoints, Postgres write-through (decision_records + execution_records, TEXT widening), AX-008 nightly Cloud Scheduler sweep LIVE, AX-021/22/23 drift sentinel (Phase F), Penrose `documentation_coverage_score` aux metric, activation-gate axioms for stages 0/4/5/9, AX-024 preflight + drift rule, AX-010 alembic-as-signoff | decision-engine-00002-vfr (gigaton-platform MIRROR) + decision-engine-00040-kn4 (carmen-beach PRIMARY) | yes (/v1/decisions, /v1/outcomes, /v1/proposals, /v1/codification, /v1/calibration, /v1/penrose/scoreboard, /v1/drift/open, /v1/axioms, /v1/doctrine, /v1/overrides) | yes (calibration page, founder pages, overrides, penrose scoreboard widget) | yes | FULL |
| **intelligence-silo** | S7 relational `memory_items` + S8 Lifecycle State Machine, GCS upload + v4 signed URL assembler (S12), multi-account Drive OAuth + ingest worker + canonical bundle endpoints (Documentation Ingest feature), EO System (Concept 3, Postgres write-through + boot hydrate), Omni connector + HTML5 assembler + Source Registry extension (L5/L6/L8), capability stub flip → real enforcement, state-table + activation-gate (031) | intelligence-silo-00001-kcf (gigaton-platform MIRROR) + intelligence-silo-00036-flc (carmen-beach PRIMARY) | yes (/v1/memory, /v1/sources, /v1/intelligence, /v1/observations, /v1/experience, /v1/documentation/*) | yes (sources page, documentation page, calibration sources, OAuth drive) | yes | FULL |
| **persona-engine** | Initial scaffold + PersonaClient SDK (Python + TS), Cloud SQL provisioning, alembic, operator_context filtering, `/bft-snapshot`, First Principles Variable Registry (Concept 2), persona-count + brand-readiness aggregators (Stages 2+3), auto-deploy GHA | persona-engine-00007-6qz | yes (/v1/personas, /v1/humans, /v1/orgs aliases) | yes (via clients) | yes | FULL |
| **ppeme** | 9-var BFT state vector + STVR Economics tag-based operator lookup, Penrose emitter wiring + finalization endpoints, counterfactual baseline endpoint (Master Calculator sim), Experience Engineering Equation Brand+Interaction→Revenue→Profit module, `/v1/stage-influence` endpoint, CTR ingest from outcomes + forecast payload, L2 experience-type router with BFT state binding + counterfactual pre-gen (RPO-01) | ppeme-00017-55b | yes (/v1/scenarios, /v1/forecasts, /v1/state, /v1/leads) | yes (penrose scoreboard widget, calibration variance) | yes | FULL |
| **gigaton-engine** (pricing/billing) | Multi-agent supervisor wrapped with rollback/override/dead-letter (CRIT-001), provider/model/prompt_version envelope on Claude calls (CRIT-003/007), explicit assumptions[] on pricing (CRIT-008), `/v1/*` cross-engine endpoints, modular-replication operator registration (liquefex, incontekst, surf_school_costa_rica + carmen-beach), cold-start fix (min-instances=1 + cpu-boost) | gigaton-engine-00001-4gq (gigaton-platform MIRROR) + gigaton-engine-00008-jr5 (carmen-beach PRIMARY) | yes (/v1/pricing) | partial — only via SalesOS HTTP bridge; **no direct FE page for pricing/billing** | partial — value via SalesOS only | **PARTIAL** |
| **sales-operating-system** | GigatonPricing HTTP bridge (3 endpoints: gigaton/status, pricing/quote, opportunities/{id}/pricing), claude_reasoning via ai_router chokepoint, Cloud SQL migration scaffolding + runtime-flip runbook (NOT executed — still SQLite per MIG-4), cold-start regression fix | sales-operating-system-00001-8lp (gigaton-platform MIRROR) + sales-operating-system-00005-47c (carmen-beach PRIMARY) | **NO** — no `/v1/sales/*` or `/v1/opportunities/*` route in gateway routing_table.py | **NO FE** — no SalesOS page in gigaton-ui-system | **NO** — built but invisible to operators | **ORPHAN** |
| **connector-api** (carmen-beach) | Per-operator connector vault + endpoints, gcal_oauth + gmail_oauth + stripe_api_key provider adapters, `/v1/connectors/credentials` + `/validate` (15 first-class probes), KMS envelope cipher, Workload Identity Federation, GHA auto-deploy | connector-api-00004-6vf | yes (/v1/connectors/) | yes (4 connector pages: WhatsApp, Stripe, Gmail, GCal + tech-stack credential paste) | yes | FULL |
| **mimi-whatsapp** (carmen-beach) | WhatsApp inbound + reply v0, per-operator credentials via connector-api, `/v1/messaging/*` gateway proxy | mimi-whatsapp-00007-zr2 | yes (S4 PR #47 — /v1/messaging/*) | partial — `/connectors/whatsapp` is credential setup only; no inbound/outbound chat surface in FE | partial — Twilio works, but **no operator can see/send messages from the platform UI** | **PARTIAL** |
| **gignet-activity-emitter** | Orchestrator fan-out function | gignet-activity-emitter-00003-cav | no (Pub/Sub event surface, not REST) | no | yes (background) | FULL (event-surface) |
| **orchestrator-trigger-fan-out** | Phase A/B orchestration fabric | orchestrator-trigger-fan-out-00002-guy | no | no | yes (background) | FULL (event-surface) |
| **SIE (api-gateway-service)** | 14 carmen-beach sub-services (action-orch, calibration, decision-engine-service, entity-resolution, feedback, feed-ingestion, interface, memory, ontology, operator-api, symbol-engine, calibration, decision-engine-service) | api-gateway-service-00004-taj | yes (/v1/sie/) | no direct page — only `intelligence/sie` calls | partial — only via aggregator | **PARTIAL** |
| **gigaton-ui-system** (FE) | 35+ pages incl. chat-first orchestrator + tier-gated nav, OAuth login + role-based landing, /sources, 5 connector pages, /onboarding/tech-stack with credential paste, Founder (proposals/signoff/drift/doctrine), Owner (proposals/recruitment/coverage), Admin (review queue + experience review + rerun editor), `/v1/**` rewrite to gateway (PR #34), DocumentationIngest, IndustryCatalogFormAffordance | Firebase Hosting `gigaton-platform.web.app` LIVE | n/a | n/a | yes | FULL |

### Hidden gigaton-platform-side surface (not in routing table)
- `decision-engine`, `intelligence-silo`, `gigaton-engine`, `sales-operating-system` ALL have parallel deployments in `gigaton-platform` (the migration mirror). Per **MIG-CANCEL**, these stay as warm DR; carmen-beach instances remain primary. Gateway URLs still point to carmen-beach (rjmcrtvuzq). No action needed unless an engine degrades.

---

## B. Specced-but-not-built (tonight's 5 docs)

| Spec | Effort (days, claude-agent) | Existing infra leveraged | Net-new endpoints | Highest-value 20% to ship first |
|---|---|---|---|---|
| **`2026_05_25_entity_creation_flow_n_wide.md`** (N-wide entity creation, 7+ types, affiliate-gated, EF-1..6 ratified) | 5-7d | UAE namespaces, HME events, gigaton-engine Stripe Customer, connectors_catalog, onboarding_v1.yaml manifest | UAE: POST /v1/entities; gigaton-engine: provision-stripe-customer; intel-silo: brand_dimensions row writer; HME: EntityCreated event | **Auto-provision `<slug>.gigaton.ai` subdomain + Stripe Customer + UAE namespace** in one chained call (EF-1, EF-3, EF-6). Day-1 of entity self-serve. |
| **`2026_05_25_interactive_experience_builder_architecture.md`** (50/day bundle factory, 3 bundle types, IEB-1..10) | 8-10d (Wave 1 only — auto-capture+score+scenario; manual send) | decision-engine variance computation, ppeme scenarios, intel-silo memory_items + assembler, HME events, regex+Haiku compliance gate | DEE: /v1/bundles/score; ppeme: /v1/bundles/economics; silo: /v1/bundles/assemble; HME: BundleDelivered event | **Auto-capture + score endpoint pair** — make Multipli sample #1 the proof, then 49 more share the same engine via operator_context. |
| **`2026_05_25_omnichannel_support_design.md`** (5 channels: email+SMS+WA+chat+Slack; 12 new endpoints, 0 new services) | 4-6d | mimi-whatsapp (SMS+WA), connector-api (Twilio creds), HME (ticket events), intel-silo (threading), Slack workspace (already created `gigaton-ai.slack.com`) | HME: /v1/support/{tickets,inbound,outbound,resolve}; intel-silo: thread-merge; connector-api: gmail+slack adapters | **Slack bridge bot + Gmail inbound watch** (richest-available reply per SUPPORT-3). 2-day MVP. |
| **`2026_05_25_platform_inbox_feature_spec.md`** (per-entity Gmail surfaced in Gigaton UI, INBOX-1..5 + FEAT-1) | 5-7d | connector-api gmail_oauth (already shipping), intel-silo OAuth pattern, gigaton-ui-system patterns | Backend: /v1/inbox/{threads,messages,send,labels}; FE: InboxPage.tsx | **Read-only thread list + reply** as FEAT-1 MVP. Defer compose/filters/labels editor to v1.1. |
| **`2026_05_25_30_day_gigaton_company_launch_roadmap.md`** (sequencing doc; not a feature) | n/a | n/a | n/a | EE-2 order: Multipli → 50/day stable → Carmen Beach paid → Gigaton SaaS → Ti DBAs |

---

## C. Carmen-Beach-Properties gap

**What's in the monorepo** (apps/services/packages):
- `apps/web` — Next.js platform app (consolidated 2026-05-16; `/platform/**` + `/api/**` routes to Cloud Run `carmen-web`); deployed?  **NOT visible at playadelcarmen.homes** — apex still serves the static brochure.
- `apps/connector-api` — DEPLOYED + LIVE (`connector-api-00004-6vf`)
- `apps/mimi` — DEPLOYED + LIVE (`mimi-whatsapp-00007-zr2`)
- `apps/admin` — empty (node_modules only; deleted in consolidation 5f5cab5)
- `services/whatsapp` — WhatsApp inbound + reply v0
- `packages/` (15): ai, auth, automation, config, db (Prisma + KMS envelope), google-drive, google-workspace, leads, media, observability, pricing, storage, tracking, ui, utils
- `docs/` — phase prompts, Mimi service spec, PPEME integration

**What's deployed at playadelcarmen.homes:** the basic real-estate static brochure (Vite/index-DVpYQuFv.js + index-DQj_tEW7.css, "Luxury Beachfront Real Estate"). Same response for `/` and `/platform` — meaning the `/platform/**` Firebase rewrite to Cloud Run is NOT active in production. firebase.json declares it; deploy never landed.

**The 3-5 specific build/deploy/wire steps:**
1. **Deploy `apps/web` to Cloud Run** as service `carmen-web` (referenced in firebase.json but not in Cloud Run list). `gcloud run deploy carmen-web --source apps/web --project=carmen-beach-properties --region=us-central1`.
2. **Push firebase.json + Firebase Hosting** for `playadelcarmen.homes`: `firebase deploy --only hosting --project=<carmen-beach-firebase-project>`. Activates `/platform/**` → Cloud Run rewrite.
3. **Wire `apps/web` → gateway**: set `NEXT_PUBLIC_GATEWAY_URL=https://gigaton-platform.web.app` (or api.gigaton.ai once DNS lands) so platform pages call `/v1/*` endpoints.
4. **Cross-link from apex** — add a "Sign in / Owner Portal" CTA on the brochure homepage pointing to `/platform`. (Brochure is hosted outside the repo; coordinate with whoever owns the apex Firebase site.)
5. **DNS post per DNS-1 (locked)**: only playadelcarmen.homes gets touched. Apex stays as brochure; `tour/chat/shop/book/api` subdomains all rewrite to gigaton-platform.web.app; Workspace MX + SPF + DMARC.

Per **MIG-1.1**: Carmen-Beach scope narrows to real-estate-specific resources (bookings, OTAs, host accounting, property dashboards). All intelligence/decision/billing engines consolidate to gigaton-platform (NOT migrated tonight per MIG-CANCEL — stays as warm DR).

---

## D. Prioritized PUNCH LIST (rank-ordered by value-per-effort)

| # | Item | ETA | Dependency chain | Who | Unblock condition |
|---|---|---|---|---|---|
| 1 | **Wire SalesOS into gateway** (add `/v1/sales/`, `/v1/opportunities/`, `/v1/leads/` routes to routing_table.py) + ship a `/sales` page in FE | 0.5d | none | claude-agent | none — pure config edit + 1 FE page |
| 2 | **Deploy `carmen-web` Cloud Run + Firebase Hosting rewrite** so playadelcarmen.homes/platform actually serves the Next.js app | 0.5d | NEXT_PUBLIC_GATEWAY_URL env decision | todd (for firebase deploy auth) + claude-agent | identity to Firebase project |
| 3 | **Build mimi chat/inbox FE page** — operator can see+reply to inbound WhatsApp/SMS without leaving platform | 1d | mimi-whatsapp already deployed + wired | claude-agent | identify auth flow (UAE bearer) |
| 4 | **Wire gigaton-engine directly into FE** — Stripe Customer create + per-deal billing UI for entity dashboards (B1-B5 locked) | 2d | gigaton-engine has /v1/* endpoints; needs Stripe wiring; FE billing page | claude-agent | Stripe API key in secret manager (status?) |
| 5 | **Entity Creation flow MVP** (entity_creation_flow_n_wide.md §2 — auto-provision subdomain + Stripe Customer + UAE namespace in one chained call) | 3d | UAE namespace endpoints exist; Stripe sub-account needs gigaton-engine; subdomain auto-provision per DNS-1 (deferred for Ti) | claude-agent + todd (DNS) | DNS-1 narrow scope (only playadelcarmen.homes today) — entity-creation subdomain flow needs gigaton.ai DNS access |
| 6 | **Slack support bridge bot** (omnichannel design §3) — inbound email → Slack thread + "Use this draft" button | 2d | Slack workspace exists; needs Workspace Gmail OAuth (EMAIL-1); needs Slack app install | claude-agent + todd (Workspace setup) | Gmail Workspace setup + Slack app install |
| 7 | **Platform Inbox MVP** (read-only thread list + reply for Gmail OAuth'd entities) | 3d | connector-api gmail_oauth ready; intel-silo OAuth pattern; new endpoints | claude-agent | Workspace Gmail OAuth client (INBOX-1 default) |
| 8 | **IEB Wave 1 — auto-capture+score+scenario endpoint trio** for Multipli + 49 future samples | 4-5d | DEE variance computation (migration 005 pending), ppeme scenarios, intel-silo assembler — all engines already deployed | claude-agent | migration 005 industry-catalog variance |
| 9 | **gigaton-platform `gigaton-engine` warm-DR cutover readiness check** — confirm migration mirror serves health/pricing correctly; document fast-cutover script (per MIG-CANCEL §"Re-evaluate if any engine degrades") | 0.5d | mirror exists | claude-agent | none |
| 10 | **Stripe Tax + Stripe Connect Express scaffolding** (B5 + 30D-4 — Carmen Beach Stripe Connect IMMEDIATELY per ratified ADR) | 2d | gigaton-engine billing logic (B3) | claude-agent + todd (Stripe dashboard) | Stripe account + Connect Express enable |
| 11 | **Founder + Owner page → live data wiring** — ensure FE pages actually populate from HME `/v1/initiatives`, decision-engine `/v1/proposals`, ppeme state. Many pages show stubs in browser smoke. | 1d | engines all responsive | claude-agent | end-to-end browser smoke list |
| 12 | **SIE `/v1/sie/*` aggregator promotion** — currently behind aggregator only; surface key SIE subservices (operator-api, feedback, calibration) via direct FE pages or hide them | 1d | SIE healthy at /v1/sie | claude-agent | decision: surface or hide |
| 13 | **Gmail Workspace setup (EMAIL-1)** — Workspace tenant + DKIM/SPF/DMARC + gmail-support-relay SA with domain-wide delegation | 1d (mostly elapsed time) | DNS-1 narrowed to playadelcarmen.homes — gigaton.ai needs separate handling | todd + paralegal? | Workspace provisioning |
| 14 | **WhatsApp Meta Business verification for gigaton-ai** (omnichannel + per-DBA WhatsApp Senders) | 3-7d (Meta review) | mimi-whatsapp already live for carmen-beach | todd (submit) | Meta Business Manager docs |
| 15 | **Onboarding 10-stage end-to-end browser smoke** — verify a fresh operator can complete Stages 0→9 via /chat?onboarding=stage-0 today | 0.5d | UAE manifest + state + intent endpoints live (verified 2026-05-22) | claude-agent | UAE strict mode verified |
| 16 | **ToS / Privacy / AUP / DPA v0 drafts** (legal scaffold) — entity creation gates on these existing | 2d (drafts) + 2-3wk (paralegal review) | none | claude-agent (drafts) + paralegal (review, ~$8-24K) | paralegal engaged |
| 17 | **`DELETE /v1/operators/{id}`** — required to allow EU operators (currently blocked per locked launch decision) | 1d | UAE namespace cascade delete | claude-agent | none |
| 18 | **api.gigaton.ai DNS cutover** — currently `gigaton-platform.web.app/v1/*` works; api subdomain pending | 1d (DNS prop) | DNS-1 says only playadelcarmen.homes touched — api.gigaton.ai needs separate go-ahead | todd (DNS provider) | DNS-1 scope expansion |
| 19 | **app.gigaton.ai mapping** — clean URL for the platform UI | 1d | DNS-1 scope question | todd | DNS-1 scope expansion |
| 20 | **Sales-OS Postgres flip** (MIG-4: data persists, current SQLite is ephemeral on every revision) | 0.5d | `sales-os-pg` provisioned tonight in gigaton-platform | claude-agent | run alembic + DATABASE_URL flip |
| 21 | **7f46371b SA key revoke investigation** (SEC-3) | 0.5d | trace binding | claude-agent | gcloud reauth |
| 22 | **`/v1/codification/analyze` & `/v1/codification/queue`** FE pages — backend exists, no operator UI | 1d | DEE backend live | claude-agent | none |
| 23 | **Connect Stripe Tax in production** (B5) | 0.5d | gigaton-engine billing | claude-agent | Stripe dashboard access |
| 24 | **gigaton-ai.slack.com per-operator `#support-{op_id}` channel auto-create** during entity onboarding | 0.5d | Slack workspace exists | claude-agent | Slack app install + bot token |
| 25 | **Affiliate-gated entity creation** (EF-5 — must originate from Gignet affiliate code) | 1d | persona-engine, UAE namespaces, gigaton-engine | claude-agent | affiliate code generator |
| 26 | **brand_dimensions catalog row per Ti DBA** (IEB-9 — Ti Life / Ti Solutions / Total Interactions) | 0.25d | intel-silo brand_dimensions table exists | claude-agent | none |
| 27 | **AX-024 CI WIF wiring** (deferred from 2026-05-22) | 0.5d | drift rule LIVE in DEE | claude-agent | none |
| 28 | **Pub/Sub watch wiring for Gmail inbound** (omnichannel + platform inbox prereq) | 1d | Workspace setup | claude-agent | Workspace tenant ready |
| 29 | **Document storage tier flip for memory_items** — confirm S7+S8 lifecycle state machine is actively transitioning items in prod | 0.5d | silo `00036-flc` | claude-agent | run sweep + verify counts |
| 30 | **Browser-driven E2E demo smoke** for beta launch readiness (login → entity → connector → support → bundle) | 1d | all above | claude-agent | items 1-7 complete |

---

## E. Top 5 LOWEST-EFFORT, HIGHEST-VALUE items to start TONIGHT (in parallel)

1. **Wire SalesOS into gateway + ship `/sales` FE page** (Punch #1, ~0.5d) — SalesOS has been deployed-but-invisible for 6+ months. 1 routing_table.py edit + 1 FE page wiring `humanManagementClient` pattern.  Concrete first step: add `Route("/v1/sales/", "sales-operating-system", "SALES_OPERATING_SYSTEM_URL")` + a sibling for `/v1/opportunities/` to `/Users/admin/Documents/GitHub/gigaton-gateway/api/routing_table.py`. Then deploy gateway. Then add `pages/SalesPage.tsx` calling those endpoints.

2. **Deploy carmen-web Cloud Run + activate Firebase /platform rewrite** (Punch #2, ~0.5d) — apps/web already exists and is consolidated. Run `gcloud run deploy carmen-web --source=apps/web --project=carmen-beach-properties --region=us-central1`. Then `firebase deploy --only hosting` from CBP. Activates `/platform/**` → Cloud Run rewrite already in firebase.json.  Concrete first step: from `/Users/admin/Documents/GitHub/Carmen-Beach-Properties/`, verify `apps/web/Dockerfile` builds locally with `pnpm --filter web build`.

3. **Sales-OS Postgres flip** (Punch #20, ~0.5d) — `sales-os-pg` was provisioned tonight in gigaton-platform per MIG-4. Run alembic against new instance + flip `DATABASE_URL` env var on the carmen-beach Cloud Run service. Stops the every-revision data loss. Concrete first step: confirm `sales-os-pg` instance is RUNNABLE in gigaton-platform; copy DSN to a temp local variable; run `cd /Users/admin/Documents/GitHub/sales-operating-system && DATABASE_URL=... alembic upgrade head`.

4. **brand_dimensions seed for 3 Ti DBAs** (Punch #26, ~0.25d) — IEB-9 locked. Single SQL INSERT against intel-silo `brand_dimensions` table. Concrete first step: `psql $INTEL_SILO_DB_URL -c "INSERT INTO brand_dimensions (entity_id, brand_voice, tagline, ppim_signature, axes) VALUES ('ti-life', ...), ('ti-solutions', ...), ('total-interactions', ...);"` — exact JSONB shape from existing carmen-beach row.

5. **`DELETE /v1/operators/{id}`** (Punch #17, ~1d but highest unblock value) — currently blocks EU operators from beta. UAE-only change: add endpoint that cascades namespace + workflow_overlays + scope_contracts deletion + persona-engine soft-delete via service token. Concrete first step: open `/Users/admin/Documents/GitHub/user-access-engine/app/api/operators.py` (or equivalent), add the route, then add UAE alembic migration for soft-delete columns if not already present.

---

## F. Total effort to "everything deployed + wired + live + generating value"

- **Tier 1 (must-ship for paying beta — Punch items 1, 2, 3, 4, 6, 7, 11, 15, 17, 20, 22, 30):** ~15-18 dev-days = **~3 weeks @ 1 claude-agent + 0.5 todd** = $0 marginal claude cost + minimal Stripe/Twilio/Workspace overhead (~$50-200/mo combined).
- **Tier 2 (productize per 30-day roadmap — Punch items 5, 8, 9, 10, 13, 14, 16, 23-29):** ~12-15 dev-days = **~3 weeks @ 1 claude-agent + 0.5 todd + paralegal $8-24K**.
- **Tier 3 (DNS + EU + polish — Punch items 18, 19, 12, 21):** ~3-4 dev-days = **~1 week @ 1 claude-agent**.

**Grand total**: **~30-37 dev-days ≈ 6-8 weeks elapsed @ 1 claude-agent + 0.5 todd + paralegal ~$8-24K + cloud overhead ~$200-400/mo.**

Per LAUNCH-1 reframing + MIG-CANCEL: beta opens as soon as Tier 1 ships. Migration cutover is OFF the critical path; warm DR stays. The fastest-to-revenue items are #1-5 above — all are 0.25-1d each and can be done in parallel by sibling agents tonight.

---

## Cross-reference index
- `decisions/2026-05-25_architecture_decisions_log.md`
- `docs/architecture/2026_05_25_*` (5 specs)
- `gigaton-gateway/api/routing_table.py` + `api/config/engines.yaml`
- `gigaton-ui-system/App.tsx` (35+ routes inventory)
- Cloud Run listings: `gigaton-platform` (11 services) + `carmen-beach-properties` (18 services)
- Live gateway aggregate: `https://gigaton-platform.web.app/v1/healthz` → 11/11 ok at 2026-05-25
