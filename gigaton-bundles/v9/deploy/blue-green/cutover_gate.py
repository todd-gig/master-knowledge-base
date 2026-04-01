import json
import sys
import urllib.request

base = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3001"

def get(path):
  with urllib.request.urlopen(base + path) as r:
    return r.status, r.read().decode("utf-8")

checks = {
  "health": get("/api/health")[0] == 200,
  "ready": get("/api/ready")[0] == 200,
  "metrics": get("/metrics")[0] == 200,
}

print(json.dumps(checks, indent=2))
if not all(checks.values()):
  raise SystemExit("cutover gate failed")
print("[OK] cutover gate passed")
