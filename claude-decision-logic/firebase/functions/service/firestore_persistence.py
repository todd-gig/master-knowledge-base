"""
Firestore Persistence Layer — Decision Engine Data Store

Replaces the flat-file JSON/JSONL storage with Firestore collections.
Provides the same interface as the local engine but backed by Firebase.

Collections:
    decisions          — Decision objects + pipeline results + lifecycle state
    audit_records      — Timestamped audit trail entries per decision
    certificates       — QC, VC, TC, EC certificate records
    learning_records   — Post-execution variance tracking
    learning_summaries — Aggregated learning digests (daily/weekly)

Design Principles:
    - Every write is idempotent (upsert by decision_id where applicable)
    - All timestamps stored as ISO 8601 strings for portability
    - Composite scores stored alongside raw inputs for query efficiency
    - Subcollections avoided in favor of flat collections with indexed decision_id
      (simplifies security rules and cross-decision queries)
"""

import json
from datetime import datetime
from dataclasses import asdict
from typing import Optional

from google.cloud.firestore_v1.base_query import FieldFilter


class FirestorePersistence:
    """Firestore-backed persistence for the decision engine."""

    def __init__(self, db):
        """
        Args:
            db: A google.cloud.firestore.Client instance (from firebase_admin.firestore.client())
        """
        self.db = db

    # ─────────────────────────────────────────
    # DECISIONS
    # ─────────────────────────────────────────

    def save_decision(self, decision, pipeline_result) -> str:
        """Persist a decision and its pipeline result to Firestore.

        Args:
            decision: DecisionObject from engine.models
            pipeline_result: PipelineResult from engine.pipeline

        Returns:
            The decision_id used as the document key.
        """
        decision_id = decision.decision_id or _generate_id()

        # Build the document
        doc = {
            "decision_id": decision_id,
            "title": decision.title,
            "decision_class": decision.decision_class.value,
            "owner": decision.owner,
            "time_horizon": decision.time_horizon.value,
            "reversibility_tag": decision.reversibility_tag.value,
            "requested_action": decision.requested_action,
            "problem_statement": getattr(decision, "problem_statement", ""),
            "context_summary": decision.context_summary,
            "constraints": decision.constraints,
            "stakeholders": decision.stakeholders,
            "evidence_refs": getattr(decision, "evidence_refs", []),
            "assumptions": decision.assumptions,
            "unknowns": decision.unknowns,
            "execution_plan": getattr(decision, "execution_plan", ""),
            "monitoring_metric": getattr(decision, "monitoring_metric", ""),
            "rollback_trigger": getattr(decision, "rollback_trigger", ""),
            "review_date": getattr(decision, "review_date", ""),
            "actor_role": getattr(decision, "actor_role", ""),
            "required_approvals": getattr(decision, "required_approvals", []),
            "has_missing_data": decision.has_missing_data,
            "ethical_conflict": decision.ethical_conflict,

            # Scores (stored flat for Firestore query indexing)
            "value_scores": _safe_asdict(decision.value_scores),
            "trust_scores": _safe_asdict(decision.trust_scores),
            "alignment_scores": _safe_asdict(decision.alignment_scores),

            # Pipeline result summary
            "success": pipeline_result.success,
            "verdict": pipeline_result.execution_packet.verdict.value
                       if pipeline_result.execution_packet else None,
            "trust_tier": pipeline_result.trust_tier.value
                          if pipeline_result.trust_tier else None,
            "priority_score": pipeline_result.priority_score,
            "lifecycle_state": pipeline_result.lifecycle_state or "draft",
            "blocking_gates": pipeline_result.execution_packet.blocking_gates
                              if pipeline_result.execution_packet else [],
            "executive_summary": pipeline_result.executive_summary or "",

            # Metadata
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }

        self.db.collection("decisions").document(decision_id).set(doc, merge=True)
        return decision_id

    def get_decision(self, decision_id: str) -> Optional[dict]:
        """Retrieve a decision document by ID."""
        doc = self.db.collection("decisions").document(decision_id).get()
        return doc.to_dict() if doc.exists else None

    def list_decisions(
        self,
        decision_class: Optional[str] = None,
        state: Optional[str] = None,
        limit: int = 50,
    ) -> list[dict]:
        """List decisions with optional filters."""
        query = self.db.collection("decisions")

        if decision_class:
            query = query.where(filter=FieldFilter("decision_class", "==", decision_class))
        if state:
            query = query.where(filter=FieldFilter("lifecycle_state", "==", state))

        query = query.order_by("created_at", direction="DESCENDING").limit(limit)
        return [doc.to_dict() for doc in query.stream()]

    def update_decision_state(self, decision_id: str, new_state: str) -> bool:
        """Update the lifecycle state of a decision."""
        ref = self.db.collection("decisions").document(decision_id)
        if not ref.get().exists:
            return False
        ref.update({
            "lifecycle_state": new_state,
            "updated_at": datetime.utcnow().isoformat(),
        })
        return True

    # ─────────────────────────────────────────
    # AUDIT RECORDS
    # ─────────────────────────────────────────

    def save_audit_trail(self, decision_id: str, pipeline_result) -> int:
        """Save all audit records from a pipeline result.

        Returns:
            Number of audit records saved.
        """
        if not pipeline_result.audit_trail:
            return 0

        batch = self.db.batch()
        count = 0

        for record in pipeline_result.audit_trail:
            doc_ref = self.db.collection("audit_records").document()
            batch.set(doc_ref, {
                "decision_id": decision_id,
                "pipeline_stage": record.pipeline_stage,
                "action_taken": record.action_taken,
                "inputs_snapshot": record.inputs_snapshot,
                "outputs_snapshot": _make_serializable(record.outputs_snapshot),
                "notes": record.notes,
                "timestamp": record.timestamp if hasattr(record, "timestamp")
                             else datetime.utcnow().isoformat(),
            })
            count += 1

        batch.commit()
        return count

    def get_decision_history(self, decision_id: str) -> dict:
        """Get full history for a decision: the decision doc + all audit records."""
        decision = self.get_decision(decision_id)

        audit_query = (
            self.db.collection("audit_records")
            .where(filter=FieldFilter("decision_id", "==", decision_id))
            .order_by("timestamp")
        )
        audit_records = [doc.to_dict() for doc in audit_query.stream()]

        return {
            "decision": decision,
            "audit_trail": audit_records,
            "record_count": len(audit_records),
        }

    # ─────────────────────────────────────────
    # CERTIFICATES
    # ─────────────────────────────────────────

    def save_certificates(self, decision_id: str, certificate_chain) -> int:
        """Save certificate chain entries to Firestore."""
        if not certificate_chain:
            return 0

        batch = self.db.batch()
        count = 0

        for cert_type in ("qc", "vc", "tc", "ec"):
            cert = getattr(certificate_chain, cert_type, None)
            if cert:
                doc_ref = self.db.collection("certificates").document(
                    f"{decision_id}_{cert_type}"
                )
                batch.set(doc_ref, {
                    "decision_id": decision_id,
                    "cert_type": cert_type.upper(),
                    "granted": cert.granted if hasattr(cert, "granted") else True,
                    "reason": cert.reason if hasattr(cert, "reason") else "",
                    "expires": cert.expires.isoformat()
                              if hasattr(cert, "expires") and cert.expires else None,
                    "issued_at": datetime.utcnow().isoformat(),
                })
                count += 1

        batch.commit()
        return count

    # ─────────────────────────────────────────
    # LEARNING LOOP
    # ─────────────────────────────────────────

    def record_learning_outcome(self, data: dict) -> str:
        """Record a post-execution learning outcome.

        Args:
            data: Dict with decision_id, decision_class, expected_value,
                  actual_value, expected_timeline, actual_timeline,
                  expected_risk, actual_risk, notes

        Returns:
            The Firestore document ID.
        """
        decision_id = data.get("decision_id", "unknown")

        # Calculate variance
        expected_value = float(data.get("expected_value", 0))
        actual_value = float(data.get("actual_value", 0))
        expected_timeline = float(data.get("expected_timeline", 0))
        actual_timeline = float(data.get("actual_timeline", 0))
        expected_risk = float(data.get("expected_risk", 0))
        actual_risk = float(data.get("actual_risk", 0))

        value_var = (actual_value - expected_value) / max(abs(expected_value), 1)
        timeline_var = (expected_timeline - actual_timeline) / max(abs(expected_timeline), 1)
        risk_var = (expected_risk - actual_risk) / max(abs(expected_risk), 1)

        composite = value_var * 0.5 + timeline_var * 0.3 + risk_var * 0.2
        composite = max(-1.0, min(1.0, composite))

        # Trust recommendation
        if composite >= 0.15:
            trust_recommendation = "upgrade"
        elif composite <= -0.15:
            trust_recommendation = "downgrade"
        else:
            trust_recommendation = "maintain"

        record = {
            "decision_id": decision_id,
            "decision_class": data.get("decision_class", "D1"),
            "expected_value": expected_value,
            "actual_value": actual_value,
            "expected_timeline": expected_timeline,
            "actual_timeline": actual_timeline,
            "expected_risk": expected_risk,
            "actual_risk": actual_risk,
            "value_variance": round(value_var, 4),
            "timeline_variance": round(timeline_var, 4),
            "risk_variance": round(risk_var, 4),
            "composite_variance": round(composite, 4),
            "trust_recommendation": trust_recommendation,
            "notes": data.get("notes", ""),
            "applied": False,
            "recorded_at": datetime.utcnow().isoformat(),
        }

        doc_ref = self.db.collection("learning_records").document()
        doc_ref.set(record)
        return doc_ref.id

    def mark_learning_applied(self, record_id: str) -> bool:
        """Mark a learning record as applied."""
        ref = self.db.collection("learning_records").document(record_id)
        if not ref.get().exists:
            return False
        ref.update({
            "applied": True,
            "applied_at": datetime.utcnow().isoformat(),
        })
        return True

    def get_learning_summary(self) -> dict:
        """Compute aggregate learning metrics across all records."""
        records = [
            doc.to_dict()
            for doc in self.db.collection("learning_records").stream()
        ]

        if not records:
            return {
                "total_records": 0,
                "applied": 0,
                "unapplied": 0,
                "avg_composite_variance": 0.0,
                "trust_recommendations": {},
                "by_class": {},
            }

        total = len(records)
        applied = sum(1 for r in records if r.get("applied"))
        unapplied = total - applied
        avg_composite = sum(r.get("composite_variance", 0) for r in records) / total

        # Count trust recommendations
        trust_counts = {}
        for r in records:
            rec = r.get("trust_recommendation", "maintain")
            trust_counts[rec] = trust_counts.get(rec, 0) + 1

        # Group by class
        by_class = {}
        for r in records:
            cls = r.get("decision_class", "unknown")
            if cls not in by_class:
                by_class[cls] = {"count": 0, "total_variance": 0.0}
            by_class[cls]["count"] += 1
            by_class[cls]["total_variance"] += r.get("composite_variance", 0)

        for cls in by_class:
            by_class[cls]["avg_variance"] = round(
                by_class[cls]["total_variance"] / by_class[cls]["count"], 4
            )

        return {
            "total_records": total,
            "applied": applied,
            "unapplied": unapplied,
            "avg_composite_variance": round(avg_composite, 4),
            "trust_recommendations": trust_counts,
            "by_class": by_class,
        }

    def get_unapplied_learning(self) -> list[dict]:
        """Get all learning records that haven't been applied yet."""
        query = (
            self.db.collection("learning_records")
            .where(filter=FieldFilter("applied", "==", False))
        )
        return [doc.to_dict() | {"id": doc.id} for doc in query.stream()]


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def _generate_id() -> str:
    from uuid import uuid4
    return f"DEC-{uuid4().hex[:12].upper()}"


def _safe_asdict(obj) -> dict:
    """Convert a dataclass to dict, handling enums gracefully."""
    if obj is None:
        return {}
    try:
        d = asdict(obj)
        return _make_serializable(d)
    except Exception:
        return {}


def _make_serializable(obj):
    """Recursively make an object JSON-serializable for Firestore."""
    if isinstance(obj, dict):
        return {k: _make_serializable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_make_serializable(i) for i in obj]
    if hasattr(obj, "value"):  # Enum
        return obj.value
    if hasattr(obj, "isoformat"):  # datetime
        return obj.isoformat()
    return obj
