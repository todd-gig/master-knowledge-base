---
name: qa_corpus_seeded_value_unlocked_2026_05_28
description: "2026-05-28 — seeded intel-silo operator_id=todd with 8,897 chunks from Obsidian vault + auto-memory + MKB. Q&A now returns grounded cited answers. First moment the platform is genuinely USABLE for value generation."
metadata: 
  node_type: memory
  type: project
  originSessionId: fd7cc3e4-1bc7-4d2e-84df-b9e539b84184
promoted_from: qa_corpus_seeded_value_unlocked_2026_05_28.md
promoted_at: 2026-06-02T20:13:25Z
---

# Q&A corpus seeded — first moment of real value (2026-05-28)

After [[semantic_search_activation_layered_fixes_2026_05_28]] activated the embedder, intel-silo had `/memory/search` returning HTTP 200 but operator `todd` had no data. This memo records the corpus seed + verification that completes the value loop.

## What was ingested (operator_id=todd)
- **Obsidian Gigaton vault** (`~/Documents/Obsidian Vault/Gigaton`): 37 files → **517 chunks**, category=`vault`
- **Auto-memory** (`~/.claude/projects/-Users-admin/memory`): 370 files → **7,047 chunks**, category=`memory`
- **MKB runbooks** (`~/Documents/GitHub/master-knowledge-base/runbooks`): 30 files → **978 chunks**, category=`runbook`
- **MKB architecture docs**: 8 files → **334 chunks**, category=`architecture`
- **MKB manifests** (`onboarding_v1.yaml`): 1 file → **21 chunks**, category=`manifest`
- **GRAND TOTAL: 446 files, 8,897 chunks**. 0 fails, 0 secrets leaked. ~504 sec at 4-way concurrency.

Source format: `<category>:<rel-path>`. Markdown auto-detected → header-aware chunking via `chunk_markdown()` (sections become chunks; ≤1,200 char per chunk).

## Verification (8/8 queries grounded)
All 8 diverse questions hit the right source file as top citation with **confidence > 0.99** (most > 1.0, indicating strong cosine matches plus principles/coverage bonuses). Samples:
- "Red Phone?" → `memory:emergency_notification_system_red_phone_v0.md`
- "INTEL-3 doctrine?" → `memory:intel_3_no_static_weights_algorithmic_determination_2026_05_26.md`
- "GCP migration?" → `runbook:2026_05_25_gcp_migration_accelerated_complete_plan.md`
- "Universal Acquisition Framework?" → `memory:universal_acquisition_framework_2026_05_26.md`
- "Compensation/payout rules?" → `memory:payout_1_and_intel_1_clarifications_locked_2026_05_26.md`

This is the first moment a Gigaton operator can ask a real question and get a real cited answer — the platform's stated purpose ([[foundational_goal_maximize_human_superpowers]]) made measurable.

## Ingest tooling
`/tmp/ingest_corpus.py` — Python urllib walker with: per-file 200 KB cap, 180 KB char truncation, 7-pattern secret scanner (sk-/AKIA/AIzaSy/ghp_/gho_/xoxb-/PEM), 4-way ThreadPoolExecutor. Re-runnable; idempotent at the chunk-id layer (silo dedupes by content hash). Move to `master-knowledge-base/scripts/` if it survives a second use.

## Operational realities + follow-ups
1. **Corpus is on carmen-beach-properties intel-silo, NOT gigaton-platform.** Per the [[two_silos_carmen_vs_gigaton_platform_2026_05_28]] separation, this corpus moves to the gigaton-platform silo during migration. Plan: re-run the same ingest script against the migrated silo URL post-cutover.
2. **Auto-memory keeps growing.** Every Claude Code session adds new memory files. Need a recurring re-ingest (incremental, by mtime > last_ingest_at). Easy follow-up: cron the ingest script + add `--since=<ts>` flag.
3. **Other operators have empty corpora.** When Carmen-Beach / Multipli / Ti-Solutions onboard, each needs its own ingest. The script's `OPERATOR` constant is a single-line change; wrap in a config + run per operator.
4. **The 5 conflict-blocked PRs from the morning resume doc still pending** ([[RESUME_HERE_2026_05_27_morning_red_phone_completion]] §5 channels). Now that semantic search works, the cowork UI calling `/v1/qa/ask` (or its operator-api shim) actually returns useful answers, so wiring the FE is no longer demo-able-but-empty.
5. **Confidence scores > 1.0** — this comes from the qa_pipeline summing cosine + principles + coverage bonuses; not a bug, but worth normalizing to [0,1] in a future Phase 3 pass so it doesn't confuse UI display.

## What this unlocks (the value chain)
- **Operators can now ask Gigaton anything in scope** and get a cited answer (cowork UI, /intelligence route, Q&A bridge).
- **Research backfill auto-fires** when corpus has gaps, creating background research_tasks the Self-Engineered HR can supervise.
- **PPIM signature** (every artifact has it) means citations carry their own provenance — the answer can show which doctrine / decision / runbook backs the claim.
- **Ti Agent Matrix** dispatch can route based on intelligence_profile.dimensions in the qa response instead of static config.
- **Onboarding stages** can use Q&A to answer operator questions during chat-first directed onboarding without static FAQ pages.
