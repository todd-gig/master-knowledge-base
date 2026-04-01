from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
MACHINE = ROOT / "machine"


class ValidationError(Exception):
    pass


def load_schema(name: str) -> Dict[str, Any]:
    path = MACHINE / name
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _check_type(value: Any, expected: Any) -> bool:
    if isinstance(expected, list):
        return any(_check_type(value, item) for item in expected)
    mapping = {
        "string": str,
        "number": (int, float),
        "object": dict,
        "array": list,
        "boolean": bool,
        "null": type(None),
    }
    py_type = mapping.get(expected)
    if py_type is None:
        return True
    if expected == "number":
        return isinstance(value, py_type) and not isinstance(value, bool)
    return isinstance(value, py_type)


def validate_payload(payload: Dict[str, Any], schema_name: str) -> Tuple[bool, List[str]]:
    schema = load_schema(schema_name)
    errors: List[str] = []

    for field in schema.get("required", []):
        if field not in payload:
            errors.append(f"Missing required field: {field}")

    properties = schema.get("properties", {})
    for key, value in payload.items():
        if key not in properties:
            continue
        prop = properties[key]
        expected_type = prop.get("type")
        if expected_type is not None and not _check_type(value, expected_type):
            errors.append(f"Field {key} expected type {expected_type}, got {type(value).__name__}")
        if "enum" in prop and value is not None and value not in prop["enum"]:
            errors.append(f"Field {key} expected one of {prop['enum']}, got {value}")
        if "minimum" in prop and value is not None and value < prop["minimum"]:
            errors.append(f"Field {key} must be >= {prop['minimum']}")
        if "maximum" in prop and value is not None and value > prop["maximum"]:
            errors.append(f"Field {key} must be <= {prop['maximum']}")

    return (len(errors) == 0, errors)


def ensure_valid(payload: Dict[str, Any], schema_name: str) -> None:
    is_valid, errors = validate_payload(payload, schema_name)
    if not is_valid:
        raise ValidationError("; ".join(errors))
