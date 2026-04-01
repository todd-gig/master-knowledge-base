"""
Zero-Dependency HTTP Service Layer

Implements the same 5 endpoints as the FastAPI service using only Python stdlib.
No external packages required — runs anywhere Python 3.10+ is available.

Endpoints:
    GET  /health                     → Health check
    GET  /v1/config                  → Engine configuration
    POST /v1/decisions/evaluate      → Full pipeline evaluation
    POST /v1/decisions/transition    → State transition validation
    POST /v1/decisions/gap-analysis  → Gap analysis

Usage:
    python -m service.http_server              # Default port 8000
    python -m service.http_server --port 9000  # Custom port
"""

import json
import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
from typing import Optional

# Ensure parent directory is on path for engine imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.models import (
    DecisionObject, DecisionClass, TrustTier, ReversibilityTag,
    TimeHorizon, ValueScores, TrustScores, AlignmentScores,
    ExecutionVerdict, RTQLStage
)
from engine.pipeline import process_decision
from engine.config import load_config
from engine.state_machine import advance_state, next_state_for_action
from engine.authority import authority_check
from engine.audit import serialize_pipeline_result
from engine.learning_loop import record_outcome, LearningStore


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

TIME_MAP = {
    "immediate": TimeHorizon.IMMEDIATE,
    "near_term": TimeHorizon.NEAR_TERM,
    "mid_term": TimeHorizon.MID_TERM,
    "long_term": TimeHorizon.LONG_TERM,
}


# ─────────────────────────────────────────────
# REQUEST → ENGINE CONVERSION
# ─────────────────────────────────────────────

def build_decision_from_json(d: dict) -> DecisionObject:
    """Convert a JSON request body into a DecisionObject."""
    pd = d.get("positive_dimensions", {})
    pen = d.get("penalty_dimensions", {})
    ti = d.get("trust_inputs", {})

    value_scores = ValueScores(
        revenue_impact=pd.get("revenue_impact", 0),
        cost_efficiency=pd.get("cost_efficiency", 0),
        time_leverage=pd.get("time_leverage", 0),
        strategic_alignment=pd.get("strategic_alignment", 0),
        customer_human_benefit=pd.get("customer_benefit", 0),
        knowledge_asset_creation=pd.get("knowledge_creation", 0),
        compounding_potential=pd.get("compounding_potential", 0),
        reversibility=pd.get("reversibility", 0),
        downside_risk=pen.get("downside_risk", 0),
        execution_drag=pen.get("execution_drag", 0),
        uncertainty=pen.get("uncertainty", 0),
        ethical_misalignment=pen.get("ethical_misalignment", 0),
    )

    trust_scores = TrustScores(
        evidence_quality=ti.get("evidence_quality", 0),
        logic_integrity=ti.get("logic_integrity", 0),
        outcome_history=ti.get("outcome_history", 0),
        context_fit=ti.get("context_fit", 0),
        stakeholder_clarity=ti.get("stakeholder_clarity", 0),
        risk_containment=ti.get("risk_containment", 0),
        auditability=ti.get("auditability", 0),
    )

    return DecisionObject(
        decision_id=d.get("decision_id", ""),
        title=d.get("title", ""),
        decision_class=CLASS_MAP.get(d.get("decision_class", "D1"), DecisionClass.D1_REVERSIBLE_TACTICAL),
        owner=d.get("owner", "unspecified"),
        time_horizon=TIME_MAP.get(d.get("time_horizon", "immediate"), TimeHorizon.IMMEDIATE),
        reversibility=REVERSIBILITY_MAP.get(d.get("reversibility", "R1"), ReversibilityTag.R1_EASILY_REVERSIBLE),
        problem_statement=d.get("problem_statement", ""),
        requested_action=d.get("requested_action", ""),
        context_summary=d.get("context_summary", ""),
        stakeholders=d.get("stakeholders", []),
        constraints=d.get("constraints", []),
        value_scores=value_scores,
        trust_scores=trust_scores,
        alignment_scores=AlignmentScores(
            doctrine_alignment=d.get("doctrine_alignment", 0.8),
            ethos_alignment=d.get("ethos_alignment", 0.8),
            first_principles_alignment=d.get("first_principles_alignment", 0.8),
        ),
        evidence_refs=d.get("evidence_refs", []),
        assumptions=d.get("assumptions", []),
        unknowns=d.get("unknowns", []),
        required_approvals=d.get("required_approvals", []),
        execution_plan=d.get("execution_plan", ""),
        monitoring_metric=d.get("monitoring_metric", ""),
        rollback_trigger=d.get("rollback_trigger", ""),
        review_date=d.get("review_date"),
        current_state=d.get("current_state", "draft"),
        actor_role=d.get("actor_role", "AI_Domain_Agent"),
        has_missing_data=d.get("has_missing_data", False),
        ethical_conflict=d.get("ethical_conflict", False),
    )


# ─────────────────────────────────────────────
# REQUEST HANDLER
# ─────────────────────────────────────────────

class DecisionEngineHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the Decision Engine API."""

    config = None  # Loaded once at startup

    def _send_json(self, status_code: int, data: dict):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def _read_body(self) -> dict:
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        return json.loads(body) if body else {}

    def do_OPTIONS(self):
        """Handle CORS preflight."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        if self.path == "/health":
            self._handle_health()
        elif self.path == "/v1/config":
            self._handle_config()
        elif self.path == "/v1/learning/summary":
            self._handle_learning_summary()
        else:
            self._send_json(404, {"error": f"Not found: {self.path}"})

    def do_POST(self):
        try:
            body = self._read_body()

            if self.path == "/v1/decisions/evaluate":
                self._handle_evaluate(body)
            elif self.path == "/v1/decisions/transition":
                self._handle_transition(body)
            elif self.path == "/v1/decisions/gap-analysis":
                self._handle_gap_analysis(body)
            elif self.path == "/v1/learning/record":
                self._handle_learning_record(body)
            else:
                self._send_json(404, {"error": f"Not found: {self.path}"})
        except json.JSONDecodeError:
            self._send_json(400, {"error": "Invalid JSON body"})
        except Exception as e:
            self._send_json(500, {"error": str(e)})

    # ── Handlers ──

    def _handle_health(self):
        self._send_json(200, {
            "status": "ok",
            "timestamp": datetime.now().isoformat(),
            "version": "0.2.0",
            "engine": "stdlib_http",
        })

    def _handle_config(self):
        cfg = self.__class__.config
        auth_matrix = {}
        for dc_key, rule in cfg.authority_matrix.items():
            auth_matrix[dc_key] = {
                "min_trust": rule.min_trust,
                "executor": rule.executor,
                "required_approval": rule.required_approval,
            }

        self._send_json(200, {
            "version": "0.2.0",
            "authority_matrix": auth_matrix,
            "valid_transitions": cfg.valid_transitions or {},
        })

    def _handle_evaluate(self, body: dict):
        # Accept both {decision: {...}} and flat format
        decision_data = body.get("decision", body)
        decision = build_decision_from_json(decision_data)

        validation_errors = decision.validate()
        if validation_errors:
            self._send_json(400, {
                "error": "Validation failed",
                "validation_errors": validation_errors,
            })
            return

        result = process_decision(decision, self.__class__.config)

        if not result.success:
            self._send_json(422, {
                "error": "Pipeline failed",
                "validation_errors": result.validation_errors,
            })
            return

        self._send_json(200, serialize_pipeline_result(result))

    def _handle_transition(self, body: dict):
        current = body.get("current_state", "")
        target = body.get("target_state", "")

        if not current or not target:
            self._send_json(400, {"error": "current_state and target_state required"})
            return

        result = advance_state(current, target, self.__class__.config)
        self._send_json(200, result)

    def _handle_gap_analysis(self, body: dict):
        decision_data = body.get("decision", body)
        decision = build_decision_from_json(decision_data)

        # Build gap items from value + trust dimensions
        from engine.gap_analysis import analyze_gaps, generate_action_items

        items = []
        vs = decision.value_scores
        for var, score in [
            ("revenue_impact", vs.revenue_impact),
            ("cost_efficiency", vs.cost_efficiency),
            ("time_leverage", vs.time_leverage),
            ("strategic_alignment", vs.strategic_alignment),
            ("customer_benefit", vs.customer_human_benefit),
            ("knowledge_creation", vs.knowledge_asset_creation),
            ("compounding_potential", vs.compounding_potential),
        ]:
            items.append({
                "category": "value", "variable": var,
                "actual_score": score, "target_score": 5.0,
                "strategic_importance": 1.0,
                "rtql_stage": "qualified",
                "leverage_score": score / 5.0 * 5.0,
                "urgency_score": 2.0,
                "value_matrix_impact": score / 5.0,
            })

        ts = decision.trust_scores
        for var, score in [
            ("evidence_quality", ts.evidence_quality),
            ("logic_integrity", ts.logic_integrity),
            ("outcome_history", ts.outcome_history),
            ("context_fit", ts.context_fit),
            ("stakeholder_clarity", ts.stakeholder_clarity),
            ("risk_containment", ts.risk_containment),
            ("auditability", ts.auditability),
        ]:
            items.append({
                "category": "trust", "variable": var,
                "actual_score": score, "target_score": 5.0,
                "strategic_importance": 1.0,
                "rtql_stage": "qualified",
                "leverage_score": score / 5.0 * 5.0,
                "urgency_score": 2.0,
                "value_matrix_impact": score / 5.0,
            })

        gaps = analyze_gaps(items)
        action_items = generate_action_items(gaps)

        self._send_json(200, {
            "decision_id": decision.decision_id,
            "gaps_found": len(gaps),
            "gaps": [
                {
                    "category": g.category,
                    "variable": g.variable,
                    "actual": g.actual_score,
                    "target": g.target_score,
                    "gap": g.gap_score,
                    "severity": g.gap_severity_label,
                    "priority": g.priority_score,
                }
                for g in gaps
            ],
            "action_items": action_items,
        })

    def _handle_learning_record(self, body: dict):
        """Record a post-execution outcome for the learning loop."""
        required = ["decision_id", "decision_class", "original_verdict",
                     "expected_value", "actual_value"]
        missing = [k for k in required if k not in body]
        if missing:
            self._send_json(400, {"error": f"Missing required fields: {missing}"})
            return

        lr = record_outcome(
            decision_id=body["decision_id"],
            decision_class=body["decision_class"],
            original_verdict=body["original_verdict"],
            expected_value=body.get("expected_value", 0),
            expected_timeline_days=body.get("expected_timeline_days", 0),
            expected_risk_level=body.get("expected_risk_level", "low"),
            actual_value=body.get("actual_value", 0),
            actual_timeline_days=body.get("actual_timeline_days", 0),
            actual_risk_materialized=body.get("actual_risk_materialized", False),
            actual_risk_description=body.get("actual_risk_description", ""),
            outcome_summary=body.get("outcome_summary", ""),
            lessons_learned=body.get("lessons_learned", []),
            recorded_by=body.get("recorded_by", "api"),
        )

        self._send_json(200, {
            "record_id": lr.record_id,
            "decision_id": lr.decision_id,
            "composite_variance": lr.variance.composite_variance_score,
            "trust_recommendation": lr.variance.trust_recommendation.value,
            "suggested_actions": lr.variance.suggested_actions,
        })

    def _handle_learning_summary(self):
        """Return institutional learning summary."""
        store = LearningStore()
        stats = store.compute_class_stats()
        summary = store.generate_learning_summary()
        self._send_json(200, {
            "summary": summary,
            "stats": stats,
            "total_records": len(store.get_all_records()),
            "unapplied": len(store.get_unapplied()),
        })

    def log_message(self, format, *args):
        """Suppress default stderr logging during tests."""
        pass


# ─────────────────────────────────────────────
# SERVER ENTRY POINT
# ─────────────────────────────────────────────

def run_server(port: int = 8000, verbose: bool = True):
    """Start the HTTP server."""
    DecisionEngineHandler.config = load_config()

    if verbose:
        # Re-enable logging for production use
        DecisionEngineHandler.log_message = BaseHTTPRequestHandler.log_message

    server = HTTPServer(("0.0.0.0", port), DecisionEngineHandler)
    print(f"Decision Engine HTTP Server running on http://0.0.0.0:{port}")
    print("Endpoints:")
    print("  GET  /health")
    print("  GET  /v1/config")
    print("  GET  /v1/learning/summary")
    print("  POST /v1/decisions/evaluate")
    print("  POST /v1/decisions/transition")
    print("  POST /v1/decisions/gap-analysis")
    print("  POST /v1/learning/record")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Decision Engine HTTP Server")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    run_server(port=args.port)
