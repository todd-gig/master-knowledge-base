def compute_weighted_value(
    positive: dict[str, float],
    penalties: dict[str, float],
    value_weights: dict[str, float],
    penalty_weights: dict[str, float],
) -> dict:
    gross = sum(positive.get(k, 0.0) * value_weights.get(k, 1.0) for k in positive)
    penalty = sum(penalties.get(k, 0.0) * penalty_weights.get(k, 1.0) for k in penalties)
    net = gross - penalty
    return {
        "gross_value_score": round(gross, 4),
        "penalty_score": round(penalty, 4),
        "net_value_score": round(net, 4),
    }
