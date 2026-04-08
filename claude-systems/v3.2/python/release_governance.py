"""
release_governance.py - claude-systems v3.2
Manage release approvals and gate checks for prompt/code versions.
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

_DDL_RELEASE_APPROVALS = """
CREATE TABLE IF NOT EXISTS release_approvals (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    prompt_id           TEXT    NOT NULL,
    version             TEXT    NOT NULL,
    approver            TEXT,
    approved_at         TEXT,
    diff_summary        TEXT,
    test_results_json   TEXT,
    schema_version      TEXT,
    code_version        TEXT,
    rollback_target     TEXT,
    status              TEXT    NOT NULL DEFAULT 'pending',  -- pending|approved|rejected
    requested_at        TEXT    NOT NULL,
    UNIQUE(prompt_id, version)
)
"""

# Release gate policy: minimum approvals required (can be overridden)
DEFAULT_MIN_APPROVALS = 1


# ---------------------------------------------------------------------------
# Public types
# ---------------------------------------------------------------------------

@dataclass
class GateResult:
    passed: bool
    prompt_id: str
    version: str
    checks: Dict[str, bool] = field(default_factory=dict)
    failures: List[str] = field(default_factory=list)
    rollback_target: Optional[str] = None

    def __str__(self) -> str:
        status = "PASS" if self.passed else "FAIL"
        return f"GateResult[{status}] {self.prompt_id}@{self.version} failures={self.failures}"


# ---------------------------------------------------------------------------
# ReleaseGovernance
# ---------------------------------------------------------------------------

class ReleaseGovernance:
    """Manage prompt/code release approvals and gate verification.

    Gate criteria:
      1. Diff summary recorded (non-empty)
      2. Tests pass (test_results_json contains ``"passed": true``)
      3. Approvals meet policy (>=min_approvals approved entries)
      4. Registry updated (``schema_version`` or ``code_version`` present)
      5. Rollback target defined (non-empty ``rollback_target``)
    """

    def __init__(self, db_path: str, min_approvals: int = DEFAULT_MIN_APPROVALS) -> None:
        self._db_path = db_path
        self._min_approvals = min_approvals
        self._init_db()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def request_approval(
        self,
        prompt_id: str,
        version: str,
        diff_summary: str,
        test_results: Dict[str, Any],
        schema_version: Optional[str] = None,
        code_version: Optional[str] = None,
        rollback_target: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create an approval request for a prompt/code release."""
        now = _now()
        sql = """
            INSERT INTO release_approvals
                (prompt_id, version, diff_summary, test_results_json,
                 schema_version, code_version, rollback_target,
                 status, requested_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'pending', ?)
        """
        try:
            with self._connect() as conn:
                conn.execute(sql, (
                    prompt_id, version, diff_summary,
                    json.dumps(test_results),
                    schema_version, code_version, rollback_target, now,
                ))
                conn.commit()
        except sqlite3.IntegrityError as exc:
            raise ValueError(
                f"Approval request for {prompt_id!r} v{version!r} already exists."
            ) from exc
        return self._get_by_pv(prompt_id, version)  # type: ignore[return-value]

    def approve(self, approval_id: int, approver: str) -> Dict[str, Any]:
        """Approve a release request by its integer ID."""
        now = _now()
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE release_approvals
                SET status='approved', approver=?, approved_at=?
                WHERE id=?
                """,
                (approver, now, approval_id),
            )
            conn.commit()
        return self._get_by_id(approval_id)  # type: ignore[return-value]

    def check_release_gate(self, prompt_id: str, version: str) -> GateResult:
        """Evaluate all gate criteria and return a GateResult."""
        record = self._get_by_pv(prompt_id, version)
        result = GateResult(passed=False, prompt_id=prompt_id, version=version)

        if not record:
            result.failures.append("No approval request found for this prompt/version.")
            return result

        # 1. Diff recorded
        diff_ok = bool(record.get("diff_summary", "").strip())
        result.checks["diff_recorded"] = diff_ok
        if not diff_ok:
            result.failures.append("Diff summary is empty.")

        # 2. Tests pass
        test_ok = False
        try:
            tr = json.loads(record.get("test_results_json") or "{}")
            test_ok = bool(tr.get("passed"))
        except (json.JSONDecodeError, TypeError):
            pass
        result.checks["tests_pass"] = test_ok
        if not test_ok:
            result.failures.append("Test results do not indicate passed=true.")

        # 3. Approvals meet policy
        approved_count = self._count_approved(prompt_id, version)
        approvals_ok = approved_count >= self._min_approvals
        result.checks["approvals_met"] = approvals_ok
        if not approvals_ok:
            result.failures.append(
                f"Approvals: {approved_count}/{self._min_approvals} required."
            )

        # 4. Registry updated (schema_version or code_version present)
        registry_ok = bool(
            record.get("schema_version") or record.get("code_version")
        )
        result.checks["registry_updated"] = registry_ok
        if not registry_ok:
            result.failures.append("Neither schema_version nor code_version is set.")

        # 5. Rollback target defined
        rollback = record.get("rollback_target") or ""
        rollback_ok = bool(rollback.strip())
        result.checks["rollback_target_defined"] = rollback_ok
        result.rollback_target = rollback or None
        if not rollback_ok:
            result.failures.append("Rollback target is not defined.")

        result.passed = len(result.failures) == 0
        return result

    def get_rollback_target(self, prompt_id: str, version: str) -> Optional[str]:
        """Return the rollback target string, or None if not set."""
        record = self._get_by_pv(prompt_id, version)
        if not record:
            return None
        target = record.get("rollback_target") or ""
        return target.strip() or None

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(_DDL_RELEASE_APPROVALS)
            conn.commit()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self._db_path)

    def _get_by_pv(self, prompt_id: str, version: str) -> Optional[Dict[str, Any]]:
        sql = """
            SELECT * FROM release_approvals
            WHERE prompt_id=? AND version=?
            ORDER BY id DESC LIMIT 1
        """
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(sql, (prompt_id, version)).fetchone()
        return dict(row) if row else None

    def _get_by_id(self, approval_id: int) -> Optional[Dict[str, Any]]:
        sql = "SELECT * FROM release_approvals WHERE id=?"
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(sql, (approval_id,)).fetchone()
        return dict(row) if row else None

    def _count_approved(self, prompt_id: str, version: str) -> int:
        sql = """
            SELECT COUNT(*) FROM release_approvals
            WHERE prompt_id=? AND version=? AND status='approved'
        """
        with self._connect() as conn:
            return conn.execute(sql, (prompt_id, version)).fetchone()[0]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _now() -> str:
    return datetime.utcnow().isoformat()
