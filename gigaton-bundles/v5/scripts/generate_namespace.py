import json
import sys
from pathlib import Path

CATEGORY_BASE = {
    "foundational_doctrine": 1.00,
    "decision_systems": 0.96,
    "knowledge_infrastructure": 0.94,
    "ontology_and_data_models": 0.92,
    "simulation_and_financial_models": 0.89,
    "commercial_systems": 0.90,
    "platform_and_tooling": 0.84,
    "organizational_models": 0.80
}

ARTIFACT_TO_CATEGORY = {
    "contracts": {"commercial_systems": 0.08},
    "decision_automation": {"decision_systems": 0.10},
    "knowledge_systems": {"knowledge_infrastructure": 0.08},
    "ops_dashboard": {"platform_and_tooling": 0.08},
    "research": {"ontology_and_data_models": 0.08}
}

REVENUE_MOTION_TO_MEMORY_BIAS = {
    "enterprise_sales": ["MEM-015","MEM-016","MEM-017","MEM-002"],
    "services": ["MEM-003","MEM-011","MEM-012","MEM-013"],
    "licensing": ["MEM-015","MEM-016","MEM-020"],
    "platform": ["MEM-002","MEM-003","MEM-013","MEM-014"]
}

def main():
    if len(sys.argv) != 5:
        print("Usage: python generate_namespace.py <intake.json> <memory_registry.json> <out_dir> <namespace_id>")
        sys.exit(1)

    intake_path = Path(sys.argv[1])
    registry_path = Path(sys.argv[2])
    out_dir = Path(sys.argv[3])
    namespace_id = sys.argv[4]
    out_dir.mkdir(parents=True, exist_ok=True)

    intake = json.loads(intake_path.read_text(encoding="utf-8"))
    registry = json.loads(registry_path.read_text(encoding="utf-8"))

    category_weights = dict(CATEGORY_BASE)
    for artifact in intake.get("artifact_priorities", []):
        for k, v in ARTIFACT_TO_CATEGORY.get(artifact, {}).items():
            category_weights[k] = round(category_weights.get(k, 0.0) + v, 4)

    preferred_memories = REVENUE_MOTION_TO_MEMORY_BIAS.get(intake.get("primary_revenue_motion", ""), [])

    selected_memories = []
    for mem in registry.get("memory_objects", []):
        score = mem.get("weighted_base_score", 0)
        if mem.get("memory_id") in preferred_memories:
            score += 0.10
        if mem.get("category") == "foundational_doctrine":
            score += 0.10
        selected_memories.append({
            "memory_id": mem["memory_id"],
            "title": mem["title"],
            "category": mem["category"],
            "score": round(score, 4)
        })

    selected_memories = sorted(selected_memories, key=lambda x: x["score"], reverse=True)

    namespace = {
        "namespace_id": namespace_id,
        "inherits_from": "global",
        "client_name": intake["client_name"],
        "industry": intake["industry"],
        "preferred_terminology": intake.get("preferred_terminology", {}),
        "custom_category_bias": category_weights,
        "workflow_variants": intake.get("workflow_preferences", []),
        "data_sources": intake.get("data_sources", []),
        "selected_memory_ids": [m["memory_id"] for m in selected_memories[:10]],
        "forbidden_overrides": [
            "foundational_doctrine",
            "ethics",
            "human_centered_technology_principle"
        ]
    }

    overlay = {
        "namespace_id": namespace_id,
        "top_objectives": intake.get("top_3_objectives", []),
        "top_constraints": intake.get("top_3_constraints", []),
        "recommended_memories": selected_memories[:10]
    }

    scoring_weights = {
        "namespace_id": namespace_id,
        "custom_category_bias": category_weights,
        "priority_revenue_motion": intake.get("primary_revenue_motion", "")
    }

    brief = f"""# Client Onboarding Brief

## Client
{intake['client_name']}

## Industry
{intake['industry']}

## Business model
{intake['business_model']}

## Primary revenue motion
{intake['primary_revenue_motion']}

## Top objectives
- """ + "\n- ".join(intake.get("top_3_objectives", [])) + f"""

## Top constraints
- """ + "\n- ".join(intake.get("top_3_constraints", [])) + f"""

## Selected memories
- """ + "\n- ".join([f"{m['memory_id']} — {m['title']}" for m in selected_memories[:10]]) + """
"""

    (out_dir / "client_namespace.generated.json").write_text(json.dumps(namespace, indent=2), encoding="utf-8")
    (out_dir / "client_memory_overlay.generated.json").write_text(json.dumps(overlay, indent=2), encoding="utf-8")
    (out_dir / "client_scoring_weights.generated.json").write_text(json.dumps(scoring_weights, indent=2), encoding="utf-8")
    (out_dir / "client_onboarding_brief.generated.md").write_text(brief, encoding="utf-8")
    print(f"[OK] Generated namespace artifacts in {out_dir}")

if __name__ == "__main__":
    main()
