import json
import sqlite3
from pathlib import Path
from datetime import datetime, timezone

root = Path(__file__).resolve().parents[1]
db_path = root / "backend" / "data" / "gigaton.db"
db_path.parent.mkdir(parents=True, exist_ok=True)
conn = sqlite3.connect(db_path)
cur = conn.cursor()

migrations_dir = root / "database" / "migrations"
files = sorted(migrations_dir.glob("*.sql"))
cur.execute("CREATE TABLE IF NOT EXISTS schema_migrations (version TEXT PRIMARY KEY, applied_at TEXT NOT NULL)")
applied = {row[0] for row in cur.execute("SELECT version FROM schema_migrations").fetchall()}

for f in files:
  version = f.name.split("_")[0]
  if version in applied:
    continue
  cur.executescript(f.read_text(encoding="utf-8"))
  cur.execute("INSERT INTO schema_migrations (version, applied_at) VALUES (?, ?)", (version, datetime.now(timezone.utc).isoformat()))
  conn.commit()

seed = json.loads((root / "database" / "seed.json").read_text(encoding="utf-8"))
for t in seed.get("tenants", []):
  cur.execute("INSERT OR REPLACE INTO tenants (id, tenant_id, name, plan_id, status, created_at) VALUES (?, ?, ?, ?, ?, ?)",
              (t["id"], t["tenant_id"], t["name"], t["plan_id"], t["status"], t["created_at"]))
for user in seed.get("users", []):
  cur.execute("INSERT OR REPLACE INTO users (id, email, role, tenant_id, created_at) VALUES (?, ?, ?, ?, ?)",
              (user["id"], user["email"], user["role"], user["tenant_id"], user["created_at"]))
for ns in seed.get("namespaces", []):
  cur.execute("INSERT OR REPLACE INTO namespaces (id, tenant_id, namespace_id, client_name, industry, status, payload_json, created_by, approved_by, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (ns["id"], ns["tenant_id"], ns["namespace_id"], ns["client_name"], ns["industry"], ns["status"], json.dumps(ns["payload_json"]), ns["created_by"], ns["approved_by"], ns["created_at"], ns["updated_at"]))

conn.commit()
conn.close()
print(f"[OK] initialized database from migrations at {db_path}")
