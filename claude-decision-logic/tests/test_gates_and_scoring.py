"""
Test Suite: Gates, Scoring, and Weighted Scoring

Tests for:
- gates: 7-gate autonomous execution authorization
- scoring: Trust tier calculation, alignment checking, priority scoring
- weighted_scoring: Weighted value and trust score computation

Run: python -m unittest tests.test_gates_and_scoring -v
"""

import unittest

from engine.models import (
    DecisionObject, DecisionClass, ReversibilityTag,
    ValueScores, TrustScores, AlignmentScores, TrustTier,
    ExecutionVerdict, CertificateChain,
)
from engine.gates import (
    gate_1_doctrine, gate_2_trust_tier, gate_3_value_threshold,
    gate_4_reversibility, gate_5_risk_containment, gate_6_approval_routing,
    gate_7_monitoring, run_7_gate_authorization,
)
from engine.scoring import (
    calculate_trust_tier, trust_adjusted_value, check_alignment,
    calculate_priority_score,
)
from engine.weighted_scoring import compute_weighted_value, compute_weighted_trust
from engine.config import EngineConfig, load_config


def _make_decision(**overrides):
    """Build a valid DecisionObject with sensible defaults, applying overrides."""
    defaults = dict(
        title="Test Decision",
        owner="user1",
        problem_statement="Test problem",
        requested_action="Test action",
        decision_class=DecisionClass.D1_REVERSIBLE_TACTICAL,
        reversibility=ReversibilityTag.R1_EASILY_REVERSIBLE,
        evidence_refs=["ref1"],
        stakeholders=["team_a"],
        execution_plan="Phase 1 deploy",
        monitoring_metric="Latency p95 < 500ms",
        rollback_trigger="Revert if latency > 1s",
        review_date="2026-04-15",
        value_scores=ValueScores(
            revenue_impact=3, cost_efficiency=3, time_leverage=3,
            strategic_alignment=3, customer_human_benefit=3,
            knowledge_asset_creation=3, compounding_potential=3,
            reversibility=3, downside_risk=1, execution_drag=1,
            uncertainty=1, ethical_misalignment=0,
        ),
        trust_scores=TrustScores(
            evidence_quality=4, logic_integrity=4, outcome_history=3,
            context_fit=4, stakeholder_clarity=4, risk_containment=4,
            auditability=4,
        ),
        alignment_scores=AlignmentScores(
            doctrine_alignment=0.8, ethos_alignment=0.8,
            first_principles_alignment=0.8,
        ),
    )
    defaults.update(overrides)
    return DecisionObject(**defaults)


# ─────────────────────────────────────────────
# INDIVIDUAL GATE TESTS
# ─────────────────────────────────────────────

class TestGate1Doctrine(unittest.TestCase):

    def test_passes_for_aligned_decision(self):
        d = _make_decision()
        alignment = AlignmentScores(
            doctrine_alignment=0.8, ethos_alignment=0.8,
            first_principles_alignment=0.8,
        )
        ok, reason = gate_1_doctrine(d, alignment)
        self.assertTrue(ok, f"Gate 1 failed: {reason}")

    def test_fails_for_ethical_conflict(self):
        d = _make_decision(ethical_conflict=True)
        alignment = AlignmentScores(
            doctrine_alignment=0.1, ethos_alignment=0.1,
            first_principles_alignment=0.1,
            anti_pattern_flags=["ethical_misalignment_above_threshold"],
        )
        ok, reason = gate_1_doctrine(d, alignment)
        self.assertFalse(ok, "Gate 1 should fail for ethical conflict")


class TestGate2TrustTier(unittest.TestCase):

    def test_passes_when_trust_meets_minimum(self):
        d = _make_decision(decision_class=DecisionClass.D1_REVERSIBLE_TACTICAL)
        ok, reason = gate_2_trust_tier(d, TrustTier.T3_CERTIFIED)
        self.assertTrue(ok, f"Gate 2 failed: {reason}")

    def test_fails_when_trust_below_minimum(self):
        d = _make_decision(decision_class=DecisionClass.D1_REVERSIBLE_TACTICAL)
        ok, reason = gate_2_trust_tier(d, TrustTier.T1_OBSERVED)
        self.assertFalse(ok, "Gate 2 should fail for insufficient trust")


class TestGate3ValueThreshold(unittest.TestCase):

    def test_passes_when_value_exceeds_threshold(self):
        d = _make_decision(decision_class=DecisionClass.D1_REVERSIBLE_TACTICAL)
        # D1 threshold is 8, our default net value is 21
        ok, reason = gate_3_value_threshold(d, 21)
        self.assertTrue(ok, f"Gate 3 failed: {reason}")

    def test_fails_when_value_below_threshold(self):
        d = _make_decision(decision_class=DecisionClass.D1_REVERSIBLE_TACTICAL)
        ok, reason = gate_3_value_threshold(d, 2)
        self.assertFalse(ok, "Gate 3 should fail for insufficient value")


class TestGate4Reversibility(unittest.TestCase):

    def test_passes_for_easily_reversible(self):
        d = _make_decision(reversibility=ReversibilityTag.R1_EASILY_REVERSIBLE)
        ok, reason = gate_4_reversibility(d)
        self.assertTrue(ok, f"Gate 4 failed: {reason}")

    def test_fails_for_irreversible(self):
        d = _make_decision(reversibility=ReversibilityTag.R4_EFFECTIVELY_IRREVERSIBLE)
        ok, reason = gate_4_reversibility(d)
        self.assertFalse(ok, "Gate 4 should fail for irreversible decision")


class TestGate5RiskContainment(unittest.TestCase):

    def test_passes_with_low_risk_and_rollback(self):
        d = _make_decision(
            rollback_trigger="Revert if metric drops 10%",
            value_scores=ValueScores(
                revenue_impact=3, cost_efficiency=3, time_leverage=3,
                strategic_alignment=3, customer_human_benefit=3,
                knowledge_asset_creation=3, compounding_potential=3,
                reversibility=4, downside_risk=1, execution_drag=1,
                uncertainty=1, ethical_misalignment=0,
            ),
        )
        ok, reason = gate_5_risk_containment(d)
        self.assertTrue(ok, f"Gate 5 failed: {reason}")

    def test_fails_with_high_risk_no_rollback(self):
        d = _make_decision(
            rollback_trigger="",
            value_scores=ValueScores(
                revenue_impact=5, cost_efficiency=1, time_leverage=1,
                strategic_alignment=4, customer_human_benefit=1,
                knowledge_asset_creation=2, compounding_potential=2,
                reversibility=1, downside_risk=5, execution_drag=4,
                uncertainty=5, ethical_misalignment=0,
            ),
        )
        ok, reason = gate_5_risk_containment(d)
        self.assertFalse(ok, "Gate 5 should fail for high risk without rollback")


class TestGate7Monitoring(unittest.TestCase):

    def test_passes_with_monitoring_configured(self):
        d = _make_decision(
            monitoring_metric="Revenue +10%",
            review_date="2026-04-15",
            rollback_trigger="Revert if metric drops",
        )
        ok, reason = gate_7_monitoring(d)
        self.assertTrue(ok, f"Gate 7 failed: {reason}")

    def test_fails_without_monitoring(self):
        d = _make_decision(
            monitoring_metric="",
            review_date=None,
            rollback_trigger="",
        )
        ok, reason = gate_7_monitoring(d)
        self.assertFalse(ok, "Gate 7 should fail without monitoring")


# ─────────────────────────────────────────────
# SCORING FUNCTIONS
# ─────────────────────────────────────────────

class TestScoringFunctions(unittest.TestCase):

    def test_calculate_trust_tier_high(self):
        scores = TrustScores(
            evidence_quality=5, logic_integrity=5, outcome_history=4,
            context_fit=5, stakeholder_clarity=5, risk_containment=5,
            auditability=5,
        )
        tier, reasons = calculate_trust_tier(scores)
        self.assertIn(tier, [TrustTier.T3_CERTIFIED, TrustTier.T4_DELEGATED])

    def test_calculate_trust_tier_low(self):
        scores = TrustScores(
            evidence_quality=1, logic_integrity=1, outcome_history=1,
            context_fit=1, stakeholder_clarity=1, risk_containment=1,
            auditability=1,
        )
        tier, reasons = calculate_trust_tier(scores)
        self.assertIn(tier, [TrustTier.T0_UNQUALIFIED, TrustTier.T1_OBSERVED])

    def test_trust_adjusted_value(self):
        vs = ValueScores(
            revenue_impact=3, cost_efficiency=3, time_leverage=3,
            strategic_alignment=3, customer_human_benefit=3,
            knowledge_asset_creation=3, compounding_potential=3,
            reversibility=3, downside_risk=1, execution_drag=1,
            uncertainty=1, ethical_misalignment=0,
        )
        adjusted = trust_adjusted_value(vs, 1.15)
        self.assertAlmostEqual(adjusted, vs.net_value() * 1.15, places=2)

    def test_check_alignment(self):
        d = _make_decision()
        alignment = check_alignment(d)
        self.assertIsInstance(alignment, AlignmentScores)

    def test_priority_score_positive(self):
        vs = ValueScores(
            revenue_impact=4, cost_efficiency=4, time_leverage=4,
            strategic_alignment=4, customer_human_benefit=3,
            knowledge_asset_creation=3, compounding_potential=3,
            reversibility=3, downside_risk=1, execution_drag=1,
            uncertainty=1, ethical_misalignment=0,
        )
        alignment = AlignmentScores(
            doctrine_alignment=0.9, ethos_alignment=0.9,
            first_principles_alignment=0.9,
        )
        score = calculate_priority_score(
            value_scores=vs,
            trust_tier=TrustTier.T3_CERTIFIED,
            alignment=alignment,
            rtql_multiplier=1.0,
            probability_of_success=0.8,
        )
        self.assertGreater(score, 0)


# ─────────────────────────────────────────────
# WEIGHTED SCORING
# ─────────────────────────────────────────────

class TestWeightedScoring(unittest.TestCase):

    def test_compute_weighted_value_returns_dict(self):
        vs = ValueScores(
            revenue_impact=4, cost_efficiency=3, time_leverage=4,
            strategic_alignment=4, customer_human_benefit=3,
            knowledge_asset_creation=3, compounding_potential=4,
            reversibility=3, downside_risk=1, execution_drag=1,
            uncertainty=1, ethical_misalignment=0,
        )
        config = load_config()
        result = compute_weighted_value(vs, config)
        self.assertIsInstance(result, dict)
        self.assertIn("weighted_net", result)
        self.assertGreater(result["weighted_net"], 0)

    def test_compute_weighted_trust_returns_dict(self):
        ts = TrustScores(
            evidence_quality=4, logic_integrity=4, outcome_history=3,
            context_fit=4, stakeholder_clarity=4, risk_containment=4,
            auditability=4,
        )
        config = load_config()
        result = compute_weighted_trust(ts, TrustTier.T3_CERTIFIED, config)
        self.assertIsInstance(result, dict)
        self.assertIn("adjusted_trust_score", result)


# ─────────────────────────────────────────────
# FULL 7-GATE AUTHORIZATION
# ─────────────────────────────────────────────

class TestFullGateAuthorization(unittest.TestCase):

    def test_auto_execute_for_d1(self):
        d = _make_decision()
        alignment = AlignmentScores(
            doctrine_alignment=0.9, ethos_alignment=0.9,
            first_principles_alignment=0.9,
        )
        chain = CertificateChain()  # Empty chain — gates will still run

        packet = run_7_gate_authorization(
            decision=d,
            trust_tier=TrustTier.T3_CERTIFIED,
            net_value=21,
            alignment=alignment,
            certificate_chain=chain,
        )

        # Without a complete certificate chain, we expect escalation or block
        # but gates themselves should mostly pass
        self.assertIsNotNone(packet.verdict)
        self.assertIsNotNone(packet.gate_results)


if __name__ == '__main__':
    unittest.main()
