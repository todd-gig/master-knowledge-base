"""
Firebase Cloud Functions — Decision Engine API

Exposes the full decision engine pipeline as Firebase Cloud Functions (Python).
Uses firebase_functions for HTTP triggers and firebase_admin for Firestore persistence.

Functions:
    api          — Main HTTP function handling all /api/* routes
    on_decision  — Firestore trigger: auto-audit on decision state changes
    scheduled_learning_summary — Scheduled function: daily learning digest
"""

import json
import os
from datetime import datetime

from firebase_functions import https_fn, firestore_fn, scheduler_fn, options
from firebase_admin import initialize_app, firestore

# Engine imports — the engine/ package is copied into functions/
from engine.models import (
    DecisionObject, DecisionClass, TrustTier, ReversibilityTag,
    TimeHorizon, ValueScores, TrustScores, AlignmentScores,
    ExecutionVerdict, RTQLStage, RTQLInput
)
from engine.pipeline import process_decision
from engine.config import load_config
from engine.state_machine import advance_state
from engine.authority import authority_check
from engine.audit import serialize_pipeline_result, generate_executive_summary
from service.firestore_persistence import FirestorePersistence

# ─────────────────────────────────────────────
# INIT
# ─────────────────────────────────────────────

app = initialize_app()
db = firestore.client()
persistence = FirestorePersistence(db)
config = load_config()

# ─────────────────────────────────────────────
# ENUM MAPS
# ─────────────────────────────────────────────

CLASS_MAP = {
    "D0": DecisionClass.D0_INFORMATIONAL,
    "D1": DecisionClass.D1_REVERSIBLE_TACTICAL,
    "D2": DecisionClass.D2_OPERATIONAL,
    "D3": DecisionClass.D3_FINANCIAL,
    "D4": DecisionClass.D4_STRATEGIC,
    "D5": DecisionClass.D5_LEGAL_ETHICAL,
    "D6": DecisionClass.D6_IRREVERSIBLE_HIGH_BLAST,
}

REVERSIBILITY_MAP = {
    "R1": ReversibilityTag.R1_EASILY_REVERSIBLE,
    "R2": ReversibilityTag.R2_MODERATELY_REVERSIBLE,
    "R3": ReversibilityTag.R3_COSTLY_TO_REVERSE,
    "R4": ReversibilityTag.R4_EFFECTIVELY_IRREVERSIBLE,
}

HORIZON_MAP = {
    "immediate": TimeHorizon.IMMEDIATE,
    "near_term": TimeHorizon.NEAR_TERM,
    "mid_term": TimeHorizon.MID_TERM,
    "long_term": TimeHorizon.LONG_TERM,
}


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def _cors_headers():
    """Standard CORS headers for API responses."""
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
    }


def _json_response(data: dict, status: int = 200) -> https_fn.Response:
    return https_fn.Response(
        json.dumps(data, default=str),
        status=status,
        headers={**_cors_headers(), "Content-Type": "application/json"},
    )


def _error_response(msg: str, status: int = 400) -> https_fn.Response:
    return _json_response({"error": msg}, status=status)


def build_decision_from_json(d: dict) -> DecisionObject:
    """Convert a JSON dict into a DecisionObject with sensible defaults."""
    vs = d.get("value_scores", {})
    ts = d.get("trust_scores", {})
    als = d.get("alignment_scores", {})

    value_scores = ValueScores(
        revenue_impact=vs.get("revenue_impact", 0),
        cost_efficiency=vs.get("cost_efficiency", 0),
        time_leverage=vs.get("time_leverage", 0),
        strategic_alignment=vs.get("strategic_alignment", 0),
        customer_human_benefit=vs.get("customer_human_benefit", 0),
        knowledge_asset_creation=vs.get("knowledge_asset_creation", 0),
        compounding_potential=vs.get("compounding_potential", 0),
        reversibility=vs.get("reversibility", 3),
        downside_risk=vs.get("downside_risk", 0),
        execution_drag=vs.get("execution_drag", 0),
        uncertainty=vs.get("uncertainty", 0),
        ethical_misalignment=vs.get("ethical_misalignment", 0),
    )

    trust_scores = TrustScores(
        evidence_quality=ts.get("evidence_quality", 0),
        logic_integrity=ts.get("logic_integrity", 0),
        outcome_history=ts.get("outcome_history", 0),
        context_fit=ts.get("context_fit", 0),
        stakeholder_clarity=ts.get("stakeholder_clarity", 0),
        risk_containment=ts.get("risk_containment", 0),
        auditability=ts.get("auditability", 0),
    )

    alignment_scores = AlignmentScores(
        doctrine_alignment=als.get("doctrine_alignment", 0.8),
        ethos_alignment=als.get("ethos_alignment", 0.8),
        first_principles_alignment=als.get("first_principles_alignment", 0.8),
        value_matrix_alignment=als.get("value_matrix_alignment", 0.8),
        human_agency_score=als.get("human_agency_score", 0.8),
    )

    rtql_input = None
    if d.get("rtql_input"):
        ri = d["rtql_input"]
        rtql_input = RTQLInput(
            claim=ri.get("claim", ""),
            source_integrity=ri.get("source_integrity", 0),
            independence=ri.get("independence", 0),
            reproducibility=ri.get("reproducibility", 0),
            explainability=ri.get("explainability", 0),
            novelty=ri.get("novelty", 0),
            causal_validity=ri.get("causal_validity", 0),
            predictive_power=ri.get("predictive_power", 0),
        )

    return DecisionObject(
        decision_id=d.get("decision_id", ""),
        title=d.get("title", "Untitled"),
        decision_class=CLASS_MAP.get(d.get("decision_class", "D1"),
                                     DecisionClass.D1_REVERSIBLE_TACTICAL),
        owner=d.get("owner", "unknown"),
        time_horizon=HORIZON_MAP.get(d.get("time_horizon", "near_term"),
                                     TimeHorizon.NEAR_TERM),
        reversibility_tag=REVERSIBILITY_MAP.get(
            d.get("reversibility_tag", "R1"),
            ReversibilityTag.R1_EASILY_REVERSIBLE),
        requested_action=d.get("requested_action", ""),
        problem_statement=d.get("problem_statement", ""),
        context_summary=d.get("context_summary", ""),
        constraints=d.get("constraints", []),
        stakeholders=d.get("stakeholders", ["owner"]),
        evidence_refs=d.get("evidence_refs", ["submitted_payload"]),
        assumptions=d.get("assumptions", []),
        unknowns=d.get("unknowns", []),
        execution_plan=d.get("execution_plan", "Execute as submitted"),
        monitoring_metric=d.get("monitoring_metric", "completion_status"),
        rollback_trigger=d.get("rollback_trigger", "manual_review"),
        review_date=d.get("review_date", "2026-04-30"),
        actor_role=d.get("actor_role", "Human_Executive"),
        required_approvals=d.get("required_approvals", []),
        value_scores=value_scores,
        trust_scores=trust_scores,
        alignment_scores=alignment_scores,
        rtql_input=rtql_input,
        has_missing_data=d.get("has_missing_data", False),
        ethical_conflict=d.get("ethical_conflict", False),
    )


# ─────────────────────────────────────────────
# ROUTE HANDLERS
# ─────────────────────────────────────────────

def handle_health() -> https_fn.Response:
    return _json_response({
        "status": "healthy",
        "engine": "decision-engine-firebase",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
    })


def handle_config() -> https_fn.Response:
    from dataclasses import asdict
    return _json_response({"config": asdict(config)})


def handle_evaluate(data: dict) -> https_fn.Response:
    try:
        decision = build_decision_from_json(data)
        result = process_decision(decision, config)
        serialized = json.loads(serialize_pipeline_result(result))

        # Persist to Firestore
        persistence.save_decision(decision, result)
        persistence.save_audit_trail(decision.decision_id, result)

        return _json_response(serialized)
    except Exception as e:
        return _error_response(f"Pipeline error: {str(e)}", 500)


def handle_transition(data: dict) -> https_fn.Response:
    try:
        current = data.get("current_state", "draft")
        action = data.get("action", "qualify")
        result = advance_state(current, action)
        return _json_response({"transition": result})
    except Exception as e:
        return _error_response(f"Transition error: {str(e)}", 500)


def handle_gap_analysis(data: dict) -> https_fn.Response:
    try:
        from engine.gap_analysis import analyze_gaps
        decision = build_decision_from_json(data)
        result = process_decision(decision, config)
        gaps = analyze_gaps(decision, result, config)
        return _json_response({"gaps": gaps})
    except Exception as e:
        return _error_response(f"Gap analysis error: {str(e)}", 500)


def handle_learning_record(data: dict) -> https_fn.Response:
    try:
        record = persistence.record_learning_outcome(data)
        return _json_response({"stored": True, "record_id": record})
    except Exception as e:
        return _error_response(f"Learning record error: {str(e)}", 500)


def handle_learning_summary() -> https_fn.Response:
    try:
        summary = persistence.get_learning_summary()
        return _json_response(summary)
    except Exception as e:
        return _error_response(f"Learning summary error: {str(e)}", 500)


def handle_decision_history(decision_id: str) -> https_fn.Response:
    try:
        history = persistence.get_decision_history(decision_id)
        return _json_response(history)
    except Exception as e:
        return _error_response(f"History error: {str(e)}", 500)


def handle_list_decisions(params: dict) -> https_fn.Response:
    try:
        decisions = persistence.list_decisions(
            decision_class=params.get("class"),
            state=params.get("state"),
            limit=int(params.get("limit", 50)),
        )
        return _json_response({"decisions": decisions})
    except Exception as e:
        return _error_response(f"List error: {str(e)}", 500)


# ─────────────────────────────────────────────
# MAIN HTTP FUNCTION
# ─────────────────────────────────────────────

@https_fn.on_request(
    cors=options.CorsOptions(cors_origins="*", cors_methods=["GET", "POST"]),
    memory=options.MemoryOption.MB_512,
    timeout_sec=120,
)
def api(req: https_fn.Request) -> https_fn.Response:
    """Main API gateway — routes all /api/* requests."""

    path = req.path.rstrip("/")

    # Strip /api prefix if present (from hosting rewrite)
    if path.startswith("/api"):
        path = path[4:]

    # OPTIONS handled by CORS decorator
    if req.method == "OPTIONS":
        return _json_response({})

    # ── GET routes ──
    if req.method == "GET":
        if path in ("", "/", "/health"):
            return handle_health()
        if path == "/v1/config":
            return handle_config()
        if path == "/v1/learning/summary":
            return handle_learning_summary()
        if path.startswith("/v1/decisions/history/"):
            decision_id = path.split("/")[-1]
            return handle_decision_history(decision_id)
        if path == "/v1/decisions":
            return handle_list_decisions(dict(req.args))

    # ── POST routes ──
    if req.method == "POST":
        try:
            data = req.get_json(silent=True) or {}
        except Exception:
            return _error_response("Invalid JSON body")

        if path == "/v1/decisions/evaluate":
            return handle_evaluate(data)
        if path == "/v1/decisions/transition":
            return handle_transition(data)
        if path == "/v1/decisions/gap-analysis":
            return handle_gap_analysis(data)
        if path == "/v1/learning/record":
            return handle_learning_record(data)

    return _error_response(f"Not found: {req.method} {path}", 404)


# ─────────────────────────────────────────────
# FIRESTORE TRIGGER — Auto-audit on state change
# ─────────────────────────────────────────────

@firestore_fn.on_document_updated(document="decisions/{decisionId}")
def on_decision_update(event: firestore_fn.Event) -> None:
    """Fires when a decision document is updated in Firestore.
    Logs state transitions to the audit_records collection."""

    before = event.data.before.to_dict()
    after = event.data.after.to_dict()
    decision_id = event.params["decisionId"]

    old_state = before.get("lifecycle_state")
    new_state = after.get("lifecycle_state")

    if old_state != new_state:
        db.collection("audit_records").add({
            "decision_id": decision_id,
            "pipeline_stage": "state_transition",
            "action_taken": f"State changed: {old_state} → {new_state}",
            "timestamp": datetime.utcnow().isoformat(),
            "inputs_snapshot": {"old_state": old_state},
            "outputs_snapshot": {"new_state": new_state},
            "notes": "Auto-logged by Firestore trigger",
        })


# ─────────────────────────────────────────────
# SCHEDULED — Daily learning summary
# ─────────────────────────────────────────────

@scheduler_fn.on_schedule(schedule="every day 06:00")
def scheduled_learning_summary(event: scheduler_fn.ScheduledEvent) -> None:
    """Runs daily at 6 AM UTC. Computes aggregate learning metrics
    and stores them in the learning_summaries collection."""

    summary = persistence.get_learning_summary()
    summary["generated_at"] = datetime.utcnow().isoformat()
    summary["type"] = "daily_digest"

    db.collection("learning_summaries").add(summary)
