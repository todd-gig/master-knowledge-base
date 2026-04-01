import json
import sys
import urllib.request
import urllib.error

base = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3001"

def get(path):
  with urllib.request.urlopen(base + path) as r:
    return r.status, r.read().decode("utf-8"), dict(r.headers)

def post(path, payload):
  data = json.dumps(payload).encode("utf-8")
  req = urllib.request.Request(base + path, data=data, headers={"Content-Type":"application/json"}, method="POST")
  with urllib.request.urlopen(req) as r:
    return r.status, r.read().decode("utf-8"), dict(r.headers)

checks = []
checks.append(("health",) + get("/api/health"))
checks.append(("ready",) + get("/api/ready"))
checks.append(("draft",) + post("/api/intake/generate-namespace", {
  "client_name":"ACME Template",
  "industry":"template",
  "preferred_terminology":{"customer":"stakeholder"},
  "workflow_preferences":["research_first"]
}))
checks.append(("metrics",) + get("/metrics"))

failures = [c for c in checks if c[1] != 200]
for c in checks:
  print(c[0], c[1], c[3].get("x-correlation-id", ""))
if failures:
  raise SystemExit("integration failures detected")
print("[OK] integration checks passed")
