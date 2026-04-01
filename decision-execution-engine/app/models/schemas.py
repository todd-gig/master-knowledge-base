from pydantic import BaseModel, Field
from typing import Literal

TrustTier = Literal["T0", "T1", "T2", "T3", "T4"]
DecisionClass = Literal["D1", "D2", "D3", "D4", "D5", "D6"]

class DecisionInput(BaseModel):
    decision_id: str
    title: str
    decision_class: DecisionClass
    current_state: str = "draft"
    actor_role: str
    trust_tier: TrustTier
    positive_dimensions: dict[str, float]
    penalty_dimensions: dict[str, float]
    trust_inputs: dict[str, float]
    evidence_refs: list[str] = Field(default_factory=list)
    ethical_conflict: bool = False
    has_missing_data: bool = False
    reversibility: str = "R1"

class DecisionEvaluationRequest(BaseModel):
    decision: DecisionInput

class AuditEntry(BaseModel):
    stage: str
    detail: dict

class DecisionEvaluationResponse(BaseModel):
    decision_id: str
    recommended_action: str
    reason_code: str
    value_result: dict
    trust_result: dict
    authority_result: dict
    next_state: str
    certificate_status: dict
    audit_log: list[AuditEntry]

class TransitionRequest(BaseModel):
    current_state: str
    target_state: str

class TransitionResponse(BaseModel):
    allowed: bool
    current_state: str
    target_state: str
