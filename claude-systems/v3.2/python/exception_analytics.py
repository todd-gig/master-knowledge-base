"""
exception_analytics.py - claude-systems v3.2
Compute analytics from exception logs.
"""

from __future__ import annotations

import statistics
from collections import defaultdict
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# ExceptionAnalytics
# ---------------------------------------------------------------------------

class ExceptionAnalytics:
    """Ingest exception records and compute structured analytics.

    Each exception record dict is expected to contain (all optional unless noted):
        exception_class (str)          -- required for class-level metrics
        decision_type / request_type (str)
        prompt_version (str)
        architecture / chosen_architecture (str)
        confidence_score (float)
        human_review_required (bool | int)
        human_review_outcome (str)
        is_exception (bool | int)      -- 1/True if this record IS an exception
        codification_candidate (bool | int)
        path_id / decision_id (str)
    """

    def __init__(self) -> None:
        self._records: List[Dict[str, Any]] = []

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def ingest(self, exception_records: List[Dict[str, Any]]) -> None:
        """Append records to the internal store."""
        self._records.extend(exception_records)

    def compute_metrics(self) -> Dict[str, Any]:
        """Compute and return all analytics metrics as a nested dict."""
        records = self._records
        if not records:
            return {}

        metrics: Dict[str, Any] = {}

        # 1. exception_count_by_class
        count_by_class: Dict[str, int] = defaultdict(int)
        for r in records:
            cls = str(r.get("exception_class", "unknown"))
            count_by_class[cls] += 1
        metrics["exception_count_by_class"] = dict(count_by_class)

        # 2. exception_rate_by_decision_type
        metrics["exception_rate_by_decision_type"] = _rate_by(
            records, "decision_type", "request_type"
        )

        # 3. exception_rate_by_prompt_version
        metrics["exception_rate_by_prompt_version"] = _rate_by(
            records, "prompt_version"
        )

        # 4. exception_rate_by_architecture
        metrics["exception_rate_by_architecture"] = _rate_by(
            records, "chosen_architecture", "architecture"
        )

        # 5. mean_confidence_by_class
        conf_by_class: Dict[str, List[float]] = defaultdict(list)
        for r in records:
            if "confidence_score" in r:
                cls = str(r.get("exception_class", "unknown"))
                conf_by_class[cls].append(float(r["confidence_score"]))
        metrics["mean_confidence_by_class"] = {
            cls: round(statistics.mean(vals), 4)
            for cls, vals in conf_by_class.items()
        }

        # 6. human_escalation_frequency
        total = len(records)
        escalated = sum(
            1 for r in records
            if _truthy(r.get("human_review_required"))
        )
        metrics["human_escalation_frequency"] = {
            "escalated_count": escalated,
            "total_count": total,
            "escalation_rate": round(escalated / total, 4) if total else 0.0,
        }

        return metrics

    def get_codification_backlog(self) -> List[Dict[str, Any]]:
        """Return records flagged as codification candidates, sorted by exception_class."""
        backlog = [
            r for r in self._records
            if _truthy(r.get("codification_candidate"))
        ]
        backlog.sort(key=lambda r: str(r.get("exception_class", "")))
        return backlog


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _truthy(val: Any) -> bool:
    if isinstance(val, bool):
        return val
    if isinstance(val, (int, float)):
        return val != 0
    if isinstance(val, str):
        return val.lower() in ("true", "1", "yes")
    return bool(val)


def _rate_by(
    records: List[Dict[str, Any]],
    primary_key: str,
    fallback_key: Optional[str] = None,
) -> Dict[str, Dict[str, Any]]:
    """Compute per-group exception rate.

    An individual record counts as an exception if its ``exception_class``
    is present and not 'none' / '' / None.
    """
    groups: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for r in records:
        group_val = r.get(primary_key)
        if group_val is None and fallback_key:
            group_val = r.get(fallback_key)
        groups[str(group_val or "unknown")].append(r)

    result: Dict[str, Dict[str, Any]] = {}
    for group, recs in groups.items():
        n = len(recs)
        exc_count = sum(
            1 for r in recs
            if r.get("exception_class") not in (None, "", "none", "None")
        )
        result[group] = {
            "total": n,
            "exception_count": exc_count,
            "exception_rate": round(exc_count / n, 4) if n else 0.0,
        }
    return result
