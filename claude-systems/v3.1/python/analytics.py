from __future__ import annotations

from collections import Counter
from typing import Any, Dict, Iterable, List


def summarize_exceptions(records: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    records = list(records)
    total = len(records)
    exceptions = [r for r in records if r.get("exception_class")]
    counts = Counter(r["exception_class"] for r in exceptions)
    by_prompt = Counter((r.get("prompt_version"), r.get("exception_class")) for r in exceptions)
    return {
        "total_records": total,
        "exception_records": len(exceptions),
        "exception_rate": round((len(exceptions) / total), 4) if total else 0.0,
        "exception_counts": dict(counts),
        "exceptions_by_prompt_version": {f"{k[0]}::{k[1]}": v for k, v in by_prompt.items()},
    }


def codification_candidate_score(metrics: Dict[str, float]) -> float:
    weights = {
        "decision_frequency": 0.20,
        "pattern_repeatability": 0.20,
        "average_confidence": 0.15,
        "exception_rate_inverse": 0.15,
        "estimated_savings_per_run": 0.15,
        "implementation_feasibility": 0.10,
        "review_agreement_rate": 0.05,
    }
    score = 0.0
    for key, weight in weights.items():
        score += float(metrics.get(key, 0.0)) * weight
    return round(min(max(score, 0.0), 1.0), 4)


def rank_codification_candidates(candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    ranked = []
    for item in candidates:
        score = codification_candidate_score(item.get("metrics", {}))
        ranked.append({**item, "codification_candidate_score": score})
    return sorted(ranked, key=lambda x: x["codification_candidate_score"], reverse=True)
