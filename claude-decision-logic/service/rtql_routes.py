"""FastAPI routes for RTQL Classifier, Client Intelligence, and Exception engines."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter
from pydantic import BaseModel, Field

from engine.rtql_classifier import InputRecord, RTQLClassifier
from engine.rtql_integration_layer import MutationRequest, RTQLIntegrationLayer
from engine.client_intelligence_engine import ClientIntelligenceEngine
from engine.exception_engine import ExceptionEngine

router = APIRouter(prefix="/v2", tags=["v2-rtql"])

# Shared engine instances
_classifier = RTQLClassifier()
_integration = RTQLIntegrationLayer()
_intelligence = ClientIntelligenceEngine()
_exceptions = ExceptionEngine()


# ── Request Schemas ────────────────────────────────────────────────────


class RTQLClassifyRequest(BaseModel):
    """Maps to InputRecord fields for RTQL classification."""
    # 7 trust dimensions
    source_integrity: int = Field(0, description="Source integrity score (allowed: 0,1,2,3,4,5,6,8,10,12)")
    exposure_count: int = Field(0, description="Exposure count score")
    independence: int = Field(0, description="Independence score")
    explainability: int = Field(0, description="Explainability score")
    replicability: int = Field(0, description="Replicability score")
    adversarial_robustness: int = Field(0, description="Adversarial robustness score")
    novelty_yield: int = Field(0, description="Novelty yield score")

    # 4 causal checks
    reveals_causal_mechanism: bool = False
    is_irreducible: bool = False
    survives_authority_removal: bool = False
    survives_context_shift: bool = False

    # Optional metadata
    record_id: Optional[str] = None
    label: Optional[str] = None
    raw_value: float = 0.0


class AdjustValueRequest(BaseModel):
    raw_value: float = Field(..., description="The raw value to adjust")
    stage: str = Field(..., description="Trust stage string (e.g. 'certified', 'qualified')")


class MutationRequestSchema(BaseModel):
    """Maps to MutationRequest fields for registry mutation control."""
    action: str = Field(..., description="One of: create | upgrade | downgrade | relink | reclassify")
    entry_id: Optional[str] = None
    proposed_statement: str
    current_stage: Optional[str] = None
    target_stage: str
    source_summary: str
    evidence: List[str] = []
    scores: Dict[str, Any] = Field(default_factory=dict, description="RTQL dimension score dict")
    causal_checks: Dict[str, Any] = Field(default_factory=dict, description="Causal check booleans dict")
    requested_by: str
    notes: str = ""


class EscalationRequest(BaseModel):
    exception_class: str = Field(..., description="One of the 8 canonical exception class strings")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score 0.0–1.0")
    action_reversible: bool = Field(..., description="Whether the proposed action can be undone")
    compliance_risk: bool = Field(False, description="Whether a compliance risk has been detected")
    failure_cost_tolerance: str = Field("medium", description="One of: zero | low | medium | high")


# ── RTQL Classifier Routes ─────────────────────────────────────────────


@router.post("/rtql/classify")
def classify_rtql(req: RTQLClassifyRequest) -> dict:
    """Classify an input record into a trust stage and return supporting metadata."""
    record = InputRecord(
        source_integrity=req.source_integrity,
        exposure_count=req.exposure_count,
        independence=req.independence,
        explainability=req.explainability,
        replicability=req.replicability,
        adversarial_robustness=req.adversarial_robustness,
        novelty_yield=req.novelty_yield,
        reveals_causal_mechanism=req.reveals_causal_mechanism,
        is_irreducible=req.is_irreducible,
        survives_authority_removal=req.survives_authority_removal,
        survives_context_shift=req.survives_context_shift,
        record_id=req.record_id,
        label=req.label,
        raw_value=req.raw_value,
    )
    stage = _classifier.classify(record)
    trust_multiplier = _classifier.get_trust_multiplier(stage)
    research_actions = _classifier.route_research(record, stage)
    return {
        "classification": stage,
        "stage": stage,
        "trust_multiplier": trust_multiplier,
        "research_actions": research_actions,
    }


@router.post("/rtql/adjust-value")
def adjust_value(req: AdjustValueRequest) -> dict:
    """Apply a trust multiplier to a raw value based on its trust stage."""
    adjusted = _classifier.adjust_value(req.raw_value, req.stage)
    return {"adjusted_value": adjusted}


@router.post("/rtql/mutation")
def process_mutation(req: MutationRequestSchema) -> dict:
    """Evaluate a registry mutation request against RTQL gates and return a decision."""
    mutation = MutationRequest(
        action=req.action,
        entry_id=req.entry_id,
        proposed_statement=req.proposed_statement,
        current_stage=req.current_stage,
        target_stage=req.target_stage,
        source_summary=req.source_summary,
        evidence=req.evidence,
        scores=req.scores,
        causal_checks=req.causal_checks,
        requested_by=req.requested_by,
        notes=req.notes,
    )
    decision = _integration.process_mutation(mutation)
    return {
        "approved": decision.approved,
        "action": decision.action,
        "assigned_stage": decision.assigned_stage,
        "target_stage_passed": decision.target_stage_passed,
        "reasons": decision.reasons,
        "missing_requirements": decision.missing_requirements,
        "research_actions": decision.research_actions,
        "write_target": decision.write_target,
        "audit_log": decision.audit_log,
    }


# ── Client Intelligence Route ──────────────────────────────────────────


@router.post("/intelligence/analyze")
def analyze_intelligence(survey_data: Dict[str, Any]) -> dict:
    """
    Run a full 15-category client intelligence analysis from survey data.

    Expected survey_data schema:
        {
            "client_id": "optional string",
            "rtql_input": {<InputRecord fields>},
            "category_inputs": {
                "<category_key>": {
                    "variable_strength": float,
                    "evidence_quality": float,
                    "execution_maturity": float,
                    "consistency": float,
                    "strategic_fit": float,
                    "<sub_variable>": float,
                    ...
                },
                ...
            },
            "targets": {"<category_key>": float, ...},
            "rtql_stages": {"<sub_variable>": "<stage>"}
        }
    """
    report = _intelligence.full_analysis(survey_data)
    return {
        "category_scores": [
            {
                "category_key": cs.category_key,
                "category_label": cs.category_label,
                "weight": cs.weight,
                "raw_score": cs.raw_score,
                "trust_adjusted_score": cs.trust_adjusted_score,
                "trust_multiplier": cs.trust_multiplier,
                "sub_variable_scores": cs.sub_variable_scores,
            }
            for cs in report.category_scores
        ],
        "gaps": [
            {
                "category_key": g.category_key,
                "category_label": g.category_label,
                "actual": g.actual,
                "target": g.target,
                "gap_score": g.gap_score,
                "severity": g.severity,
            }
            for g in report.gap_results
        ],
        "priority_actions": [
            {
                "category_key": a.category_key,
                "category_label": a.category_label,
                "description": a.description,
                "priority_score": a.priority_score,
                "severity": a.severity,
                "gap_score": a.gap_score,
                "leverage": a.leverage,
                "urgency": a.urgency,
                "value_impact": a.value_impact,
            }
            for a in report.action_items
        ],
        "summary": report.summary,
    }


# ── Exception Engine Routes ────────────────────────────────────────────


@router.post("/exceptions/classify")
def classify_exception(decision_payload: Dict[str, Any]) -> dict:
    """
    Classify a decision payload into one of the 8 canonical exception classes.

    Expected optional keys in decision_payload:
        compliance_flags, is_reversible, reversibility_tag,
        data_conflicts, missing_fields, intent, action, outcome,
        threshold_violations, confidence, out_of_distribution, input_range_flags
    """
    exception_class = _exceptions.classify(decision_payload)
    return {"exception_class": exception_class}


@router.post("/exceptions/escalation")
def check_escalation(req: EscalationRequest) -> dict:
    """Evaluate whether an exception warrants escalation and return the EscalationRule."""
    rule = _exceptions.check_escalation(
        exception_class=req.exception_class,
        confidence=req.confidence,
        action_reversible=req.action_reversible,
        compliance_risk=req.compliance_risk,
        failure_cost_tolerance=req.failure_cost_tolerance,
    )
    return {
        "condition_type": rule.condition_type,
        "threshold": rule.threshold,
        "current_value": rule.current_value,
        "should_escalate": rule.should_escalate,
        "reason": rule.reason,
    }
