---
name: matt-stripe-connect-express-eod-thursday-5-28-2026-05-26
description: Matt delegated Stripe Connect Express verification + setup with EOD Thursday 2026-05-28 deadline. Aligns with Thursday comp+payout doc deadline so the rails are ready when the policy goes ACTIVE. Todd authorized 2026-05-26 EOD.
metadata: 
  node_type: memory
  type: project
  established: 2026-05-26
  deadline: 2026-05-28
  owner: matt (delegated by Todd)
  status: DELEGATED — assume completion by EOD Thursday 5/28 unless Friday verification fires red
  originSessionId: b8909926-050d-414d-acfb-51bd96fca09c
promoted_from: matt_stripe_connect_express_eod_thursday_5_28_2026_05_26.md
promoted_at: 2026-06-02T20:13:25Z
---

# Matt — Stripe Connect Express EOD Thursday 2026-05-28

## The delegation

Todd 2026-05-26 EOD: *"assume stripe will be completed by matt before EOD thursday"*

Matt now owns:

1. Stripe dashboard → Settings → Connect → enable Connect Express
2. KYC/onboarding flow verification
3. ACH alternative rail enablement (per PAYOUT-1 doctrine)
4. Confirm `payout_schedule` config primitives are accessible:
   - `minimum_amount = 100000` cents ($1k floor per PAYOUT-1)
   - `weekly_anchor = wednesday` + internal bi-weekly skip logic
   - `application_fee = 0` on payout side (platform absorbs ACH fee)
5. Test-mode first payout to confirm rails work end-to-end

## Why Thursday 5/28

Aligns with the comp+payout doc deadline. Comp+payout structure ([[compensation_payout_structure_thursday_5_28_deadline]] + mkb PR #17) flips DRAFT→ACTIVE Thursday. Stripe Connect Express must be ready that same day so the gigaton-engine billing module can read both:
- the LOCKED §2 rules from the doc
- the live Stripe Connect config

Without Stripe Connect Express, the doc can be ACTIVE but the rails can't execute. Both must land Thursday EOD.

## Already-delegated context

Matt already owns:
- **WhatsApp/Meta verification** (3-7 day Meta review) — Slack DM in `ti-gigaton.slack.com`

So Matt's Thursday is: Stripe Connect Express + WhatsApp progress check.

## Verification routine

One-time routine fires **Fri 2026-05-29 14:00 UTC** (9am Cancun). Checks:

1. Stripe Connect Express enabled on platform Stripe account (signal: presence of Connect-related config or via Matt's Slack confirmation)
2. mkb `docs/governance/comp_payout_structure_v1.md` status: ACTIVE on main
3. gigaton-engine billing module has a successful `PayoutScheduled` event emit (any operator, any amount)

If all GREEN → DM Todd: "Stripe + comp+payout Thursday deadline MET. Billing rails active."
If any RED → DM Todd: "Friday Thursday-deadline check — N items still pending: [list]. Suggest follow-up with Matt re Stripe."

Routine ID: `<to-be-filled>` (see below)

## Re-routing implications

- **Todd's Tier 1 leverage list** loses Stripe Connect Express (was the highest-leverage action). Now Todd's top remaining items are:
  - 3 Multipli vendor URLs (Tier 2)
  - ui-system #20/#24/#25 rebase authorization (Tier 1)
  - Content for sub-client surfaces (Tier 3)
- The eve session handoff [[RESUME_HERE_2026_05_26_eve_session_handoff]] should reflect Stripe as DELEGATED, not on Todd's plate.

## Escalation path

If Friday verification fires RED on Stripe specifically:
1. DM Matt in `ti-gigaton.slack.com` for status
2. Surface to Todd same morning
3. The Wed 6/03 weekly gate-check routine will re-test as part of migration-readiness Gate D — but that's 5 days later than the deadline, so Friday morning is the right escalation point.

## Cross-references

- [[compensation_payout_structure_thursday_5_28_deadline]] — same deadline
- [[payout_1_min_threshold_1k_2026_05_26]] — $1k floor (Stripe min amount config)
- [[payout_1_and_intel_1_clarifications_locked_2026_05_26]] — rounding/cadence/fee-bearer config
- [[intel_3_no_static_weights_algorithmic_determination_2026_05_26]] — INTEL-3 governs HOW Stripe payout %s compute (algorithmic, not static)
- [[RESUME_HERE_2026_05_26_eve_session_handoff]] §7 — Tier 1 list (update: Stripe → delegated)
