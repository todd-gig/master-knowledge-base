"""
db_migrations.py - claude-systems v3.2
Simple migration runner for SQLite.  Reads numbered .sql files from a
migrations/ directory and tracks applied migrations in a _migrations table.
"""

from __future__ import annotations

import os
import re
import sqlite3
from datetime import datetime
from typing import List, Optional, Tuple


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

_DDL_MIGRATIONS_TABLE = """
CREATE TABLE IF NOT EXISTS _migrations (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    filename    TEXT    NOT NULL UNIQUE,
    applied_at  TEXT    NOT NULL,
    checksum    TEXT
)
"""


# ---------------------------------------------------------------------------
# MigrationRunner
# ---------------------------------------------------------------------------

class MigrationRunner:
    """Apply and rollback numbered SQL migration files.

    Migration files must be named ``<NNN>_<description>.sql`` (e.g.
    ``001_create_audit.sql``).  They are applied in ascending numeric order.

    Rollback executes the last applied migration's SQL in reverse line order
    (simple approach: it drops objects whose CREATE statements appear in the
    migration — callers should write explicit rollback scripts for complex
    migrations).

    Usage::

        runner = MigrationRunner()
        runner.init("/tmp/app.db", "/path/to/migrations")
        runner.apply_pending()
        print(runner.get_status())
    """

    def __init__(self) -> None:
        self._db_path: Optional[str] = None
        self._migrations_dir: Optional[str] = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def init(self, db_path: str, migrations_dir: str) -> None:
        """Set database path and migrations directory, create tracking table."""
        self._db_path = db_path
        self._migrations_dir = migrations_dir
        with self._connect() as conn:
            conn.execute(_DDL_MIGRATIONS_TABLE)
            conn.commit()

    def apply_pending(self) -> List[str]:
        """Apply all unapplied migrations in order.  Returns list of applied filenames."""
        self._require_init()
        applied = self._get_applied_set()
        pending = self._get_pending(applied)
        results: List[str] = []
        for filename, sql_path in pending:
            sql = self._read_sql(sql_path)
            with self._connect() as conn:
                # Execute each statement in the file
                for stmt in _split_statements(sql):
                    if stmt.strip():
                        conn.execute(stmt)
                conn.execute(
                    "INSERT INTO _migrations (filename, applied_at) VALUES (?, ?)",
                    (filename, _now()),
                )
                conn.commit()
            results.append(filename)
        return results

    def rollback_last(self) -> Optional[str]:
        """Roll back the most recently applied migration.

        Returns the filename that was rolled back, or None if nothing to roll back.
        Note: This removes the migration record.  Callers should write explicit
        DOWN migration files (``<NNN>_<desc>.down.sql``) alongside their UP files
        for complex rollbacks.
        """
        self._require_init()
        last = self._get_last_applied()
        if not last:
            return None
        filename, migration_id = last

        # Try to load a corresponding .down.sql
        base = filename.replace(".sql", "")
        down_filename = base + ".down.sql"
        down_path = os.path.join(self._migrations_dir, down_filename)  # type: ignore[arg-type]
        if os.path.isfile(down_path):
            sql = self._read_sql(down_path)
            with self._connect() as conn:
                for stmt in _split_statements(sql):
                    if stmt.strip():
                        conn.execute(stmt)
                conn.execute("DELETE FROM _migrations WHERE id=?", (migration_id,))
                conn.commit()
        else:
            # Just remove the tracking record (schema changes remain)
            with self._connect() as conn:
                conn.execute("DELETE FROM _migrations WHERE id=?", (migration_id,))
                conn.commit()

        return filename

    def get_status(self) -> List[dict]:
        """Return status of all migration files (applied / pending)."""
        self._require_init()
        applied_map = self._get_applied_map()
        all_files = self._list_migration_files()
        status: List[dict] = []
        for filename, _ in all_files:
            info = applied_map.get(filename)
            status.append({
                "filename": filename,
                "applied": filename in applied_map,
                "applied_at": info["applied_at"] if info else None,
            })
        return status

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self._db_path)  # type: ignore[arg-type]

    def _require_init(self) -> None:
        if self._db_path is None or self._migrations_dir is None:
            raise RuntimeError("MigrationRunner.init() must be called first.")

    def _get_applied_set(self) -> set:
        with self._connect() as conn:
            rows = conn.execute("SELECT filename FROM _migrations").fetchall()
        return {r[0] for r in rows}

    def _get_applied_map(self) -> dict:
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("SELECT * FROM _migrations").fetchall()
        return {r["filename"]: dict(r) for r in rows}

    def _get_last_applied(self) -> Optional[Tuple[str, int]]:
        sql = "SELECT filename, id FROM _migrations ORDER BY id DESC LIMIT 1"
        with self._connect() as conn:
            row = conn.execute(sql).fetchone()
        return (row[0], row[1]) if row else None

    def _get_pending(self, applied: set) -> List[Tuple[str, str]]:
        all_files = self._list_migration_files()
        return [(f, p) for f, p in all_files if f not in applied]

    def _list_migration_files(self) -> List[Tuple[str, str]]:
        """Return (filename, full_path) pairs for .sql files (not .down.sql), sorted."""
        d = self._migrations_dir
        if not d or not os.path.isdir(d):
            return []
        files = [
            f for f in os.listdir(d)
            if f.endswith(".sql") and not f.endswith(".down.sql")
        ]
        files.sort(key=_migration_sort_key)
        return [(f, os.path.join(d, f)) for f in files]

    @staticmethod
    def _read_sql(path: str) -> str:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _migration_sort_key(filename: str) -> int:
    """Extract leading integer from filename for sorting."""
    m = re.match(r"^(\d+)", filename)
    return int(m.group(1)) if m else 0


def _split_statements(sql: str) -> List[str]:
    """Split SQL text on semicolons, skipping comment lines."""
    return [s.strip() for s in sql.split(";") if s.strip()]


def _now() -> str:
    return datetime.utcnow().isoformat()
