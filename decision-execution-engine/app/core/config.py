from pathlib import Path
import yaml
from pydantic import BaseModel

class Thresholds(BaseModel):
    value_execute_min: float
    value_escalate_min: float
    trust_execute_min: float
    trust_recommend_min: float

class Settings(BaseModel):
    thresholds: Thresholds
    value_weights: dict[str, float]
    penalty_weights: dict[str, float]
    trust_multiplier: dict[str, float]
    authority_matrix: dict[str, dict]
    valid_transitions: dict[str, list[str]]

def _load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_settings() -> Settings:
    root = Path(__file__).resolve().parents[2]
    cfg = _load_yaml(root / "config" / "engine.yaml")
    return Settings(**cfg)

settings = load_settings()
