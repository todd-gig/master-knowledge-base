import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from migrate import load_manifest
from release_manager import evaluate_release, prompt_diff
from benchmark import load_fixtures, compare_modes


def test_manifest_has_ordered_migrations():
    manifest = load_manifest()
    assert len(manifest) >= 4
    assert manifest[0]["id"] == "001"


def test_prompt_diff_detects_change():
    diff = prompt_diff("alpha\n", "alpha\nbeta\n")
    assert "beta" in diff


def test_release_approval_threshold():
    approvals = [
        {"decision": "approve"},
        {"decision": "approve"},
        {"decision": "reject"},
    ]
    assert evaluate_release(approvals, minimum_required=2) is True


def test_benchmark_fixtures_load():
    fixtures = load_fixtures()
    assert len(fixtures) >= 3


def test_compare_modes():
    summary = compare_modes([
        {"execution_mode": "Claude", "unit_cost": 0.02, "latency_ms": 1200, "quality_score": 0.91, "agreement_rate": 0.88, "exception_rate": 0.12, "human_review_rate": 0.20},
        {"execution_mode": "Python", "unit_cost": 0.0001, "latency_ms": 20, "quality_score": 0.94, "agreement_rate": 0.94, "exception_rate": 0.03, "human_review_rate": 0.01},
    ])
    assert "Claude" in summary and "Python" in summary
