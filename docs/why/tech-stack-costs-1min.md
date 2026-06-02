# Why Stage 8 — Tech Stack + Unit Economics + Financial Audit (1-minute read)

**PPIM expands to "predictably PROFITABLE interaction management of a gigaton engineered brand experience" — and profitability requires knowing what every atomic action actually costs.** Stage 8 is where the cost side gets backfilled.

The platform has been recommending, drafting, projecting, and assigning since Stage 4. None of those activities are free: each one has an LLM cost, an API cost, a human-time cost. Without Stage 8, those costs are invisible to the operator and to the decision-engine, which means every Stage 4-7 recommendation has been graded on lift alone, not on lift-minus-cost. **Profitability requires knowing what every atomic action actually costs.**

Stage 8 has three structural functions:

- **Inventory every 3rd-party tool** the operator pays for — Stripe, Twilio, Anthropic, Google, OTAs, Slack, the long tail.
- **Connect billing** so the platform can ingest actual invoices and bank transactions (read-only access only — no write authority requested).
- **Register credentials** for each inventoried tool so the platform can use them on the operator's behalf in tier_5_live.

**Stage 8 backfills unit economics across all prior stages.** The decision-engine re-grades every active recommendation against actual cost-per-atomic-action; the Influence vs Cost dashboard turns on; Penrose scores now reflect lift-minus-cost instead of lift alone.

**True**: the Influence vs Cost dashboard turns on as a result of Stage 8 completion. It is the visible artifact of `tier_4_costs` closing.

The activation gate has two predicates: `tools_with_unit_cost_pct >= 80` (cost coverage of the inventoried tool set) AND `invoice_days_ingested >= 90` (90 days of billing history). Both must hold. 90 days is the empirical floor for stable unit-economics inference; below 90, seasonality and one-off spikes distort the picture.

Credentials are stored in **per-operator Google Secret Manager** with a strict naming pattern. The credential paste affordance is masked end-to-end: values are never echoed back, never logged in the transcript, never sent to the LLM router. Pre-storage validation against the provider's API ensures bad credentials don't land in Secret Manager.

If you only remember one thing: **PPIM is profitable, not just predictable. Stage 8 is where "profitable" stops being a slogan and starts being measured against actual cost per atomic action.**
