"""Trust Engine — 7-dimension trust assessment with tier multipliers.

Trust dimensions: consistency, transparency, domain_expertise,
track_record, stakeholder_alignment, data_quality, ethical_standing.
"""


TRUST_DIMENSION_WEIGHTS = {
    "consistency": 0.15,
    "transparency": 0.15,
    "domain_expertise": 0.20,
    "track_record": 0.15,
    "stakeholder_alignment": 0.10,
    "data_quality": 0.15,
    "ethical_standing": 0.10,
}


def compute_trust_score(
    inputs: dict[str, float],
    multiplier_map: dict[str, float],
    trust_tier: str,
) -> dict:
    # Weighted base score using known dimensions, fallback to equal-weight average
    weighted_sum = 0.0
    total_weight = 0.0
    for dim, val in inputs.items():
        w = TRUST_DIMENSION_WEIGHTS.get(dim, 1.0 / max(len(inputs), 1))
        weighted_sum += val * w
        total_weight += w

    base = weighted_sum / total_weight if total_weight > 0 else 0.0
    multiplier = multiplier_map.get(trust_tier, 0.5)
    score = base * multiplier

    # Dimension-level breakdown
    dimension_scores = {}
    for dim, val in inputs.items():
        w = TRUST_DIMENSION_WEIGHTS.get(dim, 0.1)
        dimension_scores[dim] = round(val * w, 4)

    # Trust risk flags
    flags = []
    if inputs.get("ethical_standing", 1.0) < 0.5:
        flags.append("low_ethical_standing")
    if inputs.get("data_quality", 1.0) < 0.4:
        flags.append("poor_data_quality")
    if score < 1.5:
        flags.append("low_overall_trust")

    return {
        "trust_base_score": round(base, 4),
        "trust_multiplier": multiplier,
        "trust_score": round(score, 4),
        "dimension_scores": dimension_scores,
        "trust_tier": trust_tier,
        "risk_flags": flags,
    }
