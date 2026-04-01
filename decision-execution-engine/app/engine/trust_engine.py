def compute_trust_score(
    inputs: dict[str, float],
    multiplier_map: dict[str, float],
    trust_tier: str,
) -> dict:
    base = sum(inputs.values()) / max(len(inputs), 1)
    multiplier = multiplier_map.get(trust_tier, 0.5)
    score = base * multiplier
    return {
        "trust_base_score": round(base, 4),
        "trust_multiplier": multiplier,
        "trust_score": round(score, 4),
    }
