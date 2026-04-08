"""
validation_layer.py - claude-systems v3.2
Validate decision payloads against the audit log schema.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Schema definition
# ---------------------------------------------------------------------------

REQUIRED_FIELDS: List[str] = [
    "decision_id",
    "timestamp",
    "request_type",
    "input_snapshot",
    "normalized_variables",
    "routing_classification",
    "chosen_architecture",
    "python_score",
    "claude_score",
    "hybrid_score",
    "confidence_score",
    "assumptions",
    "exception_class",
    "recommended_action",
    "actual_action",
    "human_review_required",
    "human_review_outcome",
    "estimated_unit_cost",
    "estimated_failure_cost",
    "codification_candidate",
    "outcome_quality",
    "notes",
]

OPTIONAL_FIELDS: List[str] = [
    "model_name",
    "prompt_version",
    "code_version",
    "latency_ms",
    "customer_impact_score",
    "compliance_flag",
    "rollback_available",
]

ALL_KNOWN_FIELDS: List[str] = REQUIRED_FIELDS + OPTIONAL_FIELDS

# Allowed routing classifications and architecture values
VALID_ROUTING_CLASSIFICATIONS: List[str] = [
    "Python-First",
    "Claude-First",
    "Hybrid",
]

VALID_ARCHITECTURES: List[str] = [
    "Python-First",
    "Claude-First",
    "Hybrid",
]


# ---------------------------------------------------------------------------
# Public types
# ---------------------------------------------------------------------------

@dataclass
class ValidationResult:
    valid: bool
    missing_fields: List[str] = field(default_factory=list)
    type_errors: List[str] = field(default_factory=list)
    value_errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    unknown_fields: List[str] = field(default_factory=list)

    @property
    def errors(self) -> List[str]:
        return self.missing_fields + self.type_errors + self.value_errors

    def __str__(self) -> str:
        if self.valid:
            return "ValidationResult: PASS"
        return (
            f"ValidationResult: FAIL | "
            f"missing={self.missing_fields} | "
            f"type_errors={self.type_errors} | "
            f"value_errors={self.value_errors}"
        )


# ---------------------------------------------------------------------------
# ValidationLayer
# ---------------------------------------------------------------------------

class ValidationLayer:
    """Validate decision and audit payloads.

    ``validate_decision`` checks a real-time decision payload (must have the
    required fields).  ``validate_audit_record`` additionally checks numeric
    range constraints and enum values.
    """

    def __init__(
        self,
        required_fields: Optional[List[str]] = None,
        optional_fields: Optional[List[str]] = None,
    ) -> None:
        self._required = required_fields or REQUIRED_FIELDS
        self._optional = optional_fields or OPTIONAL_FIELDS

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def validate_decision(self, payload: Dict[str, Any]) -> ValidationResult:
        """Validate a real-time decision payload for required field presence."""
        result = ValidationResult(valid=True)

        # Missing required fields
        for f in self._required:
            if f not in payload:
                result.missing_fields.append(f)

        # Unknown fields
        known = set(self._required) | set(self._optional)
        for f in payload:
            if f not in known:
                result.unknown_fields.append(f)
                result.warnings.append(f"Unknown field: {f}")

        result.valid = len(result.errors) == 0
        return result

    def validate_audit_record(self, record: Dict[str, Any]) -> ValidationResult:
        """Full validation of an audit log record including types and values."""
        # Start with structural check
        result = self.validate_decision(record)

        if result.missing_fields:
            # Don't bother with deeper checks if fields are missing
            return result

        # Type / value checks
        self._check_numeric(record, result, "python_score", 0.0, 5.0 * 9 * 1.4)
        self._check_numeric(record, result, "claude_score", 0.0, 5.0 * 9 * 1.4)
        self._check_numeric(record, result, "hybrid_score", 0.0, 5.0 * 6 * 1.5)
        self._check_numeric(record, result, "confidence_score", 0.0, 1.0)
        self._check_numeric(record, result, "outcome_quality", 0.0, 1.0)
        self._check_numeric(record, result, "estimated_unit_cost", 0.0, None)
        self._check_numeric(record, result, "estimated_failure_cost", 0.0, None)

        self._check_enum(
            record, result,
            "routing_classification",
            VALID_ROUTING_CLASSIFICATIONS,
        )
        self._check_enum(
            record, result,
            "chosen_architecture",
            VALID_ARCHITECTURES,
        )
        self._check_bool_like(record, result, "human_review_required")
        self._check_bool_like(record, result, "codification_candidate")

        result.valid = len(result.errors) == 0
        return result

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    @staticmethod
    def _check_numeric(
        record: Dict[str, Any],
        result: ValidationResult,
        field: str,
        lo: Optional[float],
        hi: Optional[float],
    ) -> None:
        val = record.get(field)
        if val is None:
            return
        try:
            fval = float(val)
        except (TypeError, ValueError):
            result.type_errors.append(f"{field} must be numeric, got {type(val).__name__}")
            return
        if lo is not None and fval < lo:
            result.value_errors.append(f"{field}={fval} below minimum {lo}")
        if hi is not None and fval > hi:
            result.value_errors.append(f"{field}={fval} above maximum {hi}")

    @staticmethod
    def _check_enum(
        record: Dict[str, Any],
        result: ValidationResult,
        field: str,
        allowed: List[str],
    ) -> None:
        val = record.get(field)
        if val is None:
            return
        if str(val) not in allowed:
            result.value_errors.append(
                f"{field}={val!r} not in allowed values {allowed}"
            )

    @staticmethod
    def _check_bool_like(
        record: Dict[str, Any],
        result: ValidationResult,
        field: str,
    ) -> None:
        val = record.get(field)
        if val is None:
            return
        if not isinstance(val, (bool, int)):
            result.type_errors.append(
                f"{field} should be bool or int (0/1), got {type(val).__name__}"
            )
