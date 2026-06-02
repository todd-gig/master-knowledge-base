# Documentation Ingest — Deep Dive (10-minute read)

This deep dive covers the structural model behind Stage 1 (Sources): how the intelligence-silo engine ingests operator documentation, how the consolidated bundle is shaped, how cost-and-payoff math works at scale, and the recovery paths when ingest goes wrong. It assumes you have read the `why_1min` and `what_3min` documents for Stage 1.

---

## 1. The structural outcome — one canonical, NotebookLM-ready folder

Every Stage 1 ingest produces the same structural outcome regardless of how many Google Drive accounts you connected: **a single canonical folder** in the operator's namespace, organized to be **NotebookLM-ready**.

NotebookLM-ready means the folder structure satisfies three constraints:

- **No more than 50 top-level folders.** NotebookLM's source-binding UI caps at this; we mirror it for parity.
- **All files unambiguously typed.** PDF, Markdown, text, Google Doc, Google Sheet, plain CSV. Mixed-type bundles are split.
- **No circular references.** Drive shortcuts that point back into the bundle are resolved at ingest time.

Whether the operator linked one Drive, five Drives, or dropped files directly into chat, the canonical bundle has one path. This is what NotebookLM, persona-engine, Penrose, and the chat-with-your-data capability all read from. There is no parallel copy.

## 2. The ingest pipeline

intel-silo runs a four-stage pipeline per file:

1. **Fetch** — Google Drive API pull (OAuth scoped to the operator's session) or direct upload bytes (for `file_drop`).
2. **Normalize** — extract text via the appropriate adapter (PDF → pdfplumber, Google Doc → Docs API, Markdown → passthrough, CSV → pandas).
3. **Chunk** — recursive-character chunking at the 1024-token boundary with 128-token overlap. Chunks carry per-chunk metadata: source_doc_id, position, taxonomy_tags.
4. **Embed + index** — embedding via the operator's currently selected embedding model (default `text-embedding-3-small`), written to the per-operator FAISS index.

Each pipeline run emits `DocumentationIngestRun` with a payload containing `files_processed`, `files_skipped_duplicate`, `bytes_in`, `embedding_cost_usd`.

## 3. Taxonomy + coverage

intel-silo carries an internal taxonomy of documentation categories: **brand, processes, people, financials, compliance, products, customers, vendors, regulators, technology**. As each file is ingested, intel-silo runs a lightweight classification step to attach taxonomy tags. When a previously empty taxonomy node receives its first file, `DocumentationCoverageAdvanced` fires with `{ taxonomy_node, coverage_pct }`.

The side panel uses these events to render the coverage gauge. The decision-engine reads coverage to decide which recommendations it has enough grounding to produce; coverage below 30% on a taxonomy node forces the engine into "ask the operator" mode rather than "draft a recommendation" mode.

## 4. Capability gate vs activation gate — the distinction

Stage 1 has two thresholds:

- **Capability gate (the unlock):** ≥1 source connected. As soon as one Google Drive account is linked OR one file is dragged into chat, `gigaton.chat.with_documents` turns on. The operator can immediately start asking grounded questions.
- **Activation gate (the stage advance):** `file_count >= 20`. The stage doesn't advance until the bundle has at least 20 files.

The split exists because **the operator should experience value before stage completion**. Forcing the operator to ingest 20 files before "chat with your data" works would be a hostile UX. The capability turns on at 1 file; the stage advances at 20.

## 5. The tier that closes — `tier_1_data`

Stage 1 completion **closes `tier_1_data`** — the tier Stage 0 partially opened. After Stage 1, both of the following are unlocked:

- `gigaton.chat.with_documents` — full grounded chat
- `gigaton.documentation.view_bundle` — browseable canonical bundle

Other tiers (`tier_2_personalized`, `tier_3_recommend`, etc.) remain locked until their respective stages complete.

## 6. Cost-and-payoff math at scale

The PPIM signature claims:

- **Cost**: avg $0.50 / operator / month (storage + embedding + FAISS index)
- **Payoff**: $1-3k / month in founder time saved

The cost number assumes 200-800 documents in the canonical bundle, ~5MB of net text after normalization, monthly delta-ingest of <50 new files. At those volumes, embedding cost is dominated by initial ingest (one-shot) and storage is the recurring tail.

The payoff number assumes the operator asks 5-15 grounded questions per week that would otherwise have taken 5-15 minutes each of human search-and-recall. At a $200-300/hour founder time rate, that's $1-3k/month conservative.

The 6000x ratio (payoff / cost) is the structural reason Stage 1 is **streak-eligible** in the gamification system — sustained ingest cadence keeps the index fresh, which keeps the chat-with-data capability accurate, which keeps the payoff coming.

## 7. Streak eligibility — why and how

The gamification system flags Stage 1 as `streak_eligible: true`. A streak is a 7-day window in which at least one `DocumentationIngestRun` event fires. Sustained streaks earn the `Documentation Connector Pro` badge variants (Bronze: 4 weeks, Silver: 12 weeks, Gold: 26 weeks).

Streaks matter operationally because document staleness is the #1 silent cause of degraded chat-with-data quality. An index that hasn't seen a new file in 90 days starts answering questions against a stale snapshot of the operator's reality. The streak nudges the operator to keep the bundle living.

## 8. The relationship to Stage 9

Stage 9's evidence-based graduation gate (per the v1.1.0 amendment) includes `education_tests_passed_all == true` and `drift_critical_count == 0`. A common silent cause of drift_critical regressions is **Stage 1 falling out of date** — the canonical bundle stops reflecting the operator's actual processes, the chat-with-data answers drift, the decision-engine recommendations drift with them. Keeping Stage 1 healthy post-graduation is part of staying graduated.

## 9. Recovery paths

- **OAuth expired** — `DocumentationAccountConnectionLost` fires; operator is prompted to re-link in chat. The canonical bundle retains existing files; only new-file ingest is paused for the affected account.
- **Drive folder deleted on the source side** — `DocumentationFolderUnreachable` fires. Ingested files remain in the bundle (immutable per the manifest's audit posture); future ingest from that folder is paused until a new subscription is created.
- **Duplicate detection false-positive** — operator can mark a deduped file as `force_include` from the bundle view; intel-silo re-ingests with a content-hash override.
- **Below the 20-file activation threshold for >7 days** — orchestrator surfaces a chat nudge: "Drag any 15 more files into chat to unlock Sources." The stage does not time out.

## 10. Edge cases

- **Operator wants to delete a file from the canonical bundle.** Supported via the bundle view → "Remove from bundle." The file remains in the source Drive; only the canonical-bundle copy + FAISS embedding are removed. A `DocumentationFileRemoved` event is emitted; the decision-engine re-runs any cached recommendation that depended on the removed file.
- **Operator wants to ingest a non-Drive source.** Drag-drop into chat is the canonical path for one-offs. For recurring non-Drive sources (Notion, Confluence, etc.), the connector hub in Stage 8 (`storage` credential class) handles registration; intel-silo treats the resulting documents identically to Drive-sourced documents.
- **Operator's documentation is in multiple languages.** Fully supported; the embedding model is multilingual. The chat-with-data layer answers in whichever language the operator asks the question.
- **Operator's documentation is mostly PDFs of scanned paper.** OCR runs automatically; quality is lower than native text. Coverage gauge flags low-quality OCR with a `coverage_quality` field; the decision-engine treats these chunks with a discount factor.

## 11. Telemetry

Every Stage 1 event is logged to the operator's activity stream with `stage_id: stage-1-sources`. The Stage 9 calibration logic consumes these events to validate that ingest cadence is healthy before graduating the operator to live mode. Specifically, an operator who completed Stage 1 but has had zero `DocumentationIngestRun` events in 30 days is flagged with `drift_warning: stage_1_stale` — not blocking, but visible in the calibration scoreboard.

## 12. The PPIM signature, restated

- **interaction**: doctrine grounding for every later decision
- **economics**: avg $0.50/operator/mo ingest cost; unlocks chat-with-data ($1-3k/mo founder time saved)
- **predictability**: HIGH
- **brand_dimension**: knowledge_coherence + auditability

"Auditability" is the second-order benefit most operators don't notice until they need it: every grounded chat answer can cite the specific chunks it drew from. The same audit trail flows into every decision-engine recommendation. When the operator (or their counsel, or their regulator) asks "what was this based on?", the answer is a specific list of files and chunks. That property is structural; it can't be retrofit later.
