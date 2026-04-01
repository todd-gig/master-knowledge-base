import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from router import DecisionRouter


def test_python_first_routing():
    router = DecisionRouter()
    result = router.route({
        "structured_input": 5,
        "explicit_rules": 5,
        "deterministic_output": 5,
        "high_volume": 4,
        "repeatability": 5,
        "stable_logic": 5,
        "ambiguous_input": 0,
        "contextual_reasoning": 0,
        "codification_path_exists": 4,
    })
    assert result.classification == "Python-First"
