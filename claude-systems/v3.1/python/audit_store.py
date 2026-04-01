from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

try:
    import psycopg  # type: ignore
except Exception:
    psycopg = None

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "runtime"
RUNTIME.mkdir(exist_ok=True)

AUDIT_TABLE_SQL = '''
CREATE TABLE IF NOT EXISTS decision_audit (
    decision_id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    request_type TEXT NOT NULL,
    routing_classification TEXT NOT NULL,
    chosen_architecture TEXT NOT NULL,
    confidence_score REAL NOT NULL,
    recommended_action TEXT NOT NULL,
    prompt_id TEXT NOT NULL,
    prompt_version TEXT NOT NULL,
    schema_version TEXT NOT NULL,
    code_version TEXT NOT NULL,
    exception_class TEXT,
    codification_candidate_score REAL,
    payload_json TEXT NOT NULL
);
'''


class AuditStore:
    def __init__(self, backend: str = "sqlite", sqlite_path: Optional[Path] = None, postgres_dsn: Optional[str] = None) -> None:
        self.backend = backend
        self.sqlite_path = sqlite_path or (RUNTIME / "claude_decisions.db")
        self.postgres_dsn = postgres_dsn or os.getenv("DATABASE_URL")

    def initialize(self) -> None:
        if self.backend == "postgres":
            if not self.postgres_dsn:
                raise ValueError("DATABASE_URL not set for postgres backend")
            if psycopg is None:
                raise ImportError("psycopg is required for postgres backend")
            with psycopg.connect(self.postgres_dsn) as conn:
                with conn.cursor() as cur:
                    cur.execute(AUDIT_TABLE_SQL)
                conn.commit()
            return
        with sqlite3.connect(self.sqlite_path) as conn:
            conn.execute(AUDIT_TABLE_SQL)
            conn.commit()

    def write_record(self, record: Dict[str, Any]) -> None:
        row = (
            record["decision_id"],
            record["timestamp"],
            record["request_type"],
            record["routing_classification"],
            record["chosen_architecture"],
            record["confidence_score"],
            record["recommended_action"],
            record["prompt_id"],
            record["prompt_version"],
            record["schema_version"],
            record["code_version"],
            record.get("exception_class"),
            record.get("codification_candidate_score"),
            json.dumps(record, ensure_ascii=False),
        )
        if self.backend == "postgres":
            if not self.postgres_dsn:
                raise ValueError("DATABASE_URL not set for postgres backend")
            if psycopg is None:
                raise ImportError("psycopg is required for postgres backend")
            with psycopg.connect(self.postgres_dsn) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        '''
                        INSERT INTO decision_audit (
                            decision_id, timestamp, request_type, routing_classification,
                            chosen_architecture, confidence_score, recommended_action,
                            prompt_id, prompt_version, schema_version, code_version,
                            exception_class, codification_candidate_score, payload_json
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (decision_id) DO UPDATE SET
                            timestamp = EXCLUDED.timestamp,
                            payload_json = EXCLUDED.payload_json
                        ''',
                        row,
                    )
                conn.commit()
            return
        with sqlite3.connect(self.sqlite_path) as conn:
            conn.execute(
                '''
                INSERT OR REPLACE INTO decision_audit (
                    decision_id, timestamp, request_type, routing_classification,
                    chosen_architecture, confidence_score, recommended_action,
                    prompt_id, prompt_version, schema_version, code_version,
                    exception_class, codification_candidate_score, payload_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                row,
            )
            conn.commit()

    def fetch_all(self) -> Iterable[Dict[str, Any]]:
        if self.backend == "postgres":
            if not self.postgres_dsn:
                raise ValueError("DATABASE_URL not set for postgres backend")
            if psycopg is None:
                raise ImportError("psycopg is required for postgres backend")
            with psycopg.connect(self.postgres_dsn) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT payload_json FROM decision_audit ORDER BY timestamp")
                    for (payload_json,) in cur.fetchall():
                        yield json.loads(payload_json)
            return
        with sqlite3.connect(self.sqlite_path) as conn:
            cur = conn.execute("SELECT payload_json FROM decision_audit ORDER BY timestamp")
            for (payload_json,) in cur.fetchall():
                yield json.loads(payload_json)
