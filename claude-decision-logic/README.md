# Claude Decision Logic Pack

This pack provides a starting operating system for Claude-based executive decision support.

## Primary file
- `claude.md`

## Supporting files
- `docs/01_doctrine.md`
- `docs/02_first_principles_registry.md`
- `docs/03_org_ethos.md`
- `docs/04_value_matrix.md`
- `docs/05_trust_matrix.md`
- `docs/06_decision_taxonomy.md`
- `docs/07_certification_logic.md`
- `docs/08_execution_protocol.md`
- `docs/09_learning_loop.md`
- `docs/10_glossary.md`

## Templates
- `templates/decision_record.template.md`
- `templates/trust_certificate.template.md`
- `templates/value_assessment.template.md`
- `templates/initiative_brief.template.md`

## Schemas / matrices
- `schemas/decision_schema.yaml`
- `matrices/granular_data_matrix.md`

## CLI Usage

The decision engine can be invoked directly via the command-line interface:

```bash
python cli.py evaluate <json_file>      # Run full pipeline and output executive summary
python cli.py validate <json_file>      # Validate payload structure only
python cli.py score <json_file>         # Compute value/trust/alignment scores
python cli.py gaps <json_file>          # Run gap analysis on survey input
python cli.py demo                      # Run 5 built-in test scenarios
```

### Input Format

Decision payloads are provided as JSON files with this structure:

```json
{
  "decision": {
    "decision_id": "DEC-001",
    "title": "...",
    "decision_class": "D1",
    "owner": "...",
    "time_horizon": "immediate",
    "reversibility": "R1",
    "problem_statement": "...",
    "requested_action": "...",
    "context_summary": "...",
    "stakeholders": [...],
    "constraints": [...],
    "value_scores": { "revenue_impact": 0, ... },
    "trust_scores": { "evidence_quality": 0, ... },
    "alignment_scores": { "doctrine_alignment": 0.0, ... },
    "rtql_input": { "claim": "...", "scores": { ... } }
  }
}
```

See `sample_payload.json` for a complete example.

### Output

- **evaluate**: Prints executive summary to stdout; optionally saves full JSON result with `--output`
- **validate**: Prints validation status and decision metadata
- **score**: Prints value, trust, alignment, and priority scores
- **gaps**: Prints gap analysis by severity; optionally saves detailed output
- **demo**: Runs 5 test scenarios with verdicts

### Exit Codes

- `0` = success
- `1` = validation failure
- `2` = runtime error

## Deployment intent
Use `claude.md` as the root instruction file. Ingest the rest as linked operating documents.
