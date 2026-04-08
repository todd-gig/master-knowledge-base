"""FastAPI routes for OVS, Value Leakage, ROI, Causal Mapping, Governance Gates,
Adaptive Learning, Layer Tracking, and Outcome Reporting.
"""
from __future__ import annotations


from fastapi import APIRouter
from pydantic import BaseModel

from engine.adaptive_learning import (
    AdaptiveLearningEngine,
)
from engine.causal_mapper import CausalMapper
from engine.governance_gates import (
    Gate1Inputs,
    Gate2Inputs,
    Gate3Inputs,
    GovernanceGateEngine,
)
from engine.layer_tracker import LayerTracker
from engine.outcome_reporter import OutcomeReporter
from engine.ovs_engine import (
    LearningDimensions,
    OVSEngine,
    PeopleDimensions,
    ProcessDimensions,
    TechnologyDimensions,
)
from engine.roi_engine import ImplementationCost, LeverageScope, ROIEngine, ROIInput
from engine.value_leakage import ValueLeakageDetector

router = APIRouter(prefix="/v2", tags=["v2-engines"])

# Shared instances
_ovs = OVSEngine()
_leakage = ValueLeakageDetector()
_roi = ROIEngine()
_causal = CausalMapper()
_gates = GovernanceGateEngine()
_learning = AdaptiveLearningEngine()
_tracker = LayerTracker()
_reporter = OutcomeReporter()


# ── OVS ────────────────────────────────────────────────────────────────


class OVSRequest(BaseModel):
    people: dict[str, float]
    process: dict[str, float]
    technology: dict[str, float]
    learning: dict[str, float]
    confidence_factors: dict[str, float] = {}


@router.post("/ovs/calculate")
def calculate_ovs(req: OVSRequest) -> dict:
    result = _ovs.calculate(
        PeopleDimensions(**req.people),
        ProcessDimensions(**req.process),
        TechnologyDimensions(**req.technology),
        LearningDimensions(**req.learning),
        confidence_factors=req.confidence_factors,
    )
    return {
        "composite_ovs": result.composite_ovs,
        "organizational_value": result.organizational_value,
        "maturity_level": result.maturity_level.value,
        "systems": {
            s.name: {"score": s.score, "status": s.status.value}
            for s in [result.people_score, result.process_score,
                      result.technology_score, result.learning_score]
        },
        "warnings": result.warnings,
    }


# ── Value Leakage ─────────────────────────────────────────────────────


class LeakageRequest(BaseModel):
    annual_org_value: float = 1_000_000.0
    people: dict[str, float]
    process: dict[str, float]
    technology: dict[str, float]
    learning: dict[str, float]


@router.post("/leakage/detect")
def detect_leakage(req: LeakageRequest) -> dict:
    _leakage.annual_org_value = req.annual_org_value
    ovs = _ovs.calculate(
        PeopleDimensions(**req.people),
        ProcessDimensions(**req.process),
        TechnologyDimensions(**req.technology),
        LearningDimensions(**req.learning),
    )
    report = _leakage.detect(ovs)
    return {
        "total_estimated_annual_loss": report.total_estimated_annual_loss,
        "systems_in_leakage": report.systems_in_leakage,
        "cascade_multiplier": report.cascade_multiplier_applied,
        "alerts": [
            {
                "rule_type": a.rule_type.value,
                "system": a.system_name,
                "dimension": a.dimension,
                "loss": a.estimated_annual_loss,
                "severity": a.severity,
                "description": a.description,
            }
            for a in report.alerts
        ],
    }


# ── ROI ────────────────────────────────────────────────────────────────


class ROIInputSchema(BaseModel):
    name: str
    annual_leakage_loss: float
    expected_performance_after: float
    personnel_cost: float = 0
    capital_cost: float = 0
    coordination_cost: float = 0
    opportunity_cost: float = 0
    leverage_scope: str = "single_system"
    confidence: float = 0.8
    complexity_score: float = 0.5
    org_readiness_gap: float = 0.2
    required_hours: float = 100
    strategic_urgency: float = 0.5
    is_dependency_blocker: bool = False


class ROIPortfolioRequest(BaseModel):
    initiatives: list[ROIInputSchema]


@router.post("/roi/rank")
def rank_roi(req: ROIPortfolioRequest) -> dict:
    inputs = [
        ROIInput(
            name=i.name,
            annual_leakage_loss=i.annual_leakage_loss,
            expected_performance_after=i.expected_performance_after,
            implementation_cost=ImplementationCost(
                i.personnel_cost, i.capital_cost, i.coordination_cost, i.opportunity_cost
            ),
            leverage_scope=LeverageScope(i.leverage_scope),
            confidence=i.confidence,
            complexity_score=i.complexity_score,
            org_readiness_gap=i.org_readiness_gap,
            required_hours=i.required_hours,
            strategic_urgency=i.strategic_urgency,
            is_dependency_blocker=i.is_dependency_blocker,
        )
        for i in req.initiatives
    ]
    portfolio = _roi.rank_portfolio(inputs)
    return {
        "total_impact": portfolio.total_impact,
        "total_cost": portfolio.total_cost,
        "portfolio_roi": portfolio.portfolio_roi,
        "ranked": [
            {
                "rank": r.rank,
                "name": r.name,
                "roi_score": r.roi_score,
                "impact_value": r.impact_value,
                "passes_threshold": r.passes_threshold,
                "value_per_hour": r.value_per_hour,
            }
            for r in portfolio.results
        ],
    }


# ── Governance Gates ───────────────────────────────────────────────────


class Gate1Request(BaseModel):
    adoption_rate: float
    critical_failure_rate: float
    schedule_slip_rate: float
    resource_deployment_rate: float


class Gate2Request(BaseModel):
    efficiency_gain: float
    behavioral_alignment: float
    new_critical_failures_per_week: float
    cascade_materialization_rate: float


class Gate3Request(BaseModel):
    behavioral_alignment_sustained: float
    structural_adaptation_complete: bool
    compound_value_improvement: float
    ovs_composite: float


def _gate_response(assessment) -> dict:
    return {
        "gate": assessment.gate.value,
        "decision": assessment.decision.value if assessment.decision else None,
        "authority": assessment.decision_authority.value,
        "criteria": [
            {"name": c.name, "value": c.measured_value, "threshold": c.pass_threshold, "status": c.status.value}
            for c in assessment.criteria
        ],
        "escalations": [
            {"metric": e.metric, "threshold": e.threshold, "actual": e.actual, "owner": e.response_owner}
            for e in assessment.escalations if e.triggered
        ],
    }


@router.post("/gates/day30")
def evaluate_gate1(req: Gate1Request) -> dict:
    return _gate_response(_gates.evaluate_gate1(Gate1Inputs(**req.model_dump())))


@router.post("/gates/day60")
def evaluate_gate2(req: Gate2Request) -> dict:
    return _gate_response(_gates.evaluate_gate2(Gate2Inputs(**req.model_dump())))


@router.post("/gates/day90")
def evaluate_gate3(req: Gate3Request) -> dict:
    return _gate_response(_gates.evaluate_gate3(Gate3Inputs(**req.model_dump())))
