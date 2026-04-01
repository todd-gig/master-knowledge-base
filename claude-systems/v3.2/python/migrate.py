from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / "migrations"
RUNTIME = ROOT / "runtime"
RUNTIME.mkdir(exist_ok=True)

MIGRATION_TABLE_SQL = '''
CREATE TABLE IF NOT EXISTS schema_migrations (
    migration_id TEXT PRIMARY KEY,
    file_name TEXT NOT NULL,
    applied_at TEXT DEFAULT CURRENT_TIMESTAMP
);
'''


def load_manifest() -> List[dict]:
    with (MIGRATIONS / "migration_manifest.json").open("r", encoding="utf-8") as f:
        return json.load(f)["migrations"]


def apply_sqlite_migrations(db_path: Path | None = None) -> None:
    db_path = db_path or (RUNTIME / "claude_decisions.db")
    with sqlite3.connect(db_path) as conn:
        conn.execute(MIGRATION_TABLE_SQL)
        applied = {row[0] for row in conn.execute("SELECT migration_id FROM schema_migrations")}
        for migration in load_manifest():
            if migration["id"] in applied:
                continue
            sql = (MIGRATIONS / migration["file"]).read_text(encoding="utf-8")
            conn.executescript(sql)
            conn.execute(
                "INSERT INTO schema_migrations (migration_id, file_name) VALUES (?, ?)",
                (migration["id"], migration["file"])
            )
        conn.commit()


if __name__ == "__main__":
    apply_sqlite_migrations()
    print("SQLite migrations applied.")
