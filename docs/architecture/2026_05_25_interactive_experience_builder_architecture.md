# Interactive Experience Builder — Productized Architecture

**Date.** 2026-05-25
**Author.** Claude (design only — no code, no branches).
**Status.** DRAFT — design freeze target end of Week 1.
**Throughput target.** 50 sellable interactive-experience bundles / day (steady state).
**Reference instance #1.** Multipli vendor-growth bundle (per `runbooks/2026_05_25_multipli_bundle_manual_production_recipe.md`). Multipli is example #1, not the deadline.
**Doctrine anchors.** [[foundational_goal_gigaton_engineered_brand_experience]] (PPIM) · [[foundational_modular_replication_via_input_substitution]] · [[gignet_auto_trigger_orchestration]] · [[product_service_package_gigaton_ti_solutions]] · [[universal_connector_hub_architecture]].

---

## 1. Goal & Non-Goals

### Goal
Take a `vendor_signal_in` (URL list, CRM lead, webhook event, manual paste) and emit a `sellable_interactive_experience_bundle_out` (6+ file PPIM-signed artifact set with fit score, scenario economics, proposal, dashboard event, summary) — fully automated for the auto-capture/score/scenario/proposal/event/summary loop, with human-in-loop checkpoints at compliance + send.

At 50 bundles/day (~6/hour @ 8h working window; ~2/hour continuous), with two delivery surfaces:
- **Gigaton self-serve SaaS** — operator drives the funnel; pays per bundle or subscription.
- **Ti Solutions managed** — Ti Solutions ops team curates + reviews; charges higher per-bundle fee for white-glove.

### Non-Goals
- New module, repo, or Cloud Run service. Distribute across 11 existing engines.
- Bespoke per-vendor logic. Engine substitution per modular-replication doctrine; `operator_context` swap only.
- Autonomous outbound send. Human approval before external delivery.
- A replacement for the Multipli sprint output — that recipe stays as the manual fallback until A-B endpoints land.

---

## 2. System Architecture

```
                          ┌──────────────────────────────────────┐
INPUT SOURCES             │   gigaton-gateway (edge + LLM router)│
                          │   /webhooks/{github,cloudbuild,...}  │
  vendor URLs ──┐         │   /v1/{ingest, llm/call, healthz}    │
  CRM webhook ──┼─────────▶                                      │
  CSV upload  ──┤         └──┬───────────────────────────────────┘
  manual paste ─┘            │ publish external_signal
                             ▼
                   ┌─────────────────────────┐
                   │  Pub/Sub gignet-orch.   │  ──▶  Firestore task_registry
                   │   (Phase A/B LIVE)      │       (claim/lease/heartbeat)
                   └────────┬────────────────┘
                            │  fan-out by event_type
            ┌───────────────┼────────────────┬─────────────────────┐
            ▼               ▼                ▼                     ▼
    ┌───────────────┐  ┌────────────┐  ┌──────────────┐    ┌──────────────┐
    │ intel-silo    │  │ decision-  │  │ ppeme        │    │ persona-     │
    │ (ingest+EO+   │  │ engine     │  │ (scenarios + │    │ engine       │
    │ memory_items+ │  │ (fit score │  │ BFT state +  │    │ (buyer + ICP │
    │ docs ingest)  │  │ + DEE +    │  │ Penrose)     │    │ snapshots)   │
    │               │  │ LLM-mediated│ │              │    │              │
    │               │  │ proposal)  │  │              │    │              │
    └───────┬───────┘  └─────┬──────┘  └──────┬───────┘    └──────┬───────┘
            │                │                │                   │
            └────────────────┴──────┬─────────┴───────────────────┘
                                    ▼
                         ┌────────────────────────┐
                         │ HME (events,           │
                         │ initiatives,           │
                         │ coaching_prompts,      │
                         │ supervisor_alerts)     │
                         └─────────┬──────────────┘
                                   │
                          ┌────────┴─────────┐
                          ▼                  ▼
                 ┌─────────────────┐  ┌────────────────────┐
                 │ gigaton-ui-     │  │ GCS bundle store   │
                 │ system (review, │  │ gs://gigaton-      │
                 │ approve, send,  │  │ bundles/<op>/<id>/ │
                 │ download)       │  │ (PPIM-signed)      │
                 └────────┬────────┘  └─────────┬──────────┘
                          │                     │
              human-in-loop approval ───────────┘
                          │
                          ▼
                ┌─────────────────────┐
                │ Delivery channels    │
                │ • mimi-whatsapp     │
                │ • connector-api     │
                │   (email, CRM, etc.)│
                │ • signed GCS link    │
                │ • outcome → ppeme    │
                │   Penrose feedback  │
                └─────────────────────┘

operator_context (UAE client_namespaces or prospect_id tag) threads through every call.
PPIM signature stamped on every artifact at write time.
gigaton-engine = orchestration shell binding the chain (no new code; uses existing routing).
```

---

## 3. Pipeline Stages

| # | Stage | Input | Engine | Output | Latency budget | Cost target | Failure mode |
|---|---|---|---|---|---|---|---|
| 1 | Signal ingest | URL list / CRM webhook / CSV / paste | gigaton-gateway `/v1/ingest` → publishes `vendor.signal.received.v1` | `signal_id`, raw payload in intel-silo `documentation_bundles` | <2s | $0 | Bad URL → flag + dead-letter queue |
| 2 | Source fetch + provenance | `signal_id` | intel-silo (Source Registry, ingest worker) | per-URL fetched docs with `observed_at`, source tags | <90s (10-15 URLs parallel) | $0.01 (HTTP+storage) | 4xx/5xx → partial fetch ok if ≥1 source succeeds |
| 3 | LLM extract → schema | fetched docs + `operator_context` | gateway `/v1/llm/call` (Haiku 4.5 default, Sonnet 4.6 escalate) | populated `<bundle>_opportunity.json` skeleton with per-field confidence | <60s | $0.05-0.15 | Low confidence → mark field for human-fill, do not block |
| 4 | EO persist + multi-axis tags | extracted payload | intel-silo (`ethnographic_objects` + `vendor_opportunity` JSONB) | `eo_id`, queryable record | <2s | $0 | Schema reject → 422 to UI gap-fill route |
| 5 | Gap detect | `eo_id` | intel-silo `/gaps` | `missing_fields[]`, `confidence_per_field{}` | <1s | $0 | n/a (deterministic) |
| 6 | Human gap fill (conditional) | gap list | gigaton-ui-system gap-fill page OR sales-agent edit pane | PATCHed EO + `source=sales_agent_manual` | human-paced | $0 (operator time) | Operator skips → confidence cap enforced |
| 7 | Fit scoring | `eo_id` + scoring rubric (catalog) | decision-engine 8-component scorer | `score`, `label`, `reason_codes[]`, decision record | <3s | $0 (Python deterministic) | Missing critical field → low_fit + reason code |
| 8 | Scenario economics | `eo_id` + `score` | ppeme N-scenario modeler (6 take-rate default) | `deal_economics_model.json` + warnings | <2s | $0 (Python deterministic) | n/a (deterministic with assumptions surfaced) |
| 9 | Persona / buyer ICP | `eo_id` + segment tags | persona-engine ICP snapshot | buyer-objection bullets, talk-track | <5s | $0.02-0.05 (Sonnet 4.6) | Fallback to template objections by segment |
| 10 | Proposal language (LLM-mediated) | `eo_id` + score + scenarios + persona + compliance prompt | decision-engine `compose_proposal` → gateway `/v1/llm/call` (Sonnet 4.6) | `proposal_recommendation.md` (compliance-disciplined) | <30s | $0.15-0.40 | Compliance regex strip + retry once on violation |
| 11 | Compliance gate | composed proposal | decision-engine guardrail (regex + classifier) | pass/fail + violations[] | <1s | $0.005 (Haiku classifier if regex passes) | Fail → block + human review queue |
| 12 | Bundle assemble + PPIM-sign | all artifacts | gigaton-engine (orchestration shell — pure code) → GCS write | bundle dir at `gs://gigaton-bundles/<op>/<id>/` with 6 files + manifest | <5s | $0 (storage trivial) | Partial → save what exists, mark `partial=true` |
| 13 | HME event emit | bundle manifest | HME `experience.bundle.assembled.v1` | event row + supervisor alert if low_fit | <2s | $0 | Pub/Sub retry built-in |
| 14 | Human review queue | bundle URL | gigaton-ui-system review page | approve / reject / edit | human-paced | $0 (operator time) | Reject → loop to stage 3/6 with feedback note |
| 15 | Deliver | approved bundle | mimi-whatsapp / connector-api / signed link | delivery receipt + `experience.bundle.delivered.v1` event | <10s | $0.01-0.05 | Channel fail → retry next channel or notify |
| 16 | Outcome capture + Penrose feedback | delivery + downstream response | HME `outcome.recorded.v1` → ppeme Penrose calibration | calibration tick + `super_additive_network_value` move | async (days) | $0 | n/a (asynchronous) |

**Per-bundle automated wall-clock budget (stages 1-13, 15):** ~3-4 min in the happy path.
**Per-bundle human time (stages 6 + 14):** 5-15 min (Gigaton self-serve) or 15-30 min (Ti Solutions managed).

---

## 4. Gignet Trigger Map (event → action)

Seeded into existing `orchestrator_triggers` Postgres table (gateway DB):

| Completion event | Next task |
|---|---|
| `vendor.signal.received.v1` | `intel.silo.source_fetch` |
| `intel.silo.source_fetch.completed` | `gateway.llm.extract_schema` |
| `gateway.llm.extract_schema.completed` | `intel.silo.eo_persist` |
| `intel.silo.eo_persist.completed` | `intel.silo.gap_detect` |
| `intel.silo.gap_detect.completed` (no_gaps OR confidence ≥ 0.65) | `decision.engine.fit_score` |
| `intel.silo.gap_detect.completed` (gaps_present AND confidence < 0.65) | `ui.gap_fill_queue.enqueue` |
| `ui.gap_fill.submitted` | `decision.engine.fit_score` |
| `decision.engine.fit_score.completed` | `ppeme.scenario_economics` AND `persona.engine.icp_snapshot` (parallel) |
| `ppeme.scenario_economics.completed` AND `persona.engine.icp_snapshot.completed` | `decision.engine.compose_proposal` |
| `decision.engine.compose_proposal.completed` | `decision.engine.compliance_gate` |
| `decision.engine.compliance_gate.passed` | `gigaton.engine.bundle_assemble` |
| `decision.engine.compliance_gate.failed` | `ui.human_review.priority_queue` |
| `gigaton.engine.bundle_assemble.completed` | `hme.event_emit` AND `ui.human_review.standard_queue` |
| `ui.human_review.approved` | `delivery.dispatch` (channel chosen by `operator_context.delivery_pref`) |
| `delivery.dispatch.completed` | `hme.outcome_listener_arm` (async) |
| `hme.outcome.recorded.v1` | `ppeme.penrose_calibration_tick` |

All events carry `task_id`, `operator_context`, `bundle_id`, `ppim_signature`. Idempotency key = `(bundle_id, stage)`.

---

## 5. LLM Router Config

Per-stage routing + cost ceiling (writes to existing `llm_call_cost` table; gateway `/v1/llm/call` already LIVE per Phase D).

| Stage | Default model | Fallback | Cost ceiling / call | Rationale |
|---|---|---|---|---|
| 3 — extract → schema | Claude Haiku 4.5 | Sonnet 4.6 if confidence < 0.5 on >2 fields | $0.15 | Structured extraction is Haiku's sweet spot |
| 9 — persona ICP | Claude Sonnet 4.6 | Haiku 4.5 | $0.10 | Some judgment but stable shape |
| 10 — proposal | Claude Sonnet 4.6 | Opus 4.7 only if compliance retry fails | $0.40 | Quality matters; cost-bounded |
| 11 — compliance classifier (regex-pass path) | Claude Haiku 4.5 | Python regex only | $0.01 | High-volume gate |
| 16 — Penrose calibration narration (optional) | Python deterministic | Haiku for narrative summary | $0.02 | Mostly deterministic |

**Global per-bundle LLM cost ceiling: $1.00** (alarm at $0.80). Bundle blocks if it exceeds; routed to human review.

**Second-opinion gate:** stage 10 with `compliance_gate.violations[] > 0` retries once via Opus 4.7; second failure → human review.

---

## 6. Human-in-Loop Checkpoints

Five specific gates (none optional, but the work surface differs by delivery model):

1. **Gap-fill (stage 6, conditional)** — confidence < 0.65 or any required field missing. Operator/agent fills via UI gap-fill page. Self-serve OR sales-agent mode (per Multipli runbook §2.1). Bypassed if extraction is fully confident.
2. **Compliance review (stage 11→14, conditional)** — if classifier flags or regex hits `guarantee|approved|will receive|will be funded|commit to`. Bundle goes to priority queue with diff view; human edits proposal text and resubmits to stage 11.
3. **Bundle review (stage 14, every bundle)** — humans see fit score + scenarios + proposal + persona on one screen with `approve / reject / edit / re-run` controls. **This is the always-on gate; nothing leaves Gigaton without it.**
4. **Send authorization (stage 15)** — distinct from review. Reviewer selects channel + recipient + send-time. Prevents one-click sends and forces a deliberate dispatch.
5. **Outcome tag (stage 16, ongoing)** — humans tag downstream responses (replied / meeting-booked / closed-won / no-response) to feed Penrose calibration. Lightweight; one click per response.

**Doctrine:** the platform NEVER auto-sends prospect-facing content. Per PPIM "Facilitate" — the system enables; the human chooses.

---

## 7. Throughput Model — 50 bundles/day

Assume 8-hour operator-attended window (Gigaton) or 16-hour shift coverage (Ti Solutions). Concrete plan:

- 50 / 8h = **6.25 bundles/hour** (Gigaton) → ~10 min between bundle starts.
- 50 / 16h = **3.1 bundles/hour** (Ti Solutions, managed window).
- Per-bundle automated wall-clock (stages 1-13, 15): ~3-4 min happy path → 1 bundle can complete every ~4 min start-to-finish.
- **Parallelism target: 4 concurrent bundles in flight** (independent `task_id`s). Even at 10 min/bundle in steady state, 4-wide gives 24/hour theoretical; comfortably above the 6/hour requirement.

**Queue depth:**
- Cold queue (stages 1-2 ingest): up to 200 deep; Pub/Sub native back-pressure handles spikes.
- LLM call queue (stages 3, 9, 10, 11): rate-limited at 8 concurrent (Anthropic API headroom). Burst of 20 absorbed in <3 min.
- Human review queue (stage 14): target <12 bundles waiting (= 2h backlog at 6/hour); alert at 20.

**Latency budgets per stage are in §3.** End-to-end automated SLA target: **P50 ≤ 4 min, P95 ≤ 8 min, P99 ≤ 15 min** (stages 1-13 + 15).

**Bottleneck order (most likely):**
1. Stage 14 human review — operator throughput, not engine throughput.
2. Stage 3 LLM extract — slow if source docs are large.
3. Stage 10 proposal compose — Sonnet 4.6 latency P95 ~25s.

---

## 8. Cost Model

**Per-bundle cost target: $0.75 - $1.20 (LLM + infra)**, depending on retries.

Build-up:
- Source fetch + storage: $0.01
- LLM extract (Haiku): $0.10
- LLM persona ICP (Sonnet): $0.05
- LLM proposal (Sonnet): $0.30 (~$0.40 ceiling)
- LLM compliance classifier (Haiku): $0.01
- Cloud Run + Pub/Sub + Firestore + GCS: $0.05
- Delivery (mimi WhatsApp or connector-api): $0.05
- Buffer for retry + escalation: $0.15

**Justification.** At a $50-$250 per-bundle sell price (Gigaton self-serve) or $500-$2000 per-bundle Ti Solutions managed fee, a $1 unit cost yields ≥98% gross margin on COGS-of-LLM. PPIM is satisfied: cost-per-touch is bounded; revenue-per-touch >> cost.

**Daily run cost @ 50 bundles:** ~$50-60. Acceptable.

**Cost alarm:** any bundle exceeding $1.50 cost halts the pipeline + emits supervisor alert. Drift sentinel flags any LLM call without `bundle_id` attribution.

---

## 9. Output Schema (PPIM-signed, multi-axis tagged)

Bundle directory: `gs://gigaton-bundles/<operator_or_prospect_id>/<bundle_id>/`

Canonical structure (extends the Calendly sample bundle):

```
<bundle_id>/
  manifest.json                       # bundle-level metadata + ppim_signature + checksums
  vendor_opportunity_profile.json     # per Multipli schema; multi-axis tagged
  fit_score_report.md                 # 8-component score + reason codes
  deal_economics_model.json           # N-scenario model
  proposal_recommendation.md          # compliance-disciplined text
  dashboard_event_payload.json        # HME event payload (vendor.financing.assessed.v1 et al)
  beta_test_summary.md                # executive summary + missing-info gates
  persona_icp_snapshot.json           # NEW vs Multipli — buyer profile + objections
  compliance_audit.json               # NEW — what regex hit, what classifier said, who approved
```

**Every file carries a PPIM signature block** (`_ppim_signature` for JSON, fenced ```ppim-signature``` for Markdown) with: `interaction / economics / predictability / brand_dimension / lifecycle`.

**Every file carries multi-axis tags** (per [[foundational_modular_replication_via_input_substitution]]): `industry / sub_vertical / geo / regime / segment / lifecycle / provenance / modality`.

**Every record stamps `operator_context`** (UAE `client_namespace_id` if signed operator, else `prospect_id` tag).

**Reference structure:** `master-knowledge-base/multipli/sample_bundles/calendly/` — canonical exemplar; any new vendor bundle starts from this shape.

---

## 10. Delivery — How the Bundle Leaves Gigaton

Three channels, operator-chosen at stage 15:

1. **Signed GCS download link** — default. Valid 7 days. Recipient gets URL via whatever channel operator pastes it into.
2. **mimi-whatsapp** — for WhatsApp-first prospects. Sends a 2-message intro + signed link. Existing engine; no new code.
3. **connector-api** — generic channel adapter. Today wires email + CRM-task creation; future Slack/SMS/LinkedIn DM.

**Outcome capture:**
- For WhatsApp: mimi webhook fires on reply → `outcome.recorded.v1` event.
- For email: connector-api polls reply box OR operator manually tags in HME.
- For CRM-task: connector-api listens for task status change.

All outcomes feed back into stage 16 → ppeme Penrose calibration → tightens future scoring.

---

## 11. Gigaton vs Ti Solutions Delivery Model Diff

Same engines; different surfaces and price points.

| Dimension | Gigaton (self-serve SaaS) | Ti Solutions (managed) |
|---|---|---|
| Who drives the funnel | Operator | Ti Solutions ops |
| Who fills gaps (stage 6) | Operator OR system-asks-prospect | Ti Solutions agent |
| Who reviews bundle (stage 14) | Operator | Ti Solutions agent + (optional) operator co-sign |
| Who selects channel + sends (stage 15) | Operator | Ti Solutions on operator's behalf |
| `operator_context` shape | UAE `client_namespace_id` | `client_namespace_id` + `delivery_partner=ti_solutions` |
| Pricing | $50-$250 per bundle OR subscription | $500-$2000 per bundle (managed service) |
| SLA | Best-effort (queue-depth visible) | Guaranteed turnaround (24h or 4h tiers) |
| Custom-branded bundle | Self-branded via brand_dimensions catalog | Either Ti Solutions co-brand OR operator white-label |

Engines + endpoints are identical. The diff lives entirely in `operator_context`, FE shell, billing tier, and supervisor SLA in HME.

---

## 12. Build Sequence — 4-Week Roadmap

**Week 1 (2026-05-25 → 2026-05-31) — DESIGN FREEZE**
- This doc reviewed + ratified.
- Schema for `manifest.json`, `compliance_audit.json`, `persona_icp_snapshot.json` finalized.
- Decision: Multipli Phase A-B endpoints (per 5/22 runbook §4-5) are the SCAFFOLD; the Builder design generalizes them via `bundle_type` parameter. Re-name `/v1/multipli/*` routes to `/v1/bundles/*` with `bundle_type=vendor_financing` as default.
- Drift-sentinel rules for: missing `bundle_id` on LLM call, missing PPIM signature, missing multi-axis tags.
- 1 ADR committed to master-knowledge-base.

**Week 2 (2026-06-01 → 2026-06-07) — FIRST DEPLOY + FIRST PAID BUNDLE**
- intel-silo migration 033 lands (`eo_type=vendor`, `vendor_opportunity` JSONB column, `prospect_id` first-class tag).
- decision-engine: `/v1/bundles/fit-score` + `/v1/bundles/compose-proposal` + compliance gate.
- ppeme: `/v1/bundles/scenario-economics`.
- gigaton-engine: bundle-assemble worker (no new repo; new module).
- HME: register `experience.bundle.{assembled,delivered,outcome_recorded}.v1` event types.
- Pub/Sub `orchestrator_triggers` rows seeded for the 16 events in §4.
- gigaton-ui-system: gap-fill page + review/approve page + send-authorize page.
- First end-to-end paid bundle delivered (target: Calendly redo via engines, NOT hand).
- Cost & latency dashboards (Phase G) extended with `bundle_*` metrics.

**Week 3 (2026-06-08 → 2026-06-14) — SCALE TO 10/DAY**
- Parallelism tuning: 4 concurrent bundle workers verified stable.
- Sonnet 4.6 latency profiling on proposal compose; promote frequently-used prompt prefixes to prompt-cache.
- mimi-whatsapp delivery integrated end-to-end.
- connector-api email + CRM-task channels integrated.
- Persona-engine ICP snapshot endpoint live.
- Ti Solutions ops onboarded as first managed-tier user (separate `client_namespace`).
- Penrose calibration loop closed for first 50 delivered bundles.

**Week 4 (2026-06-15 → 2026-06-21) — 50/DAY LIVE**
- Throughput soak test: 50 bundles in 8h, observe queue depths + LLM cost + human-review latency.
- Drift sentinel: red-line any bundle missing PPIM sig or multi-axis tags.
- Billing wired: per-bundle metering against operator's plan (Stripe webhook via gateway).
- Affiliate hook (Chapter 11 of [[master_project_plan]]): each delivered bundle emits affiliate-credit event if `referrer_id` present.
- Documentation in `gigaton-knowledge-base` + Ti Solutions runbook.

---

## 13. Open Decisions (max 5)

1. **`bundle_type` taxonomy.** Multipli = `vendor_financing`. Other types likely: `partnership_proposal`, `enterprise_outreach`, `affiliate_referral_pack`, `industry_report`. Decide first 3 to seed in Week 1 to avoid premature generalization, or commit to `vendor_financing` only for Week 2 and add types per demand.
2. **Self-serve gap-fill prospect-facing UI.** Multipli runbook §2.1 defers self-serve + live-call-tandem to Phase 2. For 50/day Gigaton, do we ship self-serve gap-fill in Week 2 (recommended — it unblocks operator throughput) or Week 3?
3. **Compliance classifier model choice.** Haiku 4.5 default; but financing/regulated language might warrant a fine-tuned Python classifier in Week 3. Decide whether to invest in training data collection in Week 2.
4. **Ti Solutions branding mechanism.** Co-brand markers in `brand_dimensions` catalog vs. operator white-label vs. Ti Solutions banner. Forces a brand-dimensions schema decision.
5. **Stripe metering granularity.** Per-bundle, per-stage (LLM cost passthrough), or per-LLM-token? Affects pricing-page transparency and refund logic when bundles fail compliance.

---

## 14. Anti-Patterns

1. **Creating a "bundle-builder" Cloud Run service.** No new repos; distribute across the 11 engines per Multipli sprint §1 doctrine.
2. **Hardcoding `multipli` or `calendly` or any prospect name anywhere outside `operator_context` or `prospect_id` tag.** Modular replication is non-negotiable.
3. **Auto-send.** Step 15 is human-authorized. Always.
4. **Bypassing the compliance gate.** Even if `urgent=true`. Every external-bound artifact passes regex + classifier.
5. **One-LLM-routes-everything.** Stage 3 + stage 10 + stage 11 have different cost/quality/latency trade-offs; route each independently per §5.
6. **Single-operator JSONB tags.** Every artifact carries multi-axis tags from day one even if only one operator uses it. Otherwise the second operator triggers a schema rewrite.
7. **PPIM signature added as an afterthought.** Stamped at write-time by the bundle-assemble worker; missing signature = drift-sentinel MAJ.
8. **Treating the Multipli manual recipe as the production system.** That recipe is a stopgap; this design supersedes it by Week 2 deploy.
9. **Letting human-review queue grow without back-pressure.** When stage 14 backlog > 20, automatically slow stage 1 ingest (Pub/Sub flow control) — don't pile up work that can't be reviewed.

---

## Cross-references

- [[gignet_auto_trigger_orchestration]] — substrate for §4 trigger map.
- [[product_service_package_gigaton_ti_solutions]] — drives §11 dual-delivery model.
- [[foundational_modular_replication_via_input_substitution]] — drives §9 schema discipline.
- [[foundational_goal_gigaton_engineered_brand_experience]] — PPIM signature requirement.
- [[multipli_vendor_growth_engine_sprint_2026_05_22]] — Multipli sprint = first instance.
- `runbooks/2026_05_22_multipli_vendor_growth_engine_4day_sprint.md` — engine-assignment precedent (§1).
- `runbooks/2026_05_25_multipli_bundle_manual_production_recipe.md` — manual fallback recipe.
- `multipli/sample_bundles/calendly/` — canonical bundle exemplar.
- `docs/architecture/CODEBASE_MAP.md` — engine boundary reference.
