# Gigaton Intelligence-Utilized Q&A on Ingested Files — Implementation Plan

**Status:** SPEC — not yet implemented
**Authored:** 2026-05-25
**Author:** planning subagent (`af80136f42c47410a`), reviewed by Claude main session
**Repos in scope:** `intelligence-silo`, `MD Files/intelligence-engine` (chat gateway), `gigaton-ui-system`, `master-knowledge-base`
**Effort estimate:** ~7 engineering days, 4-5 PRs

---

## 1. Origin

User directive (verbatim, 2026-05-25 session):

> "ensure that gigaton intelligence is utilized to answer questions about files after ingestion > analysis to glean all possible context utilizing the ethnographic research skills + gigaton principles & additional research where required"

This plan operationalizes that into a concrete pipeline so that after a document is ingested into intelligence-silo (currently lands as text in semantic memory), the operator can ask questions in chat (`/chat`) and get answers that:

1. Cite specific source files from the ingest folder
2. Use the silo's Society-of-Minds reasoning (Perceiver → Analyst → Critic → Synthesizer) rather than flat RAG retrieval
3. Apply "ethnographic research skills" — interpret cultural / behavioral / contextual nuance, not just literal text matching
4. Honor "Gigaton principles" — `GIGATON_CANONICAL_FIRST_PRINCIPLES.md` (15 principles, 8 ethos filters, 12 anti-patterns)
5. Pull in external research where the ingested files have gaps (silo has web-search backfill via EO `self_heal.spawn_research_task`)

---

## 2. Current State Survey

### What already exists

| Capability | Location | State |
|---|---|---|
| Drive ingest → chunk → embed → FAISS | `intelligence-silo/core/api.py` `/memory/ingest` (line ~372), `core/memory/embedder.py`, `core/memory/semantic.py` | Working. Stores `text/heading/source/chunk_index/author` with each chunk, source-tagged to a `sources` row. |
| Plain-text semantic search with citations | `core/api.py` `/memory/search` (line ~443) | Working. Returns `text + source + heading + score + chunk_id`. This is **flat RAG**, no Society reasoning. |
| Multi-account NotebookLM-canonical Drive bundle | `core/documentation_ingest.py` | Working. Categorized files written back to a canonical Drive folder per operator. |
| Society of Minds orchestrator | `core/orchestrator/society.py`, `core/orchestrator/mind.py` | Working. `SocietyOfMinds.think()` runs PERCEIVER → ANALYST → CRITIC → SYNTHESIZER → EXECUTOR → MEMORY_KEEPER → SENTINEL. Currently driven by `/process` only, **not wired to chat Q&A**. |
| SLM matrix (6 specialists) | `core/models/matrix.py` | Working. `SocietyOfMinds.think()` calls `matrix.infer(input_ids, query_embedding=…)`. |
| Memory hierarchy (working/episodic/semantic/procedural) | `core/memory/hierarchy.py` | Working. `memory.query_flat(query_embedding, top_k=5)` is what the society sees as context. |
| EO (Ethnographic Objects) + self-heal loop | `core/eo/models.py`, `core/eo/router.py`, `core/eo/self_heal.py`, `core/eo/endpoints.py` | Working. `self_heal.spawn_research_task(..., source_preference="web_search")` is the web-research backfill primitive. |
| Chat gateway w/ middleware | `MD Files/intelligence-engine/api/engine_middleware.py`, `api/routes/chat.py`, endpoint `POST /api/chat/message/stream` on port 8002 | Working. Classifies intent/entity/depth, derives a 3-tier trust proxy, assembles `EngineInsight`. **Does not call silo.** |
| Chat UI | `gigaton-ui-system/pages/ChatPage.tsx` + `services/intelligenceSiloClient.ts` | Working but `intelligenceSiloClient.ts` is **not invoked from `ChatPage.tsx`** — chat goes straight to `/api/chat/message/stream`. |
| Canonical doctrine doc | `decision-engine/drift_sentinel/GIGATON_CANONICAL_FIRST_PRINCIPLES.md` (15 principles, 8 ethos filters, 12 anti-patterns) | Working; **not loaded into chat prompt assembly today**. |
| Ethnographic research doctrine prose | `master-knowledge-base/chatgpt-conversations/gigaton-threads/ChatGPT MD -Ethnographic research explained.md` + `…Ethnographic Research and Optimization.md` | Prose only — **no machine-readable skill or schema**. |
| Web-search backfill policy | `~/.claude/projects/-Users-admin/memory/feedback_web_search_for_data_backfill.md` | Policy memo only — wired into EO self-heal but **not into chat answer generation**. |

### What's missing

- **No bridge** from `POST /api/chat/message/stream` to `intelligence-silo` `/memory/search` or `/process`. Chat answers today are LLM-only with the engine_middleware classification tacked on — no document grounding, no Society reasoning, no citation surface.
- **No "ethnographic skill"** file. The doctrine exists as ChatGPT export prose. There is no `~/.claude/skills/ethnographic-research/SKILL.md` and no module the silo can import to project ethnographic frames onto retrieval.
- **No principles filter** in the answer path. `GIGATON_CANONICAL_FIRST_PRINCIPLES.md` is the drift anchor for code review, but no runtime hook checks an answer against it.
- **No web-research backfill on Q&A**. EO has `self_heal.spawn_research_task` for low-confidence objects, but Q&A does not detect retrieval gaps and trigger backfill.
- **No "ingested-corpus Q&A" endpoint** on the silo. `/memory/search` is bare top-k; `/process` is generic Society but does not assemble a citation-bearing answer.

---

## 3. Gap Analysis

| Gap | Concrete missing artifact |
|---|---|
| G1. Q&A endpoint on silo | `POST /v1/qa/ask` returning `{answer, citations[], society_trace, confidence, principles_check, research_backfill[]}` |
| G2. Society-driven RAG | `core/orchestrator/qa_pipeline.py` that wraps `SocietyOfMinds.deliberate()` around a retrieval step; injects citations into the Synthesizer's verdict |
| G3. Ethnographic skill | `~/.claude/skills/ethnographic-research/SKILL.md` + machine-readable frames in `intelligence-silo/core/intelligence/ethnographic_frames.py` (state vars / triggers / mental models / latent needs) used by the Perceiver |
| G4. Principles filter | `intelligence-silo/core/intelligence/principles_filter.py` — loads `GIGATON_CANONICAL_FIRST_PRINCIPLES.md`, exposes `check(answer_draft) -> {violations[], suggestions[]}`. Sentinel calls it. |
| G5. Research-backfill on retrieval gap | `core/intelligence/coverage_detector.py` — if top-k results below score floor OR ethnographic axes uncovered, the Critic spawns an `EOResearchTask` with `source_preference="web_search"` and the Synthesizer waits (or returns a "partial answer + research-in-flight" verdict) |
| G6. Chat bridge | New silo client call in `MD Files/intelligence-engine/api/routes/chat.py` (`call_silo_qa(...)`) when `engine_middleware.intent in {explanation, analytics, decision_governance, …}` OR when the operator's session has any ingested sources; falls back to plain LLM if silo is unreachable |
| G7. UI citation rendering | `gigaton-ui-system/components/chat/Citation.tsx` + `SocietyTrace.tsx`; `MessageBubble.tsx` renders an inline citation chip linked to the source file in the operator's NotebookLM bundle |

---

## 4. Architecture Proposal

```
                      ┌─────────────────────────────────────────────────────────┐
                      │  ChatPage.tsx  ──►  POST /api/chat/message/stream       │
                      └─────────────────────────────────────────────────────────┘
                                                │
                                                ▼
                  ┌────────────────────────────────────────────────────────────┐
                  │  intelligence-engine/api/routes/chat.py                    │
                  │   ├── engine_middleware  (intent/entity/depth/trust)       │
                  │   └── if intent ∈ {qa, explanation, analytics, ...}        │
                  │       AND operator has ingested sources                    │
                  │       ──► silo_client.qa_ask(question, operator_id, ...)   │
                  └────────────────────────────────────────────────────────────┘
                                                │
                                                ▼
                  ┌────────────────────────────────────────────────────────────┐
                  │  intelligence-silo  POST /v1/qa/ask                        │
                  │                                                            │
                  │   ┌──────────────────────────────────────────────────┐     │
                  │   │  qa_pipeline.answer(question, operator_id)       │     │
                  │   └──────────────────────────────────────────────────┘     │
                  │            │                                               │
                  │   (1) embed_text(question)                                 │
                  │   (2) semantic.search(query, top_k=20, filter=op)          │
                  │   (3) ethnographic_frames.project(chunks)                  │
                  │   (4) SocietyOfMinds.deliberate(                           │
                  │         input_data={question, retrieved_chunks,            │
                  │                     ethnographic_projection,               │
                  │                     operator_context},                     │
                  │         input_ids=tokens, query_embedding=qvec)            │
                  │                                                            │
                  │       PERCEIVER  ── ethnographic frame projection          │
                  │       ANALYST    ── scorer SLM re-rank + trust assessor    │
                  │       CRITIC     ── coverage_detector; if gaps, spawns     │
                  │                     self_heal.spawn_research_task          │
                  │       SYNTHESIZER── inline-citation answer assembly        │
                  │       EXECUTOR   ── (no-op for Q&A; reserved for actions)  │
                  │       MEMORY_KEEPER ── episodic record (Q + verdict)       │
                  │       SENTINEL   ── principles_filter.check(answer)        │
                  │                                                            │
                  │   (5) Fast path: return partial + research_backfill[];     │
                  │       Slow path: wait for backfill, re-synthesize          │
                  └────────────────────────────────────────────────────────────┘
                                                │
                                                ▼
                  Response shape (streamed back to chat):
                  {
                    answer: "...",
                    citations: [{source, heading, chunk_id, score, drive_file_id?, excerpt}],
                    society_trace: {minds_activated, cycle_time_ms, consensus, confidence},
                    ethnographic_frames_applied: ["mental_model", "latent_need", ...],
                    principles_check: {violations: [], ethos_flags: [...]},
                    research_backfill: [{eo_id, question, status, eta_ms}]
                  }
```

### Where each agent fires

- **Perceiver** — runs `ethnographic_frames.project(chunks)` to convert raw text excerpts into a structured ethnographic substrate (state vars, triggers, mental models, latent needs). Feeds Speech-101 encoding for downstream minds.
- **Analyst** — uses `scorer` SLM to re-rank chunks; uses `classifier` SLM to bucket chunks under canonical domains.
- **Critic** — runs `coverage_detector` (new module). If any ethnographic axis is uncovered OR no chunk crosses `min_score=0.45` for a given sub-question, emits `needs_backfill` and triggers `self_heal.spawn_research_task`.
- **Synthesizer** — composes the natural-language answer with inline `[1][2]` citation markers mapped to retrieved chunks.
- **Executor** — pass-through for plain Q&A; if the answer contains an action proposal, wraps in `<<<gigaton:action>>>` for the gignet-gated approval queue.
- **Memory Keeper** — stores `(question, answer, citations, confidence)` in episodic memory.
- **Sentinel** — runs `principles_filter.check(answer)` against `GIGATON_CANONICAL_FIRST_PRINCIPLES.md`. Hard-blocks non-negotiable violations; annotates ethos-filter flags.

### Where ethnographic skills apply

- Created as a Claude skill under `~/.claude/skills/ethnographic-research/SKILL.md` **and** mirrored as `intelligence-silo/core/intelligence/ethnographic_frames.py` so the silo runtime applies the same projection without needing Claude in the loop.
- The skill encodes five frames: (1) state variables, (2) trigger events, (3) conditional dependencies, (4) behavioral probabilities, (5) decision pathways — plus mental-model segmentation (vs. demographic).
- Perceiver tags every retrieved chunk with the frames it satisfies; Critic flags frames with zero retrieval coverage as candidates for web-backfill.

### Where the principles filter applies

- Sentinel (last in `phase_order`) calls `principles_filter.check(answer_draft, signals[])` → returns `{violations, ethos_flags, suggestions}`.
- A hard violation flips `verdict.consensus=False`; UI renders this as a red banner above the message bubble. Soft ethos flags render as amber chips.

### Where web-research backfill is triggered

- Critic phase: `coverage_detector.check(chunks, ethnographic_frames)` → if uncovered_axes ≠ ∅ OR max_score < floor, call `core/eo/self_heal.spawn_research_task(eo_or_synthetic, source_preference="web_search")`.
- Fast path: return partial answer immediately with `research_backfill[]`. Slow path (`deliberate(... wait_for_backfill=True)`): silo blocks for up to N seconds for the research task to complete, then re-runs the Synthesizer with the augmented context.

---

## 5. Implementation Phases

### Phase 1 — Doctrine + skill assets (no code in critical path)
- **Repo:** `master-knowledge-base`, `~/.claude/skills/`
- **Files (new):**
  - `~/.claude/skills/ethnographic-research/SKILL.md`
  - `~/.claude/skills/ethnographic-research/frames.yaml`
  - `master-knowledge-base/runbooks/2026_05_25_intelligence_qa_on_ingested_files.md` (this doc)
- **Effort:** 0.5d
- **Acceptance:** `SKILL.md` invocable from a Claude session; `frames.yaml` parses cleanly; runbook merged.

### Phase 2 — Silo Q&A pipeline (core feature)
- **Repo:** `intelligence-silo`
- **Files (new):**
  - `core/intelligence/ethnographic_frames.py`
  - `core/intelligence/principles_filter.py`
  - `core/intelligence/coverage_detector.py`
  - `core/orchestrator/qa_pipeline.py`
  - `tests/test_qa_pipeline.py`, `tests/test_ethnographic_frames.py`, `tests/test_principles_filter.py`, `tests/test_coverage_detector.py`
- **Files (modified):**
  - `core/orchestrator/society.py` — extend `Mind.process()` to read structured `memory_context["ethnographic_projection"]` and `Sentinel` to call `principles_filter`
  - `core/api.py` — new `POST /v1/qa/ask` endpoint + `QaAskRequest`/`QaAskResponse` Pydantic models at module scope
- **Endpoint:**
  ```
  POST /v1/qa/ask
  Body: { question, operator_id, category?, top_k=10, fast=true, max_backfill_ms=8000 }
  Returns: { answer, citations[], society_trace, ethnographic_frames_applied[], principles_check, research_backfill[] }
  ```
- **Effort:** 3d
- **Acceptance:**
  - `pytest tests/test_qa_pipeline.py -v` green
  - `curl POST /v1/qa/ask` against a freshly-ingested fixture returns ≥1 citation pointing to the right source file
  - Sentinel blocks a synthetic-number answer (Non-Negotiable #6 test case)
  - Critic spawns a `research_task` when ingest is empty for the asked domain

### Phase 3 — Chat gateway bridge
- **Repo:** `MD Files/intelligence-engine`
- **Files (new):** `api/silo_client.py`
- **Files (modified):**
  - `api/routes/chat.py` (`/chat/message/stream`) — after `engine_middleware.process()`, if `intent ∈ {explanation, analytics, decision_governance, strategy, property_ops, owner_acquisition}` AND `sources_count(operator_id) > 0`, call `silo_client.call_silo_qa(...)` and stream silo answer before falling through to provider LLM. Provider LLM is called only when the silo returns `confidence < 0.5`.
  - `api/translation/*` — encode `citations[]` and `society_trace` into provider-specific prompt prefix.
- **SSE event shape extended with:** `event: citation`, `event: society_trace`, `event: principles_check`, `event: research_backfill`.
- **Effort:** 1.5d
- **Acceptance:**
  - Ask a question in `/chat` about a file the operator ingested today → response includes a citation chip pointing to the right Drive file
  - Disconnect silo → chat still works (fail-soft path)

### Phase 4 — UI rendering
- **Repo:** `gigaton-ui-system`
- **Files (new):**
  - `components/chat/Citation.tsx` (inline chip + tooltip + "open in Drive" link)
  - `components/chat/SocietyTrace.tsx` (collapsible: minds_activated, confidence, cycle_time_ms)
  - `components/chat/PrinciplesCheckBanner.tsx` (red for violations, amber for ethos flags)
  - `components/chat/ResearchBackfillChip.tsx` ("researching the web for X…" with eta)
- **Files (modified):**
  - `pages/ChatPage.tsx` — handle new SSE event types
  - `components/chat/MessageBubble.tsx` — render `Citation` and `PrinciplesCheckBanner`
  - `services/intelligenceSiloClient.ts` — add `qaAsk(...)` for direct-call/debug usage
- **Effort:** 1d
- **Acceptance:** End-to-end test: ingest a fixture file → ask a question in `/chat` → DOM contains `[data-testid="citation-chip"]` whose `href` resolves to the right `drive_file_id`.

### Phase 5 — Backfill loop close
- **Repo:** `intelligence-silo`
- **Files (modified):**
  - `core/eo/self_heal.py` — add `wait_for_completion(task_id, timeout_ms)` helper
  - `core/orchestrator/qa_pipeline.py` — implement `wait_for_backfill=True` slow path with re-synthesis
- **Effort:** 1d
- **Acceptance:** With `wait_for_backfill=true`, asking about an un-ingested domain produces an answer that cites a web source URL (not just a Drive chunk) and the web finding is also persisted as a new chunk into FAISS (so a second ask is instant).

**Total spec effort:** ~7 engineering days, 4-5 PRs.

---

## 6. Open Questions (need operator decision before Phase 2 ships)

1. **Operator scoping of FAISS search** — `core/memory/semantic.search()` does not currently filter by `operator_id`. Is multi-tenant isolation already enforced upstream (one silo per operator) or do we need to add an `operator_id` tag and a filter pass? *(Affects Phase 2 query construction.)*
2. **Web-search backend** — `self_heal.spawn_research_task(source_preference="web_search")` says "web_search" — is there an actual configured backend (Brave/Tavily/SerpAPI/Anthropic web_search tool), or does Phase 5 need to spec one first?
3. **Fast vs. slow path default** — Should `/v1/qa/ask` default to `fast=true` (return partial + stream backfill) or `wait_for_backfill=true` (single complete answer, higher latency)? Chat UX implications differ.
4. **Principles-filter strictness in dev** — Should violations of non-negotiables (e.g. unlabeled synthetic data) hard-block the answer in dev, or only annotate? Hard-blocking is correct per doctrine but will surprise during early testing.
5. **Citation linkout** — For Drive-ingested chunks we have `drive_file_id`. Should Citation.tsx open the raw Drive file, the NotebookLM canonical bundle entry, or an in-app preview? *(Affects Phase 4 component.)*

---

## 7. Critical Files for Implementation

- `intelligence-silo/core/api.py`
- `intelligence-silo/core/orchestrator/society.py`
- `intelligence-silo/core/eo/self_heal.py`
- `MD Files/intelligence-engine/api/routes/chat.py`
- `gigaton-ui-system/pages/ChatPage.tsx`
- `decision-engine/drift_sentinel/GIGATON_CANONICAL_FIRST_PRINCIPLES.md` (read-only doctrine source)
