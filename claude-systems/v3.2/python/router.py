from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
from typing import Dict, Any

ROOT = Path(__file__).resolve().parents[1]
MACHINE = ROOT / "machine"


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_yaml_weights(path: Path) -> Dict[str, Any]:
    weights: Dict[str, Any] = {}
    current_section = None
    with path.open("r", encoding="utf-8") as f:
        for raw in f:
            line = raw.rstrip()
            if not line or line.lstrip().startswith("#"):
                continue
            if not line.startswith(" ") and line.endswith(":"):
                current_section = line[:-1]
                weights[current_section] = {}
                continue
            if ":" in line and current_section:
                key, value = [x.strip() for x in line.split(":", 1)]
                try:
                    parsed = float(value.strip('"'))
                except ValueError:
                    parsed = value.strip('"')
                weights[current_section][key] = parsed
    return weights


@dataclass
class RoutingResult:
    python_score: float
    claude_score: float
    hybrid_score: float
    classification: str


class DecisionRouter:
    def __init__(self) -> None:
        self.config = load_json(MACHINE / "routing_config.json")
        self.weights = load_yaml_weights(MACHINE / "scoring_weights.yaml")

    def _score(self, features: Dict[str, float], bucket: str) -> float:
        total = 0.0
        for key, weight in self.weights.get(bucket, {}).items():
            if key in ("dominance_margin_pct", "hybrid_within_top_pct", "high_confidence_min", "moderate_confidence_min", "low_confidence_min"):
                continue
            total += float(features.get(key, 0.0)) * float(weight)
        return round(total, 4)

    def route(self, features: Dict[str, float]) -> RoutingResult:
        python_score = self._score(features, "python")
        claude_score = self._score(features, "claude")
        hybrid_score = self._score(features, "hybrid")
        scores = {
            "Python-First": python_score,
            "Claude-First": claude_score,
            "Hybrid": hybrid_score,
        }
        classification = max(scores, key=scores.get)
        return RoutingResult(
            python_score=python_score,
            claude_score=claude_score,
            hybrid_score=hybrid_score,
            classification=classification,
        )


if __name__ == "__main__":
    router = DecisionRouter()
    sample_features = {
        "structured_input": 5,
        "explicit_rules": 5,
        "deterministic_output": 5,
        "high_volume": 4,
        "repeatability": 5,
        "stable_logic": 5,
        "ambiguous_input": 1,
        "contextual_reasoning": 1,
        "parse_then_score_viable": 2,
        "codification_path_exists": 4,
    }
    result = router.route(sample_features)
    print(result)
