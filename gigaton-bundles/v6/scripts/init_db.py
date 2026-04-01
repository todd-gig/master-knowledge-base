import json
import sqlite3
from pathlib import Path

root = Path(__file__).resolve().parents[1]
db_path = root / "backend" / "data" / "gigaton.db"
db_path.parent.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

schema = (root / "database" / "schema.sql").read_text(encoding="utf-8")
cur.executescript(schema)

seed = json.loads((root / "database" / "seed.json").read_text(encoding="utf-8"))
for user in seed.get("users", []):
    cur.execute("INSERT OR REPLACE INTO users (id, email, role, created_at) VALUES (?, ?, ?, ?)",
                (user["id"], user["email"], user["role"], user["created_at"]))
for ns in seed.get("namespaces", []):
    cur.execute("INSERT OR REPLACE INTO namespaces (id, namespace_id, client_name, industry, status, payload_json, created_by, approved_by, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (ns["id"], ns["namespace_id"], ns["client_name"], ns["industry"], ns["status"], json.dumps(ns["payload_json"]), ns["created_by"], ns["approved_by"], ns["created_at"], ns["updated_at"]))

conn.commit()
conn.close()
print(f"[OK] initialized database at {db_path}")
