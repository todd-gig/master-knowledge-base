from app.engine.value_engine import compute_weighted_value
from app.engine.trust_engine import compute_trust_score
from app.engine.policy_engine import determine_action
from app.engine.authority_engine import authority_check
from app.engine.state_machine import can_transition, next_state_for_action
from app.models.schemas import (
    DecisionEvaluationRequest,
    DecisionEvaluationResponse,
    TransitionRequest,
    TransitionResponse,
    AuditEntry,
)

class DecisionService:
    def __init__(self, settings):
        self.settings = settings

    def evaluate(self, payload: DecisionEvaluationRequest) -> DecisionEvaluationResponse:
        d = payload.decision

        value_result = compute_weighted_value(
            d.positive_dimensions,
            d.penalty_dimensions,
            self.settings.value_weights,
            self.settings.penalty_weights,
        )
        trust_result = compute_trust_score(
            d.trust_inputs,
            self.settings.trust_multiplier,
            d.trust_tier,
        )
        authority_result = authority_check(
            d.decision_class,
            d.actor_role,
            d.trust_tier,
            self.settings.authority_matrix,
        )

        required_approval_missing = (
            not authority_result["can_execute"]
            and d.decision_class in {"D2", "D3", "D4", "D5", "D6"}
        )

        recommended_action, reason_code = determine_action(
            value_score=value_result["net_value_score"],
            trust_score=trust_result["trust_score"],
            has_missing_data=d.has_missing_data or not bool(d.evidence_refs),
            ethical_conflict=d.ethical_conflict,
            required_approval_missing=required_approval_missing,
            thresholds=self.settings.thresholds,
        )

        next_state = next_state_for_action(d.current_state, recommended_action)

        certificate_status = {
            "qc": d.current_state in {
                "qualified",
                "value_confirmed",
                "trust_certified",
                "execution_cleared",
                "executed",
                "reviewed",
                "archived",
            },
            "vc": value_result["net_value_score"] >= self.settings.thresholds.value_escalate_min,
            "tc": trust_result["trust_score"] >= self.settings.thresholds.trust_recommend_min,
            "ec": recommended_action == "execute" and authority_result["can_execute"],
        }

        audit_log = [
            AuditEntry(stage="value_engine", detail=value_result),
            AuditEntry(stage="trust_engine", detail=trust_result),
            AuditEntry(stage="authority_engine", detail=authority_result),
            AuditEntry(
                stage="policy_engine",
                detail={
                    "recommended_action": recommended_action,
                    "reason_code": reason_code,
                },
            ),
            AuditEntry(
                stage="state_machine",
                detail={
                    "current_state": d.current_state,
                    "next_state": next_state,
                },
            ),
        ]

        return DecisionEvaluationResponse(
            decision_id=d.decision_id,
            recommended_action=recommended_action,
            reason_code=reason_code,
            value_result=value_result,
            trust_result=trust_result,
            authority_result=authority_result,
            next_state=next_state,
            certificate_status=certificate_status,
            audit_log=audit_log,
        )

    def transition(self, payload: TransitionRequest) -> TransitionResponse:
        allowed = can_transition(
            payload.current_state,
            payload.target_state,
            self.settings.valid_transitions,
        )
        return TransitionResponse(
            allowed=allowed,
            current_state=payload.current_state,
            target_state=payload.target_state,
        )
