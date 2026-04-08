"""
scoring_weights.py - claude-systems v3.2
Store all weight configs as dictionaries. Load from YAML if available, else use defaults.
"""

from __future__ import annotations

import os
from typing import Any, Dict

try:
    import yaml
    _YAML_AVAILABLE = True
except ImportError:
    _YAML_AVAILABLE = False

# ---------------------------------------------------------------------------
# Default weight definitions
# ---------------------------------------------------------------------------

PYTHON_SIGNAL_NAMES: list[str] = [
    "structured_input",
    "explicit_rules",
    "deterministic_output",
    "high_volume",
    "low_error_tolerance",
    "auditability_required",
    "latency_sensitivity",
    "repeatability",
    "stable_logic",
]

PYTHON_WEIGHTS_DEFAULT: Dict[str, float] = {
    "structured_input": 1.2,
    "explicit_rules": 1.3,
    "deterministic_output": 1.4,
    "high_volume": 1.4,
    "low_error_tolerance": 1.3,
    "auditability_required": 1.2,
    "latency_sensitivity": 1.1,
    "repeatability": 1.3,
    "stable_logic": 1.4,
}

CLAUDE_SIGNAL_NAMES: list[str] = [
    "ambiguous_input",
    "contextual_reasoning",
    "incomplete_rules",
    "novel_cases",
    "synthesis_required",
    "edge_case_frequency",
    "high_learning_value",
    "semantic_variability",
    "interpretation_burden",
]

CLAUDE_WEIGHTS_DEFAULT: Dict[str, float] = {
    "ambiguous_input": 1.4,
    "contextual_reasoning": 1.3,
    "incomplete_rules": 1.3,
    "novel_cases": 1.2,
    "synthesis_required": 1.3,
    "edge_case_frequency": 1.2,
    "high_learning_value": 1.1,
    "semantic_variability": 1.2,
    "interpretation_burden": 1.4,
}

HYBRID_SIGNAL_NAMES: list[str] = [
    "parse_then_score_viable",
    "exception_isolation_possible",
    "structured_output_possible",
    "mid_maturity_logic",
    "rapid_deployment_needed",
    "codification_path_exists",
]

HYBRID_WEIGHTS_DEFAULT: Dict[str, float] = {
    "parse_then_score_viable": 1.5,
    "exception_isolation_possible": 1.3,
    "structured_output_possible": 1.4,
    "mid_maturity_logic": 1.3,
    "rapid_deployment_needed": 1.1,
    "codification_path_exists": 1.5,
}

CODIFICATION_BANDS_DEFAULT: Dict[str, Any] = {
    "codify_now":       {"min": 0.80, "max": 1.00},
    "prepare_design":   {"min": 0.60, "max": 0.80},
    "continue_logging": {"min": 0.40, "max": 0.60},
    "keep_in_claude":   {"min": 0.00, "max": 0.40},
}

ROUTING_THRESHOLDS_DEFAULT: Dict[str, float] = {
    # One mode must be >= this fraction above others to be chosen outright
    "dominant_margin": 0.15,
    # Hybrid within this fraction of best score + codification path -> choose Hybrid
    "hybrid_catch_margin": 0.10,
}

_DEFAULTS: Dict[str, Any] = {
    "python_weights": PYTHON_WEIGHTS_DEFAULT,
    "claude_weights": CLAUDE_WEIGHTS_DEFAULT,
    "hybrid_weights": HYBRID_WEIGHTS_DEFAULT,
    "codification_bands": CODIFICATION_BANDS_DEFAULT,
    "routing_thresholds": ROUTING_THRESHOLDS_DEFAULT,
}


# ---------------------------------------------------------------------------
# Loader
# ---------------------------------------------------------------------------

def load_weights(yaml_path: str | None = None) -> Dict[str, Any]:
    """Return the full weight config dict.

    If *yaml_path* is given (or the env-var ``CLAUDE_SYSTEMS_WEIGHTS_YAML``
    is set) and PyYAML is available, the YAML file is loaded and merged on
    top of the defaults.  Missing keys fall back to defaults.
    """
    config: Dict[str, Any] = {k: dict(v) if isinstance(v, dict) else v
                               for k, v in _DEFAULTS.items()}

    path = yaml_path or os.environ.get("CLAUDE_SYSTEMS_WEIGHTS_YAML")
    if path and _YAML_AVAILABLE:
        try:
            with open(path, "r", encoding="utf-8") as fh:
                overrides: Dict[str, Any] = yaml.safe_load(fh) or {}
            for section, values in overrides.items():
                if section in config and isinstance(values, dict):
                    config[section].update(values)
                else:
                    config[section] = values
        except (OSError, yaml.YAMLError):
            pass  # fall back to defaults silently

    return config


# Convenience module-level singletons (loaded once on import)
_WEIGHTS = load_weights()

PYTHON_WEIGHTS: Dict[str, float] = _WEIGHTS["python_weights"]
CLAUDE_WEIGHTS: Dict[str, float] = _WEIGHTS["claude_weights"]
HYBRID_WEIGHTS: Dict[str, float] = _WEIGHTS["hybrid_weights"]
CODIFICATION_BANDS: Dict[str, Any] = _WEIGHTS["codification_bands"]
ROUTING_THRESHOLDS: Dict[str, float] = _WEIGHTS["routing_thresholds"]
