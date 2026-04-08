"""
audit_log.py - claude-systems v3.2
SQLite-backed audit log store for decision records.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

_DDL_DECISION_AUDIT = """
CREATE TABLE IF NOT EXISTS decision_audit (
    -- required fields
    decision_id              TEXT PRIMARY KEY,
    timestamp                TEXT NOT NULL,
    request_type             TEXT,
    input_snapshot           TEXT,          -- JSON blob
    normalized_variables     TEXT,          -- JSON blob
    routing_classification   TEXT,
    chosen_architecture      TEXT,
    python_score             REAL,
    claude_score             REAL,
    hybrid_score             REAL,
    confidence_score         REAL,
    assumptions              TEXT,          -- JSON blob
    exception_class          TEXT,
    recommended_action       TEXT,
    actual_action            TEXT,
    human_review_required    INTEGER,       -- 0/1
    human_review_outcome     TEXT,
    estimated_unit_cost      REAL,
    estimated_failure_cost   REAL,
    codification_candidate   INTEGER,       -- 0/1
    outcome_quality          REAL,
    notes                    TEXT,
    -- optional fields
    model_name               TEXT,
    prompt_version           TEXT,
    code_version             TEXT,
    latency_ms               REAL,
    customer_impact_score    REAL,
    compliance_flag          TEXT,
    rollback_available       INTEGER,       -- 0/1
    -- housekeeping
    created_at               TEXT DEFAULT (datetime('now'))
)
"""

_JSON_FIELDS = {"input_snapshot", "normalized_variables", "assumptions"}


# ---------------------------------------------------------------------------
# AuditLog
# ---------------------------------------------------------------------------

class AuditLog:
    """SQLite-backed audit log.

    Usage::

        log = AuditLog()
        log.init_db("/tmp/audit.db")
        log.log_decision({...})
        records = log.query_decisions({"request_type": "pricing"})
    """

    def __init__(self) -> None:
        self._db_path: Optional[str] = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def init_db(self, db_path: str) -> None:
        """Initialise (or attach to) the SQLite database at *db_path*."""
        self._db_path = db_path
        with self._connect() as conn:
            conn.execute(_DDL_DECISION_AUDIT)
            conn.commit()

    def log_decision(self, record: Dict[str, Any]) -> None:
        """Insert a decision record.  JSON-serialisable values are serialised."""
        self._require_init()
        row = self._prepare_row(record)
        columns = ", ".join(row.keys())
        placeholders = ", ".join(f":{k}" for k in row.keys())
        sql = (
            f"INSERT OR REPLACE INTO decision_audit ({columns}) "
            f"VALUES ({placeholders})"
        )
        with self._connect() as conn:
            conn.execute(sql, row)
            conn.commit()

    def query_decisions(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Return records matching *filters* (exact equality on each key).

        Pass ``None`` or an empty dict to return all records.
        """
        self._require_init()
        where_parts: List[str] = []
        params: Dict[str, Any] = {}
        for k, v in (filters or {}).items():
            where_parts.append(f"{k} = :{k}")
            params[k] = v

        sql = "SELECT * FROM decision_audit"
        if where_parts:
            sql += " WHERE " + " AND ".join(where_parts)
        sql += " ORDER BY timestamp DESC"

        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(sql, params).fetchall()
        return [self._deserialise_row(dict(r)) for r in rows]

    def get_by_id(self, decision_id: str) -> Optional[Dict[str, Any]]:
        """Return a single record by decision_id, or None if not found."""
        self._require_init()
        sql = "SELECT * FROM decision_audit WHERE decision_id = :did"
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(sql, {"did": decision_id}).fetchone()
        return self._deserialise_row(dict(row)) if row else None

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self._db_path)  # type: ignore[arg-type]

    def _require_init(self) -> None:
        if self._db_path is None:
            raise RuntimeError("AuditLog.init_db() must be called before use.")

    @staticmethod
    def _prepare_row(record: Dict[str, Any]) -> Dict[str, Any]:
        row: Dict[str, Any] = {}
        for k, v in record.items():
            if k in _JSON_FIELDS and not isinstance(v, str):
                row[k] = json.dumps(v)
            elif isinstance(v, bool):
                row[k] = int(v)
            elif isinstance(v, (dict, list)):
                row[k] = json.dumps(v)
            else:
                row[k] = v
        # Ensure timestamp exists
        if "timestamp" not in row:
            row["timestamp"] = datetime.utcnow().isoformat()
        return row

    @staticmethod
    def _deserialise_row(row: Dict[str, Any]) -> Dict[str, Any]:
        for field in _JSON_FIELDS:
            val = row.get(field)
            if isinstance(val, str):
                try:
                    row[field] = json.loads(val)
                except (json.JSONDecodeError, TypeError):
                    pass
        return row
