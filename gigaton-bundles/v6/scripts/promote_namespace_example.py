import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
draft = {
    "namespace_id": "client_acme_template",
    "client_name": "ACME Template",
    "industry": "template",
    "payload_json": {
        "inherits_from": "global",
        "preferred_terminology": {"customer": "stakeholder"},
        "workflow_variants": ["research_first"]
    }
}
out = root / "examples" / "namespace_promotion_payload.json"
out.write_text(json.dumps(draft, indent=2), encoding="utf-8")
print(f"[OK] wrote {out}")
