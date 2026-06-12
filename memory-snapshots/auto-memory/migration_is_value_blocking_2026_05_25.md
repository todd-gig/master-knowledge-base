---
name: migration-is-value-blocking-2026-05-25
description: "USER DIRECTIVE 2026-05-25 evening: GCP engine migration (carmen-beach-properties → gigaton-platform) is value-blocking. No value generation, no dogfood, no Multipli engagement begins until migration completes. Complete ASAP."
metadata: 
  node_type: memory
  type: feedback
  established: 2026-05-25
  urgency: CRITICAL
  originSessionId: 6548918b-da46-4372-8d92-a5dd5667de87
promoted_from: migration_is_value_blocking_2026_05_25.md
promoted_at: 2026-06-02T20:13:25Z
---

# Migration is value-blocking — complete ASAP

**Rule:** GCP engine migration (per [[gcp_engine_migration_accelerated_2026_05_25]]) is the critical-path constraint to all value-generation activity. No dogfood, no Multipli engagement, no Sales-OS production runs begin until all 4 platform engines + 2 Cloud SQL + 8 secrets + 5 SAs are successfully migrated from `carmen-beach-properties` to `gigaton-platform` and soak-validated.

**Why:** User directive 2026-05-25 evening. The rationale (architect-derived, user-confirmed):
- Two parallel Cloud Run footprints (full carmen-beach-properties + slim gigaton-platform) create constant ambiguity about which is canonical.
- Dogfooding on the wrong footprint contaminates the labeled-training-signal corpus.
- Beta-cohort engagements (Multipli #1, LiqueFex #2, CBP #3, walking-tour DBA sub-client) cannot be promised durably on carmen-beach-properties since that project is end-of-life.
- "Predictably profitable" requires a single source of truth for the production engines, not two.

**How to apply:**
- Sequence ALL work behind migration completion.
- Sales-OS orchestrator code work (D-1 per [[sales_operating_system_state_2026_05_25]]) and Wave 2 dispatch (per [[stage_5_variance_aware_self_healing_spec]]) MAY run in parallel where they don't touch engines being actively migrated — but their value-generating use must wait for migration.
- Multipli proposal package authoring (P-1..P-6 per the v0.4/v0.5 planning artifacts) does NOT ship until migration complete + dogfood validation done. Promising what an unmigrated system "will do" violates the foundational sequence.
- Exception: the Multipli sprint bundle EOD Tue 2026-05-26 runs on carmen-beach-properties existing footprint — it does not depend on migration and should complete as planned (it's a demo, not a production engagement).
- Migration kickoff should be the EARLIEST safe moment that does not collide with the Tue sprint completion. Recommended: kickoff Tue 2026-05-26 evening (post-sprint) at the earliest, or Wed 2026-05-27 morning. The previously-recommended Wed 2026-05-27 evening kickoff is too late — bring forward.

**Estimated migration window:** ~1 week (12–16 operator-attended hours) per accelerated plan. Target migration-complete: ~Tue 2026-06-02.

**Linked memories:**
- [[gcp_engine_migration_accelerated_2026_05_25]] — the actual migration plan
- [[sales_operating_system_state_2026_05_25]] — D-1 dependency
- [[beta_cohort_entity_structure_2026_05_25]] — the cohort that's blocked on this
- [[multipli_vendor_growth_engine_sprint_2026_05_22]] — the one carve-out (sprint runs on existing footprint)
