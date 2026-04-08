"""
benchmark_runner.py - claude-systems v3.2
Run benchmarks comparing Claude vs Python across standard dimensions.
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional


# ---------------------------------------------------------------------------
# Benchmark dimensions
# ---------------------------------------------------------------------------

DIMENSIONS: List[str] = [
    "unit_cost",
    "latency",
    "decision_quality",
    "agreement_rate",
    "exception_rate",
    "human_review_burden",
    "codification_savings",
]

# Direction: "lower_is_better" or "higher_is_better"
DIMENSION_DIRECTION: Dict[str, str] = {
    "unit_cost":             "lower_is_better",
    "latency":               "lower_is_better",
    "decision_quality":      "higher_is_better",
    "agreement_rate":        "higher_is_better",
    "exception_rate":        "lower_is_better",
    "human_review_burden":   "lower_is_better",
    "codification_savings":  "higher_is_better",
}

# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

_DDL_BENCHMARK_RUNS = """
CREATE TABLE IF NOT EXISTS benchmark_runs (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    fixture_id          TEXT    NOT NULL,
    python_result_json  TEXT    NOT NULL,
    claude_result_json  TEXT    NOT NULL,
    comparison_json     TEXT    NOT NULL,
    created_at          TEXT    NOT NULL
)
"""


# ---------------------------------------------------------------------------
# Public types
# ---------------------------------------------------------------------------

@dataclass
class BenchmarkResult:
    fixture_id: str
    python_result: Dict[str, Any]
    claude_result: Dict[str, Any]
    comparison: Dict[str, Any]
    winner: Optional[str]       # "python" | "claude" | "tie"
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


# ---------------------------------------------------------------------------
# BenchmarkRunner
# ---------------------------------------------------------------------------

class BenchmarkRunner:
    """Execute benchmarks and persist results to SQLite.

    A *fixture* is a dict with:
        fixture_id (str)             -- unique identifier
        python_fn (callable)         -- zero-arg callable returning a metrics dict
        claude_fn (callable)         -- zero-arg callable returning a metrics dict

    The metrics dict returned by each callable should contain any subset of
    the DIMENSIONS keys (numeric values).
    """

    def __init__(self, db_path: str) -> None:
        self._db_path = db_path
        self._init_db()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run_benchmark(self, fixture: Dict[str, Any]) -> BenchmarkResult:
        """Execute both callables in the fixture and return a BenchmarkResult."""
        fixture_id: str = fixture["fixture_id"]
        python_fn: Callable[[], Dict[str, Any]] = fixture["python_fn"]
        claude_fn: Callable[[], Dict[str, Any]] = fixture["claude_fn"]

        python_result = _safe_call(python_fn)
        claude_result = _safe_call(claude_fn)
        comparison = self.compare_results(python_result, claude_result)
        winner = comparison.get("overall_winner")

        result = BenchmarkResult(
            fixture_id=fixture_id,
            python_result=python_result,
            claude_result=claude_result,
            comparison=comparison,
            winner=winner,
        )
        self._persist(result)
        return result

    def compare_results(
        self,
        python_result: Dict[str, Any],
        claude_result: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Compare Python vs Claude metrics across all shared dimensions."""
        comparison: Dict[str, Any] = {"dimensions": {}}
        python_wins = 0
        claude_wins = 0
        ties = 0

        all_dims = set(python_result) | set(claude_result)
        for dim in DIMENSIONS:
            if dim not in all_dims:
                continue
            py_val = float(python_result.get(dim, float("nan")))
            cl_val = float(claude_result.get(dim, float("nan")))
            direction = DIMENSION_DIRECTION.get(dim, "higher_is_better")

            if _is_nan(py_val) or _is_nan(cl_val):
                winner = "n/a"
            elif py_val == cl_val:
                winner = "tie"
                ties += 1
            elif direction == "lower_is_better":
                winner = "python" if py_val < cl_val else "claude"
                if winner == "python":
                    python_wins += 1
                else:
                    claude_wins += 1
            else:  # higher_is_better
                winner = "python" if py_val > cl_val else "claude"
                if winner == "python":
                    python_wins += 1
                else:
                    claude_wins += 1

            comparison["dimensions"][dim] = {
                "python": py_val,
                "claude": cl_val,
                "direction": direction,
                "winner": winner,
            }

        comparison["python_wins"] = python_wins
        comparison["claude_wins"] = claude_wins
        comparison["ties"] = ties
        if python_wins > claude_wins:
            comparison["overall_winner"] = "python"
        elif claude_wins > python_wins:
            comparison["overall_winner"] = "claude"
        else:
            comparison["overall_winner"] = "tie"

        return comparison

    def get_history(self, fixture_id: str) -> List[Dict[str, Any]]:
        """Return all benchmark runs for *fixture_id*, newest first."""
        sql = """
            SELECT * FROM benchmark_runs
            WHERE fixture_id=?
            ORDER BY created_at DESC
        """
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(sql, (fixture_id,)).fetchall()
        results = []
        for row in rows:
            r = dict(row)
            for key in ("python_result_json", "claude_result_json", "comparison_json"):
                try:
                    r[key.replace("_json", "")] = json.loads(r.pop(key))
                except (json.JSONDecodeError, KeyError):
                    pass
            results.append(r)
        return results

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(_DDL_BENCHMARK_RUNS)
            conn.commit()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self._db_path)

    def _persist(self, result: BenchmarkResult) -> None:
        sql = """
            INSERT INTO benchmark_runs
                (fixture_id, python_result_json, claude_result_json,
                 comparison_json, created_at)
            VALUES (?, ?, ?, ?, ?)
        """
        with self._connect() as conn:
            conn.execute(sql, (
                result.fixture_id,
                json.dumps(result.python_result),
                json.dumps(result.claude_result),
                json.dumps(result.comparison),
                result.created_at,
            ))
            conn.commit()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _safe_call(fn: Callable[[], Dict[str, Any]]) -> Dict[str, Any]:
    try:
        return fn() or {}
    except Exception as exc:
        return {"_error": str(exc)}


def _is_nan(val: float) -> bool:
    try:
        return val != val  # NaN != NaN
    except TypeError:
        return True
