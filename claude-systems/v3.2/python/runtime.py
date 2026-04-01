from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Dict
from uuid import uuid4

from audit_store import AuditStore
from analytics import codification_candidate_score
from router import DecisionRouter
from validation import ensure_valid

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry" / "prompt_registry.json"


def load_active_prompt() -> Dict[str, Any]:
    with REGISTRY.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return {"prompt_id": data["active_prompt_id"], "prompt_version": data["active_prompt_version"]}


def choose_architecture(classification: str) -> str:
    mapping = {
        "Python-First": "Pure Python",
        "Claude-First": "Pure Claude",
        "Hybrid": "Claude parse -> Python score -> Claude review exceptions",
    }
    return mapping[classification]


def build_audit_record(payload: Dict[str, Any], route_result: Any, architecture: str) -> Dict[str, Any]:
    prompt_meta = load_active_prompt()
    candidate_metrics = payload.get("candidate_metrics", {})
    candidate_score = codification_candidate_score(candidate_metrics) if candidate_metrics else None
    return {
        "decision_id": payload.get("decision_id", str(uuid4())),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "request_type": payload["decision_type"],
        "input_snapshot": payload.get("input_snapshot", payload.get("normalized_variables", {})),
        "normalized_variables": payload["normalized_variables"],
        "routing_classification": route_result.classification,
        "chosen_architecture": architecture,
        "python_score": route_result.python_score,
        "claude_score": route_result.claude_score,
        "hybrid_score": route_result.hybrid_score,
        "confidence_score": float(payload["confidence_score"]),
        "assumptions": payload.get("assumptions", []),
        "exception_class": payload.get("exception_class"),
        "recommended_action": payload["recommended_action"],
        "actual_action": payload.get("actual_action"),
        "human_review_required": bool(payload.get("human_review_required", False)),
        "human_review_outcome": payload.get("human_review_outcome"),
        "estimated_unit_cost": payload.get("estimated_unit_cost"),
        "estimated_failure_cost": payload.get("estimated_failure_cost"),
        "codification_candidate": candidate_score is not None and candidate_score >= 0.8,
        "codification_candidate_score": candidate_score,
        "outcome_quality": payload.get("outcome_quality"),
        "notes": payload.get("notes"),
        "prompt_id": prompt_meta["prompt_id"],
        "prompt_version": prompt_meta["prompt_version"],
        "schema_version": payload.get("schema_version", "3.1"),
        "code_version": payload.get("code_version", "0.2.0"),
        "execution_latency_ms": payload.get("execution_latency_ms"),
    }


def process_decision(payload: Dict[str, Any], backend: str = "sqlite") -> Dict[str, Any]:
    ensure_valid(payload, "decision_schema.json")
    router = DecisionRouter()
    route_result = router.route(payload.get("routing_features", {}))
    architecture = choose_architecture(route_result.classification)
    record = build_audit_record(payload, route_result, architecture)
    ensure_valid(record, "audit_log_schema.json")
    store = AuditStore(backend=backend)
    store.initialize()
    store.write_record(record)
    return {
        "decision_id": record["decision_id"],
        "classification": route_result.classification,
        "architecture": architecture,
        "codification_candidate_score": record["codification_candidate_score"],
        "prompt_id": record["prompt_id"],
        "prompt_version": record["prompt_version"],
    }
