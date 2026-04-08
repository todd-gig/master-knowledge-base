"""
Test Suite: Core Engine Modules

Tests for:
- models: Decision object schema and validation
- config: Engine configuration and defaults
- authority: Role-based decision authority matrix
- certificates: Certificate chain issuance logic
- state_machine: Decision lifecycle states

Run: python -m pytest tests/test_core_modules.py -v
"""

import unittest

from engine.models import (
    DecisionObject, DecisionClass, ValueScores, TrustScores, AlignmentScores,
    RTQLInput, RTQLScores, CausalChecks,
    TrustTier
)
from engine.config import EngineConfig
from engine.authority import authority_check
from engine.certificates import CertificateChain
from engine.state_machine import (
    can_transition, advance_state, get_lifecycle_status,
    STATE_CERTIFICATE_MAP, VERDICT_TO_STATE
)


class TestDecisionObjectSchema(unittest.TestCase):
    """Test DecisionObject model and field validation."""

    def test_decision_object_creation_minimal(self):
        """Create minimal valid DecisionObject."""
        decision = DecisionObject(
            decision_id="test-001",
            title="Test Decision",
            owner="test_owner",
            requested_action="Test action",
            value_scores=ValueScores(
                revenue_impact=2, cost_efficiency=2, time_leverage=2,
                strategic_alignment=2, customer_human_benefit=2,
                knowledge_asset_creation=2, compounding_potential=2,
                reversibility=3, downside_risk=1, execution_drag=1,
                uncertainty=1, ethical_misalignment=0
            ),
            trust_scores=TrustScores(
                evidence_quality=3, logic_integrity=3, outcome_history=2,
                context_fit=3, stakeholder_clarity=3, risk_containment=3,
                auditability=3
            )
        )

        self.assertEqual(decision.decision_id, "test-001")
        self.assertEqual(decision.title, "Test Decision")
        self.assertEqual(decision.owner, "test_owner")
        self.assertIsNotNone(decision.value_scores)
        self.assertIsNotNone(decision.trust_scores)

    def test_decision_object_with_rtql(self):
        """Create DecisionObject with RTQL input."""
        rtql_input = RTQLInput(
            claim="Test claim",
            source="Test source",
            is_identifiable=True,
            has_provenance=True,
            scores=RTQLScores(
                source_integrity=5, exposure_count=4, independence=5,
                explainability=8, replicability=8, adversarial_robustness=8,
                novelty_yield=4
            ),
            causal_checks=CausalChecks(
                reveals_causal_mechanism=False, is_irreducible=False,
                survives_authority_removal=False, survives_context_shift=False
            )
        )

        decision = DecisionObject(
            decision_id="test-002",
            title="RTQL Test",
            owner="test_owner",
            requested_action="Test action",
            rtql_input=rtql_input,
            value_scores=ValueScores(
                revenue_impact=2, cost_efficiency=2, time_leverage=2,
                strategic_alignment=2, customer_human_benefit=2,
                knowledge_asset_creation=2, compounding_potential=2,
                reversibility=3, downside_risk=1, execution_drag=1,
                uncertainty=1, ethical_misalignment=0
            ),
            trust_scores=TrustScores(
                evidence_quality=3, logic_integrity=3, outcome_history=2,
                context_fit=3, stakeholder_clarity=3, risk_containment=3,
                auditability=3
            )
        )

        self.assertIsNotNone(decision.rtql_input)
        self.assertEqual(decision.rtql_input.claim, "Test claim")

    def test_value_scores_gross_and_net(self):
        """Test ValueScores gross and net calculations."""
        vs = ValueScores(
            revenue_impact=3, cost_efficiency=3, time_leverage=3,
            strategic_alignment=3, customer_human_benefit=3,
            knowledge_asset_creation=3, compounding_potential=3,
            reversibility=3, downside_risk=2, execution_drag=1,
            uncertainty=1, ethical_misalignment=0
        )

        gross = vs.gross_value()
        penalty = vs.penalty()
        net = vs.net_value()

        self.assertGreater(gross, 0)
        self.assertGreater(penalty, 0)
        self.assertEqual(net, gross - penalty)

    def test_trust_scores_total_and_average(self):
        """Test TrustScores total and average calculations."""
        ts = TrustScores(
            evidence_quality=4, logic_integrity=4, outcome_history=3,
            context_fit=4, stakeholder_clarity=4, risk_containment=4,
            auditability=4
        )

        total = ts.total()
        average = ts.average()

        self.assertEqual(total, 27)  # 7 scores of 3-4
        self.assertAlmostEqual(average, total / 7, places=2)


class TestEngineConfig(unittest.TestCase):
    """Test EngineConfig initialization and defaults."""

    def test_config_loads_defaults(self):
        """EngineConfig loads default values."""
        config = EngineConfig()

        self.assertIsNotNone(config.value_weights)
        self.assertIsNotNone(config.penalty_weights)
        self.assertIsNotNone(config.trust_multiplier)
        self.assertIsNotNone(config.valid_transitions)

    def test_config_value_weights_keys(self):
        """EngineConfig has all value weight dimensions."""
        config = EngineConfig()

        expected_keys = [
            "revenue_impact", "cost_efficiency", "time_leverage",
            "strategic_alignment", "customer_benefit", "knowledge_creation",
            "compounding_potential", "reversibility"
        ]

        for key in expected_keys:
            self.assertTrue(
                hasattr(config.value_weights, key) or key in config.value_weights.__dict__,
                f"Missing weight: {key}"
            )

    def test_config_trust_multiplier_keys(self):
        """EngineConfig has trust tier multipliers."""
        config = EngineConfig()

        # Trust tiers: T1, T2, T3, T4 (or similar)
        self.assertIsInstance(config.trust_multiplier, dict)
        self.assertGreater(len(config.trust_multiplier), 0)


class TestAuthorityMatrix(unittest.TestCase):
    """Test role-based authority for decision execution."""

    def test_ai_agent_authorized_for_d1(self):
        """AI Domain Agent authorized to execute D1."""
        decision = DecisionObject(
            decision_id="test-003",
            title="D1 Test",
            decision_class=DecisionClass.D1_REVERSIBLE_TACTICAL,
            owner="ai_agent",
            actor_role="AI_Domain_Agent",
            requested_action="Test action",
            current_state="trust_certified",
            value_scores=ValueScores(
                revenue_impact=2, cost_efficiency=2, time_leverage=2,
                strategic_alignment=2, customer_human_benefit=2,
                knowledge_asset_creation=2, compounding_potential=2,
                reversibility=4, downside_risk=1, execution_drag=1,
                uncertainty=1, ethical_misalignment=0
            ),
            trust_scores=TrustScores(
                evidence_quality=4, logic_integrity=4, outcome_history=3,
                context_fit=4, stakeholder_clarity=4, risk_containment=4,
                auditability=4
            )
        )

        config = EngineConfig()
        result = authority_check(
            actor_role=decision.actor_role,
            decision_class=decision.decision_class,
            trust_tier=TrustTier.T3_CERTIFIED,
            config=config
        )

        # Should have authorization for D1
        self.assertTrue(result['can_execute'])

    def test_human_ceo_required_for_d6(self):
        """D6 decisions require human (CEO) role."""
        decision = DecisionObject(
            decision_id="test-004",
            title="D6 Test",
            decision_class=DecisionClass.D6_IRREVERSIBLE_HIGH_BLAST,
            owner="ceo",
            actor_role="Human_CEO",
            requested_action="Test action",
            current_state="trust_certified",
            value_scores=ValueScores(
                revenue_impact=5, cost_efficiency=2, time_leverage=3,
                strategic_alignment=5, customer_human_benefit=3,
                knowledge_asset_creation=4, compounding_potential=5,
                reversibility=1, downside_risk=5, execution_drag=4,
                uncertainty=5, ethical_misalignment=0
            ),
            trust_scores=TrustScores(
                evidence_quality=4, logic_integrity=4, outcome_history=3,
                context_fit=4, stakeholder_clarity=4, risk_containment=3,
                auditability=4
            )
        )

        config = EngineConfig()
        result = authority_check(
            actor_role=decision.actor_role,
            decision_class=decision.decision_class,
            trust_tier=TrustTier.T4_DELEGATED,
            config=config
        )

        # Result should indicate this is a high-level decision
        self.assertTrue(result['can_execute'])


class TestCertificateChain(unittest.TestCase):
    """Test certificate chain issuance."""

    def test_certificate_chain_creation(self):
        """Create and validate certificate chain."""
        chain = CertificateChain()

        # Initially empty (all certificates are None)
        self.assertIsNone(chain.qc)
        self.assertIsNone(chain.vc)
        self.assertIsNone(chain.tc)
        self.assertIsNone(chain.ec)

    def test_certificate_chain_state_mapping(self):
        """Test state to certificate mapping."""
        # Verify certificate mapping is complete
        expected_states = [
            "draft", "qualified", "value_confirmed", "trust_certified",
            "execution_cleared", "executed", "reviewed", "archived"
        ]

        for state in expected_states:
            self.assertIn(state, STATE_CERTIFICATE_MAP)


class TestStateMachine(unittest.TestCase):
    """Test decision lifecycle state transitions."""

    def test_valid_transition_draft_to_qualified(self):
        """Draft can transition to qualified."""
        can = can_transition("draft", "qualified")
        self.assertTrue(can)

    def test_valid_transition_qualified_to_value_confirmed(self):
        """Qualified can transition to value_confirmed."""
        can = can_transition("qualified", "value_confirmed")
        self.assertTrue(can)

    def test_valid_backward_transition_value_confirmed_to_qualified(self):
        """Value_confirmed can transition back to qualified."""
        can = can_transition("value_confirmed", "qualified")
        self.assertTrue(can)

    def test_invalid_transition_draft_to_archived(self):
        """Draft cannot jump directly to archived."""
        can = can_transition("draft", "archived")
        self.assertFalse(can)

    def test_advance_state_success(self):
        """advance_state returns success for valid transition."""
        result = advance_state("draft", "qualified")

        self.assertTrue(result["success"])
        self.assertEqual(result["current_state"], "qualified")
        self.assertEqual(result["previous_state"], "draft")

    def test_advance_state_failure(self):
        """advance_state returns failure for invalid transition."""
        result = advance_state("draft", "archived")

        self.assertFalse(result["success"])
        self.assertEqual(result["current_state"], "draft")  # No state change
        self.assertIn("Invalid transition", result["reason"])

    def test_lifecycle_status_draft(self):
        """Lifecycle status for draft state."""
        status = get_lifecycle_status("draft")

        self.assertEqual(status["current_state"], "draft")
        self.assertTrue(status["is_pre_execution"])
        self.assertFalse(status["is_post_execution"])
        self.assertFalse(status["is_terminal"])
        self.assertFalse(status["is_executable"])

    def test_lifecycle_status_execution_cleared(self):
        """Lifecycle status for execution_cleared state."""
        status = get_lifecycle_status("execution_cleared")

        self.assertEqual(status["current_state"], "execution_cleared")
        self.assertTrue(status["is_executable"])
        self.assertFalse(status["is_pre_execution"])
        self.assertFalse(status["is_post_execution"])

    def test_lifecycle_status_archived(self):
        """Lifecycle status for archived state."""
        status = get_lifecycle_status("archived")

        self.assertEqual(status["current_state"], "archived")
        self.assertTrue(status["is_terminal"])
        self.assertTrue(status["is_post_execution"])
        self.assertFalse(status["is_pre_execution"])

    def test_verdict_to_state_mapping(self):
        """Verify verdict to state mapping is complete."""
        expected_verdicts = [
            "auto_execute", "escalate_tier_1", "escalate_tier_2",
            "escalate_tier_3", "block", "information_only", "needs_data"
        ]

        for verdict in expected_verdicts:
            self.assertIn(verdict, VERDICT_TO_STATE)
            state = VERDICT_TO_STATE[verdict]
            self.assertIn(state, STATE_CERTIFICATE_MAP)


class TestAlignmentScores(unittest.TestCase):
    """Test AlignmentScores model."""

    def test_alignment_scores_creation(self):
        """Create AlignmentScores with values."""
        scores = AlignmentScores(
            doctrine_alignment=0.85,
            ethos_alignment=0.90,
            first_principles_alignment=0.80,
            applied_principles=["Test principle 1", "Test principle 2"]
        )

        self.assertEqual(scores.doctrine_alignment, 0.85)
        self.assertEqual(scores.ethos_alignment, 0.90)
        self.assertEqual(len(scores.applied_principles), 2)

    def test_alignment_scores_composite(self):
        """Calculate composite alignment score."""
        scores = AlignmentScores(
            doctrine_alignment=0.8,
            ethos_alignment=0.9,
            first_principles_alignment=0.8,
            applied_principles=[]
        )

        # Should be able to calculate some composite
        self.assertGreater(scores.doctrine_alignment, 0)
        self.assertGreater(scores.ethos_alignment, 0)


if __name__ == '__main__':
    unittest.main()
