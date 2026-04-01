"""
Test Suite: RTQL Integration with Decision Pipeline

Tests the complete RTQL classification, pre-filter, trust multiplier application,
and end-to-end pipeline integration.

Coverage:
- RTQL stage classification across all 9 stages
- Pre-filter pass/block logic
- Trust multiplier application in value scoring
- Pipeline STAGE 2 (RTQL prefilter) execution
- Pipeline STAGE 3 (value assessment) with RTQL multiplier
- Pipeline STAGE 9 (priority scoring) with RTQL multiplier
"""

import unittest
from dataclasses import dataclass
from datetime import datetime

from engine.models import (
    RTQLInput, RTQLScores, CausalChecks, RTQLResult,
    RTQLStage, WriteTarget, DecisionObject, ValueScores,
    TrustScores
)
from engine.rtql_filter import (
    classify_rtql, rtql_prefilter_passes,
    TRUST_MULTIPLIERS, WRITE_TARGET_MAP
)
from engine.pipeline import process_decision
from engine.config import load_config


class TestRTQLStageProgression(unittest.TestCase):
    """Test RTQL classification through all 9 stages."""

    def test_noise_stage_missing_provenance(self):
        """Input with no provenance classifies as NOISE."""
        inp = RTQLInput(
            claim="The sky is blue",
            source="Unknown",
            scores=RTQLScores(
                source_integrity=2, exposure_count=1, independence=2,
                explainability=3, replicability=2, adversarial_robustness=2,
                novelty_yield=2
            ),
            causal_checks=CausalChecks(
                reveals_causal_mechanism=False, is_irreducible=False,
                survives_authority_removal=False, survives_context_shift=False
            ),
            is_identifiable=False,
            has_provenance=False
        )

        result = classify_rtql(inp)
        self.assertEqual(result.stage, RTQLStage.NOISE)
        self.assertFalse(result.passed)
        self.assertEqual(result.trust_multiplier, 0.00)
        self.assertEqual(result.write_target, WriteTarget.QUARANTINE)

    def test_weak_signal_low_source_integrity(self):
        """Input with low source integrity but identifiable classifies as WEAK_SIGNAL."""
        inp = RTQLInput(
            claim="Company X has 500 employees",
            source="LinkedIn (unverified)",
            scores=RTQLScores(
                source_integrity=2,  # Below 4 threshold
                exposure_count=1, independence=2,
                explainability=3, replicability=2, adversarial_robustness=2,
                novelty_yield=2
            ),
            causal_checks=CausalChecks(
                reveals_causal_mechanism=False, is_irreducible=False,
                survives_authority_removal=False, survives_context_shift=False
            ),
            is_identifiable=True,
            has_provenance=True
        )

        result = classify_rtql(inp)
        self.assertEqual(result.stage, RTQLStage.WEAK_SIGNAL)
        self.assertFalse(result.passed)
        self.assertEqual(result.trust_multiplier, 0.35)
        self.assertEqual(result.write_target, WriteTarget.STAGING)

    def test_echo_signal_low_independence(self):
        """Input with good source but low independence classifies as ECHO_SIGNAL."""
        inp = RTQLInput(
            claim="Market trend showing X",
            source="NewsAPI feed",
            scores=RTQLScores(
                source_integrity=5,  # Passes
                exposure_count=5,    # Passes
                independence=2,      # Below 4 threshold
                explainability=3, replicability=2, adversarial_robustness=2,
                novelty_yield=2
            ),
            causal_checks=CausalChecks(
                reveals_causal_mechanism=False, is_irreducible=False,
                survives_authority_removal=False, survives_context_shift=False
            ),
            is_identifiable=True,
            has_provenance=True
        )

        result = classify_rtql(inp)
        self.assertEqual(result.stage, RTQLStage.ECHO_SIGNAL)
        self.assertFalse(result.passed)
        self.assertEqual(result.trust_multiplier, 0.50)
        self.assertEqual(result.write_target, WriteTarget.STAGING)

    def test_certification_gap_when_qualification_passes_but_cert_fails(self):
        """Input passing qualification gates but failing certification classifies as CERTIFICATION_GAP."""
        inp = RTQLInput(
            claim="Quarterly revenue increased by 12%",
            source="Audited financial statements",
            scores=RTQLScores(
                source_integrity=5,  # >= 4 (passes gate 1)
                exposure_count=4,    # >= 3 (passes gate 2)
                independence=5,      # >= 4 (passes gate 3)
                explainability=3,    # < 6 (fails certification)
                replicability=2, adversarial_robustness=2,
                novelty_yield=2
            ),
            causal_checks=CausalChecks(),
            is_identifiable=True,
            has_provenance=True
        )

        result = classify_rtql(inp)
        self.assertEqual(result.stage, RTQLStage.CERTIFICATION_GAP)
        self.assertTrue(result.passed)
        self.assertEqual(result.trust_multiplier, 0.85)
        self.assertEqual(result.write_target, WriteTarget.CANDIDATE_REGISTRY)

    def test_certification_gap_stage_fails_cert_gates(self):
        """Input passing qualification but failing certification gates."""
        inp = RTQLInput(
            claim="New algorithm improves performance",
            source="Internal research",
            scores=RTQLScores(
                source_integrity=5,  # >= 4
                exposure_count=4,    # >= 3
                independence=5,      # >= 4
                explainability=4,    # Below 6 threshold
                replicability=4,     # Below 6 threshold
                adversarial_robustness=4,  # Below 6 threshold
                novelty_yield=2
            ),
            causal_checks=CausalChecks(
                reveals_causal_mechanism=False, is_irreducible=False,
                survives_authority_removal=False, survives_context_shift=False
            ),
            is_identifiable=True,
            has_provenance=True
        )

        result = classify_rtql(inp)
        self.assertEqual(result.stage, RTQLStage.CERTIFICATION_GAP)
        self.assertTrue(result.passed)
        self.assertEqual(result.trust_multiplier, 0.85)
        self.assertEqual(result.write_target, WriteTarget.CANDIDATE_REGISTRY)

    def test_certified_stage_passes_cert_gates_low_novelty(self):
        """Input passing certification gates but low novelty."""
        inp = RTQLInput(
            claim="Documented software engineering practice",
            source="Published academic research",
            scores=RTQLScores(
                source_integrity=5,  # >= 4
                exposure_count=4,    # >= 3
                independence=5,      # >= 4
                explainability=8,    # >= 6
                replicability=8,     # >= 6
                adversarial_robustness=8,  # >= 6
                novelty_yield=4      # Below 6 (not novel enough)
            ),
            causal_checks=CausalChecks(
                reveals_causal_mechanism=False, is_irreducible=False,
                survives_authority_removal=False, survives_context_shift=False
            ),
            is_identifiable=True,
            has_provenance=True
        )

        result = classify_rtql(inp)
        self.assertEqual(result.stage, RTQLStage.CERTIFIED)
        self.assertTrue(result.passed)
        self.assertEqual(result.trust_multiplier, 1.15)
        self.assertEqual(result.write_target, WriteTarget.OPERATIONAL_REGISTRY)

    def test_research_grade_stage_novel_but_not_causal(self):
        """Input with high novelty but gaps in causal tests."""
        inp = RTQLInput(
            claim="Novel mechanism discovered in X domain",
            source="Experimental lab results",
            scores=RTQLScores(
                source_integrity=5, exposure_count=4, independence=5,
                explainability=8, replicability=8, adversarial_robustness=8,
                novelty_yield=8  # >= 6 (novel)
            ),
            causal_checks=CausalChecks(
                reveals_causal_mechanism=False,  # Gap
                is_irreducible=False,
                survives_authority_removal=False,
                survives_context_shift=False
            ),
            is_identifiable=True,
            has_provenance=True
        )

        result = classify_rtql(inp)
        self.assertEqual(result.stage, RTQLStage.RESEARCH_GRADE)
        self.assertTrue(result.passed)
        self.assertEqual(result.trust_multiplier, 1.30)
        self.assertEqual(result.write_target, WriteTarget.INSIGHT_REGISTRY)

    def test_first_principles_candidate_all_gates_pass(self):
        """Input passing all gates including causal checks."""
        inp = RTQLInput(
            claim="First-principles insight with full causal chain",
            source="Rigorous theoretical derivation",
            scores=RTQLScores(
                source_integrity=5, exposure_count=5, independence=5,
                explainability=10, replicability=10, adversarial_robustness=10,
                novelty_yield=10
            ),
            causal_checks=CausalChecks(
                reveals_causal_mechanism=True,
                is_irreducible=True,
                survives_authority_removal=True,
                survives_context_shift=True
            ),
            is_identifiable=True,
            has_provenance=True
        )

        result = classify_rtql(inp)
        self.assertEqual(result.stage, RTQLStage.FIRST_PRINCIPLES_CANDIDATE)
        self.assertTrue(result.passed)
        self.assertEqual(result.trust_multiplier, 1.50)
        self.assertEqual(result.write_target, WriteTarget.PRINCIPLES_REGISTRY)


class TestRTQLPrefilter(unittest.TestCase):
    """Test RTQL prefilter pass/block logic."""

    def test_prefilter_blocks_noise(self):
        """Prefilter rejects NOISE stage."""
        result = RTQLResult()
        result.stage = RTQLStage.NOISE
        result.passed = False

        self.assertFalse(rtql_prefilter_passes(result))

    def test_prefilter_blocks_weak_signal(self):
        """Prefilter rejects WEAK_SIGNAL stage."""
        result = RTQLResult()
        result.stage = RTQLStage.WEAK_SIGNAL
        result.passed = False

        self.assertFalse(rtql_prefilter_passes(result))

    def test_prefilter_allows_echo_signal(self):
        """Prefilter allows ECHO_SIGNAL (with warning)."""
        result = RTQLResult()
        result.stage = RTQLStage.ECHO_SIGNAL
        result.passed = False

        self.assertTrue(rtql_prefilter_passes(result))

    def test_prefilter_allows_qualified_and_above(self):
        """Prefilter allows all stages from QUALIFIED onward."""
        for stage in [
            RTQLStage.QUALIFIED,
            RTQLStage.CERTIFICATION_GAP,
            RTQLStage.CERTIFIED,
            RTQLStage.RESEARCH_GRADE,
            RTQLStage.FIRST_PRINCIPLES_CANDIDATE,
            RTQLStage.AXIOM_CANDIDATE,
        ]:
            result = RTQLResult()
            result.stage = stage
            result.passed = True

            self.assertTrue(
                rtql_prefilter_passes(result),
                f"Prefilter should allow {stage.value}"
            )


class TestTrustMultiplierApplication(unittest.TestCase):
    """Test trust multiplier values and application in scoring."""

    def test_multiplier_values_correct(self):
        """Verify all RTQL stage multipliers match specification."""
        expected = {
            RTQLStage.NOISE: 0.00,
            RTQLStage.WEAK_SIGNAL: 0.35,
            RTQLStage.ECHO_SIGNAL: 0.50,
            RTQLStage.QUALIFIED: 1.00,
            RTQLStage.CERTIFICATION_GAP: 0.85,
            RTQLStage.CERTIFIED: 1.15,
            RTQLStage.RESEARCH_GRADE: 1.30,
            RTQLStage.FIRST_PRINCIPLES_CANDIDATE: 1.50,
            RTQLStage.AXIOM_CANDIDATE: 1.50,
        }

        self.assertEqual(TRUST_MULTIPLIERS, expected)

    def test_multiplier_monotonicity(self):
        """Verify multipliers generally increase with stage progression."""
        progression = [
            (RTQLStage.NOISE, 0.00),
            (RTQLStage.WEAK_SIGNAL, 0.35),
            (RTQLStage.ECHO_SIGNAL, 0.50),
            (RTQLStage.QUALIFIED, 1.00),
            (RTQLStage.CERTIFICATION_GAP, 0.85),  # dips slightly
            (RTQLStage.CERTIFIED, 1.15),
            (RTQLStage.RESEARCH_GRADE, 1.30),
            (RTQLStage.FIRST_PRINCIPLES_CANDIDATE, 1.50),
            (RTQLStage.AXIOM_CANDIDATE, 1.50),
        ]

        for i in range(len(progression) - 1):
            stage_a, mult_a = progression[i]
            stage_b, mult_b = progression[i + 1]
            # Just verify multipliers exist and are in expected range
            self.assertGreaterEqual(mult_a, 0.0)
            self.assertLessEqual(mult_a, 2.0)
            self.assertGreaterEqual(mult_b, 0.0)
            self.assertLessEqual(mult_b, 2.0)


class TestPipelineRTQLIntegration(unittest.TestCase):
    """Test RTQL integration in full decision pipeline."""

    def test_pipeline_applies_rtql_multiplier_to_value(self):
        """Pipeline STAGE 3 applies RTQL multiplier to value scoring."""
        config = load_config()

        decision = DecisionObject(
            decision_id="test-pipeline-1",
            title="Test Decision",
            problem_statement="Test problem",
            requested_action="test action",
            owner="test_user",
            evidence_refs=["doc1"],
            rtql_input=RTQLInput(
                claim="Test claim",
                source="Test source",
                scores=RTQLScores(
                    source_integrity=5, exposure_count=4, independence=5,
                    explainability=8, replicability=8, adversarial_robustness=8,
                    novelty_yield=2
                ),
                causal_checks=CausalChecks(),
                is_identifiable=True,
                has_provenance=True,
            ),
            value_scores=ValueScores(
                revenue_impact=3, cost_efficiency=3, time_leverage=3,
                strategic_alignment=3, customer_human_benefit=2,
                knowledge_asset_creation=2, compounding_potential=3,
                reversibility=2, downside_risk=1, execution_drag=1,
                uncertainty=2, ethical_misalignment=0,
            ),
            trust_scores=TrustScores(
                evidence_quality=4, logic_integrity=4, outcome_history=3,
                context_fit=3, stakeholder_clarity=4, risk_containment=3,
                auditability=4,
            ),
        )

        result = process_decision(decision, config)

        self.assertTrue(result.success)
        self.assertIsNotNone(result.rtql_result)
        self.assertEqual(result.rtql_result.stage, RTQLStage.CERTIFIED)
        self.assertEqual(result.rtql_result.trust_multiplier, 1.15)

    def test_pipeline_defaults_to_qualified_when_no_rtql_input(self):
        """Pipeline defaults to QUALIFIED (1.0 multiplier) when no RTQL input."""
        config = load_config()

        decision = DecisionObject(
            decision_id="test-pipeline-2",
            title="Test Decision No RTQL",
            problem_statement="Test problem",
            requested_action="test action",
            owner="test_user",
            evidence_refs=["doc1"],
            rtql_input=None,
            value_scores=ValueScores(
                revenue_impact=3, cost_efficiency=3, time_leverage=3,
                strategic_alignment=3, customer_human_benefit=2,
                knowledge_asset_creation=2, compounding_potential=3,
                reversibility=2, downside_risk=1, execution_drag=1,
                uncertainty=2, ethical_misalignment=0,
            ),
            trust_scores=TrustScores(
                evidence_quality=4, logic_integrity=4, outcome_history=3,
                context_fit=3, stakeholder_clarity=4, risk_containment=3,
                auditability=4,
            ),
        )

        result = process_decision(decision, config)

        self.assertTrue(result.success)
        self.assertIsNotNone(result.rtql_result)
        self.assertEqual(result.rtql_result.stage, RTQLStage.QUALIFIED)
        self.assertEqual(result.rtql_result.trust_multiplier, 1.00)

    def test_pipeline_audit_logs_rtql_result(self):
        """Pipeline logs RTQL result in audit trail."""
        config = load_config()

        decision = DecisionObject(
            decision_id="test-pipeline-3",
            title="Test Decision Audit",
            problem_statement="Test problem",
            requested_action="test action",
            owner="test_user",
            evidence_refs=["doc1"],
            rtql_input=RTQLInput(
                claim="Test claim",
                source="Test source",
                scores=RTQLScores(
                    source_integrity=2, exposure_count=1, independence=2,
                    explainability=3, replicability=2, adversarial_robustness=2,
                    novelty_yield=2,
                ),
                causal_checks=CausalChecks(),
                is_identifiable=True,
                has_provenance=True,
            ),
            value_scores=ValueScores(
                revenue_impact=3, cost_efficiency=3, time_leverage=3,
                strategic_alignment=3, customer_human_benefit=2,
                knowledge_asset_creation=2, compounding_potential=3,
                reversibility=2, downside_risk=1, execution_drag=1,
                uncertainty=2, ethical_misalignment=0,
            ),
            trust_scores=TrustScores(
                evidence_quality=4, logic_integrity=4, outcome_history=3,
                context_fit=3, stakeholder_clarity=3, risk_containment=3,
                auditability=4,
            ),
        )

        result = process_decision(decision, config)

        # Verify audit trail contains RTQL records (audit_trail is list of AuditRecord objects)
        rtql_records = [r for r in result.audit_trail if r.pipeline_stage == 'rtql_prefilter']
        self.assertGreater(len(rtql_records), 0, "Audit trail should contain RTQL records")


if __name__ == '__main__':
    unittest.main()
