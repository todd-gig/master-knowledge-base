---
name: learning-loop-architecture
description: How auto-memory → MKB → intelligence-silo Q&A → telemetry forms the recursive learning loop, and which files/launchd jobs implement it.
status: ratified
version: 1.0.0
ratified: 2026-05-28
companion: CONSTITUTION.md §Article VI (Enforcement)
---

# Recursive Learning Loop — Architecture

Closes the open-circuit in the Pascal Protocol (`for-the-group/March 18, 2026/`). Working / Session / Long-Term memory now form an actual loop instead of three stranded layers.

## The loop

```
  ┌─────────────────────────────────────────────────────────────────┐
  │                                                                 ▼
[conversation]  →  [auto-memory]  →  [MKB PR]  →  [doctrine ratified]
                   ~/.claude/         scripts/        CONSTITUTION,
                   projects/.../      auto_memory_    decisions/,
                   memory/            promote.py      runbooks/
                                                                    │
  ┌─────────────────────────────────────────────────────────────────┘
  ▼
[intelligence-silo ingest]  →  [Q&A grounded in doctrine]  →  [telemetry]
 scripts/                       /v1/qa/ask                    drift_sentinel
 ingest_mkb_to_silo.sh          (operator_id=gigaton)         + Cloud Logging
                                                                    │
  ┌─────────────────────────────────────────────────────────────────┘
  ▼
[doctrine violation]  →  [auto MKB issue]  →  back to conversation
 drift_sentinel hook    gh issue create
```

## Why this matters (user-stated goal)

> "Every user receives all information / education required to maximize new feature & functionality + process creation & automatic human-adherence management within human management systems to ensure long-term alignment."

Implementation:
- **Education delivery** — every doctrine + capability lives in MKB → ingested into intel-silo → answered by `/v1/qa/ask` with citations. A user asking *"how does comp work?"* gets the PR #17 comp/payout doctrine cited, not a hallucination.
- **Process creation** — runbooks in `runbooks/` are ingested as `category=runbook`; the universal acquisition framework, onboarding stages, escalation pathways are retrievable.
- **Adherence management** — `drift_sentinel` already emits axiom-violation events (CONSTITUTION §6.1); the new hook routes those into MKB issues so the loop closes back into doctrine PRs.

## Components (and where they live)

| # | Component | Path | Cadence |
|---|-----------|------|---------|
| 1 | Auto-memory → MKB bridge | `scripts/auto_memory_promote.py` | Weekly (Sun 06:00 UTC) |
| 2 | MKB → intel-silo ingest | `scripts/ingest_mkb_to_silo.sh` | On MKB main push + weekly fallback |
| 3 | MKB GCS backup bundle | `scripts/mkb_gcs_backup.sh` | Nightly (02:30 UTC) |
| 4 | Knowledge-sync repair | `scripts/repair_knowledge_sync.sh` | One-shot installer |
| 5 | Knowledge-extracts refresh | `scripts/xlsx_to_knowledge.py` (existing) | Weekly (Sun 05:00 UTC) |
| 6 | Constitution mirror CI | `.github/workflows/constitution-mirror.yml` | Every PR |
| 7 | Onboarding manifest sync CI | `.github/workflows/onboarding-manifest-sync.yml` | Every PR |
| 8 | LaunchAgent installer | `scripts/install_launchagents.sh` | One-shot |
| 9 | Drift-sentinel → MKB issue | (drift_sentinel repo) | Per violation |

## Promotion criteria — auto-memory → MKB

An auto-memory entry is promoted (= PR opened against MKB) when **any** of:

1. Frontmatter contains `promote_to_mkb: true`
2. Frontmatter `lifecycle_state: canonical` AND `metadata.type` in {feedback, project, reference}
3. Body contains one of the doctrinal sentinels: `LOCKED`, `RATIFIED`, `INTEL-3`, `PAYOUT-1`, `EMAIL-1`, `DNS-1`, `MIG-DEFER`, `AXIOM-`
4. Memory file is referenced from `MEMORY.md` index AND has `metadata.type: feedback` (these encode behavioral rules)

**Excluded** (never promoted):
- `RESUME_HERE_*.md` (session handoffs — ephemeral)
- `_lifecycle_log.jsonl`
- `active_work_registry.md` (in-flight TODO state)
- Anything with frontmatter `promote_to_mkb: false`

Promoted content lands in `memory-snapshots/auto-memory/` with the original frontmatter + a `promoted_from:` line. The PR body lists the diff so humans approve consciously.

## Ingestion taxonomy — MKB → intel-silo

`scripts/ingest_mkb_to_silo.sh` walks these roots and tags each with a category:

| Root | Category | operator_id |
|------|----------|-------------|
| `CONSTITUTION.md`, `PRINCIPLES.md`, `LEARNING_LOOP.md` | foundational | gigaton |
| `decisions/` | doctrine | gigaton |
| `decision-execution-engine/*.md` | doctrine | gigaton |
| `for-the-group/` | doctrine | gigaton |
| `manifests/` | capability | gigaton |
| `runbooks/` | runbook | gigaton |
| `knowledge-extracts/` | extract | gigaton |
| `memory-snapshots/auto-memory/` | session-memory | gigaton |
| `claude-systems/v3.2/` | operating-system | gigaton |

All ingest with `operator_id=gigaton` (matches the multi-tenant scoping shipped in intel-silo PR #46). Cross-operator visibility for foundational/doctrine is handled by intel-silo's foundational-tier query bypass (planned — currently every operator-scoped query against gigaton-tagged foundational content goes through the Society's principles filter).

## Closing the doctrine-violation arrow

`drift_sentinel/violation_hook.py` (in the gigaton-platform repo) should call:

```
gh issue create \
  --repo todd-gig/master-knowledge-base \
  --title "AXIOM violation: <axiom_id> — <one-line>" \
  --body "<violation context + suggested doctrine amendment>" \
  --label "drift-sentinel,axiom-violation"
```

This routes runtime adherence failures back into the constitutional amendment process (Article V) rather than dying in Cloud Logging.

## Versioning

This document is itself doctrine — amendments follow Article V §5.4 (SemVer). New §clauses = MINOR. Component re-paths = PATCH. Removal or scope change of the loop = MAJOR.
