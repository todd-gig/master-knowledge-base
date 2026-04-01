from __future__ import annotations

import difflib
import json
from pathlib import Path
from typing import Dict, Any, List

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry"


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def prompt_diff(old_text: str, new_text: str) -> str:
    return "".join(
        difflib.unified_diff(
            old_text.splitlines(keepends=True),
            new_text.splitlines(keepends=True),
            fromfile="old",
            tofile="new",
        )
    )


def evaluate_release(approvals: List[Dict[str, Any]], minimum_required: int) -> bool:
    approved = [a for a in approvals if a.get("decision") == "approve"]
    return len(approved) >= minimum_required


def release_summary() -> Dict[str, Any]:
    policy = load_json(REGISTRY / "release_policy.json")
    prompt_registry = load_json(REGISTRY / "prompt_registry.json")
    return {
        "active_prompt_id": prompt_registry["active_prompt_id"],
        "active_prompt_version": prompt_registry["active_prompt_version"],
        "minimum_required_approvals": policy["minimum_required_approvals"],
        "required_checks": policy["required_checks"],
    }
