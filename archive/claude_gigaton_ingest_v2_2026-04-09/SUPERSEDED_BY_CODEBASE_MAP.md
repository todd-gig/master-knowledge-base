# SUPERSEDED

This package (`claude_gigaton_standalone_project_v2`, manifest v2.0.0) was authored against the **April 9, 2026 meeting state**. The codebase is far past P0–P3.

**Read these instead:**

- [`docs/architecture/CODEBASE_MAP.md`](../../docs/architecture/CODEBASE_MAP.md) — canonical layer-by-layer map of what currently exists in production.
- [`decisions/2026-05-22_claude_gigaton_ingest_reconciliation.md`](../../decisions/2026-05-22_claude_gigaton_ingest_reconciliation.md) — the ADR that reconciles this package against live reality. ACCEPTED 2026-05-22 by todd@gigaton.ai.

## Why this package is not an execution mandate

~80% of its P0–P3 backlog is already LIVE in production. Following it literally would:

- create duplicate auth (UAE already LIVE),
- regress the Penrose 8-metric falsification scoreboard to a 5-factor weighted sum (C1 in the ADR),
- regress the PPIM-signed decision record schema to an 8-field subset (C2 in the ADR),
- replace UAE category × persona sign-off routing with a single scalar threshold (C3 in the ADR),
- duplicate the messenger UI, approval queue, namespace generator, task generation, Drive ingest, and 8 of 9 Control Plane UI pages.

## What was kept from this package (per the ADR)

- The governance policy authority hierarchy (foundational → user → repo → memory → package → inference).
- The source-provenance confidence levels (0.95 / 0.85 / 0.70 / 0.50 / <0.50).
- The decision-record optional-auxiliary fields (rationale prose, validation_plan, options array) — additive to the production schema, not replacements.

## Genuine gaps the ADR accepts as the active work list

- Stripe / billing / payment processing
- Liquifax productization (canonical TBD)
- Local tourism SMB package, Upwork package, proposal generator
- Production storage flip for Decision Execution Engine + EO System
- Cross-engine event-driven storage/retrieval (sprint 2026-05-22)
- mimi-whatsapp gateway aggregator registration
- `api.gigaton.ai` GoDaddy DNS + OPENAI_API_KEY operator paste
- 8 registry-drift items in `master_project_plan.md` §3.6

— Archived 2026-05-22.
