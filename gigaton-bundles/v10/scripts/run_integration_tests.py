import json
import sys
import urllib.request

base = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3001"
tenant = sys.argv[2] if len(sys.argv) > 2 else "tenant_liquefex"

def get(path, headers=None):
  req = urllib.request.Request(base + path, headers=headers or {})
  with urllib.request.urlopen(req) as r:
    return r.status, r.read().decode("utf-8"), dict(r.headers)

def post(path, payload, headers=None):
  req = urllib.request.Request(base + path, data=json.dumps(payload).encode("utf-8"),
                               headers={"Content-Type":"application/json", **(headers or {})}, method="POST")
  with urllib.request.urlopen(req) as r:
    return r.status, r.read().decode("utf-8"), dict(r.headers)

h = {"x-tenant-id": tenant}
checks = []
checks.append(("health",) + get("/api/health"))
checks.append(("ready",) + get("/api/ready"))
checks.append(("draft",) + post("/api/intake/generate-namespace", {"client_name":"ACME","industry":"template","preferred_terminology":{"customer":"stakeholder"},"workflow_preferences":["research_first"]}, h))
checks.append(("billing",) + post("/api/billing/events", {"event_type":"tenant_created","amount_cents":50000,"currency":"USD","metadata":{"source":"integration"}}, h))
checks.append(("metrics",) + get("/metrics"))

failures = [c for c in checks if c[1] != 200]
for c in checks:
  print(c[0], c[1], c[3].get("x-correlation-id", ""))
if failures:
  raise SystemExit("integration failures detected")
print("[OK] integration checks passed")
