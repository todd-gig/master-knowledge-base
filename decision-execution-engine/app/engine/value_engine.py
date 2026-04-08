"""Value Engine — 8-dimension positive scoring + 4-dimension penalties.

Positive dimensions: revenue_impact, cost_efficiency, time_leverage,
strategic_alignment, customer_benefit, knowledge_creation,
compounding_potential, reversibility.

Penalty dimensions: downside_risk, execution_drag, uncertainty,
ethical_misalignment.
"""


def compute_weighted_value(
    positive: dict[str, float],
    penalties: dict[str, float],
    value_weights: dict[str, float],
    penalty_weights: dict[str, float],
) -> dict:
    # Dimension-level breakdown
    positive_breakdown = {}
    gross = 0.0
    for k, v in positive.items():
        w = value_weights.get(k, 1.0)
        contrib = v * w
        positive_breakdown[k] = round(contrib, 4)
        gross += contrib

    penalty_breakdown = {}
    penalty_total = 0.0
    for k, v in penalties.items():
        w = penalty_weights.get(k, 1.0)
        contrib = v * w
        penalty_breakdown[k] = round(contrib, 4)
        penalty_total += contrib

    net = gross - penalty_total

    # Value classification
    if net >= 14.0:
        classification = "high_value"
    elif net >= 8.0:
        classification = "moderate_value"
    elif net >= 4.0:
        classification = "low_value"
    else:
        classification = "insufficient_value"

    # Risk-adjusted score (penalize more when uncertainty is high)
    uncertainty = penalties.get("uncertainty", 0.0)
    risk_adjusted = net * (1 - uncertainty * 0.1) if uncertainty > 0 else net

    return {
        "gross_value_score": round(gross, 4),
        "penalty_score": round(penalty_total, 4),
        "net_value_score": round(net, 4),
        "risk_adjusted_score": round(risk_adjusted, 4),
        "classification": classification,
        "positive_breakdown": positive_breakdown,
        "penalty_breakdown": penalty_breakdown,
    }
