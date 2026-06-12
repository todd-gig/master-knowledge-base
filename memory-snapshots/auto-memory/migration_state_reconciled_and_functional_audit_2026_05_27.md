---
name: migration_state_reconciled_and_functional_audit_2026_05_27
description: Live-verified 2026-05-27 — migration is 0/4 in-scope engines routed to gigaton-platform (decision-engine reverted to carmen-beach); re-flip would REGRESS data; core platform is functional with no broken paths.
metadata: 
  node_type: memory
  type: project
  originSessionId: 943a8dc1-3984-4d2b-8bc3-e20e7dcc92d8
promoted_from: migration_state_reconciled_and_functional_audit_2026_05_27.md
promoted_at: 2026-06-02T20:13:25Z
---

Live GCP verification on 2026-05-27 (todd@gigaton.ai), against the gateway routing table + Cloud Run, NOT memory:

## Migration true state + session-1 RE-LOCKED 2026-05-27
Hash map: `rjmcrtvuzq` = carmen-beach-properties, `sqatlxhlza` = gigaton-platform (confirmed via service URLs).
On 2026-05-27 the live gateway (was rev 00053-msq) had **0 of 4 in-scope engines** on gigaton-platform — decision-engine had silently reverted to carmen (`rjmcrtvuzq`), the exact failure the marker warned about (root cause: `cloudbuild.yaml:52` hardcodes the carmen URL, so every gateway Cloud Build redeploy re-reverts the flip).

**FIXED THIS SESSION (Todd authorized override of DEFER for decision-engine only):**
- Verified carmen's `decision_engine` DB held only **2 trivial rows** (1 test decision_record + 1 execution_record) → my initial "~2 days of valuable writes" hypothesis was WRONG; data-regression risk was nil. (Dump saved as backup: `gs://gigaton-migration-staging/decision-engine-redo-session1-20260528T002323Z.sql.gz`.)
- Verified target gigaton-platform decision-engine healthy (`/health` ok, engine_version 2.0.0 == live).
- Did **verify-and-flip** (skipped destructive DB restore — unnecessary at 2 rows; the target instance also hosts the LIVE `red_phone` DB, do NOT drop it). Flipped live gateway `DECISION_ENGINE_URL` → `https://decision-engine-sqatlxhlza-uc.a.run.app` → **gateway rev `gigaton-gateway-00054-fmw`, 100% traffic, zero 5xx post-flip.**
- Prepared durable guard: commit `6a4eb3e` on gateway branch `fix/decision-engine-route-gigaton-platform-2026-05-27` fixes cloudbuild.yaml:52. **NOT PUSHED** — `gh`/git authed as bella-byte can't access `todd-gig/gigaton-gateway` (404). Todd must push w/ his GitHub auth + open PR, else next gateway Cloud Build redeploy re-reverts again.

So the marker's "keep decision-engine on gigaton-platform, do not revert" guidance was CORRECT all along — the issue was config drift, now resolved at runtime (and durably once the PR lands).
Still on carmen (sessions 2/3 DEFERRED, correct): INTELLIGENCE_SILO_URL / GIGATON_ENGINE_URL / SALES_OPERATING_SYSTEM_URL. Intentional-stay: connector-api / SIE gateway / mimi-whatsapp. Net-new on gigaton-platform: user-access / HME / ppeme / persona.
Aligns with [[sibling_fleet_state_and_mig_cancel_conflict_2026_05_26]] MIG-DEFER.

**Migration is NOT the blocker to "functional for users."** The gateway already serves users; finishing carmen→gigaton is a cost/ownership/sovereignty win, not a user-functionality gate. This re-frames the "binding constraint to all value generation" premise in [[migration_is_value_blocking_2026_05_25]].

## No-broken-paths audit result (8-item, per [[red_phone_v0_channels_gated_email_inplatform_only]])
Deployed FE = origin/main (Firebase Hosting on gigaton-platform, auto-deploy on merge). gigaton-platform.web.app + playadelcarmen.homes + acks.playadelcarmen.homes all 200.
- PASS: /cowork (TierBadge+RoutingReasonsAccordion), /admin/review-queue (pool chips+empty state), NavRail 5 circles (tooltip, real routes), /v1/intelligence/query (fail-soft, graceful 200 for default op), Connector Hub silent-400 (X-Client-Namespace injection centralized in apiClient.ts #42; resolver backed by client_namespaces+seeds), onboarding (zero red-phone/SMS deps).
- MINOR: /founder/signoff renders+empty-state but `pool` field not wired in FE interface.
- DARK-BUT-NOT-BROKEN (unbuilt, not exposed → no broken path): Red Phone config UI absent; red-phone-engine has NO ENABLED_CHANNELS allowlist + silently filters channels (no clean reject) + only sms.py adapter (email/in_platform NOT built); expert_escalation.py exists (5-class, 31 tests) but NOT wired into operator-api integration_hooks.py; fire_red_phone helper only on `feat/emergency-class-wiring` branch (unmerged); `tier` field NOT in intelligence response so TierBadge stays dark even with flag on; INTELLIGENCE_SYSTEM_ROUTING off by default.

**Verdict: core platform is functional end-to-end with no broken paths today.** The intended Red Phone v0 (email+in_platform) deployment from the resume doc is the real next build increment, not the migration.
