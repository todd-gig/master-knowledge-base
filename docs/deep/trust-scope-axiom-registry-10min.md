# Trust, Scope, and the Axiom Registry — Deep Dive (10-minute read)

This deep dive explains the structural role of the Axiom Registry inside the Gigaton decision-engine, how a scope contract becomes a per-operator enforcement boundary, and how Stage 0 interacts with the rest of the platform. It assumes you have already read the `why_1min` and `what_3min` documents for Stage 0.

---

## 1. The Axiom Registry as decision-engine substrate

The Axiom Registry is a catalog of **inviolable rules** the platform enforces. Structurally it sits inside the decision-engine at `decision-engine/drift_sentinel/AXIOM_REGISTRY.md` and is loaded into memory as part of every decision-engine evaluation cycle.

When the decision-engine produces a recommendation, the recommendation flows through three filters before it is surfaced to a human or executed:

1. **Variable Registry** — does every variable the recommendation depends on exist for this operator with a value within the bounded range?
2. **Penrose Falsification Scoreboard** — does the recommendation move the operator's declared north star + supporting metrics in the right direction without crossing any constraint?
3. **Axiom Registry** — does the recommendation violate any axiom this operator has acknowledged?

A recommendation that fails (3) is **blocked at the engine, not at human review**. The axiom is treated as a hard guardrail. The scope contract is what makes that filter operator-specific: an axiom this operator never acknowledged (because it lives outside their jurisdiction, say) doesn't get applied to their decisions.

The Axiom Registry's structural role: **inviolable guardrail enforced by the decision-engine, scoped per operator by the scope contract.**

## 2. Severities and what they bind to

Each axiom carries a severity:

- **CRIT** — platform-level inviolable. A recommendation that would violate a CRIT axiom is blocked and the attempt is logged to `drift_sentinel`. CRIT axioms are platform-wide; they cannot be unacknowledged.
- **MAJ** — major. Treated as a hard constraint within scope. Unacknowledged MAJ axioms generate a warning in the chat side panel; the stage cannot complete until the operator either acknowledges or formally flags conflict.
- **MIN** — minor. Recommended best practice; non-acknowledgement does not block stage completion.
- **INFO** — informational. Used to surface platform conventions; no enforcement.

Stage 0's `acknowledge-axioms` action requires `CRIT: all` and `MAJ: all`. MIN and INFO axioms can be deferred without blocking the stage.

## 3. Why acknowledgement is required (instead of a one-way disclosure)

A disclosure-only model would let the operator skip the registry entirely; the platform would have no signal that any axiom applied. Acknowledgement does two things:

- **Captures consent** — an explicit row in the `axiom_acknowledgements` table proves the operator saw and accepted each axiom in scope.
- **Captures conflict** — when an axiom genuinely doesn't apply (a US-only operator and a GDPR-scoped axiom, for example), the operator can flag conflict with a reason. The decision-engine then skips that axiom for this operator's recommendations.

The second capability is the bigger one. Without it, the Axiom Registry would be a one-size-fits-all rulebook that produces false-positive blocks for every operator outside the original scope. With it, the registry becomes a **per-operator enforcement boundary** that reflects the operator's actual context.

## 4. Jurisdiction selection → downstream consequences

The `select-jurisdictions` action drives **every later compliance check + data-residency choice**. Specifically:

- **Stage 1 (Sources)** — which Google Drive accounts may be ingested; which countries the ingested artifacts may be stored in (data-residency bucket selection in intel-silo).
- **Stage 2 (People)** — which lawful basis applies for processing each person's behavioral data; whether explicit consent must be captured.
- **Stage 8 (Tech Stack + Costs)** — which billing providers can be connected (jurisdictional payment-processor coverage); which OTA connectors are even available.
- **Stage 9 (Calibration → Live)** — which auto-execute classes are permitted in this jurisdiction (e.g., outbound marketing automation in jurisdictions with strict opt-in rules).

Jurisdiction is not a label — it is a routing key for compliance machinery across all later stages. Pick it carefully.

## 5. The scope contract as cryptographic artifact

The `sign-scope-contract` action produces a record with the following shape (simplified):

```
{
  operator_id: <uuid>,
  legal_entity_record_id: <uuid>,
  jurisdictions: [<iso-3166>...],
  regulated_frameworks: [<framework>...],
  acknowledged_axioms: [{axiom_id, severity, status: acknowledged|flagged, reason?}...],
  contract_text_sha256: <hex>,
  signature: <ed25519 signature over the above by the operator's session key>,
  signed_at: <ISO-8601>
}
```

A **signed copy is stored in the operator's namespace** — specifically in the UAE `scope_contracts` table, scoped by `operator_id`. The `signed_at` field is what the activation gate predicate (`$.signed_at is_not_null`) reads. The signature is verifiable end-to-end against the operator's session public key, which is why "cryptographic acknowledgement" is more than a slogan: it survives downstream argument over what was acknowledged when.

## 6. Why Stage 0 must precede Stage 1

The order is enforced by the manifest's `entry_signal` on Stage 1 (`prior_stage_completed: stage-0-trust-scope`). The reason is structural: every Stage 1 ingest call attaches the resulting artifact to `operator_id` and queries the scope contract for permitted jurisdictions, regulated frameworks, and acknowledged axioms. If the scope contract doesn't exist, the attach has no rules to enforce against, and the resulting compliance debt is silent (no warning fires at ingest time; the violation only surfaces when an auditor or a regulator asks the question months later).

The cost of silent compliance debt averages **$12k per operator** to retrofit. Stage 0 prevents it by making the rules explicit before any artifact lands.

## 7. Workflow overlays cannot bypass Stage 0

`overlay_schema.inviolable_stage_ids` is server-enforced and constant:

```
inviolable_stage_ids: [stage-0-trust-scope, stage-9-calibration-live]
```

Any `workflow_overlays` JSONB that tries to hide, reorder away, or otherwise skip Stage 0 is rejected by the resolver inside `gigaton-gateway/app/onboarding/resolver.py`. There is no operator-side configuration that removes Stage 0 from the sequence. The same applies to Stage 9 — the two anchors are the entry and exit gates of onboarding.

## 8. Recovery paths

A handful of recovery paths exist if Stage 0 goes off the rails:

- **Wrong legal entity declared** — re-fire `ScopeIdentityDeclared` with the corrected payload. UAE rewrites `legal_entity_record`; the prior version is archived in `legal_entity_record_history`. The scope contract must then be re-signed because its hash changes.
- **Missed jurisdiction** — re-fire `ScopeJurisdictionsSelected`. Same archival pattern. Stage 1 ingest is paused for the operator until the re-sign completes.
- **Axiom that should have been flagged was acknowledged** — fire `AxiomAcknowledgementWithdrawn`. The platform re-evaluates any pending recommendations against the updated set and re-files the scope contract.
- **Scope contract signed under wrong key** — operator generates a new session key, then re-fires `ScopeContractSigned` with the new signature over the existing payload. The old signed copy is retained for audit.

All recovery paths re-emit the same `StageCompleted` event when the contract returns to a valid state; the downstream stages re-validate their assumptions automatically.

## 9. Edge cases

- **Multiple jurisdictions** — fully supported; the platform takes the union of all applicable rules per artifact.
- **Conflicting axioms across jurisdictions** — the platform applies the strictest acknowledged rule. If two acknowledged axioms genuinely conflict (rare, but possible across regulators), the decision-engine raises a `DoctrineConflict` event for human review; recommendations dependent on the conflicting domain are paused.
- **Operator changes jurisdictions later** — supported via the recovery path above. The scope contract is re-signed; all artifacts created under the old jurisdictions are tagged with their original scope (so a later audit can prove which rules applied when).
- **Regulated framework added mid-flight** — same pattern: re-fire `ScopeIdentityDeclared` with the framework appended; re-sign.

## 10. Stage 0 in the gamification system

Stage 0 emits a `Trust Anchored` badge on completion. It is **not streak-eligible** — it's a one-shot achievement, not a daily cadence. The fallback predicted-influence is **$4,500**; PPEME may override with a live prediction once the operator's industry + size are known.

The PPIM signature for the stage:

- **interaction**: governance + compliance posture
- **economics**: prevents avg $12k compliance retrofit cost
- **predictability**: foundational
- **brand_dimension**: integrity + legitimacy

That dimensionality — integrity + legitimacy — is what every later stage compounds against. Without it, the rest of PPIM is unreachable.
