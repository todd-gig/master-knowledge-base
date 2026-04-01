from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any, List

ROOT = Path(__file__).resolve().parents[1]
MACHINE = ROOT / "machine"


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_fixtures() -> List[Dict[str, Any]]:
    return load_json(MACHINE / "benchmark_fixtures.json")["fixtures"]


def compare_modes(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    summary: Dict[str, Dict[str, float]] = {}
    counts: Dict[str, int] = {}
    for row in results:
        mode = row["execution_mode"]
        summary.setdefault(mode, {
            "unit_cost": 0.0,
            "latency_ms": 0.0,
            "quality_score": 0.0,
            "agreement_rate": 0.0,
            "exception_rate": 0.0,
            "human_review_rate": 0.0,
        })
        counts[mode] = counts.get(mode, 0) + 1
        for key in summary[mode]:
            summary[mode][key] += float(row.get(key, 0.0))
    for mode, metrics in summary.items():
        n = counts[mode]
        for key in metrics:
            metrics[key] = round(metrics[key] / n, 4) if n else 0.0
    return summary


if __name__ == "__main__":
    fixtures = load_fixtures()
    print(json.dumps({"fixture_count": len(fixtures), "fixtures": fixtures}, indent=2))
