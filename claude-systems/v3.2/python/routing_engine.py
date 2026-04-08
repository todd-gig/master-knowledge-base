"""
routing_engine.py - claude-systems v3.2
Decision routing classifier.  Routes a signal dict to Python-First,
Claude-First, or Hybrid based on weighted suitability scores.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional

from scoring_weights import (
    PYTHON_WEIGHTS,
    CLAUDE_WEIGHTS,
    HYBRID_WEIGHTS,
    ROUTING_THRESHOLDS,
)

# ---------------------------------------------------------------------------
# Public types
# ---------------------------------------------------------------------------

PYTHON_FIRST = "Python-First"
CLAUDE_FIRST = "Claude-First"
HYBRID = "Hybrid"


@dataclass
class RoutingDecision:
    mode: str                                  # Python-First | Claude-First | Hybrid
    python_score: float
    claude_score: float
    hybrid_score: float
    confidence: float                          # 0.0 – 1.0
    rationale: str
    signals_used: Dict[str, float] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------

class RoutingEngine:
    """Classify a decision-request into a routing mode.

    Parameters
    ----------
    python_weights, claude_weights, hybrid_weights:
        Override the module-level defaults from scoring_weights.py.
    dominant_margin:
        Fractional margin (default 0.15) above which a mode is chosen outright.
    hybrid_catch_margin:
        Fractional margin (default 0.10) within which Hybrid wins when a
        codification path exists.
    """

    def __init__(
        self,
        python_weights: Optional[Dict[str, float]] = None,
        claude_weights: Optional[Dict[str, float]] = None,
        hybrid_weights: Optional[Dict[str, float]] = None,
        dominant_margin: Optional[float] = None,
        hybrid_catch_margin: Optional[float] = None,
    ) -> None:
        self._pw = python_weights or PYTHON_WEIGHTS
        self._cw = claude_weights or CLAUDE_WEIGHTS
        self._hw = hybrid_weights or HYBRID_WEIGHTS
        self._dominant_margin = (
            dominant_margin
            if dominant_margin is not None
            else ROUTING_THRESHOLDS["dominant_margin"]
        )
        self._hybrid_catch_margin = (
            hybrid_catch_margin
            if hybrid_catch_margin is not None
            else ROUTING_THRESHOLDS["hybrid_catch_margin"]
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def route(self, signals: Dict[str, float]) -> RoutingDecision:
        """Compute routing decision from a flat signals dict.

        Signal values must be in [0, 5].  Unknown keys are ignored.
        Missing keys default to 0.
        """
        py_score = self._weighted_sum(signals, self._pw)
        cl_score = self._weighted_sum(signals, self._cw)
        hy_score = self._weighted_sum(signals, self._hw)

        mode, confidence, rationale = self._decide(
            py_score, cl_score, hy_score, signals
        )

        # Normalise for confidence: ratio of winner vs max possible
        max_possible = max(py_score, cl_score, hy_score) or 1.0
        best = {"Python-First": py_score,
                "Claude-First": cl_score,
                "Hybrid": hy_score}[mode]
        confidence = round(min(best / (max_possible + 1e-9), 1.0), 4)

        return RoutingDecision(
            mode=mode,
            python_score=round(py_score, 4),
            claude_score=round(cl_score, 4),
            hybrid_score=round(hy_score, 4),
            confidence=confidence,
            rationale=rationale,
            signals_used=dict(signals),
        )

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    @staticmethod
    def _weighted_sum(signals: Dict[str, float], weights: Dict[str, float]) -> float:
        return sum(
            signals.get(k, 0.0) * w
            for k, w in weights.items()
        )

    def _decide(
        self,
        py: float,
        cl: float,
        hy: float,
        signals: Dict[str, float],
    ) -> tuple[str, float, str]:
        scores = {PYTHON_FIRST: py, CLAUDE_FIRST: cl, HYBRID: hy}
        best_mode = max(scores, key=scores.__getitem__)
        best_score = scores[best_mode]
        others = {m: s for m, s in scores.items() if m != best_mode}

        # If all scores are equal (including all-zero), treat as tie immediately
        if py == cl == hy:
            rationale = (
                f"All scores equal (py={py:.3f}, cl={cl:.3f}, hy={hy:.3f}). "
                "Defaulting to Hybrid (tie-break)."
            )
            return HYBRID, 0.5, rationale

        # Check whether best_mode is >= 15 % above ALL others
        dominant = all(
            best_score >= s * (1 + self._dominant_margin)
            for s in others.values()
        )

        if dominant:
            rationale = (
                f"{best_mode} dominates: score={best_score:.3f} is "
                f">={self._dominant_margin*100:.0f}% above all alternatives."
            )
            return best_mode, 1.0, rationale

        # Check Hybrid catch: Hybrid is within 10 % of the best AND
        # codification_path_exists signal > 0
        codification_path = signals.get("codification_path_exists", 0.0)
        if codification_path > 0:
            best_non_hybrid = max(py, cl)
            if hy >= best_non_hybrid * (1 - self._hybrid_catch_margin):
                rationale = (
                    f"Hybrid selected: hybrid_score={hy:.3f} within "
                    f"{self._hybrid_catch_margin*100:.0f}% of best "
                    f"({best_non_hybrid:.3f}) with codification_path_exists "
                    f"signal={codification_path}."
                )
                return HYBRID, 1.0, rationale

        # Tie-break -> Hybrid
        rationale = (
            f"No dominant mode detected (py={py:.3f}, cl={cl:.3f}, "
            f"hy={hy:.3f}). Defaulting to Hybrid (tie-break)."
        )
        return HYBRID, 0.5, rationale
