def authority_check(decision_class: str, actor_role: str, trust_tier: str, authority_matrix: dict) -> dict:
    rule = authority_matrix.get(decision_class, {})
    min_trust = rule.get("min_trust", "T9")
    executor = rule.get("executor", "none")
    required_approval = rule.get("required_approval", "none")
    can_execute = actor_role in {executor, required_approval} and trust_tier >= min_trust
    return {
        "min_trust": min_trust,
        "executor": executor,
        "required_approval": required_approval,
        "can_execute": can_execute,
    }
