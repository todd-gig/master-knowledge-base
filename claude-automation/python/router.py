from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
MACHINE = ROOT / "machine"

def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def load_yaml_weights(path: Path):
    weights = {}
    section = None
    with path.open("r", encoding="utf-8") as f:
        for raw in f:
            line = raw.rstrip()
            if not line or line.lstrip().startswith("#"):
                continue
            if not line.startswith(" ") and line.endswith(":"):
                section = line[:-1]
                weights[section] = {}
                continue
            if ":" in line and section:
                key, value = [x.strip() for x in line.split(":", 1)]
                weights[section][key] = float(value)
    return weights

@dataclass
class RoutingResult:
    python_score: float
    claude_score: float
    hybrid_score: float
    classification: str

class DecisionRouter:
    def __init__(self):
        self.config = load_json(MACHINE / "routing_config.json")
        self.weights = load_yaml_weights(MACHINE / "scoring_weights.yaml")

    def _score(self, features, bucket):
        total = 0.0
        for key, weight in self.weights.get(bucket, {}).items():
            total += float(features.get(key, 0.0)) * float(weight)
        return round(total, 4)

    def route(self, features):
        python_score = self._score(features, "python")
        claude_score = self._score(features, "claude")
        hybrid_score = self._score(features, "hybrid")
        scores = {
            "Python-First": python_score,
            "Claude-First": claude_score,
            "Hybrid": hybrid_score
        }
        classification = max(scores, key=scores.get)
        return RoutingResult(
            python_score=python_score,
            claude_score=claude_score,
            hybrid_score=hybrid_score,
            classification=classification
        )
