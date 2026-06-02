---
name: directive-local-mind-buildout-2026-06-01
description: "COMMITMENT — 3-phase ~3.5wk buildout of gigaton-local-mind MCP server to offload Vertex AI cost to operator's local machine compute. Phase 1 (embeddings + dedup + PII redactor) ships EOD Wed 2026-06-03; Phase 2 (Whisper + local classifier + cowork routing-transparency UI) EOD Fri 2026-06-12; Phase 3 (local SLM + capability-ladder UI) EOD Fri 2026-06-26. Architecture decisions locked: server name gigaton-local-mind, persistence ~/.gigaton/local-mind/<operator_id>/, substrate extended with local_runtime.py separate from D1 do_read/do_write, dogfood-week gate to operator_id=todd through 2026-06-10. Phase 1 launched via 3 parallel worktree agents."
metadata: 
  node_type: memory
  type: project
  established: 2026-06-01
  status: PHASE 1 IN FLIGHT
  ph1_deadline: 2026-06-03 EOD
  ph2_deadline: 2026-06-12 EOD
  ph3_deadline: 2026-06-26 EOD
  originSessionId: 4dd609ce-cf49-4eb8-8ded-c7232f9be05f
promoted_from: directive_local_mind_buildout_2026_06_01.md
promoted_at: 2026-06-02T20:13:25Z
---

# Local Mind Buildout Directive — 2026-06-01

> Origin: this-session prompt "explain how vertex is being used + identify any instances where we are able to utilize user local machine compute after install of gigaton MCP + additional technology to reduce actual gigaton unit cost + follow foundational design principles." Recommendation accepted in full; Todd authorized "Complete ALL + give me a deadline."

## Why

Vertex AI is correctly chosen as the **invoicing + IAM + sovereignty wrapper for frontier reasoning** ([vertex_anthropic.py:75](file:///Users/admin/Documents/GitHub/gigaton-gateway/app/llm_router/providers/vertex_anthropic.py#L75) for Claude Opus/Sonnet/Haiku via Anthropic SDK on Vertex; [vertex_gemini.py:45-46](file:///Users/admin/Documents/GitHub/gigaton-gateway/app/llm_router/providers/vertex_gemini.py#L45-L46) for Gemini). Vertex is NOT the cost-reduction lever.

The lever is the **local half of the routing doctrine** (`third_party_vs_local_llm_routing_doctrine.md` — "frontier 3rd-party for novel reasoning; local for bounded repeatable ability") that currently doesn't exist at scale. Foundational doctrine support: `gignet_local_node_doctrine.md` ("local computation always has inherent advantages") + `platform_hub_circles_design_directive.md` (capability ladder Tier 1 Reading Eyes → Tier 4+).

## Phase 1 — Local Mind v0 (embeddings + dedup + PII redactor)

**Deadline: EOD Wed 2026-06-03** (aligned to Phase 1 closeout)

### Architecture (LOCKED via AskUserQuestion 2026-06-01)
- **Server name:** `gigaton-local-mind`
- **Persistence:** `~/.gigaton/local-mind/<operator_id>/{index.faiss, metadata.sqlite}`
- **Substrate change APPROVED:** extend `gigaton-mcp-common` with `local_runtime.py` (`local_read` / `local_write` / `assert_local_write_allowed`); CI linter `scripts/lint_writes_declare_operator_id.py` teaches about two contracts (D1 path AND local path). Keeps existing D1 invariant pristine.
- **Dogfood gate:** install only on operator_id=todd through 2026-06-10; open to Multipli/LiqueFex/CBP/Carmen-Beach/Ti-Solutions after dogfood week clean.

### What ships
- New server `servers/gigaton-local-mind/` in `/Users/admin/Gigaton-UI-Platform/gigaton-mcp/`
- Tools:
  - `embed_chunks(texts, namespace)` — sentence-transformers all-MiniLM-L6-v2, 384-dim, lazy-loaded singleton
  - `search_local(query, namespace, k)` — FAISS local index
  - `dedup_chunks(chunks)` — sha256 exact + cosine 0.95 near-dup
  - `redact_pii(text)` — regex (email/phone/SSN/credit-card) + spaCy NER (PERSON/GPE/ORG)
- intel-silo `POST /v1/qa/ingest_preembedded` — accept pre-embedded chunks, skip cloud embedder
- gateway `POST /v1/local-mind/handshake` — register operator's local mind + capability tier; returns routing hints
- ~50 tests total across 3 PRs

### Migration story for existing corpora
The 8,897-chunk Q&A corpus from [[qa_corpus_seeded_value_unlocked_2026_05_28]] stays in cloud FAISS for operator_id=todd; the local index builds in parallel on next incremental sync (via existing launchd cron from [[qa_corpus_incremental_ingest_tooling_2026_05_28]]). Both indexes coexist during dogfood week; cutover happens after Phase 2 lands cowork routing transparency.

### Build-sprint pattern (per [[build_sprint_postmortem_2026_05_28]])
3 parallel worktree agents:
- Agent 1: `/tmp/gigaton-local-mind-2026-06-01` → gigaton-mcp PR
- Agent 2: `/tmp/silo-preembedded-2026-06-01` → intelligence-silo PR
- Agent 3: `/tmp/gateway-local-mind-handshake-2026-06-01` → gigaton-gateway PR

## Phase 2 — Whisper + classifier + cowork transparency

**Deadline: EOD Fri 2026-06-12**

- `transcribe_audio` tool — mlx-whisper (Apple Silicon) / whisper.cpp (cross-platform); `base.en` default (~150MB)
- `categorize_doc` tool — heuristic-first, escalate to Vertex Haiku when confidence < 0.7
- Trained classifier head (~5MB) on MiniLM embeddings + existing categorization decisions as training data
- Cowork app v0 routing-transparency widget: per-message "local (free) / Haiku ($0.001) / Sonnet ($0.012)" + weekly cost-saved counter

### Todd owes by 2026-06-05
- Authorize cross-operator export of existing categorization decisions as classifier training data (data-governance call — Gigaton-platform-owned per `gigaton_scope_doctrine.md`)
- Pick cowork UI mount point: toast / inline / sidebar

## Phase 3 — Local SLM + capability ladder UI

**Deadline: EOD Fri 2026-06-26**

- Llama-3.2-3B Q4_K_M default (~2GB) via mlx-lm / llama.cpp
- Capability probe: RAM ≥16GB, disk ≥10GB free → Tier 4 unlock eligible
- `/v1/qa/ask` first-pass routes locally; "ask the frontier" explicit per routing doctrine
- `/platform` hub circles wire Tier 1/2/3/4 unlock UI to handshake state (per [[platform_hub_circles_design_directive]])
- Confidence-threshold telemetry → auto-tunes when to escalate

### Todd owes by 2026-06-15
- Confirm Llama-3.2-3B Q4_K_M (vs Phi-3.5-mini / Qwen2.5-3B)
- Confirm capability-probe thresholds
- Confirm initial confidence threshold (0.7 default; telemetry tunes)

## Hard dependency Todd should know about

When Phase 1 intel-silo PR merges, auto-deploy fires → ~90s of `503` on `/v1/qa/ask`. Tell agents to hold the merge if any cohort onboarding activity from Sat 5/30 / Sun 5/31 is still mid-flight.

## Cross-refs
- [[mcp_wave2_scaffold_built_2026_05_27]] — current gigaton-mcp state (35/35 tests, 4 servers, shared substrate)
- [[build_sprint_postmortem_2026_05_28]] — parallel-agent worktree pattern this build follows
- [[gignet_local_node_doctrine]] — load-bearing principle: local computation always has inherent advantages
- [[third_party_vs_local_llm_routing_doctrine]] — frontier vs local routing contract that Phases 2-3 implement
- [[platform_hub_circles_design_directive]] — Tier 1-4 capability ladder Phase 3 wires into
- [[gigaton_scope_doctrine]] — Gigaton-platform-owned vs vertical-owned (local-mind is platform-owned)
- [[feedback_pre_retarget_stacked_prs_before_merging_parent]] — Phase 1 PRs are NOT stacked (3 independent repos) so this doesn't apply, but if any Phase 2/3 PRs stack, retarget before parent merge
