---
name: Drift Sentinel — recursive doctrine-conformance scanner
description: Local-first Python scanner that walks every codebase, GitHub repo, Drive doc, ClickUp task, and local doc; grades each artifact against DRIFT_RULES.yaml (which encodes the canonical first-principles doc); emits JSON+Markdown reports and tracks scan history in SQLite for rule-promotion/retirement.
type: reference
originSessionId: db76fee0-56c0-46ab-b344-b7f636e8771a
lifecycle_state: active
state_set_at: 2026-05-19
state_set_by: auto-migration-concept-8
promoted_from: drift_sentinel_system.md
promoted_at: 2026-06-02T20:13:25Z
---

# Drift Sentinel

## Location

`/Users/admin/Documents/GitHub/decision-engine/drift_sentinel/`

## Files

- `GIGATON_CANONICAL_FIRST_PRINCIPLES.md` — single source of truth (separate memory entry)
- `DRIFT_RULES.yaml` — versioned rule set; CRIT-* / MAJ-* / MIN-* / INFO-* IDs
- `DRIFT_SCANNER_SPEC.md` — architecture: adapters, rule engine, recursion semantics
- `drift_scan.py` — CLI entry point
- `reports/` — per-run JSON + Markdown drift reports
- `drift_history.db` — SQLite scan history (used for rule firing trend → promotion/retirement)
- `deploy/local/` — launchd plist + install script
- `deploy/gcp/` — Dockerfile, cloudbuild.yaml, scheduler.yaml, secrets.md
- `README.md` — quickstart

## Quickstart

```bash
cd /Users/admin/Documents/GitHub/decision-engine/drift_sentinel
python3 drift_scan.py --source local_codebase                     # scan all GitHub repos locally
python3 drift_scan.py --source local_codebase,downloads,github    # all local + remote
python3 drift_scan.py --source github --post-to-slack             # weekly digest mode
python3 drift_scan.py --source local_codebase --fail-on critical  # CI gate
```

## Adapter status (as of 2026-05-05 EOD)

- LocalCodebaseAdapter: WORKING — walks `/Users/admin/Documents/GitHub/`, classifies code/markdown/config/schema
- LocalDocsAdapter: WORKING for .md/.txt; PDF/.docx is stubbed (returns "[binary: name]")
- GithubAdapter: WORKING — uses `gh CLI` (authenticated as todd-gig); fetches README + CLAUDE.md + AGENTS.md + PRINCIPLES.md + DOCTRINE.md + ARCHITECTURE.md per repo; skips forks/archived/older-than-365d
- DriveAdapter: STUB — must be invoked from MCP-aware Claude Code session (`mcp__claude_ai_Google_Drive__*`)
- ClickUpAdapter: STUB — must be invoked from MCP-aware Claude Code session (`mcp__claude_ai_ClickUp__*`)
- Slack posting: WORKING — `--post-to-slack` flag reads `SLACK_WEBHOOK_URL` env, posts severity-summary digest with top-5 critical findings

## Rule families implemented

- CRIT-001 automation_without_human_override
- CRIT-002 ethical_misalignment_above_threshold
- CRIT-003 prompt_without_versioning (working structural handler)
- CRIT-004 undefined_ownership (working structural handler)
- CRIT-005 decisions_without_auditability
- CRIT-006 action_without_qualification
- CRIT-007 provider_lock_in (working structural handler)
- CRIT-008 fake_market_data
- CRIT-009 irreversible_without_mandatory_human
- MAJ-001 partial_capability_shipment
- MAJ-002 complexity_without_leverage
- MAJ-003 short_term_extraction_harms_trust
- MAJ-004 unaudited_state_change
- MAJ-005 monorepo_circular_dependency
- MAJ-006 schema_first_violation
- MAJ-007 rtql_bypass
- MAJ-008 codification_overdue
- MAJ-009 missing_phase_gate
- MAJ-010 gigent_value_chain_break
- MAJ-011 dvm_single_axis_optimization
- MIN-001 typescript_any_usage (working structural handler)
- MIN-002 no_test_suite
- MIN-003 bilingual_missing
- MIN-004 missing_health_endpoint
- MIN-005 comment_overuse
- MIN-006 clickup_task_no_outcome
- INFO-001 documented_override

## First-run baseline (2026-05-05 14:00)

1,299 local artifacts → 8 critical (CRIT-003 prompt_versioning + CRIT-007 provider abstraction in 4 LLM call sites).

## After remediation (2026-05-05 EOD)

1,368 artifacts (1,328 local + 40 github) → 2 critical, 0 major, 21 minor.

Remediated 4 files by adding `_invoke_llm()` audit wrapper carrying provider/model/prompt_version/schema_version with `logging.getLogger("...llm_audit")` emit:

- `claude_decision_logic_pack/engine/learning_agent.py`
- `decision-engine/engine/learning_agent.py`
- `gigaton-engine/integration/claude_enrichment.py`
- `sales-operating-system/app/services/claude_reasoning.py`

Remaining 2 critical are CRIT-004 false-positiveish on `github:todd-gig/master-knowledge-base/CLAUDE.md` and `braintrust-knowledge-base/README.md` — rule fires on docs mentioning "decision/RFC/proposal" but lacking `owner:` frontmatter. Could be tightened to require explicit decision-record markers.

## todd-gig GitHub account

22 repos discovered; remote-only (not cloned locally) repos worth knowing:

- sovereign-influence-engine — Sovereign Influence Engine v2.0 (11-service decision pipeline)
- cxguy-methodology — CxGuy methodology layer (Trust × Value × Priority evidence ranker)
- intelligence-silo-backup — encrypted vault backup
- LiqueFex-Platform-Ui
- CxGuy-Slack-Discussions

## Deployment artifacts

- `drift_sentinel/deploy/local/` — launchd plist + `install_launchd.sh` (Sundays 08:00 local)
- `drift_sentinel/deploy/gcp/` — Dockerfile, cloudbuild.yaml, scheduler.yaml, secrets.md (Cloud Run Job + Cloud Scheduler)
- `drift_sentinel/deploy/README.md` — picks between local-now or GCP-when-ready
- NEITHER has been activated — `install_launchd.sh` awaits user run; GCP awaits explicit deploy authorization

## Recursive flywheel

After each scan: rules firing >10× across the ecosystem get promoted (MAJ→CRIT or text-rule→CI gate). Rules never firing for 6+ months get retired (principle internalized). Feeds the codification backlog per Decision Routing Framework §5.8.

## How to extend

- New rule: append to DRIFT_RULES.yaml; add structural handler to `STRUCTURAL_HANDLERS` dict if needed
- New source: implement adapter class with `stream() → Iterator[Artifact]`, register in `ADAPTERS` dict
- New severity: update `severity_order` list in `main()`

## Self-doctrine compliance

Scanner satisfies its own rules: deterministic, audit-logged (drift_history.db), idempotent, local-first, versioned rule set, no LLM in core path (so no prompt_version concern).
