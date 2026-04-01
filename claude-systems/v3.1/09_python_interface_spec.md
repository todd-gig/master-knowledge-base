---
title: Python Interface Specification
version: 3.0
status: active
category: interface
tags: [python, interface]
---

# Objective
Define the contract between Claude outputs and Python execution services.

# Input Contract
Claude should emit structured payloads with:
- decision_type
- normalized_variables
- routing_classification
- confidence_score
- exception_flags
- recommended_action
- review_required

# Output Contract
Python should return:
- execution_status
- applied_rules
- computed_scores
- result_payload
- error_flags
- execution_latency_ms
- audit_reference

# Design Rule
Claude should never pass vague prose to Python when a schema can be emitted instead.
