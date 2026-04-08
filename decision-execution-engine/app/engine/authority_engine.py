"""Authority Engine — role hierarchy enforcement with trust-tier validation.

Authority levels: AI_Domain_Agent, Domain_Owner, Human_Executive, Human_CEO.
Trust tiers: T0 (lowest) to T4 (highest).
"""

ROLE_HIERARCHY = [
    "AI_Domain_Agent",
    "Domain_Owner",
    "Human_Executive",
    "Human_CEO",
]

TRUST_TIER_ORDER = ["T0", "T1", "T2", "T3", "T4"]


def _trust_meets_minimum(actual: str, required: str) -> bool:
    actual_idx = TRUST_TIER_ORDER.index(actual) if actual in TRUST_TIER_ORDER else -1
    required_idx = TRUST_TIER_ORDER.index(required) if required in TRUST_TIER_ORDER else 99
    return actual_idx >= required_idx


def _role_has_authority(actor_role: str, required_role: str) -> bool:
    if required_role == "none":
        return True
    actor_idx = ROLE_HIERARCHY.index(actor_role) if actor_role in ROLE_HIERARCHY else -1
    required_idx = ROLE_HIERARCHY.index(required_role) if required_role in ROLE_HIERARCHY else 99
    return actor_idx >= required_idx


def authority_check(
    decision_class: str,
    actor_role: str,
    trust_tier: str,
    authority_matrix: dict,
) -> dict:
    rule = authority_matrix.get(decision_class, {})
    min_trust = rule.get("min_trust", "T4")
    executor = rule.get("executor", "none")
    required_approval = rule.get("required_approval", "none")

    trust_sufficient = _trust_meets_minimum(trust_tier, min_trust)
    role_sufficient = _role_has_authority(actor_role, executor)
    approval_needed = required_approval != "none"
    can_approve = _role_has_authority(actor_role, required_approval) if approval_needed else True

    can_execute = trust_sufficient and role_sufficient and can_approve

    # Escalation target if actor can't execute
    escalation_target = None
    if not can_execute:
        for role in ROLE_HIERARCHY:
            if _role_has_authority(role, executor) and _role_has_authority(role, required_approval):
                escalation_target = role
                break

    return {
        "min_trust": min_trust,
        "executor": executor,
        "required_approval": required_approval,
        "can_execute": can_execute,
        "trust_sufficient": trust_sufficient,
        "role_sufficient": role_sufficient,
        "approval_needed": approval_needed,
        "escalation_target": escalation_target,
    }
