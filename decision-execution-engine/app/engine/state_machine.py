"""State Machine — decision lifecycle with 8 states and action-based transitions.

States: draft → qualified → value_confirmed → trust_certified →
        execution_cleared → executed → reviewed → archived

Actions: needs_data, block, escalate, execute, review, archive
"""

# Full action→transition mapping
ACTION_TRANSITIONS: dict[tuple[str, str], str] = {
    # From draft
    ("draft", "needs_data"): "draft",
    ("draft", "block"): "draft",
    ("draft", "escalate"): "qualified",
    ("draft", "execute"): "execution_cleared",
    # From qualified
    ("qualified", "execute"): "value_confirmed",
    ("qualified", "escalate"): "qualified",
    ("qualified", "block"): "draft",
    # From value_confirmed
    ("value_confirmed", "execute"): "trust_certified",
    ("value_confirmed", "block"): "qualified",
    # From trust_certified
    ("trust_certified", "execute"): "execution_cleared",
    ("trust_certified", "block"): "qualified",
    # From execution_cleared
    ("execution_cleared", "execute"): "executed",
    ("execution_cleared", "block"): "trust_certified",
    # From executed
    ("executed", "review"): "reviewed",
    ("executed", "escalate"): "reviewed",
    # From reviewed
    ("reviewed", "archive"): "archived",
    ("reviewed", "escalate"): "qualified",
}

# Terminal states
TERMINAL_STATES = {"archived"}


def can_transition(
    current_state: str,
    target_state: str,
    valid_transitions: dict[str, list[str]],
) -> bool:
    return target_state in valid_transitions.get(current_state, [])


def next_state_for_action(current_state: str, action: str) -> str:
    return ACTION_TRANSITIONS.get((current_state, action), current_state)


def is_terminal(state: str) -> bool:
    return state in TERMINAL_STATES


def available_actions(current_state: str) -> list[str]:
    return [
        action
        for (state, action) in ACTION_TRANSITIONS
        if state == current_state
    ]


def full_path_to_execution(current_state: str) -> list[str]:
    """Return the shortest action sequence from current state to 'executed'."""
    if current_state == "executed":
        return []
    # BFS
    from collections import deque
    visited: set[str] = set()
    queue: deque[tuple[str, list[str]]] = deque([(current_state, [])])
    while queue:
        state, path = queue.popleft()
        if state in visited:
            continue
        visited.add(state)
        for (s, action), target in ACTION_TRANSITIONS.items():
            if s == state and target not in visited:
                new_path = path + [action]
                if target == "executed":
                    return new_path
                queue.append((target, new_path))
    return []  # no path found
