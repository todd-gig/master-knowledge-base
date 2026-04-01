# Decision Logic Engine — System Architecture & Gap Closure Report

**Version:** 2.0
**Date:** 2026-03-24
**Status:** Operational — all pipeline stages functional

---

## System Overview

The Decision Logic Engine is a deterministic governance layer that converts organizational decision inputs into trust-qualified, auditable execution packets. It implements a 12-stage pipeline from raw decision intake through certificate issuance to execution authorization, with a complete learning feedback loop.

The system now consists of four integrated subsystems:

1. **Core Engine** (`engine/`) — Deterministic scoring, gating, certification, and execution routing
2. **Survey Intelligence Engine** (`engine/survey_engine.py`) — Client intake processing across 15 organizational categories with RTQL trust qualification
3. **CLI Runner** (`cli.py`, `converters.py`) — Command-line interface for JSON payload processing
4. **API Service Layer** (`service/`) — FastAPI REST interface for programmatic integration

---

## Pipeline Architecture

```
Input (JSON/API/Survey)
  │
  ├─ Payload Conversion (converters.py / service/schemas.py)
  │
  ▼
Stage 1: Input Validation
  → DecisionObject.validate() — 5 required field checks + dimension range validation
  │
Stage 1.5: Pre-Check Flags
  → has_missing_data → routes to NEEDS_DATA
  → ethical_conflict → mandatory BLOCK
  │
Stage 2: RTQL Pre-Filter (rtql_filter.py)
  → 7-checkpoint trust discipline: identity → source_integrity → exposure → independence
    → explainability → replicability → robustness → novelty → causal checks
  → 9 classification stages: noise → weak_signal → echo_signal → qualified
    → certification_gap → certified → research_grade → first_principles_candidate → axiom_candidate
  → Trust multiplier applied (0.00 to 1.50)
  → Write target routing (quarantine → staging → registries)
  │
Stage 3: Value Assessment (scoring.py + weighted_scoring.py)
  → Raw: 8 positive dimensions + 4 penalty dimensions (0-5 each)
  → Weighted: asymmetric config weights from engine.yaml
  → Trust-adjusted: net_value × RTQL multiplier
  → Classification: strong (20+) | conditional (12-19) | weak (0-11) | block (<0)
  │
Stage 4: Trust Assessment (scoring.py + weighted_scoring.py)
  → 7 trust inputs → tier calculation (T0-T4)
  → Promotion guards: per-dimension minimums enforced
  → Demotion: guard failure drops one tier
  │
Stage 4.5: Authority Check (authority.py)
  → Role hierarchy: AI_Domain_Agent < Domain_Owner < Human_Executive < Human_CEO < Board
  → Per-class minimum trust tier from engine.yaml authority_matrix
  → Determines can_execute + required_approval
  │
Stage 5: Alignment Check (scoring.py)
  → Doctrine/ethos/first-principles composite (0-1)
  → Auto-detects 7 structural anti-patterns from decision object
  │
Stage 6: Certificate Chain (certificates.py)
  → QC (Qualified Context): 30-day expiry — decision object completeness
  → VC (Value Confirmed): 14-day expiry — value scored, strategic alignment confirmed
  → TC (Trust Certified): 14-day expiry — T2+ trust, evidence attached, assumptions bounded
  → EC (Execution Cleared): 7-day expiry — all gates passed, execution plan + monitoring defined
  → Hard rule: No EC without prior valid QC, VC, and TC
  │
Stage 7: 7-Gate Authorization (gates.py)
  → Gate 1: Doctrine — no non-negotiable violations
  → Gate 2: Trust Tier — meets decision class minimum
  → Gate 3: Value Threshold — net value meets class minimum
  → Gate 4: Reversibility — compatible with auto-execution (R1/R2 only)
  → Gate 5: Risk Containment — downside bounded, monitoring exists
  → Gate 6: Approval Routing — required approvals present or not needed
  → Gate 7: Monitoring — monitoring metric + review date + rollback trigger
  │
  → Verdict: AUTO_EXECUTE | ESCALATE_TIER_1/2/3 | BLOCK | NEEDS_DATA | INFORMATION_ONLY
  │
Stage 8: State Machine (state_machine.py)
  → 8 lifecycle states: draft → qualified → value_confirmed → trust_certified
    → execution_cleared → executed → reviewed → archived
  → State maps to certificate chain position
  │
Stage 9: Priority Scoring (scoring.py)
  → Formula: ((Value - Cost - Risk) × P(Success) × Time Leverage)
              × Strategic Alignment × Ethos Alignment × Trust Multiplier
  │
  ▼
Output: PipelineResult + ExecutionPacket + AuditRecord + Executive Summary
```

---

## Component Inventory

### Core Engine (`engine/`)

| Module | Purpose | Lines |
|---|---|---|
| models.py | 15 dataclasses, 10 enums — canonical data contract | ~478 |
| pipeline.py | 12-stage orchestrator — single entry point `process_decision()` | ~304 |
| gates.py | 7-gate authorization system with 3-tier escalation | ~362 |
| scoring.py | Trust tier calculation, alignment check, priority formula | ~236 |
| weighted_scoring.py | Config-driven asymmetric weighting | ~98 |
| certificates.py | QC/VC/TC/EC chain issuance with expiry | ~333 |
| rtql_filter.py | 12-checkpoint RTQL classification with research action generation | ~244 |
| authority.py | Role-based execution rights per decision class | ~96 |
| state_machine.py | 8-state lifecycle with valid transitions | ~135 |
| audit.py | Structured audit logging and serialization | ~283 |
| gap_analysis.py | Gap detection, severity banding, priority ranking | ~246 |
| survey_engine.py | 15-category client intelligence engine with RTQL integration | ~700+ |
| config.py | YAML-driven configuration with defaults | ~115 |

### Interface Layer

| Module | Purpose |
|---|---|
| cli.py | 5-command CLI: evaluate, validate, score, gaps, demo |
| converters.py | JSON ↔ dataclass bidirectional conversion with enum mapping |
| service/app.py | FastAPI application factory with middleware |
| service/routes.py | 5 REST endpoints mapping to pipeline |
| service/schemas.py | Pydantic request/response models |

### Documentation (`docs/`)

| File | Purpose |
|---|---|
| 01_doctrine.md | Non-negotiable principles and core mantras |
| 02_first_principles_registry.md | 15 logical atoms governing all reasoning |
| 03_org_ethos.md | Behavioral filters + 7 anti-patterns |
| 04_value_matrix.md | 12 scoring dimensions with thresholds |
| 05_trust_matrix.md | 7 trust inputs, 5 tiers, promotion/demotion rules |
| 06_decision_taxonomy.md | 7 classes (D0-D6), 4 time horizons, 4 reversibility tags |
| 07_certification_logic.md | 8-stage pipeline, 4 certificate types, chain rule |
| 08_execution_protocol.md | Auto-execute criteria, escalation protocol, execution packet |
| 09_learning_loop.md | Post-execution review, variance tracking, weight updates |
| 10_glossary.md | Term definitions |
| 11_schema_alignment.md | Schema audit certifying model↔YAML alignment |

---

## Gap Analysis: What Was Found and Closed

### Gaps Identified from Uploaded Files

**1. Missing FastAPI Service Layer** (from `decision_service.py`, `main.py`)
- The uploaded files defined an API contract but had no integration with the engine
- **CLOSED:** Created `service/` package with full endpoint mapping to `process_decision()`

**2. JSON Payload Format Mismatch** (from `sample_payload.json`)
- The sample payload uses flat keys (`"D1"`, `"R1"`, `"T3"`) while engine uses enum dataclasses
- **CLOSED:** Created `converters.py` with bidirectional enum mapping

**3. No CLI Entry Point**
- Engine could only be used programmatically via Python imports
- **CLOSED:** Created `cli.py` with 5 subcommands and proper exit codes

**4. Client Intelligence Engine Not Integrated** (from `Claude_Client_Intelligence_Engine_Spec.md`)
- The spec defined a 15-category survey scoring system with RTQL integration but it wasn't implemented
- **CLOSED:** Created `engine/survey_engine.py` implementing full pipeline

**5. EC Certificate Issuance Required `execution_plan` Field**
- The sample payload didn't include execution_plan, causing EC denial
- **DOCUMENTED:** This is correct behavior — execution_plan is required for EC issuance

### Remaining Open Items

1. **Learning Loop Persistence** — `docs/09_learning_loop.md` describes post-execution variance tracking, but there's no file-based or database storage for historical outcomes. This requires a persistence layer decision (SQLite, Cloudflare D1, or flat-file JSON).

2. **FastAPI Deployment Dependencies** — The service layer requires `fastapi`, `pydantic`, `uvicorn` which aren't available in the current environment. The code is written and validated via syntax check but needs runtime testing with those packages installed.

3. **Test Suite** — The existing `tests/` directory has 6 test files but `pytest` isn't available in this environment. Tests are structurally aligned with the engine but need a full run once the environment has pytest installed.

---

## Validation Results

### Pipeline Demo (5 Scenarios)

| Scenario | Expected | Actual | Status |
|---|---|---|---|
| D1 Reversible Tactical | auto_execute | auto_execute | PASS |
| D3 Financial | escalate_tier_2 | escalate_tier_2 | PASS |
| D6 Irreversible | block | block | PASS |
| RTQL Degraded | escalate_tier_1 | escalate_tier_1 | PASS |
| Missing Data | needs_data | needs_data | PASS |

### Sample Payload Processing

```
Input: sample_payload.json (D1, R1, T3)
Verdict: auto_execute
Value: 21 (strong_candidate)
Trust: T3 (total: 27)
Certificates: QC:issued | VC:issued | TC:issued | EC:issued
Priority: 7.303
```

### Survey Engine Validation

```
3 survey inputs across Revenue, Customer, Systems & Processes
15 categories scored (12 at 0.00 = no input, 3 scored from inputs)
RTQL classifications applied per-input
Research backlog populated for low-trust inputs
Gap analysis functional with trust penalty modifiers
```

---

## Deployment

### Local CLI

```bash
# Evaluate a decision
python cli.py evaluate sample_payload.json

# Run all 5 demo scenarios
python cli.py demo

# Validate without processing
python cli.py validate sample_payload.json
```

### API Server (requires fastapi/uvicorn)

```bash
pip install fastapi uvicorn pydantic
cd /path/to/claude_decision_logic_pack
uvicorn service.app:app --host 0.0.0.0 --port 8000
```

### Endpoints

- `GET /health` — Service health check
- `GET /v1/config` — Current engine configuration
- `POST /v1/decisions/evaluate` — Full pipeline processing
- `POST /v1/decisions/transition` — State machine transition validation
- `POST /v1/decisions/gap-analysis` — Gap analysis with priority ranking
