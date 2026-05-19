# The Gigaton Constitution

**Version**: v1.0.0-draft
**Status**: DRAFT awaiting triad sign-off (Todd + Matt + Bella)
**Established**: 2026-05-19
**Companion**: machine-readable Axiom Registry at `decision-engine/drift_sentinel/AXIOM_REGISTRY.md`

## Preamble

We, the operators, contributors, and stewards of Gigaton, commit to one purpose:

> Facilitate Predictably Profitable Interaction Management of a Gigaton Engineered Brand Experience.

This document encodes the inviolable rights, inviolable obligations, decision authority, amendment procedure, and enforcement that govern every action across the Gigaton ecosystem.

## Article I — North Star

§1.1 — Mission: Facilitate Predictably Profitable Interaction Management (PPIM) of a Gigaton Engineered Brand Experience — instrumenting every customer interaction with known economics, bounded predictability, and coherent brand signature so that profit is the natural consequence of value delivered.

§1.2 — Vision: A universal connector and intelligence layer where any qualified operator, by connecting their stack once, gains a methodology-driven co-pilot that compounds reusable intelligence across the network while preserving each operator's agency, data ownership, and brand voice.

§1.3 — Operating Sequence: Connect → Create → Thrive → Evolve.

§1.4 — Doctrine: Technology must serve human flourishing, empowerment, and positive evolution. Where technology and human agency conflict, human agency wins.

## Article II — Inviolable Rights

§2.1 — Operator Agency. Operators retain final authority over: production deployments, client-facing messaging, destructive changes, account/permission changes, and materially ambiguous business decisions.

§2.2 — Contributor Compensation. Contributors are compensated based on the Value of Human Contribution Matrix (time, effort, uniqueness, quality, relationships/network, risk reduction, increased probability of success). Compensation for reusable intelligence and network contribution is co-equal with compensation for tasks.

§2.3 — Customer Privacy. No customer data crosses client namespace boundaries without explicit consent. Credentials live exclusively in SecretStore.

§2.4 — Data Ownership. Operators retain ownership of their connected data and reusable intelligence derived from their workflows; Gigaton retains licensing rights for the platform-level abstractions.

§2.5 — Transparent Economics. Every interaction has a known PPIM signature: cost per call, revenue attribution path, predictability bound, brand-experience dimension.

## Article III — Inviolable Obligations

§3.1 — PPIM Signature Requirement. Every module, engine, surface, and connector declares its PPIM signature.

§3.2 — Modular Replication via Input Substitution. The same engine must serve any qualified operator by swapping `operator_context` inputs — never by editing the engine.

§3.3 — SecretStore for Credentials. No credential lives in code, env-at-rest, or chat history.

§3.4 — No Cross-Tenant Contamination. Client namespaces are isolated; cross-namespace queries require explicit `X-Client-Namespace` headers and audit logging.

§3.5 — Always-Online Priority. Production engines deploy with `--min-instances=1`, `/health` and `/ready` endpoints, and CPU boost; "deployed but not responding fast" = functionally offline = urgent.

§3.6 — Universal Cost Telemetry. Every external call (Stripe / Twilio / Anthropic / OpenAI / Gemini / OTA / Slack / SendGrid / cloud-provider) writes to `third_party_call_cost`. Invisible cost is a violation.

§3.7 — Doctrine-Claim Verification. Any memory or doc claiming "X is shipped" must be verified against `main` before being relied upon by any decision system.

## Article IV — Decision Authority

§4.1 — Founder (Todd). Authority over: platform architecture, doctrine, schema, ethics, mission, and constitutional amendments.

§4.2 — Owner (Matt). Authority over: operations, feature scope, commercial pricing, and operator-facing experience.

§4.3 — Admin (Bella). Authority over: user provisioning, queue management, and approval routing.

§4.4 — Triad. Constitutional amendments and doctrine-touching framework promotions require unanimous triad sign-off OR per the triad-signoff-assumed-window protocol where Todd has authorization for in-window sign-off on Matt/Bella's behalf.

§4.5 — Human-in-the-Loop Boundary. Irreversible actions (production deploy / IAM grants / schema migrations / billing changes / force-push to protected branches / cross-tenant flow changes) require explicit human approval — no autonomous execution.

## Article V — Amendment Procedure

§5.1 — Proposals open via PR to this document on `master-knowledge-base`.

§5.2 — Discussion period: minimum 48 hours unless emergency.

§5.3 — Sign-off: triad unanimous OR per §4.4 in-window protocol.

§5.4 — Version bump: SemVer. Article-level changes = MAJOR. New §clauses = MINOR. Clarifications = PATCH.

§5.5 — Backport: every approved amendment generates an Axiom Registry update in the same PR cycle.

## Article VI — Enforcement

§6.1 — Machine enforcement via the Axiom Registry and Drift Sentinel: violations of axioms emit Cloud Logging records and `task_blocked` events on `gignet-orchestrator`.

§6.2 — Manual enforcement via the operator approval queue surfaced in `gigaton-ui-system /founder/signoff` and `/owner/proposals`.

§6.3 — Quarterly audit: founder reviews enforcement records each quarter; corrective amendments proposed.

§6.4 — Constitution and Axiom Registry are mirrored: `decision-engine/drift_sentinel/CONSTITUTION_MIRROR.md` exists for in-engine reference, kept identical to this canonical via CI check.

## Ratification

This draft awaits triad sign-off. Upon ratification, version flips to `v1.0.0` (drop `-draft` suffix), `Status` becomes `RATIFIED`, and the mirror is enabled.

— End of Constitution v1.0.0-draft —
