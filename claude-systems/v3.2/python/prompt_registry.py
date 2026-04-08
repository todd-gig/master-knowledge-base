"""
prompt_registry.py - claude-systems v3.2
Track versioned prompts with lifecycle status management.
"""

from __future__ import annotations

import hashlib
import sqlite3
from datetime import datetime
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

_DDL_PROMPT_RELEASES = """
CREATE TABLE IF NOT EXISTS prompt_releases (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    prompt_id    TEXT    NOT NULL,
    version      TEXT    NOT NULL,
    content_hash TEXT    NOT NULL,
    content      TEXT    NOT NULL,
    status       TEXT    NOT NULL DEFAULT 'draft',  -- draft|active|deprecated
    created_at   TEXT    NOT NULL,
    activated_at TEXT,
    deprecated_at TEXT,
    UNIQUE(prompt_id, version)
)
"""

VALID_STATUSES = ("draft", "active", "deprecated")


# ---------------------------------------------------------------------------
# PromptRegistry
# ---------------------------------------------------------------------------

class PromptRegistry:
    """Store, version, and manage lifecycle of prompts.

    Usage::

        reg = PromptRegistry("/tmp/registry.db")
        reg.register("classify_intent", "1.0", "You are a ...")
        reg.activate("classify_intent", "1.0")
        active = reg.get_active("classify_intent")
    """

    def __init__(self, db_path: str) -> None:
        self._db_path = db_path
        self._init_db()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def register(self, prompt_id: str, version: str, content: str) -> Dict[str, Any]:
        """Register a new prompt version as *draft*."""
        content_hash = _sha256(content)
        now = _now()
        sql = """
            INSERT INTO prompt_releases
                (prompt_id, version, content_hash, content, status, created_at)
            VALUES (?, ?, ?, ?, 'draft', ?)
        """
        try:
            with self._connect() as conn:
                conn.execute(sql, (prompt_id, version, content_hash, content, now))
                conn.commit()
        except sqlite3.IntegrityError as exc:
            raise ValueError(
                f"Prompt {prompt_id!r} version {version!r} already exists."
            ) from exc
        return self._get(prompt_id, version)

    def activate(self, prompt_id: str, version: str) -> Dict[str, Any]:
        """Activate a prompt version (deprecates the previously active version)."""
        record = self._get(prompt_id, version)
        if not record:
            raise KeyError(f"Prompt {prompt_id!r} version {version!r} not found.")
        now = _now()
        with self._connect() as conn:
            # Deprecate any currently active version
            conn.execute(
                """
                UPDATE prompt_releases
                SET status='deprecated', deprecated_at=?
                WHERE prompt_id=? AND status='active'
                """,
                (now, prompt_id),
            )
            # Activate the requested version
            conn.execute(
                """
                UPDATE prompt_releases
                SET status='active', activated_at=?
                WHERE prompt_id=? AND version=?
                """,
                (now, prompt_id, version),
            )
            conn.commit()
        return self._get(prompt_id, version)

    def deprecate(self, prompt_id: str, version: str) -> Dict[str, Any]:
        """Explicitly deprecate a prompt version."""
        record = self._get(prompt_id, version)
        if not record:
            raise KeyError(f"Prompt {prompt_id!r} version {version!r} not found.")
        now = _now()
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE prompt_releases
                SET status='deprecated', deprecated_at=?
                WHERE prompt_id=? AND version=?
                """,
                (now, prompt_id, version),
            )
            conn.commit()
        return self._get(prompt_id, version)

    def get_active(self, prompt_id: str) -> Optional[Dict[str, Any]]:
        """Return the currently active record for *prompt_id*, or None."""
        sql = """
            SELECT * FROM prompt_releases
            WHERE prompt_id=? AND status='active'
            LIMIT 1
        """
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(sql, (prompt_id,)).fetchone()
        return dict(row) if row else None

    def list_versions(self, prompt_id: str) -> List[Dict[str, Any]]:
        """Return all versions for *prompt_id*, newest first."""
        sql = """
            SELECT * FROM prompt_releases
            WHERE prompt_id=?
            ORDER BY created_at DESC
        """
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(sql, (prompt_id,)).fetchall()
        return [dict(r) for r in rows]

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(_DDL_PROMPT_RELEASES)
            conn.commit()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self._db_path)

    def _get(self, prompt_id: str, version: str) -> Optional[Dict[str, Any]]:
        sql = """
            SELECT * FROM prompt_releases
            WHERE prompt_id=? AND version=?
            LIMIT 1
        """
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(sql, (prompt_id, version)).fetchone()
        return dict(row) if row else None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _now() -> str:
    return datetime.utcnow().isoformat()
