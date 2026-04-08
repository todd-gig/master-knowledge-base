"""
migration_loop.py - claude-systems v3.2
Track Claude-to-Python migration progress and surface migration candidates.
"""

from __future__ import annotations

import statistics
from collections import defaultdict
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# KPI keys
# ---------------------------------------------------------------------------

KPI_RECURRING_INFERENCE_COST   = "recurring_inference_cost"
KPI_PYTHON_HANDLED_VOLUME      = "python_handled_volume"
KPI_DECISION_QUALITY           = "decision_quality"
KPI_EXCEPTION_RATE             = "exception_rate"
KPI_CODIFICATION_PAYBACK       = "codification_payback_period"

ALL_KPIS: List[str] = [
    KPI_RECURRING_INFERENCE_COST,
    KPI_PYTHON_HANDLED_VOLUME,
    KPI_DECISION_QUALITY,
    KPI_EXCEPTION_RATE,
    KPI_CODIFICATION_PAYBACK,
]

# Directions: "down" means improvement = decrease, "up" = increase
KPI_DIRECTION: Dict[str, str] = {
    KPI_RECURRING_INFERENCE_COST: "down",
    KPI_PYTHON_HANDLED_VOLUME:    "up",
    KPI_DECISION_QUALITY:         "up",
    KPI_EXCEPTION_RATE:           "down",
    KPI_CODIFICATION_PAYBACK:     "down",
}


# ---------------------------------------------------------------------------
# MigrationLoop
# ---------------------------------------------------------------------------

class MigrationLoop:
    """Track migration cycles and surface KPI trends and migration candidates.

    Each cycle record is a dict with at minimum:
        cycle_id (str | int), timestamp (str | float)
    Plus any subset of the KPI keys and additional fields for candidates.

    For migration candidates, audit log records should include:
        path_id (str), routing_classification (str), exception_rate (float),
        python_handled_volume (float | int), codification_candidate (bool),
        outcome_quality (float)
    """

    def __init__(self) -> None:
        self._cycles: List[Dict[str, Any]] = []

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def record_cycle(self, cycle_data: Dict[str, Any]) -> None:
        """Append a migration cycle snapshot."""
        self._cycles.append(dict(cycle_data))

    def get_trends(self) -> Dict[str, Any]:
        """Return trend statistics for each KPI across all recorded cycles.

        Returns a dict keyed by KPI name, each containing:
            values (list), mean, stdev, trend_direction, improving (bool)
        """
        if not self._cycles:
            return {}

        trends: Dict[str, Any] = {}
        for kpi in ALL_KPIS:
            values = [
                float(c[kpi])
                for c in self._cycles
                if kpi in c
            ]
            if not values:
                continue

            mean_val = statistics.mean(values)
            stdev_val = statistics.pstdev(values) if len(values) > 1 else 0.0
            # Simple trend: compare last value to first
            if len(values) >= 2:
                delta = values[-1] - values[0]
                direction = "down" if delta < 0 else ("up" if delta > 0 else "flat")
            else:
                direction = "flat"

            desired = KPI_DIRECTION.get(kpi, "up")
            improving = (direction == desired) or direction == "flat"

            trends[kpi] = {
                "values": values,
                "mean": round(mean_val, 6),
                "stdev": round(stdev_val, 6),
                "trend_direction": direction,
                "desired_direction": desired,
                "improving": improving,
                "latest": values[-1],
            }

        return trends

    def identify_migration_candidates(
        self, audit_log: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Analyse audit log records and return migration candidates.

        Candidates are decision paths where:
          - ``codification_candidate`` is truthy, OR
          - ``routing_classification`` is 'Claude-First' and
            ``exception_rate`` <= 0.05 (low exceptions) and
            ``outcome_quality`` >= 0.7
        Records are grouped by ``path_id`` (or ``request_type`` as fallback)
        and ranked by migration_score descending.
        """
        grouped: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        for record in audit_log:
            key = str(record.get("path_id") or record.get("request_type", "unknown"))
            grouped[key].append(record)

        candidates: List[Dict[str, Any]] = []
        for path_id, records in grouped.items():
            n = len(records)
            explicit_candidates = [r for r in records if r.get("codification_candidate")]
            avg_quality = _avg(records, "outcome_quality")
            avg_exception = _avg(records, "exception_rate")
            avg_volume = _avg(records, "python_handled_volume")
            routing_modes = [r.get("routing_classification", "") for r in records]
            claude_pct = routing_modes.count("Claude-First") / n if n else 0.0

            is_candidate = bool(explicit_candidates) or (
                claude_pct >= 0.5
                and avg_exception <= 0.05
                and avg_quality >= 0.7
            )

            if is_candidate:
                # Migration score: quality * (1 - exception_rate) * (claude % indicates need)
                migration_score = avg_quality * (1 - avg_exception) * claude_pct
                candidates.append({
                    "path_id": path_id,
                    "record_count": n,
                    "explicit_candidate_count": len(explicit_candidates),
                    "avg_outcome_quality": round(avg_quality, 4),
                    "avg_exception_rate": round(avg_exception, 4),
                    "avg_python_volume": round(avg_volume, 4),
                    "claude_routing_pct": round(claude_pct, 4),
                    "migration_score": round(migration_score, 4),
                })

        candidates.sort(key=lambda c: c["migration_score"], reverse=True)
        return candidates


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _avg(records: List[Dict[str, Any]], key: str) -> float:
    vals = [float(r[key]) for r in records if key in r]
    return statistics.mean(vals) if vals else 0.0
