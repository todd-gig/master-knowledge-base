"""
sql_views.py - claude-systems v3.2
Create and manage SQL views over the audit/prompt/benchmark tables.
"""

from __future__ import annotations

import sqlite3
from typing import List


# ---------------------------------------------------------------------------
# View definitions
# ---------------------------------------------------------------------------

_VIEW_EXCEPTION_SUMMARY = """
CREATE VIEW IF NOT EXISTS vw_exception_summary AS
SELECT
    exception_class,
    request_type,
    COUNT(*)                                        AS total_decisions,
    SUM(CASE WHEN exception_class NOT IN ('', 'none', 'None') THEN 1 ELSE 0 END)
                                                    AS exception_count,
    ROUND(
        CAST(SUM(CASE WHEN exception_class NOT IN ('', 'none', 'None') THEN 1 ELSE 0 END) AS REAL)
        / NULLIF(COUNT(*), 0),
        4
    )                                               AS exception_rate,
    AVG(confidence_score)                           AS mean_confidence,
    SUM(CASE WHEN human_review_required = 1 THEN 1 ELSE 0 END)
                                                    AS human_escalations
FROM decision_audit
GROUP BY exception_class, request_type
"""

_VIEW_PROMPT_PERFORMANCE = """
CREATE VIEW IF NOT EXISTS vw_prompt_performance AS
SELECT
    prompt_version,
    COUNT(*)                                        AS decision_count,
    AVG(outcome_quality)                            AS avg_outcome_quality,
    AVG(confidence_score)                           AS avg_confidence,
    ROUND(
        CAST(SUM(CASE WHEN exception_class NOT IN ('', 'none', 'None', NULL) THEN 1 ELSE 0 END) AS REAL)
        / NULLIF(COUNT(*), 0),
        4
    )                                               AS exception_rate,
    AVG(latency_ms)                                 AS avg_latency_ms,
    SUM(CASE WHEN human_review_required = 1 THEN 1 ELSE 0 END)
                                                    AS human_review_count
FROM decision_audit
WHERE prompt_version IS NOT NULL
GROUP BY prompt_version
"""

_VIEW_CODIFICATION_BACKLOG = """
CREATE VIEW IF NOT EXISTS vw_codification_backlog AS
SELECT
    request_type,
    routing_classification,
    COUNT(*)                                        AS record_count,
    AVG(outcome_quality)                            AS avg_quality,
    AVG(confidence_score)                           AS avg_confidence,
    AVG(estimated_unit_cost)                        AS avg_unit_cost,
    ROUND(
        CAST(SUM(CASE WHEN exception_class NOT IN ('', 'none', 'None', NULL) THEN 1 ELSE 0 END) AS REAL)
        / NULLIF(COUNT(*), 0),
        4
    )                                               AS exception_rate,
    SUM(CASE WHEN codification_candidate = 1 THEN 1 ELSE 0 END)
                                                    AS candidate_count
FROM decision_audit
WHERE codification_candidate = 1
   OR routing_classification = 'Claude-First'
GROUP BY request_type, routing_classification
ORDER BY avg_quality DESC
"""

_VIEW_COST_QUALITY_COMPARISON = """
CREATE VIEW IF NOT EXISTS vw_cost_quality_comparison AS
SELECT
    chosen_architecture,
    request_type,
    COUNT(*)                                        AS decision_count,
    AVG(estimated_unit_cost)                        AS avg_unit_cost,
    AVG(estimated_failure_cost)                     AS avg_failure_cost,
    AVG(outcome_quality)                            AS avg_outcome_quality,
    AVG(confidence_score)                           AS avg_confidence,
    AVG(latency_ms)                                 AS avg_latency_ms,
    SUM(CASE WHEN human_review_required = 1 THEN 1 ELSE 0 END)
                                                    AS human_review_count,
    ROUND(
        CAST(SUM(CASE WHEN exception_class NOT IN ('', 'none', 'None', NULL) THEN 1 ELSE 0 END) AS REAL)
        / NULLIF(COUNT(*), 0),
        4
    )                                               AS exception_rate
FROM decision_audit
GROUP BY chosen_architecture, request_type
ORDER BY avg_outcome_quality DESC, avg_unit_cost ASC
"""

ALL_VIEWS: List[str] = [
    _VIEW_EXCEPTION_SUMMARY,
    _VIEW_PROMPT_PERFORMANCE,
    _VIEW_CODIFICATION_BACKLOG,
    _VIEW_COST_QUALITY_COMPARISON,
]

VIEW_NAMES: List[str] = [
    "vw_exception_summary",
    "vw_prompt_performance",
    "vw_codification_backlog",
    "vw_cost_quality_comparison",
]


# ---------------------------------------------------------------------------
# ViewManager
# ---------------------------------------------------------------------------

class ViewManager:
    """Create and refresh SQL views in a target SQLite database.

    Note: SQLite does not support materialised views, so ``refresh_views``
    simply recreates all views (dropping and re-creating them) to pick up
    any schema changes.
    """

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def create_views(self, db_path: str) -> List[str]:
        """Create all views in the database.  Returns list of view names created."""
        with self._connect(db_path) as conn:
            for ddl in ALL_VIEWS:
                conn.execute(ddl)
            conn.commit()
        return list(VIEW_NAMES)

    def refresh_views(self, db_path: str) -> List[str]:
        """Drop and recreate all views.  Returns list of view names refreshed."""
        with self._connect(db_path) as conn:
            for name in VIEW_NAMES:
                conn.execute(f"DROP VIEW IF EXISTS {name}")
            for ddl in ALL_VIEWS:
                conn.execute(ddl)
            conn.commit()
        return list(VIEW_NAMES)

    def list_views(self, db_path: str) -> List[str]:
        """Return view names that currently exist in the database."""
        sql = "SELECT name FROM sqlite_master WHERE type='view' ORDER BY name"
        with self._connect(db_path) as conn:
            rows = conn.execute(sql).fetchall()
        return [r[0] for r in rows]

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    @staticmethod
    def _connect(db_path: str) -> sqlite3.Connection:
        return sqlite3.connect(db_path)
