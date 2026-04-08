"""
FastAPI routes bridging client API to decision engine.

Endpoints:
- GET /health
- GET /v1/config
- POST /v1/decisions/evaluate
- POST /v1/decisions/transition
- POST /v1/decisions/gap-analysis
"""

import sys
import os
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, status

# Add parent directory to path for engine imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.models import (
    DecisionObject, DecisionClass, ReversibilityTag,
    TimeHorizon, ValueScores, TrustScores, AlignmentScores, PipelineResult, ExecutionVerdict
)
from engine.pipeline import process_decision
from engine.config import load_config, EngineConfig
from engine.state_machine import advance_state, next_state_for_action
from engine.authority import authority_check
from engine.gap_analysis import analyze_gaps

from .schemas import (
    DecisionEvaluationRequest, DecisionEvaluationResponse,
    TransitionRequest, TransitionResponse,
    GapAnalysisRequest, GapAnalysisResponse,
    HealthResponse, ConfigResponse,
    ValueResult, TrustResult, AuthorityResult, CertificateStatus,
    AuditEntry, GapItem
)


router = APIRouter()
_config: Optional[EngineConfig] = None


def get_config() -> EngineConfig:
    """Get or load engine config."""
    global _config
    if _config is None:
        _config = load_config()
    return _config


def map_decision_input_to_engine(decision_input) -> DecisionObject:
    """
    Convert flat client request format to engine DecisionObject.

    Maps:
    - positive_dimensions dict → ValueScores
    - penalty_dimensions dict → ValueScores (penalty fields)
    - trust_inputs dict → TrustScores
    - decision_class string → DecisionClass enum
    - reversibility string → ReversibilityTag enum
    - trust_tier string → TrustTier enum
    """

    # Map string decision class to enum
    class_map = {
        "D0": DecisionClass.D0_INFORMATIONAL,
        "D1": DecisionClass.D1_REVERSIBLE_TACTICAL,
        "D2": DecisionClass.D2_OPERATIONAL,
        "D3": DecisionClass.D3_FINANCIAL,
        "D4": DecisionClass.D4_STRATEGIC,
        "D5": DecisionClass.D5_LEGAL_ETHICAL,
        "D6": DecisionClass.D6_IRREVERSIBLE_HIGH_BLAST,
    }

    # Map reversibility string to enum
    reversibility_map = {
        "R1": ReversibilityTag.R1_EASILY_REVERSIBLE,
        "R2": ReversibilityTag.R2_MODERATELY_REVERSIBLE,
        "R3": ReversibilityTag.R3_COSTLY_TO_REVERSE,
        "R4": ReversibilityTag.R4_EFFECTIVELY_IRREVERSIBLE,
    }

    # Map time horizon string to enum (if provided)
    time_map = {
        "immediate": TimeHorizon.IMMEDIATE,
        "near_term": TimeHorizon.NEAR_TERM,
        "mid_term": TimeHorizon.MID_TERM,
        "long_term": TimeHorizon.LONG_TERM,
    }

    # Build ValueScores from positive dimensions
    pd = decision_input.positive_dimensions
    value_scores = ValueScores(
        revenue_impact=pd.revenue_impact,
        cost_efficiency=pd.cost_efficiency,
        time_leverage=pd.time_leverage,
        strategic_alignment=pd.strategic_alignment,
        customer_human_benefit=pd.customer_benefit,
        knowledge_asset_creation=pd.knowledge_creation,
        compounding_potential=pd.compounding_potential,
        reversibility=pd.reversibility,
    )

    # Add penalty dimensions to ValueScores
    pen = decision_input.penalty_dimensions
    value_scores.downside_risk = pen.downside_risk
    value_scores.execution_drag = pen.execution_drag
    value_scores.uncertainty = pen.uncertainty
    value_scores.ethical_misalignment = pen.ethical_misalignment

    # Build TrustScores
    ti = decision_input.trust_inputs
    trust_scores = TrustScores(
        evidence_quality=ti.evidence_quality,
        logic_integrity=ti.logic_integrity,
        outcome_history=ti.outcome_history,
        context_fit=ti.context_fit,
        stakeholder_clarity=ti.stakeholder_clarity,
        risk_containment=ti.risk_containment,
        auditability=ti.auditability,
    )

    # Build DecisionObject
    decision = DecisionObject(
        decision_id=decision_input.decision_id,
        title=decision_input.title,
        decision_class=class_map.get(decision_input.decision_class, DecisionClass.D1_REVERSIBLE_TACTICAL),
        owner=decision_input.owner or "unspecified",
        time_horizon=time_map.get(decision_input.time_horizon, TimeHorizon.IMMEDIATE),
        reversibility=reversibility_map.get(decision_input.reversibility, ReversibilityTag.R1_EASILY_REVERSIBLE),
        problem_statement=decision_input.problem_statement or "",
        requested_action=decision_input.requested_action or "",
        context_summary=decision_input.context_summary or "",
        stakeholders=decision_input.stakeholders or [],
        constraints=decision_input.constraints or [],
        value_scores=value_scores,
        trust_scores=trust_scores,
        alignment_scores=AlignmentScores(),  # Will be computed by pipeline
        evidence_refs=decision_input.evidence_refs or [],
        assumptions=decision_input.assumptions or [],
        unknowns=decision_input.unknowns or [],
        required_approvals=decision_input.required_approvals or [],
        execution_plan=decision_input.execution_plan or "",
        monitoring_metric=decision_input.monitoring_metric or "",
        rollback_trigger=decision_input.rollback_trigger or "",
        review_date=decision_input.review_date,
        current_state=decision_input.current_state,
        actor_role=decision_input.actor_role,
        has_missing_data=decision_input.has_missing_data,
        ethical_conflict=decision_input.ethical_conflict,
    )

    return decision


def map_pipeline_result_to_response(
    result: PipelineResult,
    decision_obj: DecisionObject,
) -> DecisionEvaluationResponse:
    """Convert PipelineResult to API response format."""

    # Determine recommended_action from execution verdict
    if result.execution_packet:
        verdict = result.execution_packet.verdict
        recommended_map = {
            ExecutionVerdict.AUTO_EXECUTE: "execute",
            ExecutionVerdict.ESCALATE_TIER_1: "escalate",
            ExecutionVerdict.ESCALATE_TIER_2: "escalate",
            ExecutionVerdict.ESCALATE_TIER_3: "escalate",
            ExecutionVerdict.BLOCK: "block",
            ExecutionVerdict.NEEDS_DATA: "needs_data",
            ExecutionVerdict.INFORMATION_ONLY: "info_only",
        }
        recommended_action = recommended_map.get(verdict, "block")
        reason_code = verdict.value
    else:
        recommended_action = "block"
        reason_code = "execution_packet_missing"

    # Build certificate status
    cert_status = CertificateStatus(
        qc=False,
        vc=False,
        tc=False,
        ec=False,
    )
    if result.certificate_chain:
        cert_status.qc = result.certificate_chain.qc is not None and result.certificate_chain.qc.is_valid()
        cert_status.vc = result.certificate_chain.vc is not None and result.certificate_chain.vc.is_valid()
        cert_status.tc = result.certificate_chain.tc is not None and result.certificate_chain.tc.is_valid()
        cert_status.ec = result.certificate_chain.ec is not None and result.certificate_chain.ec.is_valid()

    # Build value result
    value_result = ValueResult(
        gross_value=decision_obj.value_scores.gross_value(),
        penalty=decision_obj.value_scores.penalty(),
        net_value=decision_obj.value_scores.net_value(),
        classification=result.value_classification,
    )

    # Build trust result
    trust_result = TrustResult(
        total_score=result.trust_total,
        average_score=result.trust_total / 7.0 if result.trust_total > 0 else 0.0,
        trust_tier=result.trust_tier.value,
        confidence=0.8,  # Placeholder
    )

    # Build authority result from authority check
    config = get_config()
    auth_result = authority_check(
        decision_obj.decision_class,
        decision_obj.actor_role,
        result.trust_tier,
        config,
    )
    authority_result = AuthorityResult(**auth_result)

    # Convert audit records to audit entries
    audit_log = []
    for record in result.audit_trail:
        audit_log.append(AuditEntry(
            stage=record.pipeline_stage,
            action=record.action_taken,
            timestamp=record.timestamp,
            notes=record.notes,
            snapshot={
                "rtql_stage": record.rtql_stage,
                "value_net_score": record.value_net_score,
                "trust_tier": record.trust_tier,
                "execution_verdict": record.execution_verdict,
            }
        ))

    return DecisionEvaluationResponse(
        decision_id=result.decision_id,
        recommended_action=recommended_action,
        reason_code=reason_code,
        reason_text=result.executive_summary,
        value_result=value_result,
        trust_result=trust_result,
        authority_result=authority_result,
        alignment_score=result.alignment_composite,
        next_state=decision_obj.current_state,  # Will be updated by state machine
        certificate_status=cert_status,
        audit_log=audit_log,
        priority_score=result.priority_score,
        rtql_stage=result.rtql_result.stage.value if result.rtql_result else None,
    )


# ─────────────────────────────────────────────
# ENDPOINTS
# ─────────────────────────────────────────────

@router.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint."""
    return HealthResponse(
        status="ok",
        timestamp=datetime.now().isoformat(),
        version="0.1.0"
    )


@router.get("/v1/config", response_model=ConfigResponse)
async def get_engine_config():
    """Return current engine configuration."""
    config = get_config()

    # Build authority matrix response
    auth_matrix = {}
    for dc_key, rule in config.authority_matrix.items():
        auth_matrix[dc_key] = {
            "min_trust": rule.min_trust,
            "executor": rule.executor,
            "required_approval": rule.required_approval,
        }

    return ConfigResponse(
        version="0.1.0",
        authority_matrix=auth_matrix,
        valid_transitions=config.valid_transitions or {},
        value_weights=getattr(config, "value_weights", None),
        trust_thresholds=getattr(config, "trust_thresholds", None),
    )


@router.post("/v1/decisions/evaluate", response_model=DecisionEvaluationResponse)
async def evaluate_decision(request: DecisionEvaluationRequest):
    """
    Run full decision evaluation through the pipeline.

    Accepts flat client format, converts to engine format, runs pipeline,
    returns comprehensive evaluation result.
    """
    try:
        # Convert request to engine format
        decision = map_decision_input_to_engine(request.decision)

        # Validate basic structure
        validation_errors = decision.validate()
        if validation_errors:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Validation errors: {validation_errors}"
            )

        # Run pipeline
        config = get_config()
        result = process_decision(decision, config)

        # Check if pipeline failed
        if not result.success:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Pipeline failed: {result.validation_errors}"
            )

        # Determine next state based on verdict
        if result.execution_packet:
            next_state = next_state_for_action(
                decision.current_state,
                result.execution_packet.verdict.value
            )
            decision.current_state = next_state

        # Convert result to response format
        response = map_pipeline_result_to_response(result, decision)
        response.next_state = decision.current_state

        return response

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Evaluation failed: {str(e)}"
        )


@router.post("/v1/decisions/transition", response_model=TransitionResponse)
async def validate_state_transition(request: TransitionRequest):
    """
    Validate or perform a state transition.

    Checks if transition from current_state to target_state is valid
    per the state machine defined in engine.yaml.
    """
    try:
        config = get_config()

        # Check if transition is allowed
        transition_result = advance_state(
            request.current_state,
            request.target_state,
            config
        )

        return TransitionResponse(
            allowed=transition_result["success"],
            current_state=transition_result["previous_state"],
            target_state=transition_result.get("current_state", request.current_state),
            reason=transition_result["reason"],
            required_certificates=transition_result.get("required_certificates", []),
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Transition check failed: {str(e)}"
        )


@router.post("/v1/decisions/gap-analysis", response_model=GapAnalysisResponse)
async def run_gap_analysis_endpoint(request: GapAnalysisRequest):
    """
    Run gap analysis on a decision.

    Detects performance gaps across dimensions and returns
    prioritized action recommendations.
    """
    try:
        # Convert decision to engine format
        decision = map_decision_input_to_engine(request.decision)

        # Build gap items from decision scores
        gap_items = _build_gap_items_from_decision(decision)

        # Run gap analysis
        gaps = analyze_gaps(gap_items)

        # Filter to focus categories if provided
        if request.focus_categories:
            gaps = [g for g in gaps if g.category in request.focus_categories]

        # Separate by severity
        critical_gaps = [g for g in gaps if g.gap_severity_label == "critical"]
        major_gaps = [g for g in gaps if g.gap_severity_label == "major"]

        # Convert to response format
        gap_responses = [
            GapItem(
                category=g.category,
                variable=g.variable,
                actual_score=g.actual_score,
                target_score=g.target_score,
                gap_score=g.gap_score,
                gap_severity=g.gap_severity_label,
                priority_score=g.priority_score,
                leverage_score=g.leverage_score,
                urgency_score=g.urgency_score,
                recommended_action=f"Increase {g.variable} from {g.actual_score} to {g.target_score}",
            )
            for g in gaps
        ]

        critical_responses = [
            GapItem(
                category=g.category,
                variable=g.variable,
                actual_score=g.actual_score,
                target_score=g.target_score,
                gap_score=g.gap_score,
                gap_severity=g.gap_severity_label,
                priority_score=g.priority_score,
                leverage_score=g.leverage_score,
                urgency_score=g.urgency_score,
                recommended_action=f"Increase {g.variable} from {g.actual_score} to {g.target_score}",
            )
            for g in critical_gaps
        ]

        major_responses = [
            GapItem(
                category=g.category,
                variable=g.variable,
                actual_score=g.actual_score,
                target_score=g.target_score,
                gap_score=g.gap_score,
                gap_severity=g.gap_severity_label,
                priority_score=g.priority_score,
                leverage_score=g.leverage_score,
                urgency_score=g.urgency_score,
                recommended_action=f"Increase {g.variable} from {g.actual_score} to {g.target_score}",
            )
            for g in major_gaps
        ]

        return GapAnalysisResponse(
            decision_id=request.decision_id,
            gaps_found=len(gaps),
            total_gap_score=sum(g.gap_score for g in gaps),
            prioritized_gaps=gap_responses,
            critical_gaps=critical_responses,
            major_gaps=major_responses,
            audit_log=[],
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Gap analysis failed: {str(e)}"
        )


def _build_gap_items_from_decision(decision: DecisionObject) -> list[dict]:
    """Build gap analysis input items from a DecisionObject."""
    from engine.models import RTQLStage

    items = []

    # Value dimension gaps
    vs = decision.value_scores
    value_dims = [
        ("value", "revenue_impact", vs.revenue_impact),
        ("value", "cost_efficiency", vs.cost_efficiency),
        ("value", "time_leverage", vs.time_leverage),
        ("value", "strategic_alignment", vs.strategic_alignment),
        ("value", "customer_benefit", vs.customer_human_benefit),
        ("value", "knowledge_creation", vs.knowledge_asset_creation),
        ("value", "compounding_potential", vs.compounding_potential),
        ("value", "reversibility", vs.reversibility),
    ]

    for cat, var, score in value_dims:
        items.append({
            "category": cat,
            "variable": var,
            "actual_score": score,
            "target_score": 5.0,
            "strategic_importance": 1.0,
            "rtql_stage": RTQLStage.QUALIFIED.value,
            "leverage_score": score / 5.0 * 5.0,
            "urgency_score": 2.0,
            "value_matrix_impact": score / 5.0,
        })

    # Trust dimension gaps
    ts = decision.trust_scores
    trust_dims = [
        ("trust", "evidence_quality", ts.evidence_quality),
        ("trust", "logic_integrity", ts.logic_integrity),
        ("trust", "outcome_history", ts.outcome_history),
        ("trust", "context_fit", ts.context_fit),
        ("trust", "stakeholder_clarity", ts.stakeholder_clarity),
        ("trust", "risk_containment", ts.risk_containment),
        ("trust", "auditability", ts.auditability),
    ]

    for cat, var, score in trust_dims:
        items.append({
            "category": cat,
            "variable": var,
            "actual_score": score,
            "target_score": 5.0,
            "strategic_importance": 1.0,
            "rtql_stage": RTQLStage.QUALIFIED.value,
            "leverage_score": score / 5.0 * 5.0,
            "urgency_score": 2.0,
            "value_matrix_impact": score / 5.0,
        })

    # Penalty dimension gaps (inverted: higher penalty = lower actual)
    penalty_dims = [
        ("risk", "downside_risk", 5.0 - vs.downside_risk),
        ("execution", "execution_drag", 5.0 - vs.execution_drag),
        ("evidence", "uncertainty", 5.0 - vs.uncertainty),
        ("ethics", "ethical_alignment", 5.0 - vs.ethical_misalignment),
    ]

    for cat, var, score in penalty_dims:
        items.append({
            "category": cat,
            "variable": var,
            "actual_score": max(0, score),
            "target_score": 5.0,
            "strategic_importance": 1.0,
            "rtql_stage": RTQLStage.QUALIFIED.value,
            "leverage_score": max(0, score) / 5.0 * 5.0,
            "urgency_score": 3.0,
            "value_matrix_impact": max(0, score) / 5.0,
        })

    return items
