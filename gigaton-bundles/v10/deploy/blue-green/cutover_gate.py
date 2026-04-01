import json
import sys
import urllib.request

base = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3001"
tenant = sys.argv[2] if len(sys.argv) > 2 else "tenant_liquefex"

def get(path, headers=None):
  req = urllib.request.Request(base + path, headers=headers or {})
  with urllib.request.urlopen(req) as r:
    return r.status

checks = {
  "health": get("/api/health") == 200,
  "ready": get("/api/ready") == 200,
  "metrics": get("/metrics") == 200,
  "tenant_namespace_read": get("/api/namespaces", {"x-tenant-id": tenant}) == 200,
}

print(json.dumps(checks, indent=2))
if not all(checks.values()):
  raise SystemExit("cutover gate failed")
print("[OK] cutover gate passed")
