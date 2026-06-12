---
name: feedback-legal-v0-review-parked-unless-go-live-blocker
description: "Paralegal v0 legal review (external engagement ~$8-24K, 2-3 weeks, to review 14 entity legal v0 drafts at master-knowledge-base/legal/v0_drafts/) is PARKED indefinitely. Do not proactively surface, prioritize, or include in status summaries / pending-action lists unless it has become a hard requirement for going live with system functionality."
metadata: 
  node_type: memory
  type: feedback
  established: 2026-05-26
  originSessionId: b8909926-050d-414d-acfb-51bd96fca09c
promoted_from: feedback_legal_v0_review_parked_unless_go_live_blocker.md
promoted_at: 2026-06-02T20:13:25Z
---

# Paralegal v0 legal review — parked unless go-live blocker

**Rule:** Do not proactively surface, prioritize, or include the "paralegal v0 legal review" workstream in status summaries, pending-action lists, or "what's next" recommendations. Treat it as silent / off-radar.

**The one exception that re-activates it:** the review has become a *hard* requirement for going live with any system functionality. Examples that DO qualify:
- Stripe customer onboarding gated on signed entity docs / T&Cs
- A marketplace or partner refusing to list / contract without reviewed legal
- A regulator (gov, payments, data) blocking activation pending entity formation review
- An operator in the beta cohort blocked from production traffic due to missing reviewed agreements

Examples that DO NOT qualify (keep parked):
- General "we should get the legal stuff done" sentiment
- Periodic Tier 2 / backlog review surfacing it as "still pending"
- The fact that the v0 drafts exist in `master-knowledge-base/legal/v0_drafts/` and have not been touched in N days

**Why:** User directive 2026-05-26 after I summarized it as a Tier 2 pending action — "set a reminder for next week about legal and then forget unless it's a requirement for going live with any system functionality." The check-in cadence is handled out-of-band by a scheduled remote routine (one-time, Mon 2026-06-01 14:00 UTC, routine `trig_01FiCMhDi2bCkXTDzbtxbT3g`) that DMs Todd in `ti-gigaton.slack.com` asking the go-live-blocker question. Future sessions: trust that loop; do not duplicate the surface.

**How to apply:**
- When drafting handoff / resume docs, omit the paralegal v0 line from pending-action lists unless go-live-blocker condition is met. Move it (and only it) out of the standard Tier 2 list in [[RESUME_HERE_2026_05_26_full_session_handoff]] on next edit pass.
- When the user asks "what's pending" / "what's next," skip this item silently.
- If the user themselves brings it up, engage normally — the silence rule is about *proactive* surfacing only.
- Distinct from Attorney Jim's W7-W8 public T&Cs track ([[w7_w8_tcs_publication_readiness_plan]]) — that one stays on the timeline (target ~2026-06-15 gigaton.ai/terms publish for Stripe + CASA + LiquiFex + GDPR). Do not extend this parking rule to the Attorney Jim track.

**Related context:** [[RESUME_HERE_2026_05_26_full_session_handoff]] §5 lists this as Tier 2 item #6 — that entry should be updated/removed on next pass per the rule above.
