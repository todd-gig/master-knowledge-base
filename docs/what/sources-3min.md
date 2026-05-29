# What you'll do in Stage 1 — Sources (3-minute walkthrough)

Stage 1 is owned by the **intelligence-silo** engine. Unlike most stages, Stage 1's `actions: []` is empty in the manifest — the stage **delegates to an existing workflow**, `documentation-ingest-2026-05-20`. That workflow's seven-step UI IS Stage 1's UI; you don't see two flows, you see one.

## The delegated workflow

`documentation-ingest-2026-05-20` is the canonical documentation-ingest sequence that predates the onboarding manifest. Stage 1 reuses it instead of duplicating the actions. The orchestrator opens the workflow inside the chat surface and walks you through:

1. **Link a Google Drive account.** OAuth flow; you can link more than one (personal, work, shared-drive admin). Emits `DocumentationAccountsLinked`.
2. **Pick a folder (or folders) to subscribe to.** Each subscription is a watch — new files get ingested as they appear. Emits `DocumentationFolderSubscribed`.
3. **Trigger the first ingest run.** intel-silo pulls each file, deduplicates by content hash, extracts text, chunks it, and writes it into the per-operator FAISS index. Emits `DocumentationIngestRun`.
4. **Watch coverage advance.** Coverage is computed against an internal taxonomy (brand, processes, people, financials, compliance, etc.). As each taxonomy node gets a file attached, `DocumentationCoverageAdvanced` fires.
5. **Consolidate into the canonical folder.** Every connected Google Drive source ends up consolidated into a single canonical, **NotebookLM-ready folder** in the operator's namespace. That folder is what NotebookLM, the persona-engine, and Penrose all read from. There is no parallel copy.
6. **Optionally drag-drop additional files** directly into the chat. The chat affordance is `file_drop`; intel-silo treats dropped files identically to Drive-sourced files.
7. **Optionally invite teammates** to connect their own Drives. Each connection accumulates against the operator's `file_count`.

The chat affordances are auto-derived from the events: `file_drop` for `DocumentationAccountsLinked` and `DocumentationFolderSubscribed`. The chat opening message tells the operator: "the fastest path is to connect Google Drive; you can also drag-drop files directly into this chat."

## The activation gate

`GET {intel_silo_base}/v1/documentation/bundle?operator_id={operator_id}` with predicate `$.file_count >= 20`. That endpoint returns the current `file_count` for the operator's canonical bundle. When the count hits 20, the gate flips, and the stage advances.

The 20-file threshold is empirical: below 20 files, the FAISS index is too sparse for reliable grounding; above 20, retrieval quality improves dramatically and stays good. The threshold is an INTEL-3 seed within bounds — the platform may eventually raise or lower it per-operator based on observed retrieval-quality curves.

## Events emitted

- `StageStarted` — fires when the operator enters the stage.
- `DocumentationAccountsLinked` — fires each time a Google Drive OAuth completes.
- `DocumentationFolderSubscribed` — fires each time a folder is subscribed.
- `DocumentationIngestRun` — fires per ingest batch.
- `DocumentationCoverageAdvanced` — fires whenever taxonomy coverage advances.
- `StageCompleted` — fires when the activation gate predicate becomes true.

## What unlocks at completion

Stage 1 **closes `tier_1_data`** (the tier Stage 0 partially opened). Specifically, the following capabilities turn on:

- `gigaton.chat.with_documents` — every chat message is now grounded in the operator's canonical bundle.
- `gigaton.documentation.view_bundle` — the operator can browse the consolidated bundle.

The `sources` and `dashboard` nav circles illuminate.

## Streak eligibility

Stage 1 is **streak-eligible** in the gamification system. Sustained ingest cadence (new files arriving regularly) is rewarded — it's a healthy signal that the operator is using the platform as living documentation rather than a one-time dump. The badge slug is `documentation-connector-pro`.

## Predicted outcomes

Fallback predicted influence is **$8,500**. The PPIM signature claims ~$0.50/operator/month ingest cost in exchange for $1-3k/month in founder time saved (chat-with-your-data replaces "go find that doc in Drive" for routine questions).

## What happens if you stall

If you connect a Drive but don't reach 20 files, the orchestrator falls back to: "you can drag-drop more files into chat, or invite teammates to connect their Drives." The stage does not time out — Stage 9's graduation gate is what cares about Stage 1 having completed, not a calendar clock.
