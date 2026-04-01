---
title: Decision Variables Registry
version: 3.0
status: active
category: variables
tags: [variables, ontology]
---

# Core Variables
## Input Variables
- `input_structure`: structured | semi_structured | unstructured
- `input_quality`: low | medium | high
- `input_completeness`: partial | sufficient | complete
- `source_reliability`: unknown | mixed | trusted

## Logic Variables
- `logic_clarity`: low | medium | high
- `rule_stability`: volatile | emerging | stable
- `threshold_defined`: true | false
- `scoring_possible`: true | false

## Execution Variables
- `decision_volume`: low | medium | high | massive
- `latency_sensitivity`: low | medium | high
- `auditability_requirement`: low | medium | high
- `determinism_requirement`: low | medium | high

## Risk Variables
- `business_risk`: low | medium | high | critical
- `error_cost`: low | medium | high | severe
- `compliance_exposure`: none | low | medium | high
- `reversibility`: reversible | partially_reversible | irreversible

## Learning Variables
- `novelty_level`: low | medium | high
- `exception_frequency`: low | medium | high
- `pattern_repeatability`: low | medium | high
- `codification_readiness`: low | medium | high

## Value Variables
- `unit_value_of_correct_decision`
- `unit_cost_of_decision`
- `unit_cost_of_failure`
- `cost_of_latency`
- `cost_of_human_review`
- `estimated_codification_cost`
