---
title: Routing Rubric
version: 3.0
status: active
category: rubric
tags: [routing, rubric]
---

# Objective
Classify each decision as `Python-First`, `Claude-First`, or `Hybrid`.

# Python Suitability Signals
Score 0-5 each:
- structured input
- explicit rules
- deterministic output
- high volume
- low error tolerance
- high auditability requirement
- high repeatability
- high latency sensitivity
- stable logic

# Claude Suitability Signals
Score 0-5 each:
- ambiguous input
- contextual reasoning required
- incomplete rules
- novel cases common
- synthesis required
- edge case frequency high
- semantic variability high
- exploration value high
- user intent underspecified

# Hybrid Signals
Use Hybrid when:
- unstructured input can be normalized,
- Python can score or execute,
- exceptions can be isolated,
- rapid deployment matters,
- a codification path clearly exists.

# Routing Rules
- Python score materially higher -> `Python-First`
- Claude score materially higher -> `Claude-First`
- both high in different layers -> `Hybrid`

# Tie-Break Rule
When uncertain, choose `Hybrid` and isolate the expensive reasoning to the smallest possible surface area.
