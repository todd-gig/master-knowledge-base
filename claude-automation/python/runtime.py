from __future__ import annotations
from datetime import datetime, timezone
from uuid import uuid4
import json
from pathlib import Path

from router import DecisionRouter
from validation import ensure_required
from audit_store import AuditStore

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry" / "prompt_registry.json"

def load_active_prompt():
    with REGISTRY.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data["active_prompt_id"], data["active_prompt_version"]

def architecture_for(classification):
    mapping = {
        "Python-First": "Pure Python",
        "Claude-First": "Pure Claude",
        "Hybrid": "Claude parse -> Python score -> Claude review exceptions",
    }
    return mapping[classification]

def process_decision(payload):
    ensure_required(payload, "decision_schema.json")
    router = DecisionRouter()
    result = router.route(payload.get("routing_features", {}))
    prompt_id, prompt_version = load_active_prompt()
    record = {
        "decision_id": payload.get("decision_id", str(uuid4())),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "request_type": payload["decision_type"],
        "routing_classification": result.classification,
        "chosen_architecture": architecture_for(result.classification),
        "confidence_score": payload["confidence_score"],
        "recommended_action": payload["recommended_action"],
        "prompt_id": prompt_id,
        "prompt_version": prompt_version,
        "schema_version": payload.get("schema_version", "1.0.0"),
        "code_version": payload.get("code_version", "1.0.0"),
        "exception_class": payload.get("exception_class"),
        "codification_candidate_score": payload.get("codification_candidate_score"),
        "payload_json": payload,
    }
    store = AuditStore()
    store.initialize()
    store.write_record(record)
    return record
