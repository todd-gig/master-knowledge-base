# Why Stage 9 — Calibration → Live Mode (1-minute read)

**Onboarding doesn't end when data lands; it ends when the system produces live, trusted decisions.** That's the structural answer to the question "when does onboarding actually end?"

By the end of Stage 8 the operator has:

- A signed scope contract and acknowledged axioms (Stage 0)
- 20+ documents ingested as a canonical bundle (Stage 1)
- A people graph with BFT snapshots (Stage 2)
- Brand voice + ICP segments (Stage 3)
- North star, supporting metrics, constraints (Stage 4)
- Industry processes triaged (Stage 5)
- Org processes codified (Stage 6)
- Workflows assigned to humans or automation candidates (Stage 7)
- Unit economics + Influence vs Cost dashboard (Stage 8)

That's a complete substrate for decision-making. Stage 9 is where the system uses it.

Three subsystems collaborate during Stage 9's shadow period: **PPEME simulates, decision-engine recommends, OVS-Calibration scores attribution.** PPEME generates what-if projections from the substrate; decision-engine produces real-world recommendations against the operator's live context; OVS-Calibration compares projected outcomes to actual outcomes and computes per-action attribution scores.

**You cannot skip Stage 9.** The manifest's `overlay_schema.inviolable_stage_ids` lists both Stage 0 and Stage 9 as inviolable; no `workflow_overlays` configuration can hide them. The structural reason is that tier_5_live (the autonomy tier) is the platform's most consequential capability — auto-executing decisions on the operator's behalf. The platform refuses to grant it without evidence that the substrate is calibrated.

The Stage 9 graduation gate is **evidence-based**, not calendar-based. The v1.0 manifest originally required a 30-day calendar elapsed period; v1.1.0 removed that predicate in favor of four verification dimensions (covered in `/docs/what/calibration-3min.md` and the deep dive). The shift means a well-prepared operator who clears all four dimensions in 12 days graduates in 12 days; a less-prepared operator who needs 60 days takes 60. The clock no longer gates.

If you only remember one thing: **Stage 9 is the moment the platform takes over decisions on your behalf. The graduation gate is evidence-based — the platform looks at whether the substrate is actually calibrated, not at how long you've been waiting.**
