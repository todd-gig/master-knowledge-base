def can_transition(current_state: str, target_state: str, valid_transitions: dict[str, list[str]]) -> bool:
    return target_state in valid_transitions.get(current_state, [])

def next_state_for_action(current_state: str, action: str) -> str:
    mapping = {
        ("draft", "needs_data"): "draft",
        ("draft", "block"): "draft",
        ("draft", "escalate"): "qualified",
        ("draft", "execute"): "execution_cleared",
        ("qualified", "execute"): "execution_cleared",
        ("execution_cleared", "execute"): "executed",
        ("executed", "escalate"): "reviewed",
    }
    return mapping.get((current_state, action), current_state)
