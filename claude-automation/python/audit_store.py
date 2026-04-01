from __future__ import annotations
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "runtime"
RUNTIME.mkdir(exist_ok=True)

CREATE_SQL = '''
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
    def __init__(self, db_path=None):
        self.db_path = db_path or (RUNTIME / "claude_thread_export.db")

    def initialize(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(CREATE_SQL)
            conn.commit()

    def write_record(self, record):
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
        with sqlite3.connect(self.db_path) as conn:
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
