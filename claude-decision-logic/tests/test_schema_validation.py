"""
Test Suite: Schema Alignment Validation

Verifies that the decision_schema.yaml accurately reflects the DecisionObject
model and that all required/optional fields are correctly documented.
"""

import sys
from engine.models import (
    DecisionObject, ValueScores, TrustScores, RTQLScores,
    DecisionClass, TimeHorizon, ReversibilityTag
)
from dataclasses import fields


def test_decision_object_required_fields():
    """Verify DecisionObject has all fields documented in schema."""
    print("\n=== Test: DecisionObject Required Fields ===")
    
    # Fields that DecisionObject validates as required
    required_fields = {
        'title': str,
        'owner': str,
        'problem_statement': str,
        'requested_action': str,
        'evidence_refs': list,
        'value_scores': ValueScores,
        'trust_scores': TrustScores,
    }
    
    # Get actual fields from dataclass
    actual_fields = {f.name: f.type for f in fields(DecisionObject)}
    
    for field_name, field_type in required_fields.items():
        if field_name in actual_fields:
            print(f"  ✓ {field_name}: {actual_fields[field_name].__name__}")
        else:
            print(f"  ✗ MISSING: {field_name}")
            return False
    
    return True


def test_value_scores_dimensions():
    """Verify ValueScores has all documented dimensions."""
    print("\n=== Test: ValueScores Dimensions ===")
    
    # Positive dimensions (should be 8)
    positive = [
        'revenue_impact', 'cost_efficiency', 'time_leverage', 
        'strategic_alignment', 'customer_human_benefit', 
        'knowledge_asset_creation', 'compounding_potential', 'reversibility'
    ]
    
    # Penalty dimensions (should be 4)
    penalty = [
        'downside_risk', 'execution_drag', 'uncertainty', 'ethical_misalignment'
    ]
    
    vs = ValueScores()
    for dim in positive:
        if hasattr(vs, dim):
            print(f"  ✓ positive: {dim}")
        else:
            print(f"  ✗ MISSING positive: {dim}")
            return False
    
    for dim in penalty:
        if hasattr(vs, dim):
            print(f"  ✓ penalty: {dim}")
        else:
            print(f"  ✗ MISSING penalty: {dim}")
            return False
    
    return True


def test_trust_scores_dimensions():
    """Verify TrustScores has all 7 documented dimensions."""
    print("\n=== Test: TrustScores Dimensions ===")
    
    dimensions = [
        'evidence_quality', 'logic_integrity', 'outcome_history',
        'context_fit', 'stakeholder_clarity', 'risk_containment', 'auditability'
    ]
    
    ts = TrustScores()
    for dim in dimensions:
        if hasattr(ts, dim):
            print(f"  ✓ {dim}")
        else:
            print(f"  ✗ MISSING: {dim}")
            return False
    
    return True


def test_rtql_scores_dimensions():
    """Verify RTQLScores has all 7 documented dimensions."""
    print("\n=== Test: RTQLScores Dimensions ===")
    
    dimensions = [
        'source_integrity', 'exposure_count', 'independence',
        'explainability', 'replicability', 'adversarial_robustness', 'novelty_yield'
    ]
    
    rs = RTQLScores()
    for dim in dimensions:
        if hasattr(rs, dim):
            print(f"  ✓ {dim}")
        else:
            print(f"  ✗ MISSING: {dim}")
            return False
    
    return True


def test_decision_class_enum():
    """Verify DecisionClass has all documented values."""
    print("\n=== Test: DecisionClass Enum ===")
    
    expected = {
        'D0': 'D0_INFORMATIONAL',
        'D1': 'D1_REVERSIBLE_TACTICAL',
        'D2': 'D2_OPERATIONAL',
        'D3': 'D3_FINANCIAL',
        'D4': 'D4_STRATEGIC',
        'D5': 'D5_LEGAL_ETHICAL',
        'D6': 'D6_IRREVERSIBLE_HIGH_BLAST',
    }
    
    for prefix, name in expected.items():
        try:
            _ = DecisionClass[name]
            print(f"  ✓ {name}")
        except KeyError:
            print(f"  ✗ MISSING: {name}")
            return False
    
    return True


def test_time_horizon_enum():
    """Verify TimeHorizon has all documented values."""
    print("\n=== Test: TimeHorizon Enum ===")
    
    expected = ['IMMEDIATE', 'NEAR_TERM', 'MID_TERM', 'LONG_TERM']
    
    for th in expected:
        try:
            _ = TimeHorizon[th]
            print(f"  ✓ {th}")
        except KeyError:
            print(f"  ✗ MISSING: {th}")
            return False
    
    return True


def test_reversibility_enum():
    """Verify ReversibilityTag has all documented values."""
    print("\n=== Test: ReversibilityTag Enum ===")
    
    expected = ['R1_EASILY_REVERSIBLE', 'R2_MODERATELY_REVERSIBLE', 
                'R3_COSTLY_TO_REVERSE', 'R4_EFFECTIVELY_IRREVERSIBLE']
    
    for tag in expected:
        try:
            _ = ReversibilityTag[tag]
            print(f"  ✓ {tag}")
        except KeyError:
            print(f"  ✗ MISSING: {tag}")
            return False
    
    return True


def test_decision_object_validation():
    """Verify DecisionObject validation logic matches schema."""
    print("\n=== Test: DecisionObject Validation ===")
    
    # Create minimal valid decision
    decision = DecisionObject(
        title="Test Decision",
        owner="test-owner",
        problem_statement="Solve test problem",
        requested_action="Execute test action",
        evidence_refs=["ref-1"],
        value_scores=ValueScores(
            revenue_impact=3, cost_efficiency=3, time_leverage=3,
            strategic_alignment=3, customer_human_benefit=2,
            knowledge_asset_creation=2, compounding_potential=2, reversibility=3
        ),
        trust_scores=TrustScores(
            evidence_quality=3, logic_integrity=3, outcome_history=3,
            context_fit=3, stakeholder_clarity=3, 
            risk_containment=3, auditability=3
        )
    )
    
    errors = decision.validate()
    if not errors:
        print("  ✓ Minimal valid decision passes validation")
        return True
    else:
        print(f"  ✗ Validation failed: {errors}")
        return False


def test_schema_alignment_summary():
    """Summary of schema alignment status."""
    print("\n" + "="*60)
    print("SCHEMA ALIGNMENT SUMMARY")
    print("="*60)
    
    tests = [
        ("DecisionObject Required Fields", test_decision_object_required_fields),
        ("ValueScores Dimensions", test_value_scores_dimensions),
        ("TrustScores Dimensions", test_trust_scores_dimensions),
        ("RTQLScores Dimensions", test_rtql_scores_dimensions),
        ("DecisionClass Enum", test_decision_class_enum),
        ("TimeHorizon Enum", test_time_horizon_enum),
        ("ReversibilityTag Enum", test_reversibility_enum),
        ("DecisionObject Validation", test_decision_object_validation),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n✗ Test failed with exception: {e}")
            results[test_name] = False
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    return all(results.values())


if __name__ == "__main__":
    success = test_schema_alignment_summary()
    sys.exit(0 if success else 1)
