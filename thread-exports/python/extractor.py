from pathlib import Path
import json

def load_registry(base: Path):
    return {
        "project_index": json.loads((base / "registry" / "project_index.json").read_text()),
        "skill_ontology": json.loads((base / "machine" / "skill_ontology.json").read_text()),
        "team_structure_rules": json.loads((base / "machine" / "team_structure_rules.json").read_text()),
        "negotiation_framework": json.loads((base / "machine" / "negotiation_framework.json").read_text()),
        "output_template": json.loads((base / "machine" / "output_template.json").read_text()),
    }

def route_request(request_type: str, base: Path):
    registry = load_registry(base)
    routing = registry["project_index"]["routing"]
    return routing.get(request_type, routing["mixed"])

if __name__ == "__main__":
    base = Path(__file__).resolve().parents[1]
    print(route_request("mixed", base))
