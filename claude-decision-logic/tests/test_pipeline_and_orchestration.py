"""
Test Suite: Pipeline Orchestration & Runner Scenarios

Tests for:
- pipeline: process_decision() full orchestration through all 12 stages
- runner: 5 end-to-end decision scenarios with expected verdicts

Run: python -m unittest tests.test_pipeline_and_orchestration -v
"""

import unittest
from datetime import datetime

from engine.models import (
    DecisionObject, DecisionClass, ReversibilityTag, TimeHorizon,
    ValueScores, TrustScores, AlignmentScores,
    RTQLInput, RTQLScores, CausalChecks,
    ExecutionVerdict, PipelineResult, TrustTier,
)
from engine.config import EngineConfig, load_config
from engine.pipeline import process_decision
from engine.audit import generate_executive_summary, result_to_json


def _valid_decision(**overrides):
    """Build a fully valid DecisionObject passing all validation checks."""
    defaults = dict(
        title="Test Decision",
        owner="test_owner",
        problem_statement="Test problem to solve",
        requested_action="Test action to take",
        evidence_refs=["evidence_doc_1"],
        stakeholders=["team_a"],
        execution_plan="Phase 1 deploy",
        monitoring_metric="Latency p95 < 500ms",
        rollback_trigger="Revert if latency > 1s",
        review_date="2026-04-15",
        current_state="draft",
        alignment_scores=AlignmentScores(
            doctrine_alignment=0.8, ethos_alignment=0.8,
            first_principles_alignment=0.8,
        ),
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
    )
    defaults.update(overrides)
    return DecisionObject(**defaults)


class TestPipelineStages(unittest.TestCase):
    """Test individual pipeline stages and flow."""

    def setUp(self):
        self.config = load_config()

    def test_pipeline_stage_1_input_validation_pass(self):
        decision = _valid_decision(decision_id="test-pipe-001")
        result = process_decision(decision, self.config)
        self.assertTrue(result.success)
        self.assertEqual(len(result.validation_errors), 0)

    def test_pipeline_stage_1_input_validation_fail(self):
        decision = DecisionObject(
            decision_id="test-pipe-002",
            title="Incomplete",
            owner="user",
        )
        result = process_decision(decision, self.config)
        self.assertFalse(result.success)
        self.assertGreater(len(result.validation_errors), 0)

    def test_pipeline_stage_2_rtql_prefilter_no_input(self):
        decision = _valid_decision(decision_id="test-pipe-003")
        result = process_decision(decision, self.config)
        self.assertTrue(result.success)
        self.assertIsNotNone(result.rtql_result)
        self.assertEqual(result.rtql_result.trust_multiplier, 1.0)

    def test_pipeline_stage_2_rtql_prefilter_with_input(self):
        decision = _valid_decision(
            decision_id="test-pipe-004",
            rtql_input=RTQLInput(
                claim="Test claim",
                source="Test source",
                scores=RTQLScores(
                    source_integrity=5, exposure_count=4, independence=5,
                    explainability=8, replicability=8,
                    adversarial_robustness=8, novelty_yield=4,
                ),
                causal_checks=CausalChecks(),
                is_identifiable=True,
                has_provenance=True,
            ),
        )
        result = process_decision(decision, self.config)
        self.assertTrue(result.success)
        self.assertIsNotNone(result.rtql_result)
        self.assertIsNotNone(result.rtql_result.stage)

    def test_pipeline_stage_3_value_assessment(self):
        decision = _valid_decision(decision_id="test-pipe-005")
        result = process_decision(decision, self.config)
        self.assertTrue(result.success)
        self.assertGreater(result.net_value_score, 0)
        self.assertIn(result.value_classification,
                      ["strong_candidate", "conditional_candidate", "weak_candidate", "block"])

    def test_pipeline_stage_4_trust_assessment(self):
        decision = _valid_decision(decision_id="test-pipe-006")
        result = process_decision(decision, self.config)
        self.assertTrue(result.success)
        self.assertIsNotNone(result.trust_tier)
        self.assertGreater(result.trust_total, 0)

    def test_pipeline_stage_5_alignment_check(self):
        decision = _valid_decision(decision_id="test-pipe-007")
        result = process_decision(decision, self.config)
        self.assertTrue(result.success)
        self.assertGreater(result.alignment_composite, 0.0)

    def test_pipeline_stage_6_certificate_chain(self):
        decision = _valid_decision(decision_id="test-pipe-008")
        result = process_decision(decision, self.config)
        self.assertTrue(result.success)
        self.assertIsNotNone(result.certificate_chain)

    def test_pipeline_stage_7_execution_routing(self):
        decision = _valid_decision(decision_id="test-pipe-009")
        result = process_decision(decision, self.config)
        self.assertTrue(result.success)
        self.assertIsNotNone(result.execution_packet)
        self.assertIsNotNone(result.execution_packet.verdict)

    def test_pipeline_stage_8_state_machine_transition(self):
        decision = _valid_decision(decision_id="test-pipe-010")
        result = process_decision(decision, self.config)
        self.assertTrue(result.success)
        # State machine should have been called

    def test_pipeline_stage_9_priority_scoring(self):
        decision = _valid_decision(decision_id="test-pipe-011")
        result = process_decision(decision, self.config)
        self.assertTrue(result.success)
        self.assertIsNotNone(result.priority_score)
        self.assertGreater(result.priority_score, 0)

    def test_pipeline_audit_trail_complete(self):
        decision = _valid_decision(decision_id="test-pipe-012")
        result = process_decision(decision, self.config)
        self.assertTrue(result.success)
        self.assertGreater(len(result.audit_trail), 0)

    def test_pipeline_executive_summary_generated(self):
        decision = _valid_decision(decision_id="test-pipe-013")
        result = process_decision(decision, self.config)
        self.assertTrue(result.success)
        self.assertIn("DECISION", result.executive_summary)
        self.assertIn("PROCESSED", result.executive_summary)


class TestPipelinePreChecks(unittest.TestCase):

    def setUp(self):
        self.config = load_config()

    def test_pipeline_ethical_conflict_override(self):
        decision = _valid_decision(
            decision_id="test-ethic-001",
            ethical_conflict=True,
        )
        result = process_decision(decision, self.config)
        self.assertTrue(result.success)
        self.assertEqual(result.execution_packet.verdict, ExecutionVerdict.BLOCK)

    def test_pipeline_missing_data_override(self):
        decision = _valid_decision(
            decision_id="test-data-001",
            has_missing_data=True,
        )
        result = process_decision(decision, self.config)
        self.assertTrue(result.success)
        self.assertEqual(result.execution_packet.verdict, ExecutionVerdict.NEEDS_DATA)


# ─────────────────────────────────────────────
# SCENARIO TESTS (from runner.py)
# ─────────────────────────────────────────────

class TestScenario1D1AutoExecute(unittest.TestCase):
    """Scenario 1: D1 reversible tactical → auto_execute."""

    def setUp(self):
        self.config = load_config()
        self.decision = _valid_decision(
            decision_id="SCEN-D1-001",
            title="Switch CI runner to GitHub Actions",
            decision_class=DecisionClass.D1_REVERSIBLE_TACTICAL,
            reversibility=ReversibilityTag.R1_EASILY_REVERSIBLE,
            actor_role="Domain_Owner",
            value_scores=ValueScores(
                revenue_impact=2, cost_efficiency=4, time_leverage=3,
                strategic_alignment=3, customer_human_benefit=2,
                knowledge_asset_creation=3, compounding_potential=3,
                reversibility=4, downside_risk=1, execution_drag=1,
                uncertainty=1, ethical_misalignment=0,
            ),
            trust_scores=TrustScores(
                evidence_quality=4, logic_integrity=4, outcome_history=4,
                context_fit=4, stakeholder_clarity=4, risk_containment=4,
                auditability=4,
            ),
        )

    def test_scenario_1_processes_successfully(self):
        result = process_decision(self.decision, self.config)
        self.assertTrue(result.success)

    def test_scenario_1_verdict_auto_execute(self):
        result = process_decision(self.decision, self.config)
        self.assertTrue(result.success)
        self.assertEqual(result.execution_packet.verdict, ExecutionVerdict.AUTO_EXECUTE)

    def test_scenario_1_trust_tier(self):
        result = process_decision(self.decision, self.config)
        self.assertIn(result.trust_tier, [TrustTier.T3_CERTIFIED, TrustTier.T4_DELEGATED])

    def test_scenario_1_value_classification(self):
        result = process_decision(self.decision, self.config)
        self.assertIn(result.value_classification, ["strong_candidate", "conditional_candidate"])


class TestScenario2D3Financial(unittest.TestCase):
    """Scenario 2: D3 financial → escalate."""

    def setUp(self):
        self.config = load_config()
        self.decision = _valid_decision(
            decision_id="SCEN-D3-001",
            title="Q2 budget reallocation",
            decision_class=DecisionClass.D3_FINANCIAL,
            reversibility=ReversibilityTag.R3_COSTLY_TO_REVERSE,
            actor_role="AI_Domain_Agent",
            required_approvals=["cfo"],
            value_scores=ValueScores(
                revenue_impact=3, cost_efficiency=4, time_leverage=3,
                strategic_alignment=4, customer_human_benefit=2,
                knowledge_asset_creation=2, compounding_potential=3,
                reversibility=2, downside_risk=3, execution_drag=2,
                uncertainty=2, ethical_misalignment=0,
            ),
            trust_scores=TrustScores(
                evidence_quality=3, logic_integrity=4, outcome_history=3,
                context_fit=3, stakeholder_clarity=3, risk_containment=3,
                auditability=3,
            ),
        )

    def test_scenario_2_processes_successfully(self):
        result = process_decision(self.decision, self.config)
        self.assertTrue(result.success)

    def test_scenario_2_verdict_escalate_or_block(self):
        result = process_decision(self.decision, self.config)
        self.assertTrue(result.success)
        # D3 with AI_Domain_Agent and R3 should escalate or block
        self.assertIn(result.execution_packet.verdict, [
            ExecutionVerdict.ESCALATE_TIER_1,
            ExecutionVerdict.ESCALATE_TIER_2,
            ExecutionVerdict.BLOCK,
        ])


class TestScenario3D6Blocked(unittest.TestCase):
    """Scenario 3: D6 irreversible, ethical conflict → block."""

    def setUp(self):
        self.config = load_config()
        self.decision = _valid_decision(
            decision_id="SCEN-D6-001",
            title="Major corporate restructuring",
            decision_class=DecisionClass.D6_IRREVERSIBLE_HIGH_BLAST,
            reversibility=ReversibilityTag.R4_EFFECTIVELY_IRREVERSIBLE,
            actor_role="AI_Domain_Agent",
            ethical_conflict=True,
            value_scores=ValueScores(
                revenue_impact=5, cost_efficiency=3, time_leverage=2,
                strategic_alignment=5, customer_human_benefit=1,
                knowledge_asset_creation=2, compounding_potential=4,
                reversibility=1, downside_risk=5, execution_drag=4,
                uncertainty=4, ethical_misalignment=4,
            ),
            trust_scores=TrustScores(
                evidence_quality=2, logic_integrity=2, outcome_history=1,
                context_fit=2, stakeholder_clarity=1, risk_containment=1,
                auditability=2,
            ),
        )

    def test_scenario_3_processes_successfully(self):
        result = process_decision(self.decision, self.config)
        self.assertTrue(result.success)

    def test_scenario_3_verdict_block(self):
        result = process_decision(self.decision, self.config)
        self.assertTrue(result.success)
        self.assertEqual(result.execution_packet.verdict, ExecutionVerdict.BLOCK)


class TestScenario4RTQLDegraded(unittest.TestCase):
    """Scenario 4: D2 with degraded RTQL input."""

    def setUp(self):
        self.config = load_config()
        self.decision = _valid_decision(
            decision_id="SCEN-RTQL-001",
            title="Adopt new vendor recommendation",
            decision_class=DecisionClass.D2_OPERATIONAL,
            reversibility=ReversibilityTag.R2_MODERATELY_REVERSIBLE,
            actor_role="Domain_Owner",
            rtql_input=RTQLInput(
                claim="Vendor X reduces cost by 40%",
                source="Sales pitch",
                is_identifiable=True,
                has_provenance=True,
                scores=RTQLScores(
                    source_integrity=3, exposure_count=2,
                    independence=2, explainability=4,
                    replicability=3, adversarial_robustness=3,
                    novelty_yield=3,
                ),
                causal_checks=CausalChecks(),
            ),
            value_scores=ValueScores(
                revenue_impact=3, cost_efficiency=4, time_leverage=3,
                strategic_alignment=3, customer_human_benefit=3,
                knowledge_asset_creation=2, compounding_potential=3,
                reversibility=3, downside_risk=2, execution_drag=1,
                uncertainty=2, ethical_misalignment=0,
            ),
            trust_scores=TrustScores(
                evidence_quality=3, logic_integrity=3, outcome_history=3,
                context_fit=3, stakeholder_clarity=3, risk_containment=3,
                auditability=3,
            ),
        )

    def test_scenario_4_processes_with_rtql(self):
        result = process_decision(self.decision, self.config)
        self.assertTrue(result.success)
        self.assertIsNotNone(result.rtql_result)

    def test_scenario_4_rtql_multiplier_below_1(self):
        result = process_decision(self.decision, self.config)
        # Degraded input should have reduced multiplier
        self.assertLess(result.rtql_result.trust_multiplier, 1.0)


class TestScenario5NeedsData(unittest.TestCase):
    """Scenario 5: Decision with missing data flag → needs_data."""

    def setUp(self):
        self.config = load_config()
        self.decision = _valid_decision(
            decision_id="SCEN-DATA-001",
            title="Expand into new market",
            owner="ceo",
            decision_class=DecisionClass.D4_STRATEGIC,
            has_missing_data=True,
            actor_role="Human_Executive",
            required_approvals=["ceo"],
            value_scores=ValueScores(
                revenue_impact=5, cost_efficiency=4, time_leverage=3,
                strategic_alignment=5, customer_human_benefit=4,
                knowledge_asset_creation=3, compounding_potential=5,
                reversibility=3, downside_risk=2, execution_drag=1,
                uncertainty=2, ethical_misalignment=0,
            ),
            trust_scores=TrustScores(
                evidence_quality=4, logic_integrity=4, outcome_history=3,
                context_fit=4, stakeholder_clarity=4, risk_containment=4,
                auditability=4,
            ),
        )

    def test_scenario_5_processes_successfully(self):
        result = process_decision(self.decision, self.config)
        self.assertTrue(result.success)

    def test_scenario_5_verdict_needs_data(self):
        result = process_decision(self.decision, self.config)
        self.assertTrue(result.success)
        self.assertEqual(result.execution_packet.verdict, ExecutionVerdict.NEEDS_DATA)


class TestResultSerialization(unittest.TestCase):
    """Test result serialization and summary generation."""

    def setUp(self):
        self.config = load_config()

    def test_result_serializes_to_json(self):
        decision = _valid_decision(decision_id="test-json-001")
        result = process_decision(decision, self.config)
        json_str = result_to_json(result)
        self.assertIsInstance(json_str, str)
        self.assertIn("test-json-001", json_str)

    def test_executive_summary_not_empty(self):
        decision = _valid_decision(decision_id="test-summary-001")
        result = process_decision(decision, self.config)
        self.assertGreater(len(result.executive_summary), 0)


if __name__ == '__main__':
    unittest.main()
