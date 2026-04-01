from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MACHINE = ROOT / "machine"

class ValidationError(Exception):
    pass

def load_schema(name):
    with (MACHINE / name).open("r", encoding="utf-8") as f:
        return json.load(f)

def validate_required(payload, schema_name):
    schema = load_schema(schema_name)
    missing = [field for field in schema.get("required", []) if field not in payload]
    return missing

def ensure_required(payload, schema_name):
    missing = validate_required(payload, schema_name)
    if missing:
        raise ValidationError(f"Missing required fields: {missing}")
