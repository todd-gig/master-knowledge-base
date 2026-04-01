---
title: Scoring Weights
version: 3.0
status: active
category: scoring
tags: [weights, scoring]
---

# Scoring Model
Each signal is scored on a 0-5 scale, then multiplied by its weight.

# Python Weights
- structured_input: 1.2
- explicit_rules: 1.3
- deterministic_output: 1.4
- high_volume: 1.4
- low_error_tolerance: 1.3
- auditability_required: 1.2
- latency_sensitivity: 1.1
- repeatability: 1.3
- stable_logic: 1.4

# Claude Weights
- ambiguous_input: 1.4
- contextual_reasoning: 1.3
- incomplete_rules: 1.3
- novel_cases: 1.2
- synthesis_required: 1.3
- edge_case_frequency: 1.2
- high_learning_value: 1.1
- semantic_variability: 1.2
- interpretation_burden: 1.4

# Hybrid Weights
- parse_then_score_viable: 1.5
- exception_isolation_possible: 1.3
- structured_output_possible: 1.4
- mid_maturity_logic: 1.3
- rapid_deployment_needed: 1.1
- codification_path_exists: 1.5

# Decision Thresholds
- one mode >= 15% above others -> choose that mode
- Hybrid within 10% of top score with clear codification path -> choose Hybrid
- critical business risk + weak determinism -> avoid Pure Python without review
- massive volume + stable rules -> avoid Pure Claude
