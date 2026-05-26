---
type: architecture-design
established: 2026-05-26
status: ACTIVE — doctrine layer for every operator context-gathering surface
authority: locked unless explicitly revisited
serves: foundational_goal_gigaton_engineered_brand_experience (PPIM)
ppim_predictability: HIGH — every decision the platform makes is gated on a measurable completeness score, not on whatever the operator happened to upload
ppim_economics: pre-empts entire classes of wrong-answer cost (LLM tokens spent on incomplete corpora, operator-trust loss, downstream re-work)
ppim_brand_dimension: trust + intelligence-utilization
applies_to:
  - intelligence-silo (context elicitation state + coverage scoring + recursive-learning event stream)
  - gigaton-ui-system (Documentation Ingest page + onboarding chat surface extension; local-machine source; manual file/folder add; elicitation drawer)
  - decision-engine (consumes coverage_score as a precondition gate before producing decisions)
  - gigaton-gateway (routes new `/v1/context/*` endpoints; stamps coverage_score onto attribution_chain)
  - master-knowledge-base (this spec + Q&A runbook Phase 0.5 addendum + doctrine memory)
cross_refs:
  - decisions/2026-05-25_architecture_decisions_log.md (INTEL-1 Wave 2 redefinition, INTEL-2 meta-doctrine, PAYOUT-1)
  - ~/.claude/projects/-Users-admin/memory/intel_3_no_static_weights_algorithmic_determination_2026_05_26.md (INTEL-3 — this layer's thresholds + weights are INTEL-3-compliant seeds-with-bounds)
  - docs/architecture/2026_05_25_wave2_intelligence_layer_ti_agent_matrix.md (the /intelligence surface this layer feeds)
  - runbooks/2026_05_25_intelligence_qa_on_ingested_files.md (Q&A pipeline — Phase 0.5 addendum extends this)
  - foundational_goal_gigaton_engineered_brand_experience (PPIM doctrine — context completeness is a PPIM precondition)
  - foundational_modular_replication_via_input_substitution (the 7×7 schema is itself input-substitutable across operators)
  - ~/.claude/skills/ethnographic-research/SKILL.md (the 5 frames this layer projects)
  - chatgpt-conversations/gigaton-threads/ChatGPT MD -Proof of Action Influence Trust.md (the 7-stages × ≤7-questions × ≤7-options schema origin)
  - chatgpt-conversations/gigaton-threads/ChatGPT MD -Onboarding and API Key.md (operator-side origin of the 7-questions pattern)
  - documentation_ingest_feature_spec (source-collection surface this layer wraps)
  - onboarding_workflow_v1_completion_verified_2026_05_22 (10-stage onboarding gets 7×7 question schema layered on)
---

# Context Gathering Completeness Layer — Wave 2 Foundational Substrate

## 0. TL;DR

Every Gigaton surface that asks an operator for context (Documentation Ingest, onboarding chat, the `/intelligence` query box, any future "tell us about your X" form) must, by design, **measure how complete that context is** against the decision or answer the operator is about to ask for — and **refuse to produce a decision below a configurable completeness threshold**. Default at launch: **block below 80 %, produce-with-caveat between 60–80 %, produce-clean ≥ 80 %**. Per-operator thresholds adapt over time based on observed (coverage-at-decision-time × decision-outcome-quality) signal. The layer adds four net-new capabilities (local-machine source via Chromium File System Access API; manual file/folder add; an ethnographic-frame-driven 7×7 elicitation engine; coverage scoring) plus one cross-cutting hook that feeds operator answers back into the silo's recursive learning loop. Sequences **BEFORE** the Q&A pipeline build (Q&A without this gate is LLM-flavored RAG; with this gate Q&A is decision-quality-bounded).

---

## 1. Origin

User directive 2026-05-26 (verbatim, post-OAuth-publish smoke test):

> "user should be suggested local machine search access + ability to manually add folders & files + input instructions based on human management + ethnographic & 7 questions logic + additional gigaton intelligence identified as relevant to ensure all context possible > required to achieve decisions & answers to questions are completed + integrated into the recursive learning loop"

Decoded into requirements:

1. **Source palette expansion.** Beyond Drive: local-machine search + manual file/folder add as first-class operator-facing options.
2. **Intelligent input instructions.** The elicitation prompts surfaced to the operator are not free-text "describe your business"; they are structured by (a) human management lens (Self-Engineered HR), (b) ethnographic 5-frames, (c) Todd's 7×7×7 question schema, (d) other relevant Gigaton intelligence (first-principles, prior decisions, adjacent operator patterns).
3. **Completeness guarantee.** Decisions/answers are produced **only after** all context POSSIBLE is gathered (or threshold met) — not whatever happened to arrive.
4. **Recursive learning loop integration.** Operator answers persist as structured intent, embed into the silo's semantic memory, and replay into future prompt selection (which ethnographic frames + 7×7 questions to ask THIS operator next, given everything we've learned).

This document operationalizes that directive into an implementable architecture.

---

## 2. Doctrine (the load-bearing claim)

**Context completeness is a precondition of decision quality, not a byproduct of it.**

Corollary 1: A surface that produces a decision without measuring whether it had enough context is **lying about confidence**.

Corollary 2: The right cost model for context gathering is "spend whatever it takes here to avoid the *much* larger cost of producing a wrong decision downstream." LLM tokens spent on incomplete corpora are not free — they incur token cost AND operator-trust cost AND re-work cost. Trustworthy-tokens-on-complete-corpora > many-tokens-on-incomplete-corpora.

Corollary 3: Coverage is decision-relative, not corpus-relative. A 100 %-coverage corpus for one decision can be 12 % coverage for another. The layer's job is to know which decision is being asked and score against THAT decision's required-categories.

Corollary 4 (adaptive): Operators who repeatedly produce good decisions at lower coverage have demonstrated calibration; their threshold lowers. Operators who produce poor decisions at high coverage are over-confident; their threshold rises. The default 80 / 60 is a launch posture, not a fixed law.

---

## 3. Net-new capabilities

### Capability 1 — Local machine source connector

**Mechanism:** Chromium File System Access API (`window.showDirectoryPicker()` + `FileSystemDirectoryHandle`).

**Trade-off accepted:** Chrome / Edge / Brave / Opera only. Safari + Firefox users see a "Local search requires Chromium-based browser" notice with a Drive-only fallback. Acceptable because (a) operator-side power-users skew Chromium, (b) future Tauri desktop sidecar can backfill non-Chromium without rearchitecting.

**Flow:**
1. Operator clicks "Connect local folder" → browser prompts for directory selection.
2. FE walks the tree (depth-bounded, default 4 levels), hashes file contents client-side (SHA-256), filters by configurable extension allowlist (`.md, .pdf, .docx, .txt, .json, .yaml, .html` default).
3. FE uploads file payloads via existing silo `/v1/sources/upload-direct` (new endpoint — see §6) with `source_kind=local_machine`, includes path within the picked directory as relative path.
4. Silo treats them identically to Drive sources downstream (chunk → embed → categorize into canonical bundle).
5. **Permission persistence:** the `FileSystemDirectoryHandle` is `idb`-cached for re-sync; operator can disconnect or trigger manual re-walk.
6. **No silo-side filesystem access ever.** All file movement is browser → silo over HTTPS; silo never touches the operator's disk.

**Out of scope for v1:** filesystem watch (live re-sync on file change). Operator triggers re-sync manually or via nightly sync wake-up.

### Capability 2 — Manual file/folder add (drag-drop + picker)

**Beyond Drive-Picker, beyond local-machine:** direct one-shot add. Useful when the file isn't in Drive yet (PDF the operator just got via email; screenshot they took 2 min ago; transcript pasted from another tool).

**Surfaces:**
- Drag-drop zone on Documentation Ingest page.
- File picker button (`<input type="file" multiple>`) as fallback.
- "Add via URL" — paste a public URL, silo fetches.

**Flow:** identical to Capability 1 post-upload (chunk/embed/categorize).

**Tagged separately:** `source_kind=manual_upload` so the recursive loop can detect "operator manually added this because it wasn't elsewhere" — that's a signal about gap in the operator's own connectors.

### Capability 3 — Context-elicitation prompt layer (the 7×7 engine)

**The load-bearing capability.** This is what distinguishes the layer from "just better file upload."

**Inputs to the engine:**
- Operator's current decision/answer context (what they're about to ask `/intelligence` for, or what stage of onboarding they're in).
- Operator's current corpus coverage by category.
- Operator's prior elicitation answers (recursive — see §10).
- Ethnographic frames projection of current state (which frames are under-evidenced for this operator).
- Gigaton first-principles drift check (which principles haven't been confirmed for this operator's context).

**Engine output:** the **next K elicitation prompts** to render (K = 1 in chat mode, K = 5-7 in form mode), each a `(stage, question, options[])` tuple drawn from the 7-stages × ≤7-questions × ≤7-options schema.

**The 7-stage schema** (from origin doc):

| Stage | Purpose | Elicitation focus |
|---|---|---|
| A. Summary | Surface the operator's *naming* of the situation | Mental-model frame 1 (state variables: cognitive) |
| B. Purpose | Why this matters to the operator | Frame 2 (trigger events: which push/pull) |
| C. Goal | The outcome state being optimized for | Frame 4 (behavioral probabilities: what they expect of themselves) |
| D. **WHY (7 questions)** | The load-bearing stage — surfaces latent assumptions, constraints, mental-models | Frames 1+3 (state + conditional dependencies) — projected through the 5 ethnographic frames |
| E. Constraints | Hard limits the answer must respect | Frame 3 (conditionals: capability + permission + sequence + confidence) |
| F. Objectives | What "success" looks like operationally | Frame 5 (decision pathways: how they'll know they chose right) |
| G. Tasks/Prompts | Output stage — produced BY the engine, not asked OF the operator | (Engine generates this; operator confirms) |

**WHY stage detail (Stage D, ≤7 questions):** The seven questions are not fixed — they are dynamically selected from a question pool by the engine based on:
- Which ethnographic frames are under-evidenced
- Which first-principles haven't been confirmed for this operator's context
- Adjacent-operator pattern matches (other operators in similar verticals revealed Y as a load-bearing assumption — ask about Y)

This makes the engine **lazy-expandable**: the question pool grows with operator usage; each question is tagged with `frame`, `principle`, `vertical`, `decision_type` for retrieval.

**Cognitive load discipline:** ≤7 questions per stage × ≤7 options per question is non-negotiable. Per Miller's Law + Todd's documented constraint. If a stage needs >7 questions, split into sub-stages.

### Capability 4 — Coverage scoring

**Inputs:**
- Required-categories for the about-to-be-asked decision (from a `decision_type → required_categories[]` map, lazy-expandable).
- Operator's corpus state (which categories are populated, depth of evidence per category).
- Operator's elicitation answers for the WHY-7 (these count as evidence too).

**Output:** `coverage_score ∈ [0.0, 1.0]` with per-category breakdown.

**Formula (launch):**
```
coverage_score = Σ (required_category[i].weight × evidence_depth_score(category[i])) / Σ (required_category[i].weight)

evidence_depth_score(cat) = min(1.0, (corpus_hits(cat) / 5) × 0.6  +  (why7_answers_tagged_to(cat) / 3) × 0.4)
```

Numbers tunable; rationale:
- 5 corpus hits = saturation per category (diminishing returns past).
- 3 WHY-7 answers tagged to a category = saturation (3 reveals the pattern).
- 60 / 40 weighting favors corpus evidence over self-report (corpus is harder to fake).

**Threshold semantics (launch defaults):**
- `coverage ≥ 0.80` → **clean answer** (no UI caveat, full confidence stamped).
- `0.60 ≤ coverage < 0.80` → **caveat answer** (UI flag: "Based on partial context — would you like to add more before deciding?"). Engine still produces.
- `coverage < 0.60` → **block** (UI: "More context needed. Here are the 3 highest-impact questions/sources to add first." → renders elicitation drawer). Engine refuses.

**Adaptive adjustment (post-launch, builds on §10):** per-operator threshold drifts via:
```
new_threshold = old_threshold + α × (target_quality - observed_quality)
```
where `observed_quality` is the rolling-30d EWMA of decision-outcome-quality for that operator's decisions, `α = 0.05` (slow drift), target_quality = 0.85. Cap drift to ± 0.15 from launch defaults.

### Cross-cutting — Recursive learning loop hook

Every operator answer + every produced decision + every observed outcome lands as a structured event in the silo's event stream:

| Event | Producer | Consumer |
|---|---|---|
| `operator_elicitation_answer` | Capability 3 engine | Embedder → semantic memory; Coverage scorer; Adaptive threshold drift |
| `coverage_score_computed` | Capability 4 scorer | Decision-engine (precondition gate); Telemetry |
| `decision_produced_with_coverage` | Decision-engine | Outcome tracker; Adaptive threshold drift |
| `decision_outcome_observed` | Outcome tracker | Adaptive threshold drift; Question-pool re-ranking |
| `question_pool_used` | Engine | Question-pool re-ranking ("which questions correlated with high-quality decisions?") |
| `source_added` | Capability 1/2 | Coverage scorer; Embedder |

The loop closes monthly: an analyst-job re-ranks the question pool (which questions correlate with high-decision-quality outcomes) and re-weights the `required_category` map (which categories' presence correlates with high-decision-quality outcomes).

---

## 4. Data model

New tables (intelligence-silo Postgres, migration `006_context_completeness.sql`):

```sql
-- The decision-type → required-categories map (lazy-expandable doctrine)
CREATE TABLE decision_required_categories (
  decision_type        TEXT PRIMARY KEY,
  required_categories  JSONB NOT NULL,  -- [{category, weight}]
  authored_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
  authored_by          TEXT NOT NULL,
  notes                TEXT
);

-- The dynamic question pool — grows with usage
CREATE TABLE elicitation_questions (
  question_id        UUID PRIMARY KEY,
  stage              TEXT NOT NULL,  -- A..G per §3 Capability 3
  prompt_text        TEXT NOT NULL,
  options            JSONB,           -- null for free-text; [{label, value}] for constrained
  frame_tags         TEXT[] NOT NULL DEFAULT '{}',  -- ethnographic frames this question elicits
  principle_tags     TEXT[] NOT NULL DEFAULT '{}',  -- first-principles this question confirms
  vertical_tags      TEXT[] NOT NULL DEFAULT '{}',  -- industries/verticals where relevant
  decision_type_tags TEXT[] NOT NULL DEFAULT '{}',  -- decisions this question is most predictive for
  usage_count        INT NOT NULL DEFAULT 0,
  quality_correlation REAL,  -- updated by monthly re-rank job
  created_at         TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Operator's elicitation history (one row per (operator, question) — overwrite on re-answer)
CREATE TABLE operator_elicitation_answers (
  operator_id        TEXT NOT NULL,
  question_id        UUID NOT NULL REFERENCES elicitation_questions(question_id),
  stage              TEXT NOT NULL,
  answer_value       JSONB NOT NULL,
  category_tags      TEXT[] NOT NULL DEFAULT '{}',  -- which required_categories this answer evidences
  answered_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (operator_id, question_id)
);
CREATE INDEX idx_op_elicit_op ON operator_elicitation_answers(operator_id);

-- Per-operator adaptive thresholds (default seed = 0.80 / 0.60)
CREATE TABLE operator_coverage_thresholds (
  operator_id        TEXT PRIMARY KEY,
  block_below        REAL NOT NULL DEFAULT 0.60,
  caveat_below       REAL NOT NULL DEFAULT 0.80,
  observed_quality_ewma REAL,
  last_drift_at      TIMESTAMPTZ,
  updated_at         TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Append-only event stream for the recursive loop (see §3 cross-cutting)
CREATE TABLE context_loop_events (
  event_id           UUID PRIMARY KEY,
  event_type         TEXT NOT NULL,  -- see §3 cross-cutting table
  operator_id        TEXT NOT NULL,
  payload            JSONB NOT NULL,
  emitted_at         TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_cle_op_type ON context_loop_events(operator_id, event_type, emitted_at DESC);
```

PPIM multi-axis tags on every event row (per `[[foundational_modular_replication_via_input_substitution]]`): industry, sub-vertical, geo, regime, segment, lifecycle, provenance, modality.

---

## 5. UI surfaces

### 5.1 Documentation Ingest page (extension)

Layout adds three new sections above existing "Folder subscriptions":

```
+----------------------------------------------------+
| Connected sources                                  |
|  - Google Drive accounts (existing)               |
|  - Local folders (NEW — Chromium-only)            |
|  - Manual uploads (NEW — drag-drop zone)          |
+----------------------------------------------------+
| Context completeness                               |
|  [████████░░] 78% — caveat zone                   |
|  Missing categories:                               |
|   • Operator value proposition (0/5 hits)         |
|   • Pricing model (1/5 hits — partial)            |
|   • Competitive landscape (0/5 hits)              |
|  [Answer 3 questions to raise to 85%]  ←drawer    |
+----------------------------------------------------+
| Folder subscriptions (existing, unchanged)        |
+----------------------------------------------------+
```

### 5.2 Elicitation drawer

Slides in from right when operator clicks "Answer K questions" or when a `/intelligence` query is blocked by coverage. Renders one stage at a time, ≤7 questions visible, ≤7 options per question. Submit advances to next stage. "Save draft & exit" persists partial answers.

### 5.3 `/intelligence` query box (Wave 2 INTEL-1 surface)

Before submitting a query, the FE calls `POST /v1/context/coverage` with `(operator_id, decision_type)`. Three render modes:

- `≥ 0.80` — clean. Submit goes through.
- `0.60–0.80` — caveat banner above the query box: "I have ~70% of what I'd ideally know. Want me to answer with caveat, or add context first?" Two buttons.
- `< 0.60` — block. Submit button is disabled with reason: "Need more context. Open elicitation →"

### 5.4 Onboarding chat (Stage rewrite)

The 10-stage onboarding manifest (`master-knowledge-base/manifests/onboarding_v1.yaml`) gets a parallel-track 7×7 elicitation overlay. Each existing onboarding stage maps to one or more 7×7 stages. Implementation: the ChatOnboardingOrchestrator consumes from the same elicitation engine as the drawer.

---

## 6. API contracts (silo)

```
POST /v1/context/coverage
  body: { operator_id, decision_type }
  returns: {
    coverage_score: 0.78,
    breakdown: [{category, weight, evidence_depth, hits, why7_hits}, ...],
    threshold_zone: "caveat",   // clean | caveat | block
    next_questions: [...],       // top 3-5 questions to raise score most
    next_sources: [...]          // top 3 categories to add sources for
  }

POST /v1/context/elicit/next
  body: { operator_id, decision_type, max_questions, mode: "chat"|"form" }
  returns: { stage, questions: [{question_id, prompt, options}] }

POST /v1/context/elicit/answer
  body: { operator_id, question_id, answer_value }
  returns: { accepted, new_coverage_score }

POST /v1/sources/upload-direct       (Capabilities 1 + 2)
  multipart: file payload + source_kind + relative_path + sha256
  returns: { source_id, accepted, dedup_status }

PATCH /v1/operators/{operator_id}/coverage-thresholds
  body: { block_below?, caveat_below? }   // operator self-tune; admin override; or system-adaptive
  returns: updated thresholds
```

All endpoints route via `gigaton-gateway` (`/v1/context/*` added to `routing_table.py` mapping to `INTELLIGENCE_SILO_URL`). PPIM `attribution_chain` stamped per the existing middleware.

---

## 7. Build sequence — 6 PRs

Ordered for incremental value + minimal blast radius. Each PR is independently mergeable and ships value standalone.

### PR-1 (intelligence-silo) — Schema + endpoints + coverage scorer (~2 days)
- Migration `006_context_completeness.sql`
- Models + repository for the 4 new tables
- Coverage scorer module (`core/context/coverage.py`)
- Elicitation engine module (`core/context/elicit.py`) — initial heuristic: pool-based selection by frame coverage; ML re-rank later
- API routes `/v1/context/*` + `/v1/sources/upload-direct`
- Seed data: 30-50 questions across the 7 stages, tagged
- Seed data: `decision_required_categories` for 5 launch decision-types
- Unit tests + integration tests against test Postgres
- **Sibling-respect:** does NOT touch agent_roles, skill_vectors, or Society-of-Minds — strictly additive

### PR-2 (gigaton-gateway) — Route + attribution_chain stamping (~30 min)
- Add `/v1/context/` to `api/routing_table.py` → `INTELLIGENCE_SILO_URL`
- Extend attribution_chain middleware to stamp `coverage_score` when produced
- One test

### PR-3 (gigaton-ui-system) — Coverage panel + drawer (~1 day)
- New component: `components/context/CoverageWidget.tsx`
- New component: `components/context/ElicitationDrawer.tsx`
- New service: `services/contextClient.ts` (calls `/v1/context/*` via gateway base URL)
- Wire into `pages/DocumentationIngestPage.tsx` (above folder subscriptions)
- Wire into `pages/ChatPage.tsx` (pre-submit coverage check)
- Tests: 5 component tests + 2 service tests

### PR-4 (gigaton-ui-system) — Local-folder + manual-upload sources (~1 day)
- New component: `components/connectors/LocalFolderConnector.tsx` (Chromium File System Access API; gracefully degrades with "Chromium required" notice)
- New component: `components/connectors/ManualUploadZone.tsx` (drag-drop + file picker + URL paste)
- Both call `POST /v1/sources/upload-direct`
- Wire into Documentation Ingest page
- Tests: feature-detect tests for FSA API; mocked upload flow

### PR-5 (decision-engine) — Precondition gate (~30 min)
- `/v1/intelligence/classify` and other decision-producing endpoints accept optional `coverage_score` parameter and reject if `< caveat_below` (return 412 Precondition Failed with structured guidance)
- Pass-through for callers that haven't migrated yet (warn-log)
- Tests

### PR-6 (master-knowledge-base) — Monthly re-rank job spec + onboarding overlay (~1 day)
- New runbook: `runbooks/2026_06_10_monthly_question_pool_rerank_job.md` (operates on `context_loop_events` + `operator_elicitation_answers`; produces updated `quality_correlation` on `elicitation_questions` and re-weights `decision_required_categories`)
- Onboarding overlay design at `docs/architecture/2026_05_26_onboarding_v1_7x7_overlay.md` — maps existing 10 onboarding stages → 7×7 stages; ChatOnboardingOrchestrator consumes from elicitation engine
- Cross-link from `manifests/onboarding_v1.yaml`

### Dispatch order
PR-1 ships first (foundation). PR-2 immediately after (so PR-3 has gateway routing). PR-3 + PR-4 can ship in parallel. PR-5 ships after PR-3 (so the gate has UI to send users to). PR-6 ships last (operates on accumulated event data; needs ≥ a few weeks of production traffic to be meaningful — write the spec now, implement after Wave 2 Week 4).

---

## 8. Sequencing decision — BEFORE Q&A pipeline

The Q&A pipeline runbook (`runbooks/2026_05_25_intelligence_qa_on_ingested_files.md`) defines a 5-phase build. Without this layer, Phase 1 chat→silo Q&A produces answers from whatever the operator happened to ingest — i.e., LLM-flavored RAG with citation surface.

With this layer, every chat→silo Q&A goes through `POST /v1/context/coverage` first. The Q&A pipeline becomes **decision-quality-bounded**: an answer is produced if and only if the corpus + elicitation answers crossed the threshold for that question's decision-type.

Therefore: **this layer's PR-1 + PR-3 + PR-5 ship before the Q&A pipeline's Phase 1.** A Phase 0.5 addendum to the Q&A runbook formalizes the gate. See `runbooks/2026_05_25_intelligence_qa_on_ingested_files_phase_0_5_addendum.md`.

---

## 9. Adaptive threshold drift — worked example

Operator `acme-real-estate` launches at default thresholds (0.60 block, 0.80 caveat).

Over 30 days:
- 12 decisions produced at coverage ∈ [0.85, 0.95] (clean zone)
- 8 decisions produced at coverage ∈ [0.65, 0.79] (caveat zone)
- 6 decision outcomes flagged "great" by operator (outcome-quality 0.92 avg)
- 14 decision outcomes flagged "acceptable" (outcome-quality 0.72 avg)

Rolling EWMA `observed_quality` ≈ 0.79. Target 0.85. Delta = -0.06 (observed below target → operator over-confident → raise threshold).

Drift step: `caveat_below += 0.05 × 0.06 = +0.003`. New `caveat_below = 0.803`.

Effect: next month, coverage 0.79 becomes block-zone for this operator. Forces more elicitation, expected outcome-quality rises. EWMA re-evaluates.

Cap at ± 0.15 from launch (so operator can't drift to >0.95 or <0.45).

---

## 10. Recursive learning loop — implementation

Three feedback paths, all driven from `context_loop_events`:

### 10.1 Embedder loop (immediate, sub-minute)

Every `operator_elicitation_answer` event triggers an embedder run that adds the answer text to semantic memory tagged with `(operator_id, frame_tags, principle_tags)`. Future retrieval for THIS operator now includes their own elicitation answers. This is what makes the system "remember what the operator already told it."

### 10.2 Question-pool re-rank (monthly, batch)

Cron job (Cloud Scheduler → silo `/v1/admin/rerank-questions`):
- For each question, compute Pearson correlation between "question was used in elicitation" and "decision-outcome-quality" across all operators.
- Update `elicitation_questions.quality_correlation`.
- Top-decile questions surface earlier in elicitation; bottom-decile drop to "only-if-asked-for."
- New questions auto-generated by an LLM pass on the silo logs of operator free-text answers — surfaced for admin review before activation.

### 10.3 Adaptive threshold drift (continuous)

On every `decision_outcome_observed` event, the operator's EWMA updates, and the drift step runs (per §9). Drift events are themselves logged so we can audit "did the system over-correct?"

---

## 11. Sibling-respect protocol

This work was authored 2026-05-26 evening. At the time of authorship:
- A sibling Claude session (`6e6b0670...`) claimed branch `feat/context-gathering-completeness-layer-2026-05-26` (different name from this PR's branch `feat/context-completeness-layer-2026-05-26`).
- A sibling session was actively building `intelligence-silo` Wave 2 substrate (PR #42, +2 min before this work began).
- A sibling session was actively building `decision-engine` semantic classifier (PR #84 follow-on).

**This spec does not touch:**
- `agent_roles` or `skill_vectors` tables (intel-silo sibling territory).
- The Society-of-Minds orchestrator (intel-silo Wave 2 substrate).
- `/v1/intelligence/classify` internals (decision-engine sibling territory).
- The Ti Agent Matrix dispatch — this layer is upstream and feeds into it.

When PR-1 ships, it adds **new** tables + **new** endpoints. No existing schemas touched. Migration `006_context_completeness.sql` runs after sibling-added migrations (currently up to `005`).

---

## 12. Open decisions deferred to operator (max 3)

1. **Question pool seed source.** Launch with 30-50 hand-authored questions, or generate via LLM pass on Todd's existing onboarding scripts + ChatGPT-thread questions? Default: LLM-generate + Todd-review-100 before activation.
2. **Local-machine source for non-Chromium browsers.** Tauri sidecar (cross-platform, ~5 day build), or accept "Chromium-only" indefinitely? Default: Chromium-only at launch; revisit when first non-Chromium operator complains.
3. **Coverage refusal UX.** When < 0.60 blocks a query, do we (a) show only the next 3 questions, (b) show all gaps, (c) let operator override with "answer anyway" button? Default: (a) for cognitive-load discipline + (c) with prominent telemetry on override-rate.

These defaults fire 2026-06-08 (2 weeks post-merge) if no response, per INTEL-2 META-DOCTRINE.

---

## 13. Risks + doctrine mitigations

| Risk | Mitigation |
|---|---|
| Operators bounce off the elicitation drawer ("too many questions"). | ≤7 per stage hard cap; "Save draft & exit"; coverage-score progress bar shows movement; questions ranked by quality-correlation so highest-impact surface first. |
| LLM-generated questions are low quality. | Todd-review-100 gate before activation; monthly re-rank surfaces bad questions for retirement. |
| Coverage gaming (operator answers garbage to clear the gate). | `evidence_depth_score` weights corpus 60 / why7 40 — can't game by self-report alone. Outcome-quality EWMA exposes gaming over time (high coverage + low outcomes ⇒ raise threshold ⇒ corpus required). |
| Adaptive threshold drift overshoots. | ± 0.15 cap from launch defaults; α = 0.05 (slow); drift events logged for audit. |
| Capability 1 (FSA) breaks across Chromium versions. | Feature-detect at every interaction; fall back to manual upload (Capability 2) with notice. |
| Recursive loop creates a "filter bubble" where the system stops asking questions outside the operator's prior frame. | Question-pool re-rank uses cross-operator correlation, not within-operator. New questions injected from LLM pass keep the pool from collapsing. |

---

## 13.5. INTEL-3 alignment — every numeric weight in this spec is a seed-with-bounds

Per INTEL-3 doctrine (locked 2026-05-26 EOD: "no weights will be static and determined as a function of algorithm > real time adjustments"), every `0.X` / `X%` / threshold constant in this spec is a **seed with bounded range + algorithm-pending marker**, not a target. The seeds activate the system at launch; the algorithm replaces them as Phase 2 of INTEL-3 ships (week of 2026-06-02).

### Seed registry for this layer

| Symbol | Seed | Bounds | Algorithm-pending? | Purpose |
|---|---|---|---|---|
| `block_below` | `0.60` | `[0.45, 0.75]` | YES (per-operator drift on outcome-quality EWMA) | Below this, decision refused |
| `caveat_below` | `0.80` | `[0.65, 0.95]` | YES (per-operator drift on outcome-quality EWMA) | Below this, decision produces with caveat |
| Corpus/why7 weighting in `evidence_depth_score` | `0.60 / 0.40` | `[0.50, 0.80] / [0.20, 0.50]` | YES (Phase 2: per-decision-type tuning) | How much corpus evidence vs self-report counts |
| Corpus saturation hits | `5` | `[3, 10]` | YES (Phase 2: per-category tuning — some categories saturate faster) | Diminishing returns past this many hits |
| WHY-7 saturation answers | `3` | `[2, 6]` | YES (Phase 2: per-category tuning) | Diminishing returns past this many answers |
| EWMA drift rate α | `0.05` | `[0.02, 0.10]` | YES (Phase 2: adapt α to operator's decision-volume — high-volume operators can move faster) | How fast threshold drifts on observed outcomes |
| EWMA target quality | `0.85` | `[0.80, 0.92]` | YES (Phase 2: cross-operator benchmark vs absolute) | What "good decisions" means for drift trajectory |
| Drift cap from launch defaults | `± 0.15` | `[0.10, 0.25]` | YES (Phase 2: tighten for new operators, loosen for veterans) | Protect against algorithm overcorrection |
| Local-folder tree depth limit | `4` levels | `[2, 8]` | NO — binary policy (cognitive/perf safeguard, not a weight) | Walk depth on local-folder picker |
| Coverage event recursion-loop cadence | monthly re-rank | `[weekly, quarterly]` | YES (Phase 2: trigger by event volume, not calendar) | When question-pool re-rank runs |

### Exempt from INTEL-3 (binary policy or hard floor)

- **`bypass_coverage_gate` flag** — binary admin/debug toggle, not a weight.
- **Coverage zone state machine** (clean / caveat / block) — binary state classification, not a weight.
- **≤ 7 questions per stage cap** — Miller's-Law-grounded cognitive policy, locked. Hard ceiling, not a weight.
- **Chromium FSA API constraint** — capability constraint, not a weight.

### How the algorithm replaces seeds

Per INTEL-3 §38-44, every seed becomes a `WeightComputed(name, value, computed_at, inputs, model_version)` event-driven resolution:

```
function resolve_weight(name, operator_id, decision_type, event_context):
    if WEIGHT_IS_EXEMPT(name): return STATIC_POLICY_VALUE(name)
    if PHASE_2_ALGORITHM_READY(name):
        value = compute(name, operator_state(operator_id), market_state(decision_type),
                        performance_signal(operator_id, decision_type, last_30d),
                        variance_from_expected(operator_id),
                        cross_operator_benchmark_if_authorized(decision_type))
        emit_event(WeightComputed(name=name, value=value, ...))
        return clamp(value, bounds_of(name))
    else:
        emit_event(WeightSourcedFromSeed(name=name, seed=SEED[name], ...))
        return SEED[name]
```

UI / billing / scoring read the *resolved* value, never the seed directly. This makes seed-vs-computed observable for audit + Wave 2 variance display.

### Build-sequence impact

PR-1 ships **all seed values + bounded ranges + the WeightSourcedFromSeed emission pattern**. The seed values activate the layer at launch. PR-5's decision-engine precondition gate calls `resolve_weight()` instead of reading thresholds directly. Phase 2 of INTEL-3 (decision-engine team, week of 2026-06-02) replaces the seed lookups with computed values per weight.

This means: **the layer is INTEL-3-compliant at launch, not retrofitted**. Seeds operate the system today; the algorithm makes them right per-event when INTEL-3 Phase 2 ships.

---

## 14. PPIM signature (this doc)

- **ppim_outcome_quality:** every decision produced by the platform carries a coverage_score and threshold-zone marker; downstream telemetry can pair coverage with outcome and audit the entire chain.
- **ppim_predictability:** HIGH — refusing to decide below threshold is the load-bearing predictability move. We are now under-confident on incomplete data instead of falsely-confident.
- **ppim_economics:** estimated 30-50 % reduction in wrong-answer LLM cost + downstream re-work cost. Token cost on context elicitation is small (~ 1-2 K tokens / operator-month average).
- **ppim_brand_dimension:** trust + intelligence-utilization (per INTEL-1).
- **ppim_interaction:** every operator query touches this layer; it is the *first* surface every interaction passes through.
