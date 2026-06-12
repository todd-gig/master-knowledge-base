---
name: compensation-payout-structure-thursday-5-28-deadline
description: Hard deadline 2026-05-28 (Thursday) for completing the compensation > payout structure and documentation. Set by Todd 2026-05-26. Daily progress prompts authorized to increase completion probability.
metadata: 
  node_type: memory
  type: project
  established: 2026-05-26
  deadline: 2026-05-28
  status: ACTIVE — daily prompts enabled until complete
  originSessionId: fc56c866-aa65-41d6-a729-1d21c8fe1dcb
promoted_from: compensation_payout_structure_thursday_5_28_deadline.md
promoted_at: 2026-06-02T20:13:25Z
---

# Compensation + Payout Structure docs — Thursday 2026-05-28 deadline

**Directive (Todd, 2026-05-26 EOD)**:
> "Schedule compensation > payout structure and documentation completion by Thursday + remember to prompt daily when relevant to progress & increase chance of completion"

## What "complete" means

A single, ratified document (or set of documents) covering:

1. **Compensation routing per entity** — who gets paid what for what, at what cadence
   - Carmen Beach Properties: owner rev share %, cleaning ops %, Gigaton platform %, Ti Solutions service %
   - Ti Solutions clients (Kollosche, Medvidi, McGrath, CareRev, Integra-CCS): managed-service base + outcome-uplift split
   - Multipli prospect (when active): vendor financing performance share % to Gigaton
   - Gignet affiliates (when active): tier-based commission table
   - Sub-client routing (CBP walking-tour, CBP DMS marketing): parent-pass-through rules
2. **Payout structure**
   - Min threshold: $1,000 USD (locked — see [[payout_1_min_threshold_1k_2026_05_26]])
   - Cadence: per-entity (weekly / bi-weekly / monthly / per-event)
   - Rail: Stripe Connect Express (default) + ACH alternative
   - Currency-rounding rule per PAYOUT-1
   - Failed-payout retry policy
3. **Documentation deliverables**
   - File(s) under `master-knowledge-base/docs/governance/` or `decisions/`
   - Linked from operator onboarding manifest (`onboarding_v1.yaml` stage referencing it)
   - Referenced by gigaton-engine billing module (PR open per Wave 2 Week 1 supporting infra)

## Why daily prompts

Todd authorized me to prompt daily until done — pattern from past observation that
governance/legal/financial documents have low completion rates without external nudging.
The prompts should be:
- Brief (1-2 sentences max)
- Concrete (what specific section is missing, not "how is it going")
- Time-aware (count days remaining to Thursday)
- Scheduled via `/schedule` (remote agent) so they persist across Claude sessions

## How to apply (the prompt itself, when daily reminder fires)

When the daily reminder fires:
1. Re-check git log + filesystem for any new commits under `master-knowledge-base/docs/governance/`
2. Re-check existing memory + decisions log for newly-locked compensation/payout decisions
3. If incomplete + before Thursday: brief Todd on what's missing + offer to draft the missing section as a subagent
4. If Thursday + still incomplete: escalate (e.g. propose a forced-priority work block, or formally renegotiate deadline)
5. If complete: confirm + save completion memory + cancel the recurring schedule

## Related

- [[payout_1_min_threshold_1k_2026_05_26]] — $1k min threshold (locked component)
- [[product_service_package_gigaton_ti_solutions]] — go-to-market compensation framing
- [[master_project_plan]] — Chapter 11 Gignet affiliate tier table (compensation reference)
- PAYOUT-1 + OPS-1 architectural decisions
