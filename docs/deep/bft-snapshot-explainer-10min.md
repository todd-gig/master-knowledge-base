# BFT Snapshot Explainer — Deep Dive (10-minute read)

This deep dive covers the BFT (Behavioral & Functional Type) snapshot that Stage 2 produces per person: what it captures, how the persona-engine constructs it, how classifications route downstream, and the edge cases that determine snapshot quality. It assumes you've read the `why_1min` and `what_3min` documents for Stage 2.

---

## 1. What a BFT snapshot captures

A BFT snapshot is the **behavioral profile** the persona-engine builds for each person an operator interacts with. It is not a CRM record. It captures:

- **Behavioral disposition** — preferred communication channel, response cadence (fast/slow), formality (terse/elaborate), risk tolerance (cautious/aggressive), decision style (consensus/unilateral).
- **Functional position** — the role the person plays in the operator's network (decider, influencer, blocker, gatekeeper, executor), their organizational power dynamic, the cadence at which they're engaged.
- **Interaction history features** — frequency of contact, last interaction recency, escalation history, conversion (for customer/prospect classifications), churn risk (for customer classification).
- **Latent preferences** — extracted from source documents in Stage 1: meeting transcripts, emails the operator wrote to them, contracts they signed, notes they appear in.

The snapshot is a **structured object** stored in the persona-engine. Every later platform action that involves this person reads the snapshot and adapts: drafted messages match their formality preference, channel selection matches their preferred channel, cadence matches their response window.

The single-phrase answer to "what does a BFT snapshot capture": **a behavioral profile** of the person, sufficient to personalize interactions.

## 2. How the persona-engine constructs the snapshot

Construction is a four-input synthesis:

1. **Source-document extraction** (from Stage 1 intelligence-silo bundle). The persona-engine runs NLP over every chunk that mentions the person. It extracts: tone the operator typically writes to them in, the topics that appear, the channel hints ("called Carlos on his cell"), the cadence ("we sync weekly").
2. **Operator's captured intent** (the one-sentence Stage 2 input). Parsed into features: relationship-type token, cadence-implied token, asymmetric-power-dynamic token, escalation-pattern token.
3. **Classification** (internal / customer / vendor / regulator / prospect). The classification is a routing key and a feature; it conditions how the rest of the snapshot is interpreted.
4. **Telemetry from past platform interactions** (if any). Operators in their second day on the platform have none of this; operators who've been live for a quarter have rich telemetry that overrides the source-extraction baseline.

The four inputs synthesize into a snapshot object with `confidence_score` per feature. Features with low confidence are flagged; the chat side panel exposes them to the operator with "I'm guessing X about this person — confirm or correct?" prompts.

## 3. Why one-sentence intents matter so much

The intent sentence is the single highest-signal input the persona-engine has, especially for new operators with no platform telemetry yet. Source-extraction is noisy (especially for people who only appear briefly in documents). Classification is a five-way enum. The intent sentence is the operator's *interpretation* of the relationship — the only signal that explicitly captures "what is this relationship FOR?"

The `capture-initial-intent` action drives **BFT scoring** — that is the verbatim phrase the manifest uses. Skipping it or writing vague sentences ("Carlos is helpful") produces snapshots with low-confidence features that don't deliver personalization. The orchestrator nudges the operator to be specific.

## 4. Classification routing — five paths

Each classification routes the person differently in later stages:

- **internal** → eligible for Stage 7 (Assignments) workflow ownership. HME treats this person as a candidate owner for org processes. Tier_2_personalized communications to them are drafted as internal-team voice (less brand-formal, more direct).
- **customer** → flows into Stage 3's ICP segment computation as a positive example. Lifecycle stage (from Stage 3's `define-lifecycle-stages`) is tracked. Stage 8's billing connectors look for transactions tied to this person.
- **vendor** → flows into Stage 8's tech-stack inventory as a pre-fill ("you mentioned Stripe; we found Stripe contact Anna in your people graph"). Drafted communications use vendor-formal voice. Compliance routing in Stage 0's acknowledged axioms applies.
- **regulator** → triggers extra compliance routing in every later send: drafted communications are flagged for human approval before send; all interactions are logged to a separate compliance-audit stream; the decision-engine treats this person's messages as inputs to the drift_sentinel.
- **prospect** → flows into Stage 3's ICP segment computation as a candidate. Lifecycle stage starts at `prospect`. Sales-OS (Stage 9 territory) treats them as eligible for outbound cadences once tier_3_recommend unlocks.

The five-way routing is the structural reason classification is required to be ≥3 — without classification coverage, the platform can't initialize the downstream routing.

## 5. The two-engine handoff (and why secondary engines are listed)

Stage 2 lists `secondary_engines: [intelligence-silo, human-management-engine]` for a reason:

- **intelligence-silo** sources the proposals in `review-proposed-people`. Without it, the operator would have to type every person from scratch. The handoff is one-directional: intel-silo proposes, persona-engine consumes.
- **human-management-engine** consumes the classified people in Stage 6 and Stage 7. Internal-classified people become workflow-ownership candidates; the HME initiatives table joins against `persona.classification = 'internal'`. The handoff is forward-looking — HME doesn't read persona-engine in Stage 2 itself, but the manifest declares the dependency because Stage 2's outputs are HME's prerequisites.

The owning engine (persona-engine) controls the activation gate; the secondary engines participate but don't gate.

## 6. Why predictability is MEDIUM and not HIGH

The PPIM signature lists Stage 2 as **predictability: MEDIUM (depends on BFT snapshot quality)**. Most stages are HIGH. The MEDIUM tag is honest:

- High-quality snapshots → personalization that lifts conversion, reduces escalations, shortens cycle time. The $2-5k/month payoff is real.
- Low-quality snapshots → personalization that misfires. A platform that drafts a casual message to a regulator because the BFT confidence on formality is wrong is worse than no platform at all.

The MEDIUM tag is a flag to the operator: **the value of Stage 2 is operator-quality-controlled**. Time spent on thoughtful intent sentences pays back. Skipping or rushing the action under-delivers.

The platform mitigates by flagging low-confidence features explicitly, by running a re-check loop in Stage 9's calibration, and by allowing the operator to correct snapshots at any time from the `/people` nav circle.

## 7. Edge cases

- **Person has multiple roles** (an internal person who is also a customer of a different product line). Supported via classification arrays: `classifications: ['internal', 'customer']`. Routing applies the union of all classifications. BFT snapshots stay singular but carry context per classification.
- **Person appears in sources but operator doesn't recognize them.** Reject the proposal card. The persona-engine logs the rejection and de-prioritizes that person in future scans of the same source.
- **Operator wants to add a person who doesn't appear in sources.** The chat surface lets the operator say "add a person" directly; the persona-engine accepts a manual PersonaCreated with operator-supplied attributes (no source-extraction step).
- **Person's classification changes** (a prospect becomes a customer). Fire `PersonaClassificationChanged`. The BFT snapshot's classification field updates; lifecycle stage advances; downstream routing adapts. No re-onboarding required.
- **Operator has hundreds of people.** Stage 2 only requires 3 to advance. The operator continues adding people from the `/people` nav circle after Stage 2 closes; each new person produces a BFT snapshot under the same construction pipeline.

## 8. Privacy and per-operator isolation

BFT snapshots are per-operator. There is **no cross-operator persona graph**. Operator A and Operator B may both have a relationship with the same person (e.g., the same Stripe support rep); each operator has their own BFT snapshot for that person, derived from their own sources and intents. The persona-engine never reads across operator boundaries.

This is enforced at the storage layer (per-operator schemas in the persona-engine database) and at the API layer (every persona-engine endpoint requires `X-Client-Namespace`; cross-namespace reads are rejected by the gateway resolver).

## 9. The chat affordances revisited

The manifest's `chat_orchestration.affordance_resolution` ties events to UX:

- `PersonaCreated` → `proposed_review_cards` (carousel with Accept/Edit/Reject).
- `PersonaIntentCaptured` → `free_text` (conversational input).
- `PersonaClassified` → `multiple_choice` (button group).

No per-stage override is needed; the default derivation covers all three actions. The orchestrator picks the affordance based on the event the activation gate is waiting on, then renders the action as a rich chat bubble.

## 10. The relationship to Stage 9's graduation gate

Stage 9's evidence-based graduation includes `interactions_logged_count` as one of the four verification dimensions. Interactions are logged against people; people without BFT snapshots produce interactions with empty personalization features, which depresses the OVS-Calibration scoring. An operator who only created the bare-minimum 3 personas in Stage 2 typically takes longer to clear Stage 9's interaction-count threshold than one who built out their full people graph.

The lesson is not "create more personas to game the graduation gate" — it's "BFT snapshots compound; the operator who invests in Stage 2 graduates faster and stays graduated more reliably."

## 11. The PPIM signature, restated

- **interaction**: every later comm is now person-targeted
- **economics**: avg $2-5k/mo communication-quality lift from personalization
- **predictability**: MEDIUM (depends on BFT snapshot quality)
- **brand_dimension**: responsiveness + relevance

"Responsiveness + relevance" is what BFT-personalized interaction looks like from the receiver's perspective: messages that arrive on the channel they prefer, in the tone they expect, at the cadence they tolerate. That's what PPIM's "interaction management" is engineering for.
