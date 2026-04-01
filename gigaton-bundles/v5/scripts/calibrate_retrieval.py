import json
import sys
from pathlib import Path

LEARNING_RATE = 0.02

def clamp(v, low=0.5, high=1.2):
    return max(low, min(high, round(v, 4)))

def main():
    if len(sys.argv) != 4:
        print("Usage: python calibrate_retrieval.py <weights.json> <feedback.json> <out_dir>")
        sys.exit(1)

    weights_path = Path(sys.argv[1])
    feedback_path = Path(sys.argv[2])
    out_dir = Path(sys.argv[3])
    out_dir.mkdir(parents=True, exist_ok=True)

    cfg = json.loads(weights_path.read_text(encoding="utf-8"))
    data = json.loads(feedback_path.read_text(encoding="utf-8"))

    new_cfg = json.loads(json.dumps(cfg))
    rows = data.get("rows", [])
    if not rows:
        raise SystemExit("No feedback rows provided")

    avg_feedback = sum(r.get("operator_feedback_score", 0) + r.get("output_success_score", 0) for r in rows) / (2 * len(rows))
    delta = (avg_feedback - 0.85) * LEARNING_RATE

    for tier, val in list(new_cfg["base_weights"]["tier_weight"].items()):
        new_cfg["base_weights"]["tier_weight"][tier] = clamp(val + delta)

    # Commercial and knowledge-heavy tasks usually dominate early ROI, so bump slightly if evidenced.
    task_types = " ".join(r.get("task_type", "") for r in rows).lower()
    if "commercial" in task_types:
        cur = new_cfg["base_weights"]["category_weight"]["commercial_systems"]
        new_cfg["base_weights"]["category_weight"]["commercial_systems"] = clamp(cur + 0.01)
    if "knowledge" in task_types or "markdown" in " ".join(r.get("query", "") for r in rows).lower():
        cur = new_cfg["base_weights"]["category_weight"]["knowledge_infrastructure"]
        new_cfg["base_weights"]["category_weight"]["knowledge_infrastructure"] = clamp(cur + 0.01)

    report = {
        "rows_processed": len(rows),
        "average_feedback_score": round(avg_feedback, 4),
        "delta_applied": round(delta, 6),
        "notes": [
            "Human review required before promoting new weights to production.",
            "This script is a starter calibration path, not a final optimizer."
        ]
    }

    (out_dir / "retrieval_scoring_calibration.updated.json").write_text(json.dumps(new_cfg, indent=2), encoding="utf-8")
    (out_dir / "calibration_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"[OK] Wrote calibrated weights and report to {out_dir}")

if __name__ == "__main__":
    main()
