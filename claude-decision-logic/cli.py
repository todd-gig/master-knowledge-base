#!/usr/bin/env python3
"""
Decision Engine CLI — Process decision payloads from JSON files

Usage:
    python cli.py evaluate <json_file>        # Run full pipeline
    python cli.py validate <json_file>        # Validate payload only
    python cli.py score <json_file>           # Compute scores only
    python cli.py gaps <json_file>            # Gap analysis on survey input
    python cli.py demo                        # Run 5 built-in scenarios

Exit codes:
    0 = success
    1 = validation failure
    2 = runtime error
"""

import sys
import os
import argparse
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engine.pipeline import process_decision
from engine.config import load_config
from engine.gap_analysis import analyze_gaps, generate_action_items
from engine.runner import (
    scenario_1_d1_auto_execute,
    scenario_2_d3_financial_escalate,
    scenario_3_d6_blocked,
    scenario_4_rtql_degraded,
    scenario_5_needs_data,
)

from converters import (
    payload_to_decision,
    load_payload_from_file,
    save_result_to_file,
)


def print_header(text: str):
    """Print a formatted section header."""
    print(f"\n{'='*72}")
    print(f"  {text}")
    print(f"{'='*72}\n")


def print_success(text: str):
    """Print a success message."""
    print(f"✓ {text}")


def print_error(text: str):
    """Print an error message."""
    print(f"✗ {text}")


def cmd_evaluate(args) -> int:
    """
    Evaluate command: Run full pipeline on a decision JSON payload.

    Output:
    - Human-readable executive summary to stdout
    - Full JSON result to --output file if specified
    """
    # Load payload from file
    payload, load_error = load_payload_from_file(args.json_file)
    if load_error:
        print_error(f"Failed to load {args.json_file}: {load_error}")
        return 2

    # Convert payload to DecisionObject
    decision, conversion_errors = payload_to_decision(payload)
    if conversion_errors:
        print_error("Payload conversion failed:")
        for err in conversion_errors:
            print(f"  - {err}")
        return 1

    # Load config and run pipeline
    try:
        config = load_config()
        result = process_decision(decision, config)
    except Exception as e:
        print_error(f"Pipeline execution failed: {str(e)}")
        return 2

    # Output: executive summary to stdout
    print(result.executive_summary)

    # Output: full JSON to file if requested
    if args.output:
        save_error = save_result_to_file(args.output, result)
        if save_error:
            print_error(f"Failed to save result to {args.output}: {save_error}")
            return 2
        print_success(f"Full result saved to {args.output}")

    # Return exit code based on success
    return 0 if result.success else 1


def cmd_validate(args) -> int:
    """
    Validate command: Validate a decision payload without running pipeline.

    Output:
    - Validation status to stdout
    - Full validation errors if any
    """
    # Load payload
    payload, load_error = load_payload_from_file(args.json_file)
    if load_error:
        print_error(f"Failed to load {args.json_file}: {load_error}")
        return 2

    # Convert to DecisionObject (validates structure)
    decision, conversion_errors = payload_to_decision(payload)
    if conversion_errors:
        print("VALIDATION FAILED")
        for err in conversion_errors:
            print(f"  - {err}")
        return 1

    # Validate DecisionObject (check required fields, value ranges)
    validation_errors = decision.validate()
    if validation_errors:
        print("VALIDATION FAILED")
        for err in validation_errors:
            print(f"  - {err}")
        return 1

    # Success
    print_success("Validation passed")
    print(f"  Decision ID: {decision.decision_id}")
    print(f"  Title: {decision.title}")
    print(f"  Class: {decision.decision_class.value}")
    print(f"  Owner: {decision.owner}")
    return 0


def cmd_score(args) -> int:
    """
    Score command: Compute value/trust/priority scores only.

    Output:
    - Score summary to stdout
    - Optional full JSON to --output file
    """
    # Load and convert payload
    payload, load_error = load_payload_from_file(args.json_file)
    if load_error:
        print_error(f"Failed to load {args.json_file}: {load_error}")
        return 2

    decision, conversion_errors = payload_to_decision(payload)
    if conversion_errors:
        print_error("Payload conversion failed:")
        for err in conversion_errors:
            print(f"  - {err}")
        return 1

    # Validate
    validation_errors = decision.validate()
    if validation_errors:
        print_error("Validation failed:")
        for err in validation_errors:
            print(f"  - {err}")
        return 1

    # Run full pipeline to get scores
    try:
        config = load_config()
        result = process_decision(decision, config)
    except Exception as e:
        print_error(f"Pipeline execution failed: {str(e)}")
        return 2

    # Output: Score summary
    print("SCORE SUMMARY")
    print(f"  Value Score: {result.net_value_score} ({result.value_classification})")
    print(f"  Trust Tier: {result.trust_tier.value} (total: {result.trust_total})")
    print(f"  Alignment Composite: {result.alignment_composite:.3f}")
    print(f"  Priority Score: {result.priority_score:.3f}")

    if result.rtql_result:
        print(f"  RTQL Stage: {result.rtql_result.stage.value}")

    # Save full result if requested
    if args.output:
        save_error = save_result_to_file(args.output, result)
        if save_error:
            print_error(f"Failed to save result to {args.output}: {save_error}")
            return 2
        print_success(f"Full result saved to {args.output}")

    return 0


def cmd_gaps(args) -> int:
    """
    Gaps command: Run gap analysis on survey-style input.

    Expects a JSON file with gap_analysis_input structure.
    Output:
    - Gap analysis summary to stdout
    - Optional full JSON to --output file
    """
    # Load payload
    payload, load_error = load_payload_from_file(args.json_file)
    if load_error:
        print_error(f"Failed to load {args.json_file}: {load_error}")
        return 2

    try:
        # Attempt to parse as gap analysis input
        # This is a simpler format — just a list of gap items
        gap_input_data = payload.get("gap_analysis_input", [])

        # Run gap analysis
        gaps = analyze_gaps(gap_input_data)
        actions = generate_action_items(gaps, min_severity="moderate")

        # Output: Gap summary
        print("GAP ANALYSIS RESULTS")
        print(f"Total Gaps Found: {len(gaps)}")

        # Group by severity
        by_severity = {}
        for gap in gaps:
            severity = gap.gap_severity_label
            if severity not in by_severity:
                by_severity[severity] = []
            by_severity[severity].append(gap)

        for severity in ["critical", "major", "moderate", "minor"]:
            if severity in by_severity:
                items = by_severity[severity]
                print(f"\n{severity.upper()} ({len(items)}):")
                for gap in items:
                    print(f"  - {gap.category}/{gap.variable}")
                    print(f"    Score: {gap.actual_score} → {gap.target_score}")
                    print(f"    Priority: {gap.priority_score:.2f}")

        # Save full result if requested
        if args.output:
            output_data = {
                "total_gaps": len(gaps),
                "gaps": [
                    {
                        "category": g.category,
                        "variable": g.variable,
                        "actual_score": g.actual_score,
                        "target_score": g.target_score,
                        "gap_score": g.gap_score,
                        "gap_severity": g.gap_severity_label,
                        "priority_score": g.priority_score,
                    }
                    for g in gaps
                ],
                "actions": [
                    {
                        "category": a.category,
                        "variable": a.variable,
                        "current_score": a.current_score,
                        "target_score": a.target_score,
                        "gap_severity": a.gap_severity_label,
                    }
                    for a in actions
                ],
            }
            try:
                with open(args.output, 'w') as f:
                    json.dump(output_data, f, indent=2)
                print_success(f"Gap analysis saved to {args.output}")
            except Exception as e:
                print_error(f"Failed to save to {args.output}: {str(e)}")
                return 2

        return 0

    except Exception as e:
        print_error(f"Gap analysis failed: {str(e)}")
        return 2


def cmd_demo(args) -> int:
    """
    Demo command: Run 5 built-in scenarios and show results.

    Demonstrates the full pipeline with realistic decision scenarios.
    """
    print_header("DECISION ENGINE DEMO — 5 Test Scenarios")

    config = load_config()
    results = []

    try:
        # Scenario 1: D1 Auto-Execute
        print_header("Scenario 1: D1 Reversible Tactical → Auto-Execute")
        result1 = scenario_1_d1_auto_execute(config)
        results.append(("D1 Auto-Execute", result1))

        # Scenario 2: D3 Financial Escalation
        print_header("Scenario 2: D3 Financial → Escalate Tier 2")
        result2 = scenario_2_d3_financial_escalate(config)
        results.append(("D3 Financial", result2))

        # Scenario 3: D6 Blocked
        print_header("Scenario 3: D6 High-Blast → Blocked")
        result3 = scenario_3_d6_blocked(config)
        results.append(("D6 Blocked", result3))

        # Scenario 4: RTQL Degraded
        print_header("Scenario 4: RTQL-Degraded Processing")
        result4 = scenario_4_rtql_degraded(config)
        results.append(("RTQL Degraded", result4))

        # Scenario 5: Needs Data
        print_header("Scenario 5: Needs Data → Escalate")
        result5 = scenario_5_needs_data(config)
        results.append(("Needs Data", result5))

    except Exception as e:
        print_error(f"Demo execution failed: {str(e)}")
        return 2

    # Summary table
    print_header("DEMO SUMMARY")
    print(f"{'Scenario':<25} {'Status':<12} {'Verdict':<20}")
    print("-" * 57)
    for scenario_name, result in results:
        status = "PASS" if result.success else "FAIL"
        verdict = result.execution_packet.verdict.value if result.execution_packet else "none"
        print(f"{scenario_name:<25} {status:<12} {verdict:<20}")

    # Save all results if requested
    if args.output:
        try:
            output_data = {
                "demo_run": True,
                "scenarios": [
                    {
                        "name": name,
                        "decision_id": result.decision_id,
                        "success": result.success,
                        "execution_verdict": result.execution_packet.verdict.value if result.execution_packet else None,
                    }
                    for name, result in results
                ],
            }
            with open(args.output, 'w') as f:
                json.dump(output_data, f, indent=2)
            print_success(f"Demo results summary saved to {args.output}")
        except Exception as e:
            print_error(f"Failed to save to {args.output}: {str(e)}")
            return 2

    return 0


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Decision Engine CLI — Process decision payloads from JSON files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py evaluate decision.json
  python cli.py validate decision.json
  python cli.py score decision.json --output result.json
  python cli.py gaps gaps_input.json --output gaps_result.json
  python cli.py demo

Exit Codes:
  0 = success
  1 = validation failure
  2 = runtime error
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # evaluate command
    evaluate_parser = subparsers.add_parser("evaluate", help="Run full pipeline on JSON payload")
    evaluate_parser.add_argument("json_file", help="Path to decision JSON file")
    evaluate_parser.add_argument("--output", "-o", help="Save full result to JSON file")

    # validate command
    validate_parser = subparsers.add_parser("validate", help="Validate JSON payload without running pipeline")
    validate_parser.add_argument("json_file", help="Path to decision JSON file")

    # score command
    score_parser = subparsers.add_parser("score", help="Compute value/trust/priority scores only")
    score_parser.add_argument("json_file", help="Path to decision JSON file")
    score_parser.add_argument("--output", "-o", help="Save full result to JSON file")

    # gaps command
    gaps_parser = subparsers.add_parser("gaps", help="Run gap analysis on survey-style input")
    gaps_parser.add_argument("json_file", help="Path to gap analysis JSON file")
    gaps_parser.add_argument("--output", "-o", help="Save gap analysis results to JSON file")

    # demo command
    demo_parser = subparsers.add_parser("demo", help="Run 5 built-in test scenarios")
    demo_parser.add_argument("--output", "-o", help="Save demo results summary to JSON file")

    args = parser.parse_args()

    # Route to appropriate command
    if args.command == "evaluate":
        exit_code = cmd_evaluate(args)
    elif args.command == "validate":
        exit_code = cmd_validate(args)
    elif args.command == "score":
        exit_code = cmd_score(args)
    elif args.command == "gaps":
        exit_code = cmd_gaps(args)
    elif args.command == "demo":
        exit_code = cmd_demo(args)
    else:
        parser.print_help()
        exit_code = 2

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
