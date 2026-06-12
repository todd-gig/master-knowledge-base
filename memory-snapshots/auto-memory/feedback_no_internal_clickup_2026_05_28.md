---
name: feedback-no-internal-clickup-2026-05-28
description: "Gigaton internal systems do not depend on ClickUp. External clients (Multipli, CBP, etc.) may run their own ClickUp boards, but Gigaton's own state/gates/deliverables/orchestration are 100% Gigaton-native. No internal ClickUp mirroring, no clickup_task_id in internal tables, no ClickUp-named internal services."
metadata: 
  node_type: memory
  type: feedback
  established: 2026-05-28
  status: ACTIVE doctrine
  originSessionId: c3d6a014-f8e0-4829-9d0d-6197cc8ac3f6
promoted_from: feedback_no_internal_clickup_2026_05_28.md
promoted_at: 2026-06-02T20:13:25Z
---

# Feedback — No internal ClickUp dependency

**Rule:** Gigaton-internal systems do not integrate with, mirror to, or depend on ClickUp. ClickUp may be observed (external clients use it) but Gigaton's own gate decisions, deliverables, phase tracking, audit logs, and orchestration are 100% Gigaton-native.

**Why:** Todd directive 2026-05-28 during Phase Gate ratification: *"remember to ignore any tasks related to internal utilization of clickup by gigaton"*. The platform must own its state of record outright; dependence on a rented PM tool for internal coordination would couple platform velocity to a vendor and confuse the D2 sovereignty contract (Gigaton owns opinions, vendor MCPs handle raw CRUD only when externally directed).

**How to apply:**

- **Do not** add `clickup_task_id` columns to internal Gigaton tables.
- **Do not** build async mirrors (Pub/Sub subscribers, webhooks) that sync internal state to ClickUp.
- **Do not** call `mcp__claude_ai_ClickUp__*` from server-side Gigaton code for internal coordination. (The MCP is fine when external clients explicitly request a ClickUp action on their own board.)
- **Do not** name new internal Gigaton services / packages / modules with "clickup" in the name.
- **Rename follow-up:** `gigaton-clickup-phase` MCP server (35/35 tests passing, pre-built) is now misnamed for its actual role (internal Phase Gate). Plan a rename to `gigaton-phase` post-Phase-Gate-deploy. Do not rename mid-build — server still calls the three /v1/phase/* endpoints correctly under its current name.
- **Do** continue to use ClickUp externally for clients who already have ClickUp boards; do not unilaterally migrate them off.
- **Edge case:** if an external client's onboarding asks Gigaton to mirror their ClickUp into a Gigaton dashboard view, that's client-directed and allowed — but the mirror is a per-client connector configuration, not an internal Gigaton system dependency.

**Impact on prior decisions:**

- §9.3 of [[phase-gate-ratification-2026-05-28]] = DROPPED (no v0 mirror, no v1 mirror).
- §9.4 of same = NO bulk-import of Phase 1 ClickUp tasks (Phase 1 deliverables created Gigaton-native via `POST /v1/phase/deliverables`).
- D2 sovereignty contract ([[D1-D2-MIG-DEFER-ratified-2026-05-26]]) is REINFORCED, not contradicted: Gigaton owns opinions, vendor MCPs handle external CRUD when externally directed.

**Cross-refs:** [[phase-gate-ratification-2026-05-28]], [[mcp-master-tool-list-2026-05-26]] (re ClickUp MCP server availability for external use), [[audit-and-value-delivery-plan-2026-05-28]] §III (Phase Gate now ships ~3.5d not 4-5).
