from pathlib import Path

def test_required_files_exist():
    base = Path(__file__).resolve().parents[1]
    required = [
        "README.md",
        "CLAUDE.md",
        "99_full_transcript.md",
        "registry/project_index.json",
        "machine/skill_ontology.json",
        "machine/team_structure_rules.json",
        "machine/negotiation_framework.json",
        "machine/output_template.json",
    ]
    missing = [p for p in required if not (base / p).exists()]
    assert not missing, f"Missing files: {missing}"
