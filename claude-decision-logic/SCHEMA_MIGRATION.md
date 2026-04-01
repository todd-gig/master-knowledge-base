# Decision Schema Breaking Changes

**Last Updated:** 2026-03-24  
**Previous Schema Version:** Deprecated (legacy)  
**Current Schema Version:** v2  

## Overview

The decision schema has been significantly refactored to align with the actual `DecisionObject` data model in `engine/models.py`. This document describes the breaking changes and provides migration guidance.

## Breaking Changes

### 1. Field Renames

| Old Field Name | New Field Name | Type Change | Notes |
|---|---|---|---|
| `type` | `decision_class` | String → Enum | Must use DecisionClass enum (D0-D6) |
| `urgency` | `time_horizon` | String → Enum | Must use TimeHorizon enum (IMMEDIATE, NEAR_TERM, MID_TERM, LONG_TERM) |
| (new) | `reversibility` | — | New required field; use ReversibilityTag enum (R1-R4) |
| (new) | `problem_statement` | — | New required field; explicit problem definition |

### 2. Field Consolidations

#### Old Approach (Single Values)
```yaml
decision_object:
  - expected_value    # Single number
  - cost              # Single number
  - risk              # Single number
  - urgency           # Single enum value
  - trust_score       # Single number
```

#### New Approach (Composite Objects)

**Value Scores** (`value_scores`: ValueScores object)
```yaml
value_scores:
  # Positive dimensions (0-5)
  revenue_impact: 3
  cost_efficiency: 4
  time_leverage: 3
  strategic_alignment: 4
  customer_human_benefit: 2
  knowledge_asset_creation: 2
  compounding_potential: 3
  reversibility: 4
  # Penalty dimensions (0-5, subtracted from gross)
  downside_risk: 1
  execution_drag: 2
  uncertainty: 2
  ethical_misalignment: 0
```

**Trust Scores** (`trust_scores`: TrustScores object)
```yaml
trust_scores:
  evidence_quality: 4
  logic_integrity: 4
  outcome_history: 3
  context_fit: 4
  stakeholder_clarity: 3
  risk_containment: 3
  auditability: 3
```

**Time Horizon** (replaced `urgency`)
```yaml
time_horizon: "IMMEDIATE"  # or NEAR_TERM, MID_TERM, LONG_TERM
```

### 3. New Required Fields

- `decision_class`: Classification of decision (D0-D6)
- `reversibility`: Reversibility tag (R1-R4)
- `problem_statement`: Explicit problem being solved
- `time_horizon`: Time window for decision
- `value_scores`: Composite value assessment
- `trust_scores`: Composite trust assessment
- `evidence_refs`: At least one evidence reference required

## Value Assessment Migration

**Old scoring (implicit):**
```yaml
expected_value: 25
cost: 5
risk: 3
```

**New scoring (explicit dimensions):**
```yaml
value_scores:
  revenue_impact: 5
  cost_efficiency: 4
  time_leverage: 4
  strategic_alignment: 4
  customer_human_benefit: 3
  knowledge_asset_creation: 2
  compounding_potential: 3
  reversibility: 4
  downside_risk: 1
  execution_drag: 1
  uncertainty: 2
  ethical_misalignment: 0
```

Equivalent net value: (5+4+4+4+3+2+3+4) - (1+1+2+0) = 29 - 4 = 25

## Migration Path

1. **Rename fields:** `type` → `decision_class`, `urgency` → `time_horizon`
2. **Add new required fields:** `reversibility`, `problem_statement`
3. **Decompose single values into composite objects:** Split value, cost, risk into ValueScores dimensions
4. **Validate:** Run through DecisionObject.validate()

See full document for detailed examples and rollback procedures.
