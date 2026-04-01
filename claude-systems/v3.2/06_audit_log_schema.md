---
title: Audit Log Schema
version: 3.0
status: active
category: schema
tags: [audit, logging]
---

# Required Fields
- decision_id
- timestamp
- request_type
- input_snapshot
- normalized_variables
- routing_classification
- chosen_architecture
- python_score
- claude_score
- hybrid_score
- confidence_score
- assumptions
- exception_class
- recommended_action
- actual_action
- human_review_required
- human_review_outcome
- estimated_unit_cost
- estimated_failure_cost
- codification_candidate
- outcome_quality
- notes

# Optional Fields
- model_name
- prompt_version
- code_version
- latency_ms
- customer_impact_score
- compliance_flag
- rollback_available

# Purpose
Use this schema to audit decisions, compare cost vs quality, identify codification candidates, and track model or rules drift.
