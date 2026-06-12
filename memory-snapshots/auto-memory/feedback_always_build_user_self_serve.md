---
name: always-build-user-self-serve-not-admin-manual
description: "When implementing any platform feature that requires configuration / credentials / integration / wiring, build the user-facing self-serve flow (FE + API + validation + activation + gamification) instead of asking the user to run Console / gcloud / CLI commands manually. Default to \"user can wire it themselves through the platform UI.\" Admin-manual is the exception, not the norm."
metadata: 
  node_type: memory
  established: 2026-05-19
  priority: 1
  type: feedback
  originSessionId: cc574db0-93f4-4776-b0fe-dc7253ec52fc
  lifecycle_state: active
  state_set_at: 2026-05-19
  state_set_by: auto-migration-concept-8
promoted_from: feedback_always_build_user_self_serve.md
promoted_at: 2026-06-02T20:13:25Z
---

## The rule

For ANY feature that requires configuration to activate (credentials, API keys, integrations, OAuth handshakes, webhook URLs, business identifiers), the deliverable is the **full self-serve loop**, not the engine code alone:

1. **FE surface** — a page or card on the platform UI where the user enters values
2. **BE endpoint** — accepts the values, validates them (typically by pinging the upstream service), persists them encrypted with operator_context scoping
3. **Activation path** — the engine consuming those values reads from the per-operator store (NOT from process-level env vars / Secret Manager set by the platform team)
4. **Status indicator** — user can see "connected ✓" / "disconnected" / "needs reauth" on the connector card
5. **Test flow** — explicit "test connection" button + success/failure feedback inline
6. **Gamification** — progression event when user successfully connects (per [[feedback_always_include_gamification]])
7. **Disconnect / rotate** — user can revoke / re-enter credentials without admin involvement

## Why

- **PPIM doctrine**: the user IS the operator; the platform serves them. Asking the user to run gcloud commands inverts the relationship.
- **Universal Connector Hub architecture**: the entire product premise is "user logs in once, connects every 3rd-party through one UI." Admin-manual integration paths CONTRADICT this premise.
- **Engine Artifact equation** (`value = f(user, org, platform.intelligence, resources.available)`): `resources.available` includes user-owned credentials. Those resources are unlockable only when the user can self-serve.
- **Friction = lost adoption**. A user who has to copy SIDs from one Console into another Console will not adopt — they'll abandon and the feature dies.
- **Multi-operator scaling** (per [[foundational_modular_replication_via_input_substitution]]): admin-manual wiring forces N config steps per N operators; user-self-serve scales infinitely with zero operator-time cost.

## How to apply

**When adding ANY new integration / engine / connector**, the v0 PR must include all 5 layers:
- Engine code with operator_context-scoped credential reads (NOT env-var globals)
- Per-operator credential storage table + encryption
- API endpoints for connect / test / disconnect / status
- FE page or card with form + test button + status pill
- Gamification event on successful connect

**Standard pattern**: register the connector in the Connector Hub catalog. Card on `/connectors`. Click → setup wizard → form → test → activated. Inline help links to provider's where-to-find-this-key docs.

**Exceptions** (when admin-manual is genuinely required):
- GCP project creation / billing / root IAM bootstrap
- Domain ownership verification (one-time per domain)
- DNS records the platform CAN'T set programmatically (those go to operator-managed Google Cloud DNS too — but the platform should still own as much as it can via API)

**Anti-patterns to avoid:**
- "Wire these secrets in Secret Manager Console then redeploy" — NO. Build the UI.
- "User runs this gcloud command" — NO, unless it's a true bootstrap step.
- "v0 ships with hardcoded operator creds, v1 adds the UI" — NO. The UI IS the v0.
- Service-level env-var credential storage (single set of creds for all operators) — NO. Per-operator from day one.

## Concrete pattern reference

See WhatsApp connector flow built 2026-05-19 (Mimi service + `/connectors/whatsapp` page + `operator_credentials` table + per-operator credential reads in Mimi) for the canonical example of the full 5-layer self-serve loop.

## When the rule was established

2026-05-19 mid-session — Mimi WhatsApp v0 shipped with admin-manual Secret Manager wiring instructions. Todd corrected: "create the UI + process for a user to connect their credentials to whatsapp + always remember to create user functionality when possible." This memory captures the correction as a universal rule.

## Companion doctrine — directed workflow

A self-serve UI alone is necessary-but-insufficient. The operator also needs to KNOW the feature shipped, KNOW where to find it, KNOW the order of operations, and KNOW how to verify it's working. That is the job of [[feedback_directed_workflow_required_for_every_deploy]] (est. 2026-05-20) — every feature that ships under this self-serve doctrine MUST also ship a directed workflow entry in `gigaton-ui-system/services/directedWorkflows.ts`. Self-serve UI + directed workflow together = the operator can implement the feature without help.
