"""
codification_scorer.py - claude-systems v3.2
Score decision paths for Python migration readiness.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from scoring_weights import CODIFICATION_BANDS


# ---------------------------------------------------------------------------
# Public types
# ---------------------------------------------------------------------------

BAND_CODIFY_NOW       = "codify_now"
BAND_PREPARE_DESIGN   = "prepare_design"
BAND_CONTINUE_LOGGING = "continue_logging"
BAND_KEEP_IN_CLAUDE   = "keep_in_claude"

BAND_LABELS: Dict[str, str] = {
    BAND_CODIFY_NOW:       "Codify Now (0.80–1.00)",
    BAND_PREPARE_DESIGN:   "Prepare Design (0.60–0.79)",
    BAND_CONTINUE_LOGGING: "Continue Logging (0.40–0.59)",
    BAND_KEEP_IN_CLAUDE:   "Keep in Claude (<0.40)",
}


@dataclass
class CodificationResult:
    path_id: str
    priority_score: float               # raw product, unbounded
    normalised_score: float             # clipped to [0, 1]
    band: str                           # band key
    band_label: str
    recommendation: str
    expected_monthly_savings: float
    confidence_in_stability: float
    implementation_feasibility: float


# ---------------------------------------------------------------------------
# Scorer
# ---------------------------------------------------------------------------

class CodificationScorer:
    """Score a decision path record for Python migration readiness.

    The priority formula is::

        priority = expected_monthly_savings
                   * confidence_in_stability
                   * implementation_feasibility

    Each factor is expected to be in [0, 1].  The raw product is then
    normalised (clipped) to [0, 1] and assigned to a band.

    Path record keys
    ----------------
    Required
      - path_id (str)
      - expected_monthly_savings (float, 0-1)
      - confidence_in_stability  (float, 0-1)
      - implementation_feasibility (float, 0-1)
    """

    def __init__(self, bands: Optional[Dict[str, Any]] = None) -> None:
        self._bands = bands or CODIFICATION_BANDS

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def score(self, path_record: Dict[str, Any]) -> CodificationResult:
        """Score a single path record and return a CodificationResult."""
        path_id = str(path_record.get("path_id", "unknown"))
        savings = float(path_record.get("expected_monthly_savings", 0.0))
        stability = float(path_record.get("confidence_in_stability", 0.0))
        feasibility = float(path_record.get("implementation_feasibility", 0.0))

        priority = savings * stability * feasibility
        normalised = max(0.0, min(1.0, priority))

        band = self._assign_band(normalised)
        recommendation = self._recommendation(band)

        return CodificationResult(
            path_id=path_id,
            priority_score=round(priority, 6),
            normalised_score=round(normalised, 6),
            band=band,
            band_label=BAND_LABELS[band],
            recommendation=recommendation,
            expected_monthly_savings=savings,
            confidence_in_stability=stability,
            implementation_feasibility=feasibility,
        )

    def score_batch(
        self, path_records: list[Dict[str, Any]]
    ) -> list[CodificationResult]:
        """Score multiple records, sorted by normalised_score descending."""
        results = [self.score(r) for r in path_records]
        results.sort(key=lambda r: r.normalised_score, reverse=True)
        return results

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _assign_band(self, score: float) -> str:
        for band_key, limits in self._bands.items():
            lo = limits["min"]
            hi = limits["max"]
            if lo <= score <= hi:
                return band_key
        # fallback
        return BAND_KEEP_IN_CLAUDE

    @staticmethod
    def _recommendation(band: str) -> str:
        return {
            BAND_CODIFY_NOW:       "High priority: implement Python logic now.",
            BAND_PREPARE_DESIGN:   "Design phase: document rules and prepare spec.",
            BAND_CONTINUE_LOGGING: "Log decisions and gather more signal.",
            BAND_KEEP_IN_CLAUDE:   "Retain in Claude; insufficient codification value.",
        }.get(band, "Unknown band.")
