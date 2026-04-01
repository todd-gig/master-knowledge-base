"""
Test Suite: Audit Logging and Gap Analysis

Tests for:
- audit.AuditLogger: audit record creation and logging
- audit.serialize_pipeline_result: result serialization to JSON
- audit.generate_executive_summary: human-readable summary generation
- gap_analysis.calculate_gap: gap scoring with trust penalties
- gap_analysis.calculate_priority: priority formula evaluation
- gap_analysis.analyze_gaps: batch gap analysis
- gap_analysis.generate_action_items: action item generation

Run: python -m unittest tests.test_audit_and_gap_analysis -v
"""

import unittest
from datetime import datetime

from engine.models import (
    DecisionObject, DecisionClass, ValueScores, TrustScores,
    AlignmentScores, RTQLResult, RTQLStage, WriteTarget,
    PipelineResult, AuditRecord, CertificateChain, ExecutionPacket,
    ExecutionVerdict, TrustTier
)
from engine.audit import (
    AuditLogger, serialize_pipeline_result, result_to_json,
    generate_executive_summary
)
from engine.gap_analysis import (
    calculate_gap, calculate_priority, analyze_gaps, generate_action_items
)


class TestAuditLogger(unittest.TestCase):
    """Test AuditLogger record creation."""

    def test_logger_creation(self):
        logger = AuditLogger("DEC-TEST")
        self.assertEqual(logger.decision_id, "DEC-TEST")
        self.assertEqual(len(logger.records), 0)

    def test_log_creates_record(self):
        logger = AuditLogger("DEC-TEST")
        record = logger.log(stage="test", action="test_action", notes="test note")
        self.assertEqual(len(logger.records), 1)
        self.assertEqual(record.pipeline_stage, "test")
        self.assertEqual(record.action_taken, "test_action")

    def test_log_validation(self):
        logger = AuditLogger("DEC-TEST")
        record = logger.log_validation(["error1", "error2"])
        self.assertEqual(record.pipeline_stage, "validation")
        self.assertIn("2 errors", record.notes)

    def test_log_validation_pass(self):
        logger = AuditLogger("DEC-TEST")
        record = logger.log_validation([])
        self.assertIn("Passed", record.notes)

    def test_log_rtql(self):
        logger = AuditLogger("DEC-TEST")
        rtql = RTQLResult(
            stage=RTQLStage.CERTIFIED,
            trust_multiplier=1.15,
            write_target=WriteTarget.OPERATIONAL_REGISTRY,
            passed=True,
        )
        record = logger.log_rtql(rtql)
        self.assertEqual(record.pipeline_stage, "rtql_prefilter")
        self.assertIn("certified", record.notes)

    def test_log_value_assessment(self):
        logger = AuditLogger("DEC-TEST")
        record = logger.log_value_assessment(24, 4, 20, "strong_candidate")
        self.assertEqual(record.pipeline_stage, "value_assessment")
        self.assertIn("20", record.notes)

    def test_log_trust_assessment(self):
        logger = AuditLogger("DEC-TEST")
        record = logger.log_trust_assessment(TrustTier.T3_CERTIFIED, 28, [])
        self.assertEqual(record.pipeline_stage, "trust_assessment")
        self.assertIn("T3", record.notes)

    def test_log_alignment(self):
        logger = AuditLogger("DEC-TEST")
        alignment = AlignmentScores(
            doctrine_alignment=0.8, ethos_alignment=0.9,
            first_principles_alignment=0.85,
        )
        record = logger.log_alignment(alignment)
        self.assertEqual(record.pipeline_stage, "alignment_check")

    def test_log_certificate_chain(self):
        logger = AuditLogger("DEC-TEST")
        chain = CertificateChain()
        record = logger.log_certificate_chain(chain)
        self.assertEqual(record.pipeline_stage, "certification")
        self.assertIn("False", record.notes)  # chain_complete is False

    def test_log_execution(self):
        logger = AuditLogger("DEC-TEST")
        packet = ExecutionPacket(
            decision_id="DEC-TEST",
            verdict=ExecutionVerdict.AUTO_EXECUTE,
        )
        record = logger.log_execution(packet)
        self.assertEqual(record.pipeline_stage, "execution_authorization")
        self.assertIn("auto_execute", record.notes)

    def test_log_priority_score(self):
        logger = AuditLogger("DEC-TEST")
        record = logger.log_priority_score(42.5)
        self.assertEqual(record.pipeline_stage, "priority_scoring")
        self.assertIn("42.5", record.notes)


class TestSerializePipelineResult(unittest.TestCase):
    """Test PipelineResult serialization."""

    def test_serialize_minimal_result(self):
        result = PipelineResult(decision_id="DEC-TEST", success=False)
        serialized = serialize_pipeline_result(result)
        self.assertEqual(serialized["decision_id"], "DEC-TEST")
        self.assertFalse(serialized["success"])

    def test_serialize_complete_result(self):
        result = PipelineResult(
            decision_id="DEC-TEST",
            success=True,
            net_value_score=20,
            trust_tier=TrustTier.T3_CERTIFIED,
            trust_total=28,
            alignment_composite=0.85,
            value_classification="strong_candidate",
            priority_score=42.0,
        )
        serialized = serialize_pipeline_result(result)
        self.assertEqual(serialized["trust_tier"], "T3")
        self.assertEqual(serialized["net_value_score"], 20)

    def test_result_to_json_produces_string(self):
        result = PipelineResult(decision_id="DEC-TEST", success=True)
        json_str = result_to_json(result)
        self.assertIsInstance(json_str, str)
        self.assertIn("DEC-TEST", json_str)


class TestGenerateExecutiveSummary(unittest.TestCase):
    """Test executive summary generation."""

    def test_summary_for_failed_result(self):
        result = PipelineResult(
            decision_id="DEC-TEST",
            success=False,
            validation_errors=["title is required"],
        )
        summary = generate_executive_summary(result)
        self.assertIn("FAILED", summary)
        self.assertIn("title is required", summary)

    def test_summary_for_successful_result(self):
        result = PipelineResult(
            decision_id="DEC-TEST",
            success=True,
            net_value_score=20,
            trust_tier=TrustTier.T3_CERTIFIED,
            trust_total=28,
            value_classification="strong_candidate",
            alignment_composite=0.85,
            priority_score=42.0,
        )
        summary = generate_executive_summary(result)
        self.assertIn("PROCESSED", summary)
        self.assertIn("T3", summary)


class TestGapAnalysis(unittest.TestCase):
    """Test gap analysis functions."""

    def test_calculate_gap_basic(self):
        from engine.models import RTQLStage
        gap_score, _, _ = calculate_gap(2.0, 5.0, 1.0, RTQLStage.QUALIFIED)
        self.assertGreater(gap_score, 0)

    def test_calculate_gap_no_gap(self):
        from engine.models import RTQLStage
        gap_score, _, _ = calculate_gap(5.0, 5.0, 1.0, RTQLStage.QUALIFIED)
        self.assertEqual(gap_score, 0)

    def test_calculate_priority(self):
        priority = calculate_priority(
            gap_score=3.0, leverage_score=4.0,
            urgency_score=3.0, value_matrix_impact=0.8,
        )
        self.assertGreater(priority, 0)

    def test_analyze_gaps_produces_results(self):
        items = [
            {
                "category": "value", "variable": "revenue_impact",
                "actual_score": 2, "target_score": 5,
                "strategic_importance": 1.0, "rtql_stage": "qualified",
                "leverage_score": 3.0, "urgency_score": 2.0,
                "value_matrix_impact": 0.6,
            },
            {
                "category": "trust", "variable": "evidence_quality",
                "actual_score": 3, "target_score": 5,
                "strategic_importance": 1.0, "rtql_stage": "qualified",
                "leverage_score": 4.0, "urgency_score": 3.0,
                "value_matrix_impact": 0.8,
            },
        ]
        gaps = analyze_gaps(items)
        self.assertGreater(len(gaps), 0)

    def test_generate_action_items(self):
        items = [
            {
                "category": "value", "variable": "revenue_impact",
                "actual_score": 1, "target_score": 5,
                "strategic_importance": 1.0, "rtql_stage": "qualified",
                "leverage_score": 3.0, "urgency_score": 4.0,
                "value_matrix_impact": 0.8,
            },
        ]
        gaps = analyze_gaps(items)
        actions = generate_action_items(gaps)
        self.assertIsInstance(actions, list)


if __name__ == '__main__':
    unittest.main()
