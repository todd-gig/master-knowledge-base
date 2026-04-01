import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from runtime import process_decision
from validation import validate_payload


def _payload():
    return {
        "decision_type": "lead_scoring",
        "normalized_variables": {"employee_count": 120, "industry": "insurance"},
        "routing_classification": "Hybrid",
        "confidence_score": 0.91,
        "recommended_action": "score_and_rank",
        "human_review_required": False,
        "risk_level": "medium",
        "schema_version": "3.1",
        "code_version": "0.2.0",
        "routing_features": {
            "structured_input": 4,
            "explicit_rules": 4,
            "deterministic_output": 4,
            "high_volume": 4,
            "repeatability": 4,
            "stable_logic": 4,
            "ambiguous_input": 1,
            "contextual_reasoning": 1,
            "parse_then_score_viable": 5,
            "codification_path_exists": 5
        },
        "candidate_metrics": {
            "decision_frequency": 0.9,
            "pattern_repeatability": 0.9,
            "average_confidence": 0.95,
            "exception_rate_inverse": 0.85,
            "estimated_savings_per_run": 0.8,
            "implementation_feasibility": 0.8,
            "review_agreement_rate": 0.9
        }
    }


def test_decision_schema_validation_passes():
    valid, errors = validate_payload(_payload(), "decision_schema.json")
    assert valid, errors


def test_runtime_process_decision_sqlite():
    result = process_decision(_payload(), backend="sqlite")
    assert result["classification"] in {"Python-First", "Hybrid", "Claude-First"}
    assert result["prompt_id"] == "claude-core-routing"
