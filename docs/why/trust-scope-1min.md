# Why Stage 0 — Trust & Scope Anchor (1-minute read)

**Stage 0 is the foundation every later stage attaches to.** Before Gigaton can ingest a single document, draft a single recommendation, or send a single message on your behalf, it has to know two things:

1. **Who is operating** — the legal entity, where it's incorporated, and which regulated frameworks (HIPAA, GDPR, FINRA, PCI, etc.) apply.
2. **What it agrees to** — the inviolable rules captured in the Gigaton **Axiom Registry**.

Every artifact recorded after this point — every ingested file, every persona, every decision — attaches to your **scope contract**. **Without it, ingestion creates silent compliance debt.** That debt typically surfaces months later as an emergency retrofit averaging $12k per operator. Stage 0 prevents that.

The Axiom Registry is not a disclosure modal. It is the catalog of rules the platform actively enforces against every decision the decision-engine produces. By acknowledging each axiom — and flagging any that conflict with your specific context — you turn the registry into a **per-operator guardrail**. Decisions that would violate an acknowledged axiom are blocked at the engine, not at human review.

Stage 0 must precede Stage 1 (Sources) because **compliance posture determines what data may be ingested, from where, and where the resulting artifacts may be stored** (data-residency). Skipping it would mean Stage 1 pulls data the operator wasn't permitted to ingest.

The output of Stage 0 is a cryptographically signed scope contract stored in your operator namespace, a non-null `legal_entity_record`, a jurisdiction list, and acknowledgement rows for every CRIT-severity and every MAJ-severity axiom. **Stage 0 partially unlocks `tier_1_data`**; Stage 1 closes it.

If you only remember one thing: **Stage 0 is the only moment in onboarding where the operator declares its identity and accepts the rules of the system. Everything downstream assumes those declarations are true and binding.**
