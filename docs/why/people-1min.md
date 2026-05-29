# Why Stage 2 — People & Human Data (1-minute read)

**PPIM expands to "predictably profitable INTERACTION MANAGEMENT of a gigaton engineered brand experience."** Interaction management is the second word in the acronym. Without identified people and a behavioral snapshot per person, every interaction the platform manages is **generic** — and generic interactions are the opposite of PPIM.

Stage 2 is where the platform learns who the operator interacts with — internal team, customers, vendors, regulators, prospects — and captures a Behavioral & Functional Type (BFT) snapshot for each one. The BFT snapshot is the substrate every later personalized communication is built on.

Without a BFT snapshot per person, the persona-engine has no model of that person's preferences, dispositions, or communication style. Every message the platform helps draft falls back to a generic template. The chat side panel surfaces this honestly: until Stage 2 completes, the "personalized compose" capability stays locked, and the operator sees "person not profiled — generic template only" on any draft.

**After Stage 2 completes, personalized communication becomes available.** Specifically, the platform unlocks:

- `gigaton.communication.personalized_compose` — drafts written in the operator's voice, tuned for the specific recipient's BFT profile.
- `gigaton.persona.read_bft_snapshot` — read access to the snapshot per person, so the operator can see what model the platform is using to personalize.

The economic estimate is **$2-5k/month in communication-quality lift from personalization**. The mechanism is straightforward: a response that lands the way the recipient prefers to receive it converts at a higher rate, escalates less often, and shortens cycle time. Across an operator's full interaction surface that compounds quickly.

The Stage 2 activation gate requires both `human_persona_count >= 3` AND `bft_snapshots_available_count >= 3`. Three is the floor — below it, the persona-engine doesn't yet have enough population data to seed cross-person comparisons. Above it, the platform can start reasoning about your relationship network.

If you only remember one thing: **PPIM is interaction management. Stage 2 is where interactions become people-shaped instead of template-shaped.**
