def determine_action(
    *,
    value_score: float,
    trust_score: float,
    has_missing_data: bool,
    ethical_conflict: bool,
    required_approval_missing: bool,
    thresholds,
) -> tuple[str, str]:
    if ethical_conflict:
        return "block", "ethical_conflict"
    if has_missing_data:
        return "needs_data", "missing_required_data"
    if required_approval_missing:
        return "escalate", "approval_missing"
    if value_score >= thresholds.value_execute_min and trust_score >= thresholds.trust_execute_min:
        return "execute", "thresholds_met"
    if value_score >= thresholds.value_escalate_min and trust_score >= thresholds.trust_recommend_min:
        return "escalate", "requires_higher_authority"
    return "block", "insufficient_value_or_trust"
