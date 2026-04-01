import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from router import DecisionRouter

def test_routing_python_first():
    router = DecisionRouter()
    result = router.route({
        "structured_input": 5,
        "explicit_rules": 5,
        "deterministic_output": 5,
        "high_volume": 4,
        "repeatability": 5,
        "stable_logic": 5
    })
    assert result.classification == "Python-First"
