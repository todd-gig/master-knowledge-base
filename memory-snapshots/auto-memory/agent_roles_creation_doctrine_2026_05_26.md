---
name: agent-roles-creation-doctrine-2026-05-26
description: "LOCKED governance doctrine 2026-05-26 EOD (Todd directive): agent_roles in the Ti Agent Matrix can be created via TWO pathways only — system-generated OR human-analysis-and-defined. The human-defined path requires a structured signature across Gigaton responsibility / requirements / skills / experience / education → expertise / value matrix, augmented by additional Gigaton intelligence systems."
metadata: 
  node_type: memory
  type: project
  established: 2026-05-26
  status: LOCKED — Todd directive
  scope: "every agent_role row in intel-silo's agent_roles table (and any downstream consumer in Ti Agent Matrix)"
  originSessionId: fc56c866-aa65-41d6-a729-1d21c8fe1dcb
promoted_from: agent_roles_creation_doctrine_2026_05_26.md
promoted_at: 2026-06-02T20:13:25Z
---

# agent_roles creation doctrine — LOCKED 2026-05-26

## Directive (Todd, 2026-05-26 EOD)

> "agent_roles must be created by system, or via human analysis > identification of need + defined by user based on gigaton responsibility, requirements, skills, experience, education > expertise, > value matrix + additional gigaton intelligence systems"

## Two valid creation pathways

### Pathway A — System-generated

The Gigaton intelligence layer (decision-engine + persona-engine + intel-silo's emerging classifier work) MAY autonomously create an `agent_roles` row when:

- A capability gap is detected via routine operation (e.g. `/v1/intelligence/classify` repeatedly routes queries to roles that don't yet exist for a specific function area)
- A new operator onboarding identifies a function that needs a default role catalog entry
- Wave 2 self-engineered HR loop identifies a coverage gap and proposes filling it

System-generated rows MUST carry:
- `created_by = 'system'` (new column required — see schema follow-on below)
- `creation_pathway = 'system_generated'` (new column)
- `creation_rationale` JSONB explaining the detection signal (new column)
- `lifecycle_state = 'proposed'` initially (NOT auto-`active`) — must pass human approval before activating

### Pathway B — Human-defined

An operator (or Todd) defines a new `agent_roles` row by:

1. **Human analysis** → identifying the NEED (a role-shaped gap in the operator's organization)
2. **Defining the role** with explicit values across these dimensions:

   | Dimension | Where it lives | Notes |
   |---|---|---|
   | **Gigaton responsibility** | new field `gigaton_responsibility` (text) | the specific PPIM-engineered brand-experience contribution this role makes to the platform's foundational goal |
   | **Requirements** | new field `requirements` (JSONB list) | role-specific functional requirements (e.g. tools required, integrations expected, SLA commitments) |
   | **Skills** | existing `required_skills` (JSONB list of skill_key refs to `skill_vectors`) | already in schema |
   | **Experience** | new field `experience_signature` (JSONB) | shape: `{years_min: int, domains: [text], notable_outcomes: [text]}` |
   | **Education → expertise** | new field `education_expertise_path` (JSONB) | shape: `{formal: [{credential, institution_type}], experiential: [{practice, hours_min}], certifications: [text]}` |
   | **Value matrix** | new field `value_matrix` (JSONB) | shape: `{produces: [outcome_keys], consumes: [resource_keys], net_value_signature: {revenue_lift, cost_reduction, risk_mitigation, brand_coherence, predictability}}` — aligns with PPIM doctrine + Influence-vs-Cost dashboard |
   | **Augmentation context** | new field `augmenting_intelligence_refs` (JSONB list) | references to Gigaton intelligence systems consulted during definition (e.g. `["gignet-orchestrator-fn::cohort-pattern-match", "persona-engine::nearest-org-persona", "intel-silo::skill-graph-proximity"]`) |

3. **Storing it** with:
   - `created_by = <operator_user_id>`
   - `creation_pathway = 'human_defined'`
   - `creation_rationale` JSONB capturing the human's stated WHY
   - `lifecycle_state = 'proposed'` initially → operator promotes to `active` after governance review

## What does NOT count as valid creation

- Ad-hoc raw SQL INSERT bypassing the API (no governance audit trail)
- LLM hallucination via free-form chat (must go through the structured Pathway A or B endpoint)
- Copy-paste from an external source without the human-analysis step (Pathway B's first step is mandatory)
- Implicit creation via test fixtures bleeding into prod (must respect lifecycle_state='proposed' gate)

## Schema enhancement required (FOLLOW-ON PR)

Today's intel-silo migrations 033 + 034 (PR #41 + #42, merged earlier today) do NOT include the new columns required by this doctrine. The 40 currently-seeded roles were created via what is effectively "human-defined batch" (Claude subagent authored them based on master_project_plan + Wave 2 design doc context — i.e. human-curated content). They retroactively conform to Pathway B but lack the structured signature columns.

**Required follow-on PR** (intel-silo, separate from any work in flight):

```sql
ALTER TABLE agent_roles ADD COLUMN created_by TEXT NOT NULL DEFAULT 'system_migration_034';
ALTER TABLE agent_roles ADD COLUMN creation_pathway TEXT NOT NULL DEFAULT 'human_defined'
  CHECK (creation_pathway IN ('system_generated', 'human_defined'));
ALTER TABLE agent_roles ADD COLUMN creation_rationale JSONB DEFAULT '{}';
ALTER TABLE agent_roles ADD COLUMN gigaton_responsibility TEXT;
ALTER TABLE agent_roles ADD COLUMN requirements JSONB DEFAULT '[]';
ALTER TABLE agent_roles ADD COLUMN experience_signature JSONB DEFAULT '{}';
ALTER TABLE agent_roles ADD COLUMN education_expertise_path JSONB DEFAULT '{}';
ALTER TABLE agent_roles ADD COLUMN value_matrix JSONB DEFAULT '{}';
ALTER TABLE agent_roles ADD COLUMN augmenting_intelligence_refs JSONB DEFAULT '[]';
ALTER TABLE agent_roles ADD COLUMN promoted_to_active_at TIMESTAMPTZ;  -- governance audit
ALTER TABLE agent_roles ADD COLUMN promoted_by TEXT;                    -- governance audit

-- Also: tighten lifecycle_state default to 'proposed' going forward
ALTER TABLE agent_roles ALTER COLUMN lifecycle_state SET DEFAULT 'proposed';
```

Plus REST endpoint pair on intel-silo:
- `POST /v1/agent-roles/propose` — accepts the structured payload, writes with `lifecycle_state='proposed'`, requires `creation_pathway` + (if human_defined) the 6 dimension fields
- `POST /v1/agent-roles/{role_key}/promote` — flips to `active` after governance review; records `promoted_by` + `promoted_at`

## Backfill plan for the 40 already-seeded roles

The currently-seeded 40 roles (intel-silo migration 034) need backfill of:
- `created_by = 'claude-subagent-pr-42-2026-05-26'`
- `creation_pathway = 'human_defined'`
- `creation_rationale = {"source": "PR #42 by Claude Opus 4.7 (1M context) authored from master_project_plan Chapter 11 + Wave 2 design doc"}`
- The 6 dimension fields populated where derivable (most are inferable from existing `description` + `required_skills` + `authority_scope` columns); flag missing fields as `null` for human follow-up enrichment

The backfill itself can be a separate small PR after the schema-add PR lands.

## Cross-references

- [[entity_hierarchy_for_namespace_seed_2026_05_26]] — entity tree those roles serve
- [[payout_1_and_intel_1_clarifications_locked_2026_05_26]] — INTEL-1 governs how classifier consumes these rows
- [[user_influence_vs_cost_dashboard_spec]] — `value_matrix` field aligns with this observability surface
- [[foundational_goal_gigaton_engineered_brand_experience]] — `gigaton_responsibility` field maps every role to PPIM
- [[foundational_modular_replication_via_input_substitution]] — Pathway A's autonomous creation respects "engineer once, serve many" doctrine
- [[master_project_plan]] Chapter 11 — Gignet affiliate tier table (a downstream consumer of role-based attribution)
- intel-silo PR #41 + #42 — schema + initial seed (pre-doctrine; will be retroactively conformed via backfill PR)

## How to apply

- BEFORE creating any new `agent_roles` row: verify creation pathway, populate appropriate fields, set `lifecycle_state='proposed'`, require explicit governance promotion before activation
- Any code path that mutates `agent_roles` (services, migrations, ad-hoc scripts) must respect this doctrine
- The `coaching_graduation_state.nudge_category` values (persona-engine PR #15) ought to align with the `function_area` + `role_archetype` of the role responsible for emitting them — keep that consistency when authoring future categories
