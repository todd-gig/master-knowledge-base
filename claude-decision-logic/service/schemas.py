"""
Pydantic models for FastAPI request/response schemas.

Maps between flat JSON format (from client) and engine dataclasses.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List


# ─────────────────────────────────────────────
# REQUEST SCHEMAS
# ─────────────────────────────────────────────

class PositiveDimensions(BaseModel):
    """Flat format for value positive dimensions."""
    revenue_impact: int = Field(0, ge=0, le=5)
    cost_efficiency: int = Field(0, ge=0, le=5)
    time_leverage: int = Field(0, ge=0, le=5)
    strategic_alignment: int = Field(0, ge=0, le=5)
    customer_benefit: int = Field(0, ge=0, le=5)
    knowledge_creation: int = Field(0, ge=0, le=5)
    compounding_potential: int = Field(0, ge=0, le=5)
    reversibility: int = Field(0, ge=0, le=5)


class PenaltyDimensions(BaseModel):
    """Flat format for value penalty dimensions."""
    downside_risk: int = Field(0, ge=0, le=5)
    execution_drag: int = Field(0, ge=0, le=5)
    uncertainty: int = Field(0, ge=0, le=5)
    ethical_misalignment: int = Field(0, ge=0, le=5)


class TrustInputs(BaseModel):
    """Flat format for trust dimension inputs."""
    evidence_quality: int = Field(0, ge=0, le=5)
    logic_integrity: int = Field(0, ge=0, le=5)
    outcome_history: int = Field(0, ge=0, le=5)
    context_fit: int = Field(0, ge=0, le=5)
    stakeholder_clarity: int = Field(0, ge=0, le=5)
    risk_containment: int = Field(0, ge=0, le=5)
    auditability: int = Field(0, ge=0, le=5)


class DecisionInput(BaseModel):
    """Decision data from client."""
    decision_id: str
    title: str
    decision_class: str  # "D0" through "D6"
    current_state: str  # "draft", "qualified", etc.
    actor_role: str  # "AI_Domain_Agent", etc.
    trust_tier: str  # "T0" through "T4"
    positive_dimensions: PositiveDimensions
    penalty_dimensions: PenaltyDimensions
    trust_inputs: TrustInputs
    evidence_refs: List[str] = Field(default_factory=list)
    ethical_conflict: bool = False
    has_missing_data: bool = False
    reversibility: str = "R1"  # "R1" through "R4"
    problem_statement: Optional[str] = None
    requested_action: Optional[str] = None
    context_summary: Optional[str] = None
    owner: Optional[str] = None
    stakeholders: List[str] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    unknowns: List[str] = Field(default_factory=list)
    required_approvals: List[str] = Field(default_factory=list)
    execution_plan: Optional[str] = None
    monitoring_metric: Optional[str] = None
    rollback_trigger: Optional[str] = None
    review_date: Optional[str] = None
    time_horizon: Optional[str] = None


class DecisionEvaluationRequest(BaseModel):
    """Request to evaluate a decision through the pipeline."""
    decision: DecisionInput


class TransitionRequest(BaseModel):
    """Request to check/perform a state transition."""
    decision_id: str
    current_state: str
    target_state: str


class GapAnalysisRequest(BaseModel):
    """Request gap analysis on a decision."""
    decision_id: str
    decision: DecisionInput
    focus_categories: Optional[List[str]] = None


# ─────────────────────────────────────────────
# RESPONSE SCHEMAS
# ─────────────────────────────────────────────

class ValueResult(BaseModel):
    """Value assessment output."""
    gross_value: int
    penalty: int
    net_value: int
    classification: str
    weighted_value: Optional[float] = None
    trust_adjusted_value: Optional[float] = None


class TrustResult(BaseModel):
    """Trust assessment output."""
    total_score: int
    average_score: float
    trust_tier: str
    confidence: float


class AuthorityResult(BaseModel):
    """Authority check result."""
    can_execute: bool
    reason: str
    required_executor: str
    required_approval: str
    min_trust: str
    actor_sufficient: bool
    trust_sufficient: bool
    approval_required: bool


class CertificateStatus(BaseModel):
    """Certificate chain status."""
    qc: bool  # Qualified Context
    vc: bool  # Value Confirmed
    tc: bool  # Trust Certified
    ec: bool  # Execution Cleared


class AuditEntry(BaseModel):
    """Single audit trail entry."""
    stage: str
    action: str
    timestamp: str
    notes: Optional[str] = None
    snapshot: Optional[Dict[str, Any]] = None


class ExecutionVerdictResponse(BaseModel):
    """Recommended execution action."""
    verdict: str  # "auto_execute", "escalate_tier_1", "block", "needs_data", etc.
    reason_code: str
    reason_text: str


class DecisionEvaluationResponse(BaseModel):
    """Full response from decision evaluation."""
    decision_id: str
    recommended_action: str  # "execute", "escalate", "block", "needs_data"
    reason_code: str
    reason_text: str
    value_result: ValueResult
    trust_result: TrustResult
    authority_result: AuthorityResult
    alignment_score: Optional[float] = None
    next_state: str
    certificate_status: CertificateStatus
    audit_log: List[AuditEntry] = Field(default_factory=list)
    priority_score: Optional[float] = None
    rtql_stage: Optional[str] = None
    execution_packet: Optional[Dict[str, Any]] = None


class TransitionResponse(BaseModel):
    """Response to state transition request."""
    allowed: bool
    current_state: str
    target_state: str
    reason: str
    required_certificates: List[str] = Field(default_factory=list)


class GapItem(BaseModel):
    """Single gap item in analysis."""
    category: str
    variable: str
    actual_score: float
    target_score: float
    gap_score: float
    gap_severity: str  # "critical", "major", "moderate", "minor"
    priority_score: float
    leverage_score: float
    urgency_score: float
    recommended_action: str


class GapAnalysisResponse(BaseModel):
    """Gap analysis result."""
    decision_id: str
    gaps_found: int
    total_gap_score: float
    prioritized_gaps: List[GapItem] = Field(default_factory=list)
    critical_gaps: List[GapItem] = Field(default_factory=list)
    major_gaps: List[GapItem] = Field(default_factory=list)
    audit_log: List[AuditEntry] = Field(default_factory=list)


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    timestamp: str
    version: str


class ConfigResponse(BaseModel):
    """Engine configuration response."""
    version: str
    authority_matrix: Dict[str, Dict[str, str]]
    valid_transitions: Dict[str, List[str]]
    value_weights: Optional[Dict[str, float]] = None
    trust_thresholds: Optional[Dict[str, float]] = None
    thresholds: Optional[Dict[str, int]] = None
