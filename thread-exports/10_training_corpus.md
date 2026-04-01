    ---
    title: Training Corpus
    tags:
      - training
  - prompting
type: training-note
    status: draft
    created: 2026-03-26
    updated: 2026-03-26
    purpose: >
      Capture prompts, routing logic, and training instructions.
    ---
# Training Corpus

## Root training principle

Train the model to convert ambiguous organizational problems into:
- capabilities
- skills
- roles
- team structure
- supervision logic
- negotiation activity plans

## Core routing prompt

Always think in this sequence:

`problem -> capability gap -> skill requirements -> role requirements -> team structure -> supervision model -> negotiation activities -> ROI-ranked recommendation`

## Companion file usage

- `CLAUDE.md`: root control logic
- `machine/skill_ontology.json`: atomic skill classification
- `machine/team_structure_rules.json`: org and supervision rules
- `machine/negotiation_framework.json`: negotiation analysis
- `machine/output_template.json`: default response structure
