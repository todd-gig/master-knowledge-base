# Ethnographic Research and Optimization

**User:** Todd Nelson (todd.cx@turtleisland.solutions)  
**Created:** 2/10/2026 16:54:07  
**Updated:** 2/27/2026 1:42:53  
**Exported:** 3/19/2026 16:24:48  
**Link:** [https://chatgpt.com/g/g-p-6882aa12c04c8191b859fd11dc4e66da-gigaton/c/698ba8bb-5424-832e-a9c1-5f84507f088b](https://chatgpt.com/g/g-p-6882aa12c04c8191b859fd11dc4e66da-gigaton/c/698ba8bb-5424-832e-a9c1-5f84507f088b)  

## Prompt:
explain how ethnographic research and the rule of 7s in psychology + math are able to integrate into actionable code engineered to utilize recursive logic to engineer & instantly optimize systems based on user input and known accuracy variances constantly being tested in real time

## Response:
What you’re building (in one line)
----------------------------------

A **closed-loop optimization engine** that converts **ethnographic signals** (why people do what they do) + **Rule of 7s** (how much people can reliably process) + **math** (uncertainty + optimization) into **recursive code** that continuously improves a system with **measurable confidence**.

* * *

1) Ethnographic research → machine-readable primitives
------------------------------------------------------

Ethnography produces **qualitative truth** (context, motivations, constraints). To make it executable, you transform it into a **structured evidence graph**.

### Ethnographic → data model mapping

*   **Actor** (persona / role)
*   **Job-to-be-done** (desired outcome)
*   **Context** (where/when conditions)
*   **Trigger** (what initiates behavior)
*   **Constraint** (time, money, policy, cognitive load)
*   **Friction** (what causes drop-off)
*   **Workaround** (shadow process = hidden requirements)
*   **Language tokens** (verbatim phrases → intent signals)
*   **Value tradeoffs** (speed vs accuracy vs cost, etc.)

### Output: “Ethno-Objects”

Store each as a record with:

*   `claim` (what you believe is true)
*   `evidence` (source, quote, observation)
*   `scope` (who/when it applies)
*   `confidence` (initially subjective, later learned)
*   `impact` (if true, what it changes)

This becomes a **causal feature store** the system can reason over.

* * *

2) Rule of 7s → UX + prompting constraints (a hard system boundary)
-------------------------------------------------------------------

The Rule of 7s is your **interaction budget**: humans can’t reliably process large branching complexity in one shot. In code terms, it becomes a **constraint function** that governs how your engine asks questions, presents options, and sequences steps.

### Enforceable constraints

*   **Max 7 items** per screen / decision list
*   **Max 7 required fields** per step
*   **Chunking**: split workflows into “micro-commits”
*   **Progressive disclosure**: only reveal complexity when needed
*   **Error recovery**: reduce cognitive load when uncertainty is high

### Why this matters for optimization

If you violate cognitive load constraints, you corrupt your data:

*   Higher abandonment
*   More random answers
*   Lower signal-to-noise  
    So the Rule of 7s is not “nice UX”—it’s **data integrity enforcement**.

* * *

3) Math → optimization under uncertainty (accuracy variances included)
----------------------------------------------------------------------

You need math for two reasons:

1.  **Decide what to change** (optimization)
2.  **Decide how confident you are** (uncertainty / variance)

### Core math components

*   **Belief model**: every claim/assumption has a probability distribution, not a boolean.
*   **Objective function**: what “better” means (e.g., conversion, time-to-complete, cost, risk).
*   **Constraints**: compliance, budgets, cognitive load (Rule of 7s), latency, policy.
*   **Exploration vs exploitation**: test new variants without tanking outcomes.
*   **Causal attribution**: avoid optimizing on correlated noise (ethnography helps here).

### Practical modeling choices (fast ROI, scalable later)

*   Start with **Bayesian updating** or **multi-armed bandits** for variant selection.
*   Layer in **causal graphs** (from ethnography) to reduce false optimizations.
*   Use **confidence intervals** to decide when a “win” is real.

* * *

4) Recursive logic → the engine that “re-asks” and “re-writes” itself
---------------------------------------------------------------------

Recursive logic here means: the system repeatedly executes a loop where outputs become new inputs.

### The loop (UDO/OODA style)

1.  **Observe**: collect user inputs + telemetry (drop-offs, time, errors, corrections)
2.  **Orient**: map to ethno-objects + context; compute uncertainty and constraint violations
3.  **Decide**: choose next best question / workflow step / variant to test
4.  **Act**: render next UI step; deploy variant; log outcomes
5.  **Update**: revise confidence weights, feature importance, and next-step policy

This is recursion because:

*   Each step calls the same decision function with an updated state.
*   The “question strategy” is learned and re-optimized continuously.

* * *

5) “Instant optimization” without lying to yourself
---------------------------------------------------

You can optimize instantly **at the interaction layer** (sequence, phrasing, defaults, routing) while acknowledging that deeper truths require evidence accumulation.

### Two-speed system

*   **Fast loop (session-time)**: optimize flow using bandits + heuristics (low risk)
*   **Slow loop (across sessions)**: update causal assumptions, persona models, and business rules (higher leverage)

This is the best long-term ROI approach: immediate uplift + compounding learning.

* * *

6) The actionable code architecture
-----------------------------------

Implement as modular services so it’s production-grade and testable.

### A. Schema layer (ethnography as code)

*   `EthnoObjectStore` (claims, evidence, scope, confidence, impact)
*   `ContextGraph` (persona → jobs → constraints → frictions → recommended interventions)

### B. Interaction orchestrator (Rule of 7s gatekeeper)

*   `ChunkPlanner(state) -> next_questions[<=7]`
*   `DisclosurePolicy(uncertainty, risk) -> depth_level`
*   `ValidationPolicy` (detect low-quality answers, ask follow-ups)

### C. Decision engine (math + recursion)

*   `StateEstimator` (builds belief state)
*   `PolicySelector` (chooses next action)
*   `VariantAllocator` (bandit / A/B allocation)
*   `ConfidenceUpdater` (Bayes / posterior updates)

### D. Real-time testing + telemetry

*   Event stream: `view`, `click`, `time_on_step`, `edit`, `abandon`, `success`
*   Metrics: conversion, completion time, error rate, satisfaction proxy
*   Per-segment analytics: persona/context-specific performance

* * *

7) “Known accuracy variances constantly tested in real time”
------------------------------------------------------------

Treat every input as noisy and every segment as different.

### Where variance comes from

*   Persona differences
*   Context differences (device, time pressure, stakes)
*   Question phrasing effects
*   Fatigue / cognitive overload
*   Incentive misalignment (people “game” forms)

### How to code for it

*   Maintain **per-segment confidence** (persona × context × channel).
*   Track **answer stability** (does user revise later?).
*   Use **consistency checks** (lightweight, Rule-of-7-compliant).
*   Trigger **adaptive questioning** when uncertainty spikes.

* * *

8) Minimal pseudocode (conceptual)
----------------------------------

```
function run_step(state):
  context = infer_context(state.inputs, state.telemetry)
  beliefs = update_beliefs(state.beliefs, state.inputs, evidence_store, context)

  constraints = evaluate_constraints(beliefs, context)  // includes Rule-of-7s
  action_space = generate_actions(beliefs, constraints)

  action = select_action(action_space, beliefs.uncertainty) // bandit/optimizer
  ui_payload = build_ui(action, max_items=7)

  return ui_payload, new_state_after_logging()
```

* * *

What this gives you (business outcome lens)
-------------------------------------------

*   **Higher-quality inputs** (cognitive-load constrained capture)
*   **Lower CAC / higher conversion** (flow optimizes in-session)
*   **Compounding advantage** (ethnographic truth becomes proprietary causal priors)
*   **Risk-managed automation** (confidence-weighted decisions, not brittle rules)
*   **Long-term ROI**: the system becomes an asset that improves its own throughput and accuracy over time.

If you want this operationalized next: the fastest path is defining (1) the ethno-object schema, (2) the interaction “7s” policy, and (3) the initial objective function + telemetry events—then you can ship a working recursive optimizer in a thin vertical slice.

## Prompt:
utilize the liquifex project to create an ethno-object schema

## Response:
LiqueFex Ethno-Object Schema (v1)
---------------------------------

Design goal: convert qualitative field data (calls, interviews, shadowing, tickets, emails, deal notes) into **machine-actionable causal records** that drive **routing, UX, policy enforcement, and optimization** inside the LiqueFex OS.

* * *

1) Ethno-Object types (canonical taxonomy)
------------------------------------------

Use these as `object_type` enums:

1.  **ACTOR** – who is involved (role/persona + incentives)
2.  **JOB** – outcome they are hiring the system to achieve (JTBD)
3.  **CONTEXT** – conditions that shape behavior (where/when/constraints)
4.  **TRIGGER** – what initiates the workflow or decision
5.  **FRICTION** – what slows/stops progress (pain, confusion, resistance)
6.  **WORKAROUND** – what they do instead (shadow process)
7.  **DECISION\_RULE** – the actual heuristic/criteria used (often unstated)
8.  **RISK** – perceived/real downside (legal, compliance, reputational, financial)
9.  **VALUE\_SIGNAL** – what “good” means to them (KPIs, outcomes, narratives)
10.  **LANGUAGE\_TOKEN** – phrases that reliably indicate intent/objection
11.  **ARTEFACT** – documents/tools used (spreadsheets, carrier forms, PDFs)
12.  **INTERVENTION** – what changes behavior (copy, UI, automation, training)
13.  **SEGMENT** – a target cohort definition (who/where/size/stage)
14.  **METRIC** – what is measured + how (instrumentation + definitions)

* * *

2) Core Ethno-Object JSON Schema (implementation-ready)
-------------------------------------------------------

This is the **base schema** every ethno-object inherits.

```
{
  "ethno_object_id": "eo_000000",
  "object_type": "FRICTION",
  "title": "Carrier loan paperwork causes advisor drop-off",
  "summary": "Advisors abandon mid-flow when carrier requirements vary by product/state and the checklist isn't surfaced early.",
  "domain": {
    "product_line": "liquidity_infrastructure",
    "industry": "insurance_finance",
    "workflow": "policy_loan_or_liquidity_event",
    "stage": "onboarding|quote|underwriting|servicing|claim|renewal|audit",
    "channel": "portal|email|phone|sms|api|in_person",
    "jurisdiction": ["US-NY"],
    "counterparty_types": ["carrier", "broker_dealer", "ria", "bank"]
  },
  "actors": [
    {
      "actor_id": "actor_advisor_ria",
      "role": "advisor",
      "persona": "RIA growth operator",
      "incentives": ["speed_to_close", "client_trust", "minimize_compliance_risk"],
      "constraints": ["time_poor", "depends_on_back_office"],
      "power_level": "high",
      "accountability": "client_outcome"
    }
  ],
  "causal_claim": {
    "claim": "If requirements variability is revealed late, advisors abandon and revert to manual servicing.",
    "mechanism": "uncertainty + hidden work increases perceived risk and time cost",
    "expected_effects": [
      { "metric_id": "m_abandon_rate", "direction": "increase", "magnitude_estimate": 0.15 }
    ],
    "scope_conditions": ["new_advisors", "multi_state_cases", "complex_products"],
    "counterexamples": ["teams with dedicated case managers"]
  },
  "evidence": [
    {
      "evidence_id": "ev_000001",
      "evidence_type": "interview|call_transcript|shadowing|ticket|email|artifact_review",
      "source_ref": "transcript:2026-01-30_braintrust",
      "verbatim_snippet": "We always end up custom building because every client data model is different.",
      "observation": "Late-stage variability forces bespoke handling and kills standardization.",
      "sample_size": 6,
      "confidence_initial": 0.62
    }
  ],
  "quant": {
    "prevalence_estimate": 0.55,
    "severity_estimate": 0.75,
    "value_at_stake_usd_estimate": 25000,
    "time_cost_minutes_estimate": 90,
    "risk_level": "medium|high",
    "uncertainty": {
      "confidence": 0.62,
      "variance": 0.18,
      "last_updated": "2026-02-10"
    }
  },
  "dependencies": {
    "upstream": ["eo_000010"],
    "downstream": ["eo_000200"],
    "conflicts_with": ["eo_000099"]
  },
  "recommended_actions": [
    {
      "action_id": "act_00001",
      "action_type": "ux_change|policy|automation|training|data_model|integration",
      "description": "Surface carrier/state requirement checklist upfront; adapt checklist by product + jurisdiction.",
      "owner": "product",
      "effort": "m",
      "expected_roi": {
        "metric_id": "m_completion_rate",
        "direction": "increase",
        "magnitude_estimate": 0.08
      },
      "test_plan": {
        "method": "bandit|ab_test",
        "success_metrics": ["m_completion_rate", "m_time_to_complete"],
        "min_runtime_days": 14
      }
    }
  ],
  "tags": ["carrier_variance", "paperwork", "advisor_experience"],
  "status": "draft|validated|deprecated",
  "governance": {
    "created_by": "research",
    "created_at": "2026-02-10",
    "review_cadence_days": 30,
    "privacy": "internal",
    "compliance_flags": ["pii_free", "sox_relevant:false"]
  }
}
```

* * *

3) LiqueFex-specific extensions (the “money layer”)
---------------------------------------------------

Add a `liquifex` object to capture the business model physics (liquidity, AUM, servicing cost, risk).

```
{
  "liquifex": {
    "economic_unit": "policy|account|case|advisor_book|carrier_block",
    "financials": {
      "aum_impact_usd": 0,
      "liquidity_unlocked_usd": 0,
      "cost_to_serve_delta_usd": -0,
      "revenue_delta_usd": 0,
      "risk_cost_delta_usd": -0
    },
    "operational": {
      "time_to_liquidity_days": 0,
      "cycle_time_days": 0,
      "handoffs_count": 0,
      "manual_steps_count": 0,
      "error_rate_estimate": 0.0
    },
    "trust_and_adoption": {
      "trust_barriers": ["black_box_fear", "carrier_pushback", "compliance_anxiety"],
      "adoption_stage": "unaware|curious|evaluating|piloting|live|expanding",
      "switching_cost_drivers": ["legacy_process", "integration", "training"]
    },
    "data_model": {
      "entities": ["policy", "insured", "owner", "beneficiary", "carrier", "advisor", "loan"],
      "critical_fields": ["policy_number", "carrier_code", "state", "product_type", "loan_value"],
      "variance_sources": ["carrier_rules", "state_rules", "client_data_model"]
    }
  }
}
```

* * *

4) Standard metric IDs (so optimization is plug-and-play)
---------------------------------------------------------

Define these once and reuse via `metric_id`:

*   `m_completion_rate`
*   `m_abandon_rate`
*   `m_time_to_complete`
*   `m_time_to_liquidity`
*   `m_cost_to_serve`
*   `m_manual_steps`
*   `m_error_rate`
*   `m_escalation_rate`
*   `m_nps_proxy` (or satisfaction proxy)
*   `m_aum_retained`
*   `m_liquidity_unlocked`
*   `m_revenue_per_case`

* * *

5) Minimal “Rules of 7” enforcement fields
------------------------------------------

Add to any object that impacts UX or questioning:

```
{
  "interaction_constraints": {
    "max_choices": 7,
    "max_required_fields_per_step": 7,
    "progressive_disclosure": true,
    "fallback_when_uncertain": "ask_1_followup_then_route_to_human"
  }
}
```

* * *

6) Quality gates (to prevent garbage-in optimization)
-----------------------------------------------------

Add these to enforce evidence discipline:

```
{
  "validation": {
    "evidence_threshold": {
      "min_sources": 2,
      "min_sample_size": 5,
      "requires_artifact_or_telemetry": true
    },
    "bias_checks": ["selection_bias", "recency_bias", "role_bias"],
    "status_reason": "what made this validated"
  }
}
```

* * *

7) How to use this schema inside LiqueFex OS (operational loop)
---------------------------------------------------------------

*   **Ingest**: transcript → extract candidates → create `LANGUAGE_TOKEN`, `FRICTION`, `DECISION_RULE`
*   **Link**: connect to `ACTOR`, `JOB`, `CONTEXT`
*   **Quantize**: attach prevalence/severity/value-at-stake estimates
*   **Ship**: generate `INTERVENTION` + test plan
*   **Learn**: update confidence + variance from real telemetry
*   **Govern**: promote to validated, or deprecate when stale

* * *

If you want the next highest ROI deliverable: I can generate **10–20 seed ethno-objects** for LiqueFex (advisor onboarding, carrier variance, compliance objections, integration friction, “manual spreadsheet dependency”, etc.) in this exact schema so you can immediately start training the recursive optimization loop.

## Prompt:
analyze all information in the liquifex project to generate 10–20 seed ethno-objects for LiqueFex specifically as it pertains to lifehouse capital

## Response:
Below are **15 seed ethno-objects** synthesized from the LiquiFex project context, mapped **specifically to Lifehouse Capital** as the target account. These are designed to be immediately usable inside the LiquiFex OS as causal priors for routing, UX, sales enablement, risk modeling, and ROI calculation.

I am assuming Lifehouse Capital ≈ institutional / sophisticated life insurance–backed investment operator with compliance sensitivity, multi-party workflows, and AUM-at-risk exposure.

* * *

LiquiFex × Lifehouse Capital
============================

Seed Ethno-Objects (v1)
-----------------------

* * *

EO-01 — ACTOR
-------------

**Title:** Lifehouse Capital Investment Principal  
**Object Type:** ACTOR

**Summary:** Decision-maker accountable for capital deployment, downside risk, and long-term credibility.

**Key Attributes**

*   Incentives: capital preservation, asymmetric upside, reputational safety
*   Constraints: regulatory scrutiny, opaque insurance infrastructure
*   Decision Style: conservative, evidence-heavy, anti–black box
*   Power Level: very high
*   Accountability: LP outcomes + firm reputation

* * *

EO-02 — JOB
-----------

**Title:** Convert illiquid life-insurance exposure into controlled liquidity  
**Object Type:** JOB

**Causal Claim:** Lifehouse is hiring LiquiFex to unlock liquidity **without increasing regulatory or reputational risk**.

**Success Signals**

*   Liquidity events are predictable
*   No surprise carrier behavior
*   Clean audit trail
*   No bespoke firefighting

* * *

EO-03 — CONTEXT
---------------

**Title:** Multi-carrier, multi-jurisdiction insurance exposure  
**Object Type:** CONTEXT

**Summary:** Each position is governed by different carrier rules, state laws, and historical data models.

**Impact**

*   High variance in processing time
*   Manual interpretation required
*   Scaling friction compounds non-linearly

* * *

EO-04 — TRIGGER
---------------

**Title:** Capital trapped longer than modeled  
**Object Type:** TRIGGER

**Trigger Condition**

*   Liquidity timing deviates from underwriting assumptions
*   Opportunity cost exceeds internal tolerance
*   Board-level visibility increases urgency

* * *

EO-05 — FRICTION
----------------

**Title:** Carrier rule opacity breaks institutional confidence  
**Object Type:** FRICTION

**Causal Claim**

> If carrier requirements are not explicit and standardized early, Lifehouse defaults to delay or manual handling.

**Mechanism**

*   Hidden constraints = perceived unmanaged risk
*   Institutional actors avoid uncertainty, even at cost

**Expected Effects**

*   Longer cycle times
*   Reduced appetite for scale

* * *

EO-06 — WORKAROUND
------------------

**Title:** Internal spreadsheets as “risk buffers”  
**Object Type:** WORKAROUND

**Summary:** Lifehouse compensates for system opacity with internal spreadsheets, bespoke tracking, and human review.

**Hidden Cost**

*   False sense of control
*   High key-person dependency
*   Silent data drift

* * *

EO-07 — DECISION\_RULE
----------------------

**Title:** “If it can’t be audited, it can’t scale”  
**Object Type:** DECISION\_RULE

**Rule**

*   Any system must:
    *   Explain _why_ an outcome occurred
    *   Reproduce the logic post-hoc
    *   Survive regulator scrutiny

**Implication for LiquiFex**

*   Black-box AI alone will be rejected
*   Causal transparency is mandatory

* * *

EO-08 — RISK
------------

**Title:** Reputational risk outweighs marginal yield  
**Object Type:** RISK

**Summary:** A single adverse event outweighs years of incremental upside.

**Risk Types**

*   Regulatory
*   LP confidence erosion
*   Counterparty distrust

* * *

EO-09 — VALUE\_SIGNAL
---------------------

**Title:** Predictability beats optimization  
**Object Type:** VALUE\_SIGNAL

**Observed Truth**  
Lifehouse values:

*   Stable timelines
*   Known variance bands
*   Controlled downside  
    more than absolute yield maximization.

* * *

EO-10 — LANGUAGE\_TOKEN
-----------------------

**Title:** “We need to understand the mechanics”  
**Object Type:** LANGUAGE\_TOKEN

**Interpretation**

*   Not a request for education
*   A demand for causal explainability
*   Signal of trust gating

**Routing Rule**  
If this phrase appears → surface:

*   Process maps
*   Rule engines
*   Human override logic

* * *

EO-11 — ARTEFACT
----------------

**Title:** Carrier policy documents + internal memos  
**Object Type:** ARTEFACT

**Summary**

*   PDFs, scanned forms, emails
*   Often incomplete or contradictory
*   Humans reconcile inconsistencies manually

**LiquiFex Opportunity**  
Turn artefacts into structured, queryable rule sets.

* * *

EO-12 — INTERVENTION
--------------------

**Title:** Causal rule engine with audit trail  
**Object Type:** INTERVENTION

**Description**  
Expose:

*   Carrier rules
*   State dependencies
*   Decision logic
*   Variance ranges

**Expected ROI**

*   ↓ cycle time
*   ↑ trust
*   ↑ deployable capital velocity

* * *

EO-13 — SEGMENT
---------------

**Title:** Institutional life-insurance capital operators  
**Object Type:** SEGMENT

**Segment Traits**

*   $100M+ exposure
*   Low tolerance for surprises
*   Will pay for certainty
*   Long sales cycles, high LTV

* * *

EO-14 — METRIC
--------------

**Title:** Time-to-Liquidity Variance  
**Object Type:** METRIC

**Definition**  
Not just mean time-to-liquidity, but **variance and tail risk**.

**Why It Matters**  
Institutions optimize portfolios on predictability, not averages.

* * *

EO-15 — FRICTION
----------------

**Title:** Fear of vendor dependency  
**Object Type:** FRICTION

**Causal Claim**

> If LiquiFex appears as a dependency rather than infrastructure, adoption stalls.

**Mitigation Strategy**

*   Emphasize portability
*   Emphasize explainability
*   Emphasize human override + ownership

* * *

Strategic Implication for LiquiFex
==================================

For **Lifehouse Capital**, LiquiFex should **not** be positioned as:

*   “AI optimization”
*   “Automation”
*   “Efficiency tooling”

Instead, LiquiFex is:

> **A causal liquidity infrastructure that converts insurance uncertainty into auditable, controllable financial primitives.**

That framing aligns directly with the dominant ethno-objects above and maximizes long-term ROI, trust, and deal velocity.

* * *

Next High-ROI Step (recommended)
--------------------------------

I can:

*   Convert these into **confidence-weighted JSON records**
*   Map each ethno-object to **sales narrative + UX decisions**
*   Generate a **Lifehouse-specific LiquiFex demo flow** that dynamically adapts based on these objects

Tell me which direction to proceed.

## Prompt:
utilize as much information as possible from the liquifex project to create json records with as much knowlege as possible with confidence-weighted JSON records

## Response:
Thought for 39s

```
{
  "schema_version": "liquifex_ethno_object_v1",
  "generated_at": "2026-02-10",
  "source_context": {
    "project": "LiquiFex",
    "target_account": "Lifehouse Capital",
    "inputs_used": [
      "Project conversation summaries (LiquiFex + Gigaton context)",
      "Abacus case-study prompt context (risk + catastrophic failure framing)",
      "Braintrust meeting summary: PLM customization complexity, need for causal engine (GME) to understand client-specific data models",
      "LiquiFex positioning prompts: adoption urgency, pilot timelines, ROI calculators, compliance/IP attorney brief requirements"
    ],
    "limits": [
      "No direct Lifehouse documents, emails, or call transcripts were provided in-session; therefore account-specific details are modeled as high-likelihood institutional patterns and flagged as assumptions.",
      "Quant values are seed priors intended to be updated via telemetry + Lifehouse discovery."
    ]
  },
  "ethno_objects": [
    {
      "ethno_object_id": "eo_lh_0001",
      "object_type": "ACTOR",
      "title": "Lifehouse Capital Investment Principal",
      "summary": "Senior decision-maker accountable for capital deployment, downside containment, and institutional credibility; sets adoption gate for new infrastructure.",
      "domain": {
        "product_line": "liquidity_infrastructure",
        "industry": "insurance_finance",
        "workflow": "portfolio_liquidity_governance",
        "stage": "evaluating",
        "channel": "exec_meeting",
        "jurisdiction": [],
        "counterparty_types": ["institutional_investor", "carrier", "administrator"]
      },
      "actors": [
        {
          "actor_id": "actor_lh_investment_principal",
          "role": "investment_principal",
          "persona": "Institutional capital allocator",
          "incentives": ["capital_preservation", "predictable_cashflows", "auditability", "reputational_safety"],
          "constraints": ["regulatory_scrutiny", "committee_decisions", "limited_tolerance_for_variance"],
          "power_level": "very_high",
          "accountability": "lp_outcomes"
        }
      ],
      "causal_claim": {
        "claim": "If LiquiFex cannot provide auditable, explainable mechanics, Lifehouse will not scale adoption beyond pilot.",
        "mechanism": "institutional trust gating + governance requirements",
        "expected_effects": [
          { "metric_id": "m_adoption_stage", "direction": "stagnate", "magnitude_estimate": 1.0 }
        ],
        "scope_conditions": ["institutional_lp_capital", "multi_counterparty_workflows"],
        "counterexamples": ["teams with existing causal/audit infrastructure already deployed"]
      },
      "evidence": [
        {
          "evidence_id": "ev_lh_0001",
          "evidence_type": "project_context",
          "source_ref": "Gigaton/LiquiFex prompts: IP attorney tech brief requires explainability + protection; enterprise customization complexity demands causal understanding",
          "verbatim_snippet": null,
          "observation": "Repeated emphasis on causal engine, decision-maker simplification, and legal defensibility implies institutional buyers require auditability.",
          "sample_size": 3,
          "confidence_initial": 0.72
        }
      ],
      "quant": {
        "prevalence_estimate": 0.7,
        "severity_estimate": 0.85,
        "value_at_stake_usd_estimate": 250000,
        "time_cost_minutes_estimate": 180,
        "risk_level": "high",
        "uncertainty": { "confidence": 0.72, "variance": 0.2, "last_updated": "2026-02-10" }
      },
      "liquifex": {
        "economic_unit": "portfolio",
        "financials": {
          "aum_impact_usd": 0,
          "liquidity_unlocked_usd": 0,
          "cost_to_serve_delta_usd": 0,
          "revenue_delta_usd": 0,
          "risk_cost_delta_usd": 0
        },
        "operational": {
          "time_to_liquidity_days": 0,
          "cycle_time_days": 0,
          "handoffs_count": 0,
          "manual_steps_count": 0,
          "error_rate_estimate": 0.0
        },
        "trust_and_adoption": {
          "trust_barriers": ["black_box_fear", "governance_objections", "audit_gap"],
          "adoption_stage": "evaluating",
          "switching_cost_drivers": ["legacy_process", "integration", "policy_change", "training"]
        },
        "data_model": {
          "entities": ["policy", "carrier", "owner", "insured", "loan", "premium", "state", "advisor"],
          "critical_fields": ["carrier_code", "policy_number", "jurisdiction", "product_type", "loan_terms"],
          "variance_sources": ["carrier_rules", "jurisdiction_rules", "historical_data_quality"]
        }
      },
      "interaction_constraints": {
        "max_choices": 7,
        "max_required_fields_per_step": 7,
        "progressive_disclosure": true,
        "fallback_when_uncertain": "ask_1_followup_then_route_to_human"
      },
      "recommended_actions": [
        {
          "action_id": "act_lh_0001",
          "action_type": "ux_change",
          "description": "Lead with an explainable ‘Mechanics + Audit Trail’ view: rule sources, decision path, and reproducible outputs; add human override.",
          "owner": "product",
          "effort": "m",
          "expected_roi": { "metric_id": "m_adoption_stage", "direction": "increase", "magnitude_estimate": 0.25 },
          "test_plan": {
            "method": "ab_test",
            "success_metrics": ["m_sales_cycle_days", "m_pilot_to_expand_rate"],
            "min_runtime_days": 30
          }
        }
      ],
      "tags": ["institutional_buyer", "auditability", "trust_gating"],
      "status": "draft",
      "governance": { "created_by": "system", "created_at": "2026-02-10", "review_cadence_days": 30, "privacy": "internal", "compliance_flags": ["pii_free"] },
      "validation": {
        "evidence_threshold": { "min_sources": 2, "min_sample_size": 5, "requires_artifact_or_telemetry": true },
        "bias_checks": ["role_bias", "assumption_risk"],
        "status_reason": "Seed prior pending Lifehouse discovery + telemetry"
      }
    },

    {
      "ethno_object_id": "eo_lh_0002",
      "object_type": "JOB",
      "title": "Convert life-insurance exposure into controllable liquidity without governance blowback",
      "summary": "Lifehouse hires LiquiFex to transform opaque insurance operations into predictable, auditable liquidity events that fit portfolio governance.",
      "domain": {
        "product_line": "liquidity_infrastructure",
        "industry": "insurance_finance",
        "workflow": "liquidity_event_planning",
        "stage": "evaluating",
        "channel": "exec_meeting",
        "jurisdiction": [],
        "counterparty_types": ["carrier", "administrator"]
      },
      "actors": [
        {
          "actor_id": "actor_lh_investment_principal",
          "role": "investment_principal",
          "persona": "Institutional capital allocator",
          "incentives": ["predictability", "capital_velocity", "risk_control"],
          "constraints": ["committee_approvals", "audit_requirements"],
          "power_level": "very_high",
          "accountability": "portfolio_outcomes"
        }
      ],
      "causal_claim": {
        "claim": "If LiquiFex can provide predictable variance bands and an auditable path-to-liquidity, Lifehouse will treat it as infrastructure and scale.",
        "mechanism": "variance reduction increases deployable capital velocity",
        "expected_effects": [
          { "metric_id": "m_time_to_liquidity", "direction": "decrease", "magnitude_estimate": 0.15 },
          { "metric_id": "m_time_to_liquidity_variance", "direction": "decrease", "magnitude_estimate": 0.25 }
        ],
        "scope_conditions": ["multi_policy_portfolios", "multi_counterparty servicing"],
        "counterexamples": ["single-carrier blocks with stable servicing already in place"]
      },
      "evidence": [
        {
          "evidence_id": "ev_lh_0002",
          "evidence_type": "project_context",
          "source_ref": "LiquiFex prompts: ROI calculators, adoption urgency, pilot program framing + Abacus catastrophe framing",
          "verbatim_snippet": null,
          "observation": "Project focus consistently targets liquidity, profitability, and risk avoidance through infrastructure + measurement.",
          "sample_size": 3,
          "confidence_initial": 0.68
        }
      ],
      "quant": {
        "prevalence_estimate": 0.65,
        "severity_estimate": 0.8,
        "value_at_stake_usd_estimate": 500000,
        "time_cost_minutes_estimate": 0,
        "risk_level": "high",
        "uncertainty": { "confidence": 0.68, "variance": 0.22, "last_updated": "2026-02-10" }
      },
      "liquifex": {
        "economic_unit": "policy_block",
        "financials": {
          "aum_impact_usd": 0,
          "liquidity_unlocked_usd": 0,
          "cost_to_serve_delta_usd": 0,
          "revenue_delta_usd": 0,
          "risk_cost_delta_usd": 0
        },
        "operational": {
          "time_to_liquidity_days": 0,
          "cycle_time_days": 0,
          "handoffs_count": 0,
          "manual_steps_count": 0,
          "error_rate_estimate": 0.0
        },
        "trust_and_adoption": {
          "trust_barriers": ["variance_uncertainty", "carrier_opacity"],
          "adoption_stage": "evaluating",
          "switching_cost_drivers": ["integration", "data_model_alignment"]
        },
        "data_model": {
          "entities": ["policy", "loan", "carrier_rule", "jurisdiction_rule", "cashflow_schedule"],
          "critical_fields": ["policy_number", "carrier", "state", "product_type", "loan_availability"],
          "variance_sources": ["carrier_rules", "state_rules", "data_quality"]
        }
      },
      "recommended_actions": [
        {
          "action_id": "act_lh_0002",
          "action_type": "automation",
          "description": "Implement a Liquidity Forecast with variance bands (P50/P90) + audit trail explaining drivers and rule sources.",
          "owner": "engineering",
          "effort": "l",
          "expected_roi": { "metric_id": "m_pilot_to_expand_rate", "direction": "increase", "magnitude_estimate": 0.2 },
          "test_plan": { "method": "pilot", "success_metrics": ["m_time_to_liquidity_variance", "m_governance_acceptance_rate"], "min_runtime_days": 60 }
        }
      ],
      "tags": ["jtbd", "predictable_liquidity", "institutional_governance"],
      "status": "draft",
      "governance": { "created_by": "system", "created_at": "2026-02-10", "review_cadence_days": 30, "privacy": "internal", "compliance_flags": ["pii_free"] }
    },

    {
      "ethno_object_id": "eo_lh_0003",
      "object_type": "FRICTION",
      "title": "Carrier and jurisdiction variability destroys standardization",
      "summary": "Every carrier/product/jurisdiction combination behaves like a unique system; late discovery forces bespoke interventions and manual firefighting.",
      "domain": {
        "product_line": "liquidity_infrastructure",
        "industry": "insurance_finance",
        "workflow": "servicing_and_liquidity_execution",
        "stage": "evaluating",
        "channel": "ops",
        "jurisdiction": [],
        "counterparty_types": ["carrier"]
      },
      "actors": [
        { "actor_id": "actor_lh_ops", "role": "operations", "persona": "Portfolio servicing team", "incentives": ["reduce_escalations", "hit_timelines"], "constraints": ["data_gaps", "carrier_dependencies"], "power_level": "medium", "accountability": "execution" }
      ],
      "causal_claim": {
        "claim": "If variability is not modeled as first-class (rules + exceptions), Lifehouse will require custom implementations and cannot scale.",
        "mechanism": "variance creates hidden work; hidden work creates cost and delays",
        "expected_effects": [
          { "metric_id": "m_manual_steps", "direction": "increase", "magnitude_estimate": 0.3 },
          { "metric_id": "m_cost_to_serve", "direction": "increase", "magnitude_estimate": 0.2 }
        ],
        "scope_conditions": ["multi_carrier", "multi_state", "legacy_data_models"],
        "counterexamples": ["single-carrier standardized blocks"]
      },
      "evidence": [
        {
          "evidence_id": "ev_lh_0003",
          "evidence_type": "meeting_summary",
          "source_ref": "Braintrust summary: customized implementations required due to client-specific data models; need causal engine to understand complex models",
          "verbatim_snippet": null,
          "observation": "Enterprise systems fail when variability isn't modeled; same pattern applies to insurance servicing rules.",
          "sample_size": 1,
          "confidence_initial": 0.74
        }
      ],
      "quant": {
        "prevalence_estimate": 0.75,
        "severity_estimate": 0.85,
        "value_at_stake_usd_estimate": 300000,
        "time_cost_minutes_estimate": 240,
        "risk_level": "high",
        "uncertainty": { "confidence": 0.74, "variance": 0.18, "last_updated": "2026-02-10" }
      },
      "liquifex": {
        "economic_unit": "case",
        "financials": { "aum_impact_usd": 0, "liquidity_unlocked_usd": 0, "cost_to_serve_delta_usd": 0, "revenue_delta_usd": 0, "risk_cost_delta_usd": 0 },
        "operational": { "time_to_liquidity_days": 0, "cycle_time_days": 0, "handoffs_count": 6, "manual_steps_count": 20, "error_rate_estimate": 0.08 },
        "trust_and_adoption": { "trust_barriers": ["carrier_variance", "exception_handling"], "adoption_stage": "evaluating", "switching_cost_drivers": ["data_model_alignment", "integration"] },
        "data_model": { "entities": ["carrier_rule", "state_rule", "exception"], "critical_fields": ["rule_source", "effective_date", "applicability_conditions"], "variance_sources": ["carrier_rules", "state_rules"] }
      },
      "recommended_actions": [
        {
          "action_id": "act_lh_0003",
          "action_type": "data_model",
          "description": "Create a Rules + Exceptions layer (rule objects + applicability conditions + versioning) and bind it to workflow execution.",
          "owner": "engineering",
          "effort": "l",
          "expected_roi": { "metric_id": "m_manual_steps", "direction": "decrease", "magnitude_estimate": 0.2 },
          "test_plan": { "method": "pilot", "success_metrics": ["m_manual_steps", "m_escalation_rate"], "min_runtime_days": 60 }
        }
      ],
      "tags": ["variance", "rules_engine", "scale_constraint"],
      "status": "draft",
      "governance": { "created_by": "system", "created_at": "2026-02-10", "review_cadence_days": 30, "privacy": "internal", "compliance_flags": ["pii_free"] }
    },

    {
      "ethno_object_id": "eo_lh_0004",
      "object_type": "DECISION_RULE",
      "title": "If it can’t be audited, it can’t scale",
      "summary": "Institutional adoption requires reproducible logic, explicit rule sources, and post-hoc explainability.",
      "domain": {
        "product_line": "liquidity_infrastructure",
        "industry": "insurance_finance",
        "workflow": "vendor_selection",
        "stage": "evaluating",
        "channel": "governance",
        "jurisdiction": [],
        "counterparty_types": ["institutional_investor"]
      },
      "causal_claim": {
        "claim": "Auditable systems accelerate approval; non-auditable systems trigger stalls, endless diligence, or rejection.",
        "mechanism": "governance and compliance risk gating",
        "expected_effects": [{ "metric_id": "m_sales_cycle_days", "direction": "decrease", "magnitude_estimate": 0.15 }],
        "scope_conditions": ["committee_buyers", "regulated_environments"],
        "counterexamples": ["small operators with informal controls"]
      },
      "evidence": [
        {
          "evidence_id": "ev_lh_0004",
          "evidence_type": "project_context",
          "source_ref": "LiquiFex: IP attorney brief + causal engine framing + need to simplify for decision-makers",
          "verbatim_snippet": null,
          "observation": "Repeated priority on legal/protectable mechanics implies formal governance expectations.",
          "sample_size": 2,
          "confidence_initial": 0.7
        }
      ],
      "quant": {
        "prevalence_estimate": 0.7,
        "severity_estimate": 0.8,
        "value_at_stake_usd_estimate": 400000,
        "time_cost_minutes_estimate": 0,
        "risk_level": "high",
        "uncertainty": { "confidence": 0.7, "variance": 0.2, "last_updated": "2026-02-10" }
      },
      "recommended_actions": [
        {
          "action_id": "act_lh_0004",
          "action_type": "ux_change",
          "description": "Add ‘Explain’ toggles everywhere: what rule fired, what evidence used, what alternatives existed, and who can override.",
          "owner": "product",
          "effort": "m",
          "expected_roi": { "metric_id": "m_governance_acceptance_rate", "direction": "increase", "magnitude_estimate": 0.2 },
          "test_plan": { "method": "pilot", "success_metrics": ["m_governance_acceptance_rate", "m_sales_cycle_days"], "min_runtime_days": 45 }
        }
      ],
      "tags": ["auditability", "governance", "explainability"],
      "status": "draft",
      "governance": { "created_by": "system", "created_at": "2026-02-10", "review_cadence_days": 30, "privacy": "internal", "compliance_flags": ["pii_free"] }
    },

    {
      "ethno_object_id": "eo_lh_0005",
      "object_type": "WORKAROUND",
      "title": "Spreadsheets as a synthetic control layer",
      "summary": "Lifehouse likely relies on internal spreadsheets and manual reconciliation to offset carrier opacity and system gaps—creating hidden key-person risk.",
      "domain": {
        "product_line": "liquidity_infrastructure",
        "industry": "insurance_finance",
        "workflow": "portfolio_tracking",
        "stage": "current_state",
        "channel": "ops",
        "jurisdiction": [],
        "counterparty_types": ["institutional_investor"]
      },
      "causal_claim": {
        "claim": "If LiquiFex does not replace spreadsheet controls with auditable system controls, users will dual-run indefinitely (stalling ROI and adoption).",
        "mechanism": "trust transfer requires control transfer",
        "expected_effects": [
          { "metric_id": "m_time_to_value", "direction": "increase", "magnitude_estimate": 0.2 },
          { "metric_id": "m_cost_to_serve", "direction": "increase", "magnitude_estimate": 0.1 }
        ],
        "scope_conditions": ["institutional_operations", "legacy_controls"],
        "counterexamples": ["teams with modern portfolio systems already integrated"]
      },
      "evidence": [
        {
          "evidence_id": "ev_lh_0005",
          "evidence_type": "industry_pattern_assumption",
          "source_ref": "LiquiFex prompts emphasize calculators, inputs, and manual variable capture; suggests current state is spreadsheet-driven.",
          "verbatim_snippet": null,
          "observation": "When no system-of-record exists, spreadsheets become the control plane; common in complex insurance servicing.",
          "sample_size": 1,
          "confidence_initial": 0.6
        }
      ],
      "quant": {
        "prevalence_estimate": 0.6,
        "severity_estimate": 0.7,
        "value_at_stake_usd_estimate": 200000,
        "time_cost_minutes_estimate": 120,
        "risk_level": "medium",
        "uncertainty": { "confidence": 0.6, "variance": 0.28, "last_updated": "2026-02-10" }
      },
      "recommended_actions": [
        {
          "action_id": "act_lh_0005",
          "action_type": "automation",
          "description": "Offer a migration path: import spreadsheet fields → map to LiquiFex entities → validate variances → produce an auditable control dashboard.",
          "owner": "customer_success",
          "effort": "m",
          "expected_roi": { "metric_id": "m_time_to_value", "direction": "decrease", "magnitude_estimate": 0.25 },
          "test_plan": { "method": "pilot", "success_metrics": ["m_dual_run_duration_days", "m_user_trust_score"], "min_runtime_days": 30 }
        }
      ],
      "tags": ["spreadsheet_dependency", "dual_run", "controls"],
      "status": "draft",
      "governance": { "created_by": "system", "created_at": "2026-02-10", "review_cadence_days": 30, "privacy": "internal", "compliance_flags": ["pii_free", "assumption_flagged"] }
    },

    {
      "ethno_object_id": "eo_lh_0006",
      "object_type": "RISK",
      "title": "Reputational downside dominates marginal yield",
      "summary": "Institutional operators accept lower upside to avoid tail events that trigger LP distrust, regulatory issues, or counterparty fallout.",
      "domain": {
        "product_line": "liquidity_infrastructure",
        "industry": "insurance_finance",
        "workflow": "risk_management",
        "stage": "evaluating",
        "channel": "governance",
        "jurisdiction": [],
        "counterparty_types": ["institutional_investor"]
      },
      "causal_claim": {
        "claim": "If LiquiFex cannot show tail-risk controls (P90/P99), Lifehouse will cap usage to non-critical paths.",
        "mechanism": "tail risk drives policy constraints",
        "expected_effects": [{ "metric_id": "m_scope_of_deployment", "direction": "decrease", "magnitude_estimate": 0.3 }],
        "scope_conditions": ["new_vendor", "material_aum_exposure"],
        "counterexamples": ["non-institutional buyers optimizing solely for yield"]
      },
      "evidence": [
        {
          "evidence_id": "ev_lh_0006",
          "evidence_type": "project_context",
          "source_ref": "Abacus catastrophe framing + LiquiFex urgency/adoption prompts",
          "verbatim_snippet": null,
          "observation": "Project narrative emphasizes avoiding catastrophic failure as core value proposition.",
          "sample_size": 2,
          "confidence_initial": 0.66
        }
      ],
      "quant": {
        "prevalence_estimate": 0.65,
        "severity_estimate": 0.9,
        "value_at_stake_usd_estimate": 1000000,
        "time_cost_minutes_estimate": 0,
        "risk_level": "high",
        "uncertainty": { "confidence": 0.66, "variance": 0.24, "last_updated": "2026-02-10" }
      },
      "recommended_actions": [
        {
          "action_id": "act_lh_0006",
          "action_type": "policy",
          "description": "Ship a ‘Tail Risk Control Pack’: variance bands, exception playbooks, escalation thresholds, and audit exports.",
          "owner": "product",
          "effort": "m",
          "expected_roi": { "metric_id": "m_scope_of_deployment", "direction": "increase", "magnitude_estimate": 0.2 },
          "test_plan": { "method": "pilot", "success_metrics": ["m_governance_acceptance_rate", "m_exception_resolution_time"], "min_runtime_days": 60 }
        }
      ],
      "tags": ["tail_risk", "reputation", "institutional_controls"],
      "status": "draft",
      "governance": { "created_by": "system", "created_at": "2026-02-10", "review_cadence_days": 30, "privacy": "internal", "compliance_flags": ["pii_free"] }
    },

    {
      "ethno_object_id": "eo_lh_0007",
      "object_type": "VALUE_SIGNAL",
      "title": "Predictability beats optimization",
      "summary": "Lifehouse will pay for reduced variance (predictable cycle time and outcome certainty) more than incremental yield or theoretical best-case efficiency.",
      "domain": {
        "product_line": "liquidity_infrastructure",
        "industry": "insurance_finance",
        "workflow": "portfolio_planning",
        "stage": "evaluating",
        "channel": "exec_meeting",
        "jurisdiction": [],
        "counterparty_types": ["institutional_investor"]
      },
      "causal_claim": {
        "claim": "If LiquiFex is framed as predictability infrastructure (variance reduction) rather than AI optimization, adoption probability increases.",
        "mechanism": "aligning to institutional value function",
        "expected_effects": [{ "metric_id": "m_pilot_to_expand_rate", "direction": "increase", "magnitude_estimate": 0.15 }],
        "scope_conditions": ["institutional_buyers", "regulated_environments"],
        "counterexamples": ["high-risk traders optimizing purely for alpha"]
      },
      "evidence": [
        {
          "evidence_id": "ev_lh_0007",
          "evidence_type": "project_context",
          "source_ref": "LiquiFex ROI + adoption urgency prompts; emphasis on net liquidity/profit improvement and catastrophic risk avoidance",
          "verbatim_snippet": null,
          "observation": "Project value prop consistently anchored on control and downside prevention vs pure optimization.",
          "sample_size": 2,
          "confidence_initial": 0.64
        }
      ],
      "quant": {
        "prevalence_estimate": 0.6,
        "severity_estimate": 0.6,
        "value_at_stake_usd_estimate": 300000,
        "time_cost_minutes_estimate": 0,
        "risk_level": "medium",
        "uncertainty": { "confidence": 0.64, "variance": 0.26, "last_updated": "2026-02-10" }
      },
      "recommended_actions": [
        {
          "action_id": "act_lh_0007",
          "action_type": "training",
          "description": "Rewrite Lifehouse-facing narrative: ‘auditable liquidity control plane’ + ‘variance bands’ + ‘human override’ (avoid “AI magic”).",
          "owner": "sales",
          "effort": "s",
          "expected_roi": { "metric_id": "m_sales_cycle_days", "direction": "decrease", "magnitude_estimate": 0.1 },
          "test_plan": { "method": "ab_test", "success_metrics": ["m_stage_conversion_rate"], "min_runtime_days": 30 }
        }
      ],
      "tags": ["positioning", "variance_reduction", "value_function"],
      "status": "draft",
      "governance": { "created_by": "system", "created_at": "2026-02-10", "review_cadence_days": 30, "privacy": "internal", "compliance_flags": ["pii_free"] }
    },

    {
      "ethno_object_id": "eo_lh_0008",
      "object_type": "LANGUAGE_TOKEN",
      "title": "“We need to understand the mechanics”",
      "summary": "A trust-gating phrase indicating demand for causal transparency, not general education.",
      "domain": {
        "product_line": "liquidity_infrastructure",
        "industry": "insurance_finance",
        "workflow": "sales_and_diligence",
        "stage": "evaluating",
        "channel": "meeting",
        "jurisdiction": [],
        "counterparty_types": ["institutional_investor"]
      },
      "causal_claim": {
        "claim": "When this phrase appears, presenting ROI alone will not progress the deal; mechanics + audit trail content is required.",
        "mechanism": "institutional diligence prioritizes control proofs",
        "expected_effects": [{ "metric_id": "m_stage_conversion_rate", "direction": "increase", "magnitude_estimate": 0.12 }],
        "scope_conditions": ["institutional_committee_process"],
        "counterexamples": ["buyers driven purely by economics with minimal governance"]
      },
      "evidence": [
        {
          "evidence_id": "ev_lh_0008",
          "evidence_type": "inferred_pattern",
          "source_ref": "LiquiFex prompts emphasize causal engine and decision-maker simplification; token codifies the trigger for content routing.",
          "verbatim_snippet": null,
          "observation": "Project’s repeated need to simplify and explain suggests this token is common and material to conversion.",
          "sample_size": 1,
          "confidence_initial": 0.62
        }
      ],
      "quant": {
        "prevalence_estimate": 0.55,
        "severity_estimate": 0.7,
        "value_at_stake_usd_estimate": 250000,
        "time_cost_minutes_estimate": 0,
        "risk_level": "medium",
        "uncertainty": { "confidence": 0.62, "variance": 0.28, "last_updated": "2026-02-10" }
      },
      "recommended_actions": [
        {
          "action_id": "act_lh_0008",
          "action_type": "ux_change",
          "description": "Add a Lifehouse-specific ‘Mechanics Deck’ module: workflow maps, rule sources, exception handling, audit exports, and human override.",
          "owner": "marketing",
          "effort": "m",
          "expected_roi": { "metric_id": "m_stage_conversion_rate", "direction": "increase", "magnitude_estimate": 0.1 },
          "test_plan": { "method": "pilot", "success_metrics": ["m_sales_cycle_days", "m_stage_conversion_rate"], "min_runtime_days": 45 }
        }
      ],
      "tags": ["language_token", "sales_routing", "mechanics"],
      "status": "draft",
      "governance": { "created_by": "system", "created_at": "2026-02-10", "review_cadence_days": 30, "privacy": "internal", "compliance_flags": ["pii_free"] }
    },

    {
      "ethno_object_id": "eo_lh_0009",
      "object_type": "ARTEFACT",
      "title": "Carrier PDFs, endorsements, and email threads are the real rulebook",
      "summary": "Operational truth is embedded in documents and correspondence; inconsistencies are reconciled manually, creating drift and audit gaps.",
      "domain": {
        "product_line": "liquidity_infrastructure",
        "industry": "insurance_finance",
        "workflow": "servicing_rule_interpretation",
        "stage": "current_state",
        "channel": "ops",
        "jurisdiction": [],
        "counterparty_types": ["carrier"]
      },
      "causal_claim": {
        "claim": "If LiquiFex cannot convert artefacts into structured rules and evidence, execution remains human-dependent and non-scalable.",
        "mechanism": "unstructured inputs block automation and increase errors",
        "expected_effects": [{ "metric_id": "m_error_rate", "direction": "decrease", "magnitude_estimate": 0.12 }],
        "scope_conditions": ["document-driven operations"],
        "counterexamples": ["carriers with fully standardized APIs and clean data feeds"]
      },
      "evidence": [
        {
          "evidence_id": "ev_lh_0009",
          "evidence_type": "project_context",
          "source_ref": "LiquiFex: compiler forms, JSON extraction emphasis, ‘encode as much info as possible’ prompts",
          "verbatim_snippet": null,
          "observation": "Project repeatedly targets transforming unstructured artifacts into structured JSON for intelligence and operations.",
          "sample_size": 2,
          "confidence_initial": 0.69
        }
      ],
      "quant": {
        "prevalence_estimate": 0.7,
        "severity_estimate": 0.75,
        "value_at_stake_usd_estimate": 250000,
        "time_cost_minutes_estimate": 90,
        "risk_level": "medium",
        "uncertainty": { "confidence": 0.69, "variance": 0.22, "last_updated": "2026-02-10" }
      },
      "recommended_actions": [
        {
          "action_id": "act_lh_0009",
          "action_type": "automation",
          "description": "Artefact ingestion pipeline: document → extraction → rule objects w/ provenance → human review queue → versioned rule store.",
          "owner": "engineering",
          "effort": "l",
          "expected_roi": { "metric_id": "m_manual_steps", "direction": "decrease", "magnitude_estimate": 0.2 },
          "test_plan": { "method": "pilot", "success_metrics": ["m_manual_steps", "m_error_rate"], "min_runtime_days": 90 }
        }
      ],
      "tags": ["unstructured_to_structured", "rule_provenance", "audit"],
      "status": "draft",
      "governance": { "created_by": "system", "created_at": "2026-02-10", "review_cadence_days": 30, "privacy": "internal", "compliance_flags": ["pii_free"] }
    },

    {
      "ethno_object_id": "eo_lh_0010",
      "object_type": "INTERVENTION",
      "title": "Causal rule engine + audit export as the adoption wedge",
      "summary": "The fastest path to Lifehouse trust is a rules+exceptions execution layer that produces deterministic audit exports aligned to governance review.",
      "domain": {
        "product_line": "liquidity_infrastructure",
        "industry": "insurance_finance",
        "workflow": "pilot_deployment",
        "stage": "piloting",
        "channel": "product",
        "jurisdiction": [],
        "counterparty_types": ["institutional_investor", "carrier"]
      },
      "causal_claim": {
        "claim": "Implementing explainable rule execution before advanced AI optimization increases pilot success probability.",
        "mechanism": "trust-before-automation sequencing",
        "expected_effects": [
          { "metric_id": "m_pilot_success_rate", "direction": "increase", "magnitude_estimate": 0.2 },
          { "metric_id": "m_escalation_rate", "direction": "decrease", "magnitude_estimate": 0.15 }
        ],
        "scope_conditions": ["institutional buyers", "high variance workflows"],
        "counterexamples": ["buyers already comfortable with probabilistic AI control"]
      },
      "evidence": [
        {
          "evidence_id": "ev_lh_0010",
          "evidence_type": "project_context",
          "source_ref": "LiquiFex tech brief + IP attorney requirements; ‘causal engine missing piece’ framing",
          "verbatim_snippet": null,
          "observation": "Project asserts causal engine is key blocker for enterprise adoption; intervention operationalizes that.",
          "sample_size": 2,
          "confidence_initial": 0.73
        }
      ],
      "quant": {
        "prevalence_estimate": 0.65,
        "severity_estimate": 0.8,
        "value_at_stake_usd_estimate": 600000,
        "time_cost_minutes_estimate": 0,
        "risk_level": "high",
        "uncertainty": { "confidence": 0.73, "variance": 0.18, "last_updated": "2026-02-10" }
      },
      "recommended_actions": [
        {
          "action_id": "act_lh_0010",
          "action_type": "automation",
          "description": "Deploy rule execution + audit export for one Lifehouse-critical workflow (lowest integration surface, highest variance pain).",
          "owner": "engineering",
          "effort": "l",
          "expected_roi": { "metric_id": "m_pilot_success_rate", "direction": "increase", "magnitude_estimate": 0.2 },
          "test_plan": { "method": "pilot", "success_metrics": ["m_time_to_value", "m_governance_acceptance_rate"], "min_runtime_days": 60 }
        }
      ],
      "tags": ["intervention", "wedge", "causal_engine"],
      "status": "draft",
      "governance": { "created_by": "system", "created_at": "2026-02-10", "review_cadence_days": 30, "privacy": "internal", "compliance_flags": ["pii_free"] }
    },

    {
      "ethno_object_id": "eo_lh_0011",
      "object_type": "FRICTION",
      "title": "Vendor dependency fear delays commitment",
      "summary": "Lifehouse resists systems that look like a dependency rather than infrastructure; demands portability, ownership, and clear exit paths.",
      "domain": {
        "product_line": "liquidity_infrastructure",
        "industry": "insurance_finance",
        "workflow": "vendor_selection",
        "stage": "evaluating",
        "channel": "governance",
        "jurisdiction": [],
        "counterparty_types": ["institutional_investor"]
      },
      "causal_claim": {
        "claim": "If LiquiFex does not provide portability guarantees (data/export + governance artifacts), contract acceptance slows or scope is reduced.",
        "mechanism": "dependency risk triggers procurement friction",
        "expected_effects": [{ "metric_id": "m_sales_cycle_days", "direction": "increase", "magnitude_estimate": 0.15 }],
        "scope_conditions": ["institutional procurement"],
        "counterexamples": ["founder-led buyers with low procurement rigor"]
      },
      "evidence": [
        {
          "evidence_id": "ev_lh_0011",
          "evidence_type": "inferred_pattern",
          "source_ref": "LiquiFex IP/legal structuring emphasis + risk avoidance narrative",
          "verbatim_snippet": null,
          "observation": "When risk is dominant value, dependency is treated as risk; mitigation needed.",
          "sample_size": 1,
          "confidence_initial": 0.61
        }
      ],
      "quant": {
        "prevalence_estimate": 0.55,
        "severity_estimate": 0.7,
        "value_at_stake_usd_estimate": 350000,
        "time_cost_minutes_estimate": 0,
        "risk_level": "medium",
        "uncertainty": { "confidence": 0.61, "variance": 0.29, "last_updated": "2026-02-10" }
      },
      "recommended_actions": [
        {
          "action_id": "act_lh_0011",
          "action_type": "policy",
          "description": "Publish portability pack: data export spec, audit export spec, rule provenance export, and offboarding playbook.",
          "owner": "legal",
          "effort": "m",
          "expected_roi": { "metric_id": "m_stage_conversion_rate", "direction": "increase", "magnitude_estimate": 0.08 },
          "test_plan": { "method": "pilot", "success_metrics": ["m_procurement_cycle_days"], "min_runtime_days": 60 }
        }
      ],
      "tags": ["dependency_risk", "portability", "procurement"],
      "status": "draft",
      "governance": { "created_by": "system", "created_at": "2026-02-10", "review_cadence_days": 30, "privacy": "internal", "compliance_flags": ["pii_free", "assumption_flagged"] }
    },

    {
      "ethno_object_id": "eo_lh_0012",
      "object_type": "METRIC",
      "title": "Time-to-Liquidity Variance (not just average)",
      "summary": "Lifehouse optimizes on variance bands and tail risk; mean values are insufficient for governance and portfolio planning.",
      "domain": {
        "product_line": "liquidity_infrastructure",
        "industry": "insurance_finance",
        "workflow": "portfolio_reporting",
        "stage": "piloting",
        "channel": "reporting",
        "jurisdiction": [],
        "counterparty_types": ["institutional_investor"]
      },
      "causal_claim": {
        "claim": "If LiquiFex reports variance bands (P50/P90) and tail drivers, governance approval increases and escalations decrease.",
        "mechanism": "variance clarity reduces surprises and committee objections",
        "expected_effects": [
          { "metric_id": "m_governance_acceptance_rate", "direction": "increase", "magnitude_estimate": 0.12 },
          { "metric_id": "m_escalation_rate", "direction": "decrease", "magnitude_estimate": 0.1 }
        ],
        "scope_conditions": ["institutional committees"],
        "counterexamples": ["small operators with informal planning"]
      },
      "evidence": [
        {
          "evidence_id": "ev_lh_0012",
          "evidence_type": "project_context",
          "source_ref": "LiquiFex ROI calculator prompts + predictability framing + catastrophic failure avoidance",
          "verbatim_snippet": null,
          "observation": "The project’s ROI logic implies forecasting and variance management are core outputs.",
          "sample_size": 2,
          "confidence_initial": 0.67
        }
      ],
      "quant": {
        "prevalence_estimate": 0.65,
        "severity_estimate": 0.65,
        "value_at_stake_usd_estimate": 300000,
        "time_cost_minutes_estimate": 0,
        "risk_level": "medium",
        "uncertainty": { "confidence": 0.67, "variance": 0.23, "last_updated": "2026-02-10" }
      },
      "recommended_actions": [
        {
          "action_id": "act_lh_0012",
          "action_type": "ux_change",
          "description": "Default all dashboards and exports to show P50/P90 cycle time and a ‘Top drivers of variance’ section with rule provenance.",
          "owner": "product",
          "effort": "m",
          "expected_roi": { "metric_id": "m_governance_acceptance_rate", "direction": "increase", "magnitude_estimate": 0.1 },
          "test_plan": { "method": "ab_test", "success_metrics": ["m_governance_acceptance_rate"], "min_runtime_days": 45 }
        }
      ],
      "tags": ["metric", "variance_bands", "portfolio_reporting"],
      "status": "draft",
      "governance": { "created_by": "system", "created_at": "2026-02-10", "review_cadence_days": 30, "privacy": "internal", "compliance_flags": ["pii_free"] }
    },

    {
      "ethno_object_id": "eo_lh_0013",
      "object_type": "SEGMENT",
      "title": "Institutional life-insurance capital operators",
      "summary": "High-LTV cohort: large exposure, low variance tolerance, strong willingness to pay for auditable control planes; longer sales cycles but compounding expansion.",
      "domain": {
        "product_line": "liquidity_infrastructure",
        "industry": "insurance_finance",
        "workflow": "go_to_market",
        "stage": "targeting",
        "channel": "sales",
        "jurisdiction": [],
        "counterparty_types": ["institutional_investor"]
      },
      "causal_claim": {
        "claim": "If LiquiFex productizes governance and audit as first-class features, this segment becomes the fastest path to scalable ARR despite longer cycles.",
        "mechanism": "high willingness to pay for risk control; expansion after trust established",
        "expected_effects": [{ "metric_id": "m_ltv", "direction": "increase", "magnitude_estimate": 0.25 }],
        "scope_conditions": ["institutional operators"],
        "counterexamples": ["small advisors who buy purely on price"]
      },
      "evidence": [
        {
          "evidence_id": "ev_lh_0013",
          "evidence_type": "project_context",
          "source_ref": "LiquiFex prompts emphasize rapid adoption, pilot tiers, and upsell/cross-sell/downsell strategy",
          "verbatim_snippet": null,
          "observation": "Segment strategy implies tiered scaling and expansion economics are central to plan.",
          "sample_size": 2,
          "confidence_initial": 0.63
        }
      ],
      "quant": {
        "prevalence_estimate": 0.5,
        "severity_estimate": 0.6,
        "value_at_stake_usd_estimate": 0,
        "time_cost_minutes_estimate": 0,
        "risk_level": "medium",
        "uncertainty": { "confidence": 0.63, "variance": 0.27, "last_updated": "2026-02-10" }
      },
      "recommended_actions": [
        {
          "action_id": "act_lh_0013",
          "action_type": "training",
          "description": "Package ‘Institutional Control Tier’ offering: governance pack, audit exports, variance bands, and SLA-backed exception handling.",
          "owner": "sales",
          "effort": "m",
          "expected_roi": { "metric_id": "m_arr", "direction": "increase", "magnitude_estimate": 0.15 },
          "test_plan": { "method": "pilot", "success_metrics": ["m_close_rate", "m_expansion_rate"], "min_runtime_days": 90 }
        }
      ],
      "tags": ["segment", "institutional", "pricing_packaging"],
      "status": "draft",
      "governance": { "created_by": "system", "created_at": "2026-02-10", "review_cadence_days": 60, "privacy": "internal", "compliance_flags": ["pii_free"] }
    },

    {
      "ethno_object_id": "eo_lh_0014",
      "object_type": "TRIGGER",
      "title": "Capital trapped longer than modeled triggers board-level urgency",
      "summary": "When realized liquidity timelines exceed expected bands, opportunity cost becomes visible and drives leadership to seek infrastructure change.",
      "domain": {
        "product_line": "liquidity_infrastructure",
        "industry": "insurance_finance",
        "workflow": "portfolio_exception_management",
        "stage": "evaluating",
        "channel": "exec_meeting",
        "jurisdiction": [],
        "counterparty_types": ["institutional_investor"]
      },
      "causal_claim": {
        "claim": "If LiquiFex can tie trapped-capital events to explainable drivers (rules/artefacts), urgency converts into adoption rather than blame loops.",
        "mechanism": "root-cause clarity converts urgency to execution",
        "expected_effects": [{ "metric_id": "m_pilot_start_rate", "direction": "increase", "magnitude_estimate": 0.12 }],
        "scope_conditions": ["exception-heavy portfolios"],
        "counterexamples": ["teams without governance visibility into cycle times"]
      },
      "evidence": [
        {
          "evidence_id": "ev_lh_0014",
          "evidence_type": "project_context",
          "source_ref": "LiquiFex adoption urgency + pilot program emphasis; focus on speed-to-profit",
          "verbatim_snippet": null,
          "observation": "Project repeatedly frames urgency as key adoption driver; trigger object encodes that activation point.",
          "sample_size": 2,
          "confidence_initial": 0.65
        }
      ],
      "quant": {
        "prevalence_estimate": 0.55,
        "severity_estimate": 0.75,
        "value_at_stake_usd_estimate": 500000,
        "time_cost_minutes_estimate": 0,
        "risk_level": "medium",
        "uncertainty": { "confidence": 0.65, "variance": 0.25, "last_updated": "2026-02-10" }
      },
      "recommended_actions": [
        {
          "action_id": "act_lh_0014",
          "action_type": "ux_change",
          "description": "Create ‘Trapped Capital RCA’ report: what happened, why, rule provenance, and next-best actions to restore expected bands.",
          "owner": "product",
          "effort": "m",
          "expected_roi": { "metric_id": "m_pilot_start_rate", "direction": "increase", "magnitude_estimate": 0.1 },
          "test_plan": { "method": "pilot", "success_metrics": ["m_pilot_start_rate", "m_sales_cycle_days"], "min_runtime_days": 45 }
        }
      ],
      "tags": ["trigger", "urgency", "root_cause_analysis"],
      "status": "draft",
      "governance": { "created_by": "system", "created_at": "2026-02-10", "review_cadence_days": 30, "privacy": "internal", "compliance_flags": ["pii_free"] }
    },

    {
      "ethno_object_id": "eo_lh_0015",
      "object_type": "FRICTION",
      "title": "Committee buying requires multi-role alignment (ops + compliance + investing)",
      "summary": "Lifehouse likely requires alignment across investment, operations, and compliance. Single-threaded ROI pitch fails without role-specific artifacts.",
      "domain": {
        "product_line": "liquidity_infrastructure",
        "industry": "insurance_finance",
        "workflow": "stakeholder_alignment",
        "stage": "evaluating",
        "channel": "internal",
        "jurisdiction": [],
        "counterparty_types": ["institutional_investor"]
      },
      "causal_claim": {
        "claim": "If LiquiFex does not deliver role-specific artifacts (ops playbooks, compliance exports, investment variance bands), adoption stalls.",
        "mechanism": "multi-stakeholder gating + differing success criteria",
        "expected_effects": [{ "metric_id": "m_stage_conversion_rate", "direction": "decrease", "magnitude_estimate": 0.1 }],
        "scope_conditions": ["institutional procurement", "regulated workflows"],
        "counterexamples": ["single-threaded founder buyers"]
      },
      "evidence": [
        {
          "evidence_id": "ev_lh_0015",
          "evidence_type": "project_context",
          "source_ref": "LiquiFex prompts: IP counsel annotations, technical brief for attorneys, and structured variable capture for ROI",
          "verbatim_snippet": null,
          "observation": "Project already anticipates different audiences; this friction formalizes the need as a gating factor.",
          "sample_size": 2,
          "confidence_initial": 0.7
        }
      ],
      "quant": {
        "prevalence_estimate": 0.65,
        "severity_estimate": 0.7,
        "value_at_stake_usd_estimate": 450000,
        "time_cost_minutes_estimate": 0,
        "risk_level": "medium",
        "uncertainty": { "confidence": 0.7, "variance": 0.21, "last_updated": "2026-02-10" }
      },
      "recommended_actions": [
        {
          "action_id": "act_lh_0015",
          "action_type": "training",
          "description": "Generate a Lifehouse ‘Stakeholder Pack’: (1) Investor variance bands + liquidity velocity, (2) Ops workflow + exception playbooks, (3) Compliance/audit exports.",
          "owner": "sales",
          "effort": "m",
          "expected_roi": { "metric_id": "m_stage_conversion_rate", "direction": "increase", "magnitude_estimate": 0.12 },
          "test_plan": { "method": "pilot", "success_metrics": ["m_stage_conversion_rate"], "min_runtime_days": 60 }
        }
      ],
      "tags": ["committee_buying", "multi_role", "enablement"],
      "status": "draft",
      "governance": { "created_by": "system", "created_at": "2026-02-10", "review_cadence_days": 30, "privacy": "internal", "compliance_flags": ["pii_free", "assumption_flagged"] }
    }
  ],
  "metric_dictionary": [
    { "metric_id": "m_time_to_liquidity", "definition": "Elapsed days from liquidity request/need to funds availability", "unit": "days" },
    { "metric_id": "m_time_to_liquidity_variance", "definition": "Variance or spread (P90-P50) in time-to-liquidity", "unit": "days" },
    { "metric_id": "m_manual_steps", "definition": "Count of human steps per case/workflow", "unit": "count" },
    { "metric_id": "m_cost_to_serve", "definition": "Operational cost per case or per policy block", "unit": "usd" },
    { "metric_id": "m_error_rate", "definition": "Defects requiring rework or causing incorrect outputs", "unit": "ratio" },
    { "metric_id": "m_escalation_rate", "definition": "Cases requiring escalation to experts/leadership", "unit": "ratio" },
    { "metric_id": "m_governance_acceptance_rate", "definition": "Percent of governance reviews approving scope/controls", "unit": "ratio" },
    { "metric_id": "m_sales_cycle_days", "definition": "Days from first meeting to signed agreement", "unit": "days" },
    { "metric_id": "m_stage_conversion_rate", "definition": "Conversion between sales stages (eval→pilot→expand)", "unit": "ratio" },
    { "metric_id": "m_pilot_start_rate", "definition": "Rate at which evaluation converts into an active pilot", "unit": "ratio" },
    { "metric_id": "m_pilot_success_rate", "definition": "Pilot meets success criteria and proceeds to expansion", "unit": "ratio" },
    { "metric_id": "m_pilot_to_expand_rate", "definition": "Pilot expands to broader scope", "unit": "ratio" },
    { "metric_id": "m_scope_of_deployment", "definition": "Breadth of workflows/policies covered by LiquiFex", "unit": "index" },
    { "metric_id": "m_time_to_value", "definition": "Days to first measurable operational or financial improvement", "unit": "days" },
    { "metric_id": "m_ltv", "definition": "Estimated customer lifetime value", "unit": "usd" },
    { "metric_id": "m_arr", "definition": "Annual recurring revenue", "unit": "usd" },
    { "metric_id": "m_adoption_stage", "definition": "Ordinal adoption stage (unaware→live→expanding)", "unit": "ordinal" }
  ],
  "next_collection_plan": {
    "highest_roi_missing_evidence": [
      "Lifehouse: current-state process maps and artefacts (spreadsheets, PDFs, email threads)",
      "Lifehouse: governance/compliance requirements (audit export formats, retention, approvals)",
      "Lifehouse: baseline cycle times and variance (P50/P90) for 1–2 critical workflows",
      "Lifehouse: stakeholder map + buying process (committee members, gating criteria)"
    ],
    "telemetry_events_to_instrument": [
      "workflow_started",
      "step_completed",
      "rule_fired",
      "exception_triggered",
      "human_override_used",
      "audit_export_generated",
      "case_resolved",
      "cycle_time_recorded"
    ],
    "confidence_update_method": "Bayesian update on confidence using telemetry + artefact validation; decay confidence 5% per 30 days without reinforcing evidence."
  }
}
```

## Prompt:
Generate a Lifehouse-specific LiquiFex demo flow that dynamically adapts based on these objects

## Response:
Thought for 20s

Lifehouse-specific LiquiFex demo flow (adaptive)
------------------------------------------------

Design intent: **convert Lifehouse’s governance + predictability priorities into a deterministic demo path** that (a) proves auditability first, (b) quantifies variance reduction, (c) shows portability/exit safety, then (d) only introduces automation/AI as “controlled execution.”

This flow dynamically adapts based on the ethno-objects you already have (auditability, carrier variance, spreadsheet controls, tail-risk, committee buying).

* * *

1) Demo entry: pick the stakeholder lens (max 7)
================================================

**Screen:** “What role are you wearing today?”  
Options (<=7):

1.  Investment / Portfolio (principal)
2.  Operations / Servicing
3.  Compliance / Risk
4.  Data / Integration
5.  Executive sponsor
6.  Committee / Procurement
7.  Other (routes to 1 follow-up)

**Routing rule**

*   Investment → prioritize **variance bands + trapped capital RCA**
*   Ops → prioritize **rules+exceptions execution + exception playbooks**
*   Compliance → prioritize **audit exports + provenance + retention**
*   Data → prioritize **artefact ingestion + schema mapping + portability**
*   Committee/Procurement → prioritize **controls, dependency mitigation, exit pack**

* * *

2) Context capture (Rule-of-7 compliant)
========================================

**Screen:** “Pick your current state (choose up to 3).”

1.  Multi-carrier variability
2.  Multi-state variability
3.  Document-driven rules (PDF/email)
4.  Spreadsheet control plane
5.  Unpredictable time-to-liquidity
6.  High escalation rate
7.  Vendor dependency concern

**Routing rule**

*   If (5) → enable **Variance Dashboard module**
*   If (4) → enable **Spreadsheet-to-Controls migration module**
*   If (3) → enable **Artefact → Rules pipeline module**
*   If (7) → enable **Portability pack module**
*   If (1 or 2) → enable **Rules+Exceptions module**

* * *

3) Trigger selection (the “why now”)
====================================

**Screen:** “What triggered this evaluation?”

1.  Trapped capital longer than modeled
2.  Audit/governance friction
3.  Scaling servicing cost
4.  A specific carrier event / exception spike
5.  Committee mandate (prove controls)
6.  Growth / portfolio expansion
7.  Other

**Routing rule**

*   (1) routes to **Trapped Capital RCA** first
*   (2)/(5) routes to **Audit Trail & Exports** first (no ROI fluff)
*   (3) routes to **Manual steps + cost-to-serve** quant
*   (4) routes to **Exception playbook + escalation thresholds**

* * *

4) The “Trust Gate” module (always first for Lifehouse)
=======================================================

Module A — Mechanics & Audit Trail (2–4 minutes)
------------------------------------------------

**Goal:** satisfy “If it can’t be audited, it can’t scale.”

**Show (in this order):**

1.  **Workflow map**: request → rule evaluation → execution → exception → override → export
2.  **Decision path viewer** (per case):
    *   rules fired
    *   evidence used (artefacts/fields)
    *   who approved/overrode
    *   timestamps
3.  **Provenance ledger**
    *   rule source (doc/email/policy clause)
    *   effective dates/versioning
4.  **Audit export**
    *   reproducible “why” narrative + raw event log

**Adaptive callouts**

*   If user uses phrase like _“mechanics”_ (EO-LH-0008) → expand provenance + versioning detail
*   If compliance persona → show retention, access controls, SOC2-style controls mapping placeholders

* * *

5) Variance-first outcomes (not average-first)
==============================================

Module B — Time-to-Liquidity Variance Dashboard (3–5 minutes)
-------------------------------------------------------------

**Goal:** “Predictability beats optimization.”

**Show:**

1.  **P50/P90 timeline** for 1–2 liquidity workflows
2.  **Top drivers of variance** (ranked):
    *   carrier rule conditions
    *   jurisdiction rules
    *   missing artefacts/fields
    *   exception categories
3.  **Tail-risk controls**:
    *   escalation thresholds
    *   playbook selection
    *   human override governance

**Adaptive branching**

*   If “reputation risk dominates yield” (EO-LH-0006) signal → emphasize **P90/P99 containment** and “no surprises” posture
*   If investment persona → tie variance reduction to **capital velocity** and **opportunity cost** (not yield)

* * *

6) Rules + Exceptions execution (the scaling engine)
====================================================

Module C — Rules+Exceptions Layer (3–6 minutes)
-----------------------------------------------

**Goal:** neutralize “carrier/jurisdiction variability destroys standardization.”

**Show:**

1.  Rule objects (carrier/state/product applicability)
2.  Exceptions model (known exception classes + handling)
3.  Versioning + “what changed” diffs
4.  How a new rule gets added:
    *   artefact ingestion → extraction → human review → publish → telemetry

**Adaptive branching**

*   If ops persona OR exception spike trigger → demo “exception triage” UX:
    *   classify exception
    *   auto-recommend next action
    *   assign owner
    *   generate required doc checklist

* * *

7) Artefacts to structured rules (document reality)
===================================================

Module D — Artefact ingestion pipeline (2–4 minutes)
----------------------------------------------------

**Goal:** prove you can operationalize PDFs/emails into auditable rules.

**Show:**

1.  Drag-drop artefact types (PDF, email thread, scanned form)
2.  Extracted fields + confidence scores
3.  Human review queue (approve/reject/edit)
4.  Published rule with provenance link back to source artefact

**Adaptive branching**

*   If they selected “document-driven rules” → this module becomes mandatory

* * *

8) Spreadsheet dependency migration (control transfer)
======================================================

Module E — Spreadsheet → Controls migration (2–5 minutes)
---------------------------------------------------------

**Goal:** eliminate dual-run and key-person risk.

**Show:**

1.  Import spreadsheet columns → map to LiquiFex entities
2.  Detect drift / missing fields / conflicting definitions
3.  Control dashboard replacing spreadsheet:
    *   exceptions
    *   cycle time variance
    *   audit exports
4.  “Dual-run exit checklist” (time-boxed)

**Adaptive branching**

*   If “spreadsheet control plane” selected → show this before rules engine depth

* * *

9) Portability / dependency risk mitigation (committee closer)
==============================================================

Module F — Portability Pack (1–2 minutes)
-----------------------------------------

**Goal:** address vendor dependency fear.

**Show:**

1.  Data export spec (entities + history)
2.  Rule provenance export (rules + sources + versions)
3.  Audit log export (event stream)
4.  Offboarding playbook (what you retain)

* * *

10) Close: propose a Lifehouse pilot (pre-baked)
================================================

Module G — 60-day pilot blueprint (2 minutes)
---------------------------------------------

**Pilot objective:** reduce variance + prove auditability on 1 workflow.

**Outputs**

*   Baseline P50/P90 + driver attribution
*   Working audit export for governance
*   Rules+exceptions deployed for selected workflow
*   Exception playbooks + thresholds
*   Portability pack delivered

**Success metrics (choose up to 5)**

*   ↓ P90 time-to-liquidity
*   ↓ variance spread (P90–P50)
*   ↓ escalations
*   ↓ manual steps
*   ↑ governance acceptance rate

* * *

2) Adaptive engine: routing rules (simple + deterministic)
==========================================================

### A) Trigger-based priority

*   If trigger ∈ {Audit friction, Committee mandate} → start at **Module A**, then **F**, then **G**
*   If trigger = Trapped capital → **A → B → G**
*   If trigger = Exception spike → **A → C → B → G**

### B) Persona-based depth

*   Investment: A (light) → B (deep) → G
*   Ops: A (light) → C (deep) → D/E as needed → G
*   Compliance: A (deep) → F (deep) → B (light) → G
*   Data: D (deep) → C (medium) → F (medium) → G

### C) Language-token switches

*   If token matches “mechanics / audit / explain” → expand:
    *   provenance ledger
    *   versioning diffs
    *   export formats
*   If token matches “dependency / lock-in” → jump to **Module F** immediately

* * *

3) Demo flow as a configuration JSON (plug into a front-end)
============================================================

```
{
  "demo_flow_id": "liquifex_lifehouse_v1",
  "constraints": {
    "max_options_per_screen": 7,
    "max_required_fields_per_step": 7,
    "fallback_when_uncertain": "ask_one_followup_then_default_to_module_A"
  },
  "screens": [
    {
      "id": "role_select",
      "type": "single_select",
      "prompt": "What role are you wearing today?",
      "options": ["investment", "operations", "compliance", "data", "exec", "procurement", "other"],
      "next": "context_select"
    },
    {
      "id": "context_select",
      "type": "multi_select",
      "prompt": "Pick your current state (choose up to 3).",
      "options": ["multi_carrier", "multi_state", "document_rules", "spreadsheet_controls", "unpredictable_ttl", "high_escalations", "vendor_dependency"],
      "next": "trigger_select"
    },
    {
      "id": "trigger_select",
      "type": "single_select",
      "prompt": "What triggered this evaluation?",
      "options": ["trapped_capital", "audit_friction", "cost_to_serve", "exception_spike", "committee_mandate", "growth", "other"],
      "next": "module_router"
    }
  ],
  "modules": {
    "A_mechanics_audit": { "duration_min": 3, "always_first_for": ["lifehouse"] },
    "B_variance_dashboard": { "duration_min": 4 },
    "C_rules_exceptions": { "duration_min": 5 },
    "D_artefact_pipeline": { "duration_min": 3 },
    "E_spreadsheet_migration": { "duration_min": 4 },
    "F_portability_pack": { "duration_min": 2 },
    "G_pilot_blueprint": { "duration_min": 2 }
  },
  "routing_rules": [
    { "if": { "trigger": ["audit_friction", "committee_mandate"] }, "then": ["A_mechanics_audit", "F_portability_pack", "G_pilot_blueprint"] },
    { "if": { "trigger": ["trapped_capital"] }, "then": ["A_mechanics_audit", "B_variance_dashboard", "G_pilot_blueprint"] },
    { "if": { "trigger": ["exception_spike"] }, "then": ["A_mechanics_audit", "C_rules_exceptions", "B_variance_dashboard", "G_pilot_blueprint"] },

    { "if": { "context_any": ["document_rules"] }, "then_add": ["D_artefact_pipeline"] },
    { "if": { "context_any": ["spreadsheet_controls"] }, "then_add": ["E_spreadsheet_migration"] },
    { "if": { "context_any": ["vendor_dependency"] }, "then_add_front": ["F_portability_pack"] },

    { "if": { "role": ["compliance", "procurement"] }, "then_promote_depth": ["A_mechanics_audit", "F_portability_pack"] },
    { "if": { "role": ["investment"] }, "then_promote_depth": ["B_variance_dashboard"] },
    { "if": { "role": ["operations"] }, "then_promote_depth": ["C_rules_exceptions"] }
  ],
  "language_tokens": [
    { "match_any": ["mechanics", "audit", "explain", "governance"], "then_add_front": ["A_mechanics_audit"] },
    { "match_any": ["lock-in", "dependency", "exit"], "then_add_front": ["F_portability_pack"] }
  ]
}
```

* * *

What this demo flow optimizes for (Lifehouse fit)
-------------------------------------------------

*   **Trust-before-automation sequencing** (fastest approval path)
*   **Variance reduction as the core ROI** (institutional value function)
*   **Auditability + provenance** as first-class product proof
*   **Committee enablement** baked into routing, not bolted on later
*   **Portability** to neutralize dependency objections early

If you want the next layer: I can turn each module into a **screen-by-screen script** (exact UI panels, what the presenter says, what questions to ask, what metrics to show) while staying within the Rule-of-7 constraints.

## Prompt:
yes

## Response:
Lifehouse LiquiFex demo script (screen-by-screen, adaptive, Rule-of-7 compliant)
--------------------------------------------------------------------------------

**Run-time target:** 18–25 minutes end-to-end.  
**Default path:** Auditability → Variance → Rules/Exceptions → Pilot.  
**Adaptive inserts:** Artefact pipeline, Spreadsheet migration, Portability pack.

* * *

0) Operator setup (before the call)
===================================

**Have ready (no more than 7 artifacts):**

1.  One “sample case” record (synthetic) with carrier + state + product fields
2.  One PDF artefact (synthetic carrier form)
3.  One spreadsheet (synthetic control sheet)
4.  Audit export (CSV/JSON + human-readable summary)
5.  Variance dashboard screenshot (P50/P90)
6.  Rules+exceptions viewer screenshot
7.  Pilot blueprint one-pager

* * *

1) Entry: Stakeholder lens (Screen 1)
=====================================

**UI:** Single select  
**Prompt:** “What role are you wearing today?”

Options (<=7):

1.  Investment / Portfolio
2.  Operations / Servicing
3.  Compliance / Risk
4.  Data / Integration
5.  Procurement / Committee
6.  Executive sponsor
7.  Other

**Presenter script (10–15 sec):**  
“LiquiFex is a liquidity control plane for insurance infrastructure. This demo adapts based on what you need to validate today—governance, predictability, execution, or integration.”

**Branching:**

*   Investment → deepen Modules B, G
*   Ops → deepen Modules C, E
*   Compliance/Procurement → deepen Modules A, F
*   Data → deepen Modules D, C, F

* * *

2) Context capture (Screen 2)
=============================

**UI:** Multi-select (max 3)  
**Prompt:** “Pick your current state (choose up to 3).”

Options:

1.  Multi-carrier variability
2.  Multi-state variability
3.  Rules live in PDFs/emails
4.  Spreadsheets as controls
5.  Unpredictable time-to-liquidity
6.  High escalation rate
7.  Vendor dependency concern

**Presenter script (10–20 sec):**  
“These three choices determine what we show and what we skip. We’re optimizing for signal, not feature touring.”

**Branching flags:**

*   (3) → insert Module D
*   (4) → insert Module E
*   (7) → pull Module F earlier
*   (1)/(2) → ensure Module C depth
*   (5) → ensure Module B depth

* * *

3) Trigger (Screen 3)
=====================

**UI:** Single select  
**Prompt:** “What triggered this evaluation?”

Options:

1.  Trapped capital longer than modeled
2.  Audit/governance friction
3.  Scaling cost-to-serve
4.  Exception spike (carrier event)
5.  Committee mandate (prove controls)
6.  Growth / expansion
7.  Other

**Presenter script (10–15 sec):**  
“Whatever you pick, we start with the same gate: can this survive governance? Then we show predictability, then scaling.”

**Routing (hard rules):**

*   Audit friction / committee → A → F → B (light) → G
*   Trapped capital → A → B → G
*   Exception spike → A → C → D (if selected) → G
*   Cost-to-serve → A → C → E (if selected) → G

* * *

4) Trust Gate (Module A): Mechanics + Audit Trail (Screens 4–7)
===============================================================

Screen 4 — Workflow map
-----------------------

**UI:** Diagram  
**Presenter:**  
“LiquiFex treats each liquidity event as an executable workflow with explicit rules, exceptions, and a complete event log. Nothing is hidden; everything is reproducible.”

**Show (4 nodes max on screen):**

1.  Intake → 2) Rule evaluation → 3) Execution → 4) Export/Audit

**Ask (1 question max):**  
“Is your governance standard closer to ‘audit-ready always’ or ‘audit on request’?”

* * *

Screen 5 — Decision Path Viewer
-------------------------------

**UI:** Case view (collapsed)  
**Presenter:**  
“This is the critical object: the _decision path_. It shows what rules fired, what evidence was used, and what alternatives were rejected.”

**On-screen (<=7 fields):**

*   Case ID
*   Carrier
*   State
*   Product type
*   Rules fired (count)
*   Exceptions (count)
*   Status

**If they say “mechanics / explain / governance”:**  
Expand the “Rules fired” list and show **provenance links**.

* * *

Screen 6 — Provenance ledger (Rule source)
------------------------------------------

**UI:** Table (<=7 rows visible)  
**Presenter:**  
“Every rule has provenance: source document, effective date, and the exact clause or data element used. This kills black-box objections.”

Columns (<=4): Rule | Source | Effective date | Confidence

**Ask:**  
“Do you need versioning diffs for regulatory defensibility?”

*   If yes → show “what changed” diff panel (1 minute)

* * *

Screen 7 — Audit export
-----------------------

**UI:** Download/Export panel (simulated)  
**Presenter:**  
“Here is the audit export: a machine-readable event log plus a human-readable narrative that reconstructs the decision.”

Export types (<=5):

*   Event log (JSON)
*   Audit summary (PDF/HTML)
*   Rules snapshot (JSON)
*   Evidence index (CSV)
*   Override register (CSV)

**Close Module A:**  
“If we can’t do this, nothing else matters. If we _can_, now we talk predictability and scale.”

* * *

5) Predictability engine (Module B): Variance bands (Screens 8–10)
==================================================================

Screen 8 — P50/P90 timeline
---------------------------

**UI:** Simple chart  
**Presenter:**  
“Institutions don’t manage on averages. We manage on variance bands. This shows P50 and P90 time-to-liquidity, per workflow.”

**Ask:**  
“Which matters more: tightening P90 or reducing escalations?”

*   P90 → emphasize tail controls
*   Escalations → emphasize exception playbooks

* * *

Screen 9 — Drivers of variance
------------------------------

**UI:** Ranked list (<=7 drivers)  
**Presenter:**  
“Here are the drivers of variance. Each driver links back to the exact rule/evidence.”

Example drivers:

1.  Missing artefact fields
2.  Carrier rule exception class
3.  State-specific constraint
4.  Product-specific loan terms
5.  Manual approval step
6.  Data model mismatch
7.  Waiting on counterparty

**If reputational risk concern surfaces:**  
Add: “P90 containment playbook” preview.

* * *

Screen 10 — Tail-risk controls
------------------------------

**UI:** Threshold settings  
**Presenter:**  
“These are your controls: escalation thresholds, required approvals, and override governance.”

Show (<=7 toggles):

*   Escalate if > P90 forecast
*   Escalate on missing critical fields
*   Require approval for override
*   Lock rule versions per period
*   Auto-generate governance packet
*   SLA timer on counterparty waits
*   Exception playbook auto-attach

* * *

6) Scale engine (Module C): Rules + Exceptions (Screens 11–13)
==============================================================

Screen 11 — Rules objects (applicability)
-----------------------------------------

**Presenter:**  
“Carrier variability is not a bug; it’s a data model. We treat rules as first-class objects with applicability conditions.”

Show (<=6 fields):

*   Carrier
*   Product type
*   Jurisdiction
*   Condition
*   Action
*   Version

* * *

Screen 12 — Exceptions model
----------------------------

**Presenter:**  
“Exceptions are inevitable. LiquiFex makes them predictable by classifying them and attaching playbooks.”

Show (<=7 exception classes):

1.  Missing evidence
2.  Conflicting rule sources
3.  Carrier delay
4.  Jurisdiction ambiguity
5.  Manual approval required
6.  Data mismatch
7.  Out-of-policy request

* * *

Screen 13 — Change management / versioning
------------------------------------------

**Presenter:**  
“When rules change, we don’t ‘update the system.’ We publish new versions with diffs, provenance, and governance controls.”

**Ask:**  
“Do you need ‘frozen rules’ per reporting period?”

*   If yes: show “snapshot rules for quarter” export

* * *

7) Conditional insert: Artefact pipeline (Module D) (Screens 14–15)
===================================================================

**Only if context includes PDFs/emails.**

Screen 14 — Artefact ingestion
------------------------------

**Presenter:**  
“Your real rulebook is in PDFs and email threads. LiquiFex converts those into structured rules with provenance.”

Show pipeline steps (<=5):  
Upload → Extract → Review → Publish → Monitor drift

Screen 15 — Human review queue
------------------------------

**Presenter:**  
“We don’t pretend extraction is perfect. We show confidence scores and route low-confidence items to review.”

Fields (<=7):

*   Artefact ID
*   Extracted fields count
*   Confidence
*   Reviewer
*   Status
*   Published rule link
*   Notes

* * *

8) Conditional insert: Spreadsheet migration (Module E) (Screens 16–17)
=======================================================================

**Only if context includes spreadsheets as controls.**

Screen 16 — Import and map
--------------------------

**Presenter:**  
“Spreadsheets are a control plane. We replace them by importing them and turning the controls into auditable system controls.”

Show (<=7 columns mapped):

*   Policy ID
*   Carrier
*   State
*   Product
*   Expected TTL
*   Current status
*   Notes

Screen 17 — Dual-run exit checklist
-----------------------------------

**Presenter:**  
“Dual-run kills ROI. This gives a time-boxed exit plan.”

Checklist (<=7):

1.  Field parity achieved
2.  Rule parity validated
3.  Audit export approved
4.  Exceptions stabilized
5.  Override governance adopted
6.  Reporting reconciled
7.  Offboarding export tested

* * *

9) Conditional insert: Portability pack (Module F) (Screen 18)
==============================================================

**If vendor dependency concern or procurement persona.**

**Presenter:**  
“This neutralizes lock-in: you own the rules, evidence links, and event history.”

Show 4 exports:

*   Data export
*   Rules+provenance export
*   Audit/event export
*   Offboarding playbook

* * *

10) Close: 60-day Lifehouse pilot blueprint (Module G) (Screens 19–21)
======================================================================

Screen 19 — Pick 1 workflow (<=7 options)
-----------------------------------------

Prompt: “Select one workflow for pilot.”

Options:

1.  Policy loan / liquidity request
2.  Premium finance unwind
3.  Collateral update / servicing
4.  Carrier document reconciliation
5.  Exception triage pipeline
6.  Portfolio variance reporting
7.  Other

**Presenter:**  
“We pick the workflow with the highest variance pain and lowest integration surface.”

* * *

Screen 20 — Success metrics (choose up to 5)
--------------------------------------------

Options:

1.  ↓ P90 time-to-liquidity
2.  ↓ variance spread (P90–P50)
3.  ↓ escalation rate
4.  ↓ manual steps
5.  ↑ governance acceptance rate
6.  ↑ audit export usage
7.  ↓ exception resolution time

**Presenter:**  
“These are operational metrics that translate to capital velocity and reduced tail risk.”

* * *

Screen 21 — Deliverables + timeline
-----------------------------------

**Presenter:**  
“Day 0–10 baseline; Day 11–30 rules+audit; Day 31–60 variance tightening + exception playbooks.”

Deliverables (<=7):

1.  Baseline P50/P90 and drivers
2.  Audit export approved
3.  Rules+exceptions deployed
4.  Artefact pipeline (if needed)
5.  Spreadsheet migration (if needed)
6.  Tail-risk thresholds configured
7.  Portability pack delivered

**Close question (single):**  
“Who must sign off—investment, ops, compliance, or procurement—and what’s their non-negotiable control requirement?”

* * *

Adaptive “if they push back” responses (short, institutional)
=============================================================

Objection: “This looks like AI risk”
------------------------------------

**Response:**  
“LiquiFex is deterministic control first. Probabilistic components are optional, bounded, and fully auditable with human override.”

Objection: “Carrier rules change; you’ll go stale”
--------------------------------------------------

**Response:**  
“Rules are versioned with provenance, monitored for drift, and updated through a review workflow. Staleness becomes a detected exception, not a silent failure.”

Objection: “We can’t be dependent on a vendor”
----------------------------------------------

**Response:**  
“You own exports for data, rules, provenance, and event history. We provide an offboarding playbook. Dependency risk is explicitly mitigated.”

* * *

Output: talk track checklist (what to say vs what to show)
==========================================================

**Say (positioning):**

*   “Auditable liquidity control plane”
*   “Variance bands, not averages”
*   “Rules+exceptions as infrastructure”
*   “Tail-risk containment”

**Avoid (triggers governance resistance):**

*   “AI magic”
*   “Fully automated”
*   “Black-box optimization”
*   “Trust us”

* * *

If you want this to be fully executable: I can produce (1) a **demo UI wireframe list** per screen (components + fields), and (2) a **single JSON config** that a front-end can run to render the adaptive flow and log telemetry events for confidence updates.

## Prompt:
do all please

## Response:
1) Demo UI wireframe list (Lifehouse LiquiFex, v1)
--------------------------------------------------

Design system: **panel-based** layout with a left “Flow” rail, a main content canvas, and a right “Evidence/Audit” drawer that is always available.

### Global layout (all screens)

*   **Header:** Account = Lifehouse Capital | Workflow = {selected} | Mode = Demo | Timer
*   **Left rail:** Steps (auto-generated by router)
*   **Main canvas:** Screen content
*   **Right drawer (persistent):**  
    Tabs: `Provenance` | `Event Log` | `Exports` | `Overrides`
*   **Footer:** Back | Next | “Ask a question” (free text token capture)

### Screen inventory (modules → screens)

#### S1 — Role Select

*   Component: `SingleSelectCardGrid`
*   Fields: role (`investment|operations|compliance|data|procurement|exec|other`)
*   Event hooks: `demo.role_selected`

#### S2 — Context Select (max 3)

*   Component: `MultiSelectChips`
*   Options: `multi_carrier, multi_state, document_rules, spreadsheet_controls, unpredictable_ttl, high_escalations, vendor_dependency`
*   Constraint UI: “3 selected” cap with soft error
*   Event hooks: `demo.context_selected`

#### S3 — Trigger Select

*   Component: `SingleSelectList`
*   Options: `trapped_capital, audit_friction, cost_to_serve, exception_spike, committee_mandate, growth, other`
*   Event hooks: `demo.trigger_selected`

* * *

### Module A — Mechanics + Audit Trail

#### A1 — Workflow Map

*   Component: `WorkflowDiagram`
*   Nodes (fixed 4): Intake → Rule Eval → Execute → Export/Audit
*   Side panel: “Governance mode” toggle: `audit_ready_always|audit_on_request`
*   Event hooks: `workflow.viewed`, `governance.mode_set`

#### A2 — Case Overview (Sample Case)

*   Component: `CaseSummaryPanel`
*   Fields (<=7):
    *   case\_id
    *   carrier
    *   state
    *   product\_type
    *   rules\_fired\_count
    *   exceptions\_count
    *   status
*   Actions: “Open Decision Path”
*   Event hooks: `case.opened`

#### A3 — Decision Path Viewer

*   Component: `DecisionPathTree`
*   Collapsed by default, expandable nodes:
    *   Rule fired → Evidence used → Result → Alternative rejected
*   Controls:
    *   “Show provenance links” toggle
    *   “Show version diffs” toggle
*   Event hooks: `decision_path.viewed`, `rule.fired_viewed`, `evidence.link_opened`

#### A4 — Provenance Ledger

*   Component: `Table`
*   Columns: rule\_id | source\_type | source\_ref | effective\_date | confidence
*   Row click opens right-drawer Provenance tab pre-filtered
*   Event hooks: `provenance.ledger_viewed`

#### A5 — Audit Export

*   Component: `ExportPanel`
*   Export types (<=5):
    *   event\_log\_json
    *   audit\_summary\_pdf\_html
    *   rules\_snapshot\_json
    *   evidence\_index\_csv
    *   override\_register\_csv
*   Event hooks: `export.generated`, `export.previewed`

* * *

### Module B — Variance Dashboard

#### B1 — P50/P90 Timeline

*   Component: `LineOrRangeChart`
*   Metrics:
    *   P50\_time\_to\_liquidity
    *   P90\_time\_to\_liquidity
*   Filters:
    *   workflow
    *   carrier
    *   state
*   Event hooks: `variance.chart_viewed`, `filter.changed`

#### B2 — Drivers of Variance

*   Component: `RankedDriverList`
*   Drivers (<=7):
    *   missing\_fields
    *   carrier\_exception\_class
    *   state\_constraint
    *   product\_terms
    *   manual\_approval\_step
    *   data\_model\_mismatch
    *   counterparty\_wait
*   Each driver links to rules/evidence in drawer
*   Event hooks: `variance.drivers_viewed`, `driver.opened`

#### B3 — Tail-Risk Controls

*   Component: `ThresholdControls`
*   Toggles (<=7):
    *   escalate\_if\_over\_p90
    *   escalate\_on\_missing\_critical
    *   approval\_required\_for\_override
    *   lock\_rule\_versions\_per\_period
    *   auto\_generate\_governance\_packet
    *   sla\_timer\_counterparty\_wait
    *   attach\_exception\_playbook
*   Event hooks: `tail_risk.controls_viewed`, `threshold.updated`

* * *

### Module C — Rules + Exceptions

#### C1 — Rules Objects (Applicability)

*   Component: `RuleObjectTable`
*   Fields:
    *   carrier, product\_type, jurisdiction, condition, action, version
*   Actions:
    *   “Create rule from artefact”
    *   “Compare versions”
*   Event hooks: `rules.table_viewed`, `rule.version_compared`

#### C2 — Exceptions Model

*   Component: `ExceptionClassGrid`
*   Classes (<=7):
    *   missing\_evidence
    *   conflicting\_sources
    *   carrier\_delay
    *   jurisdiction\_ambiguity
    *   manual\_approval\_required
    *   data\_mismatch
    *   out\_of\_policy
*   Event hooks: `exceptions.model_viewed`, `exception_class.opened`

#### C3 — Versioning & Change Management

*   Component: `VersionDiffViewer`
*   Panels:
    *   “What changed”
    *   “Who approved”
    *   “Effective date”
*   Event hooks: `versioning.viewed`, `rule.version_published`

* * *

### Module D — Artefact Pipeline (conditional)

#### D1 — Artefact Ingestion

*   Component: `UploadAndPipeline`
*   Artefact types: pdf | email\_thread | scanned\_form
*   Pipeline steps: upload → extract → review → publish → monitor
*   Event hooks: `artifact.uploaded`, `extraction.completed`

#### D2 — Human Review Queue

*   Component: `ReviewQueueTable`
*   Fields (<=7):
    *   artifact\_id
    *   extracted\_fields\_count
    *   confidence
    *   reviewer
    *   status
    *   linked\_rules
    *   notes
*   Event hooks: `review.queue_viewed`, `review.item_approved`, `review.item_rejected`

* * *

### Module E — Spreadsheet Migration (conditional)

#### E1 — Import & Map

*   Component: `SpreadsheetMapper`
*   Mapped columns (<=7):
    *   policy\_id
    *   carrier
    *   state
    *   product
    *   expected\_ttl
    *   current\_status
    *   notes
*   Event hooks: `spreadsheet.imported`, `mapping.completed`

#### E2 — Dual-Run Exit Checklist

*   Component: `Checklist`
*   Items (<=7):
    *   field\_parity
    *   rule\_parity
    *   audit\_export\_approved
    *   exceptions\_stabilized
    *   override\_governance\_adopted
    *   reporting\_reconciled
    *   offboarding\_export\_tested
*   Event hooks: `dualrun.checklist_viewed`, `checklist.item_toggled`

* * *

### Module F — Portability Pack (conditional / procurement)

#### F1 — Portability & Offboarding

*   Component: `PortabilityPackPanel`
*   Exports:
    *   data\_export\_spec
    *   rules\_provenance\_export
    *   audit\_event\_export
    *   offboarding\_playbook
*   Event hooks: `portability.viewed`, `export.spec_opened`

* * *

### Module G — 60-Day Pilot Blueprint

#### G1 — Choose Workflow (pilot)

*   Component: `SingleSelectCardGrid`
*   Options (<=7):
    *   policy\_loan
    *   premium\_finance\_unwind
    *   collateral\_update
    *   carrier\_doc\_reconciliation
    *   exception\_triage
    *   variance\_reporting
    *   other
*   Event hooks: `pilot.workflow_selected`

#### G2 — Choose Success Metrics (max 5)

*   Component: `MultiSelectChips`
*   Options (<=7):
    *   reduce\_p90\_ttl
    *   reduce\_variance\_spread
    *   reduce\_escalation\_rate
    *   reduce\_manual\_steps
    *   increase\_governance\_acceptance
    *   increase\_audit\_export\_usage
    *   reduce\_exception\_resolution\_time
*   Event hooks: `pilot.metrics_selected`

#### G3 — Timeline & Deliverables

*   Component: `TimelineWithDeliverables`
*   Phases:
    *   Day 0–10 baseline
    *   Day 11–30 rule+audit
    *   Day 31–60 variance tightening
*   Deliverables (<=7):
    *   baseline\_p50\_p90
    *   audit\_export\_approved
    *   rules\_exceptions\_deployed
    *   artifact\_pipeline\_if\_needed
    *   spreadsheet\_migration\_if\_needed
    *   tail\_risk\_thresholds\_configured
    *   portability\_pack\_delivered
*   Event hooks: `pilot.plan_viewed`, `pilot.plan_exported`

* * *

2) Single JSON config (adaptive demo + telemetry + confidence updates)
----------------------------------------------------------------------

```
{
  "schema_version": "liquifex_demo_flow_config_v1",
  "flow_id": "liquifex_lifehouse_demo_v1",
  "account": {
    "name": "Lifehouse Capital",
    "segment": "institutional_life_insurance_capital_operator"
  },
  "constraints": {
    "max_options_per_screen": 7,
    "max_required_fields_per_step": 7,
    "max_multi_select": { "context_select": 3, "pilot_metrics": 5 },
    "fallback_when_uncertain": "ask_one_followup_then_default_to_module_A"
  },
  "state_model": {
    "inputs": {
      "role": null,
      "context": [],
      "trigger": null,
      "language_tokens": []
    },
    "runtime": {
      "active_modules": [],
      "module_order": [],
      "depth_promotions": [],
      "confidence_overrides": {}
    }
  },
  "ethno_object_bindings": {
    "eo_refs": [
      "eo_lh_0001",
      "eo_lh_0002",
      "eo_lh_0003",
      "eo_lh_0004",
      "eo_lh_0005",
      "eo_lh_0006",
      "eo_lh_0007",
      "eo_lh_0008",
      "eo_lh_0009",
      "eo_lh_0010",
      "eo_lh_0011",
      "eo_lh_0012",
      "eo_lh_0013",
      "eo_lh_0014",
      "eo_lh_0015"
    ],
    "default_prior_confidence": 0.65,
    "confidence_update_policy": {
      "method": "bayesian_update_lightweight",
      "decay": { "rate": 0.05, "period_days": 30, "if_no_new_evidence": true },
      "telemetry_weight": 0.6,
      "human_validation_weight": 0.4
    }
  },
  "screens": [
    {
      "id": "S1_role_select",
      "module": "ENTRY",
      "component": "SingleSelectCardGrid",
      "prompt": "What role are you wearing today?",
      "field": "role",
      "required": true,
      "options": [
        { "id": "investment", "label": "Investment / Portfolio" },
        { "id": "operations", "label": "Operations / Servicing" },
        { "id": "compliance", "label": "Compliance / Risk" },
        { "id": "data", "label": "Data / Integration" },
        { "id": "procurement", "label": "Procurement / Committee" },
        { "id": "exec", "label": "Executive sponsor" },
        { "id": "other", "label": "Other" }
      ],
      "telemetry": [{ "event": "demo.role_selected", "emit_on": "submit" }],
      "next": "S2_context_select"
    },
    {
      "id": "S2_context_select",
      "module": "ENTRY",
      "component": "MultiSelectChips",
      "prompt": "Pick your current state (choose up to 3).",
      "field": "context",
      "required": true,
      "max_select": 3,
      "options": [
        { "id": "multi_carrier", "label": "Multi-carrier variability" },
        { "id": "multi_state", "label": "Multi-state variability" },
        { "id": "document_rules", "label": "Rules live in PDFs/emails" },
        { "id": "spreadsheet_controls", "label": "Spreadsheets as controls" },
        { "id": "unpredictable_ttl", "label": "Unpredictable time-to-liquidity" },
        { "id": "high_escalations", "label": "High escalation rate" },
        { "id": "vendor_dependency", "label": "Vendor dependency concern" }
      ],
      "telemetry": [{ "event": "demo.context_selected", "emit_on": "submit" }],
      "next": "S3_trigger_select"
    },
    {
      "id": "S3_trigger_select",
      "module": "ENTRY",
      "component": "SingleSelectList",
      "prompt": "What triggered this evaluation?",
      "field": "trigger",
      "required": true,
      "options": [
        { "id": "trapped_capital", "label": "Capital trapped longer than modeled" },
        { "id": "audit_friction", "label": "Audit/governance friction" },
        { "id": "cost_to_serve", "label": "Scaling cost-to-serve" },
        { "id": "exception_spike", "label": "Exception spike (carrier event)" },
        { "id": "committee_mandate", "label": "Committee mandate (prove controls)" },
        { "id": "growth", "label": "Growth / expansion" },
        { "id": "other", "label": "Other" }
      ],
      "telemetry": [{ "event": "demo.trigger_selected", "emit_on": "submit" }],
      "next": "ROUTER"
    }
  ],
  "modules": {
    "A_mechanics_audit": {
      "id": "A_mechanics_audit",
      "title": "Mechanics + Audit Trail",
      "duration_min": 3,
      "screens": ["A1_workflow_map", "A2_case_overview", "A3_decision_path", "A4_provenance_ledger", "A5_audit_export"],
      "telemetry": [
        { "event": "module.viewed", "module_id": "A_mechanics_audit", "emit_on": "enter" }
      ]
    },
    "B_variance_dashboard": {
      "id": "B_variance_dashboard",
      "title": "Variance Dashboard",
      "duration_min": 4,
      "screens": ["B1_p50_p90", "B2_drivers", "B3_tail_controls"],
      "telemetry": [{ "event": "module.viewed", "module_id": "B_variance_dashboard", "emit_on": "enter" }]
    },
    "C_rules_exceptions": {
      "id": "C_rules_exceptions",
      "title": "Rules + Exceptions",
      "duration_min": 5,
      "screens": ["C1_rules_objects", "C2_exceptions_model", "C3_versioning"],
      "telemetry": [{ "event": "module.viewed", "module_id": "C_rules_exceptions", "emit_on": "enter" }]
    },
    "D_artefact_pipeline": {
      "id": "D_artefact_pipeline",
      "title": "Artefact Pipeline",
      "duration_min": 3,
      "screens": ["D1_ingestion", "D2_review_queue"],
      "telemetry": [{ "event": "module.viewed", "module_id": "D_artefact_pipeline", "emit_on": "enter" }]
    },
    "E_spreadsheet_migration": {
      "id": "E_spreadsheet_migration",
      "title": "Spreadsheet Migration",
      "duration_min": 4,
      "screens": ["E1_import_map", "E2_dualrun_exit"],
      "telemetry": [{ "event": "module.viewed", "module_id": "E_spreadsheet_migration", "emit_on": "enter" }]
    },
    "F_portability_pack": {
      "id": "F_portability_pack",
      "title": "Portability Pack",
      "duration_min": 2,
      "screens": ["F1_portability"],
      "telemetry": [{ "event": "module.viewed", "module_id": "F_portability_pack", "emit_on": "enter" }]
    },
    "G_pilot_blueprint": {
      "id": "G_pilot_blueprint",
      "title": "60-Day Pilot Blueprint",
      "duration_min": 2,
      "screens": ["G1_choose_workflow", "G2_choose_metrics", "G3_timeline"],
      "telemetry": [{ "event": "module.viewed", "module_id": "G_pilot_blueprint", "emit_on": "enter" }]
    }
  },
  "router": {
    "id": "ROUTER",
    "always_include": ["A_mechanics_audit", "G_pilot_blueprint"],
    "trigger_routes": [
      {
        "if": { "trigger_in": ["audit_friction", "committee_mandate"] },
        "then_order": ["A_mechanics_audit", "F_portability_pack", "B_variance_dashboard", "G_pilot_blueprint"],
        "depth_promote": ["A_mechanics_audit", "F_portability_pack"]
      },
      {
        "if": { "trigger_in": ["trapped_capital"] },
        "then_order": ["A_mechanics_audit", "B_variance_dashboard", "G_pilot_blueprint"],
        "depth_promote": ["B_variance_dashboard"]
      },
      {
        "if": { "trigger_in": ["exception_spike"] },
        "then_order": ["A_mechanics_audit", "C_rules_exceptions", "G_pilot_blueprint"],
        "depth_promote": ["C_rules_exceptions"]
      },
      {
        "if": { "trigger_in": ["cost_to_serve"] },
        "then_order": ["A_mechanics_audit", "C_rules_exceptions", "G_pilot_blueprint"],
        "depth_promote": ["C_rules_exceptions"]
      },
      {
        "if": { "trigger_in": ["growth", "other"] },
        "then_order": ["A_mechanics_audit", "B_variance_dashboard", "C_rules_exceptions", "G_pilot_blueprint"],
        "depth_promote": ["B_variance_dashboard"]
      }
    ],
    "context_inserts": [
      { "if": { "context_any": ["document_rules"] }, "then_add": ["D_artefact_pipeline"] },
      { "if": { "context_any": ["spreadsheet_controls"] }, "then_add": ["E_spreadsheet_migration"] },
      { "if": { "context_any": ["vendor_dependency"] }, "then_add_front": ["F_portability_pack"] },
      { "if": { "context_any": ["multi_carrier", "multi_state"] }, "then_ensure": ["C_rules_exceptions"] },
      { "if": { "context_any": ["unpredictable_ttl"] }, "then_ensure": ["B_variance_dashboard"] }
    ],
    "role_promotions": [
      { "if": { "role_in": ["investment"] }, "depth_promote": ["B_variance_dashboard"] },
      { "if": { "role_in": ["operations"] }, "depth_promote": ["C_rules_exceptions", "E_spreadsheet_migration"] },
      { "if": { "role_in": ["compliance"] }, "depth_promote": ["A_mechanics_audit", "F_portability_pack"] },
      { "if": { "role_in": ["data"] }, "depth_promote": ["D_artefact_pipeline", "C_rules_exceptions", "F_portability_pack"] },
      { "if": { "role_in": ["procurement"] }, "depth_promote": ["F_portability_pack", "A_mechanics_audit"] }
    ],
    "language_token_rules": [
      {
        "match_any": ["mechanics", "audit", "explain", "governance"],
        "then_add_front": ["A_mechanics_audit"],
        "telemetry": { "event": "token.triggered", "token_group": "mechanics_audit" }
      },
      {
        "match_any": ["lock-in", "dependency", "exit"],
        "then_add_front": ["F_portability_pack"],
        "telemetry": { "event": "token.triggered", "token_group": "dependency_exit" }
      }
    ]
  },
  "screen_definitions": {
    "A1_workflow_map": {
      "component": "WorkflowDiagram",
      "props": { "nodes": ["Intake", "Rule Eval", "Execute", "Export/Audit"] },
      "telemetry": [{ "event": "workflow.viewed", "emit_on": "enter" }]
    },
    "A2_case_overview": {
      "component": "CaseSummaryPanel",
      "props": {
        "fields": ["case_id", "carrier", "state", "product_type", "rules_fired_count", "exceptions_count", "status"]
      },
      "telemetry": [{ "event": "case.opened", "emit_on": "enter" }]
    },
    "A3_decision_path": {
      "component": "DecisionPathTree",
      "props": { "show_provenance_toggle": true, "show_version_diff_toggle": true },
      "telemetry": [{ "event": "decision_path.viewed", "emit_on": "enter" }]
    },
    "A4_provenance_ledger": {
      "component": "Table",
      "props": { "columns": ["rule_id", "source_type", "source_ref", "effective_date", "confidence"] },
      "telemetry": [{ "event": "provenance.ledger_viewed", "emit_on": "enter" }]
    },
    "A5_audit_export": {
      "component": "ExportPanel",
      "props": {
        "export_types": [
          "event_log_json",
          "audit_summary_pdf_html",
          "rules_snapshot_json",
          "evidence_index_csv",
          "override_register_csv"
        ]
      },
      "telemetry": [{ "event": "export.panel_viewed", "emit_on": "enter" }]
    },
    "B1_p50_p90": {
      "component": "LineOrRangeChart",
      "props": { "metrics": ["P50_time_to_liquidity", "P90_time_to_liquidity"], "filters": ["workflow", "carrier", "state"] },
      "telemetry": [{ "event": "variance.chart_viewed", "emit_on": "enter" }]
    },
    "B2_drivers": {
      "component": "RankedDriverList",
      "props": {
        "drivers": [
          "missing_fields",
          "carrier_exception_class",
          "state_constraint",
          "product_terms",
          "manual_approval_step",
          "data_model_mismatch",
          "counterparty_wait"
        ]
      },
      "telemetry": [{ "event": "variance.drivers_viewed", "emit_on": "enter" }]
    },
    "B3_tail_controls": {
      "component": "ThresholdControls",
      "props": {
        "toggles": [
          "escalate_if_over_p90",
          "escalate_on_missing_critical",
          "approval_required_for_override",
          "lock_rule_versions_per_period",
          "auto_generate_governance_packet",
          "sla_timer_counterparty_wait",
          "attach_exception_playbook"
        ]
      },
      "telemetry": [{ "event": "tail_risk.controls_viewed", "emit_on": "enter" }]
    },
    "C1_rules_objects": {
      "component": "RuleObjectTable",
      "props": { "fields": ["carrier", "product_type", "jurisdiction", "condition", "action", "version"] },
      "telemetry": [{ "event": "rules.table_viewed", "emit_on": "enter" }]
    },
    "C2_exceptions_model": {
      "component": "ExceptionClassGrid",
      "props": {
        "classes": [
          "missing_evidence",
          "conflicting_sources",
          "carrier_delay",
          "jurisdiction_ambiguity",
          "manual_approval_required",
          "data_mismatch",
          "out_of_policy"
        ]
      },
      "telemetry": [{ "event": "exceptions.model_viewed", "emit_on": "enter" }]
    },
    "C3_versioning": {
      "component": "VersionDiffViewer",
      "props": { "panels": ["what_changed", "who_approved", "effective_date"] },
      "telemetry": [{ "event": "versioning.viewed", "emit_on": "enter" }]
    },
    "D1_ingestion": {
      "component": "UploadAndPipeline",
      "props": { "artifact_types": ["pdf", "email_thread", "scanned_form"], "steps": ["upload", "extract", "review", "publish", "monitor"] },
      "telemetry": [{ "event": "artifact.pipeline_viewed", "emit_on": "enter" }]
    },
    "D2_review_queue": {
      "component": "ReviewQueueTable",
      "props": { "fields": ["artifact_id", "extracted_fields_count", "confidence", "reviewer", "status", "linked_rules", "notes"] },
      "telemetry": [{ "event": "review.queue_viewed", "emit_on": "enter" }]
    },
    "E1_import_map": {
      "component": "SpreadsheetMapper",
      "props": { "columns": ["policy_id", "carrier", "state", "product", "expected_ttl", "current_status", "notes"] },
      "telemetry": [{ "event": "spreadsheet.mapper_viewed", "emit_on": "enter" }]
    },
    "E2_dualrun_exit": {
      "component": "Checklist",
      "props": {
        "items": [
          "field_parity",
          "rule_parity",
          "audit_export_approved",
          "exceptions_stabilized",
          "override_governance_adopted",
          "reporting_reconciled",
          "offboarding_export_tested"
        ]
      },
      "telemetry": [{ "event": "dualrun.checklist_viewed", "emit_on": "enter" }]
    },
    "F1_portability": {
      "component": "PortabilityPackPanel",
      "props": { "exports": ["data_export_spec", "rules_provenance_export", "audit_event_export", "offboarding_playbook"] },
      "telemetry": [{ "event": "portability.viewed", "emit_on": "enter" }]
    },
    "G1_choose_workflow": {
      "component": "SingleSelectCardGrid",
      "props": {
        "options": [
          "policy_loan",
          "premium_finance_unwind",
          "collateral_update",
          "carrier_doc_reconciliation",
          "exception_triage",
          "variance_reporting",
          "other"
        ]
      },
      "telemetry": [{ "event": "pilot.workflow_selected", "emit_on": "submit" }]
    },
    "G2_choose_metrics": {
      "component": "MultiSelectChips",
      "props": {
        "max_select": 5,
        "options": [
          "reduce_p90_ttl",
          "reduce_variance_spread",
          "reduce_escalation_rate",
          "reduce_manual_steps",
          "increase_governance_acceptance",
          "increase_audit_export_usage",
          "reduce_exception_resolution_time"
        ]
      },
      "telemetry": [{ "event": "pilot.metrics_selected", "emit_on": "submit" }]
    },
    "G3_timeline": {
      "component": "TimelineWithDeliverables",
      "props": {
        "phases": ["day_0_10_baseline", "day_11_30_rule_audit", "day_31_60_variance_playbooks"],
        "deliverables": [
          "baseline_p50_p90",
          "audit_export_approved",
          "rules_exceptions_deployed",
          "artifact_pipeline_if_needed",
          "spreadsheet_migration_if_needed",
          "tail_risk_thresholds_configured",
          "portability_pack_delivered"
        ]
      },
      "telemetry": [{ "event": "pilot.plan_viewed", "emit_on": "enter" }]
    }
  },
  "telemetry": {
    "event_schema_version": "liquifex_telemetry_v1",
    "common_fields": [
      "timestamp",
      "flow_id",
      "account",
      "session_id",
      "user_role",
      "screen_id",
      "module_id",
      "object_refs",
      "metadata"
    ],
    "events": [
      "demo.role_selected",
      "demo.context_selected",
      "demo.trigger_selected",
      "module.viewed",
      "workflow.viewed",
      "case.opened",
      "decision_path.viewed",
      "provenance.ledger_viewed",
      "export.panel_viewed",
      "export.generated",
      "variance.chart_viewed",
      "variance.drivers_viewed",
      "tail_risk.controls_viewed",
      "rules.table_viewed",
      "exceptions.model_viewed",
      "versioning.viewed",
      "artifact.pipeline_viewed",
      "review.queue_viewed",
      "spreadsheet.mapper_viewed",
      "dualrun.checklist_viewed",
      "portability.viewed",
      "pilot.workflow_selected",
      "pilot.metrics_selected",
      "pilot.plan_viewed",
      "token.triggered"
    ],
    "confidence_update_triggers": [
      {
        "event": "export.generated",
        "effect": { "ethno_objects": ["eo_lh_0004", "eo_lh_0012"], "delta_confidence": 0.03 }
      },
      {
        "event": "portability.viewed",
        "effect": { "ethno_objects": ["eo_lh_0011"], "delta_confidence": 0.02 }
      },
      {
        "event": "variance.drivers_viewed",
        "effect": { "ethno_objects": ["eo_lh_0007", "eo_lh_0012"], "delta_confidence": 0.02 }
      },
      {
        "event": "token.triggered",
        "effect": { "delta_confidence": 0.01, "note": "token indicates salience; validate with follow-up evidence" }
      }
    ]
  }
}
```

3) What to do next (operational)
--------------------------------

*   Implement the config loader + router in the demo front-end.
*   Add a simple token-capture box wired to `language_tokens` matching.
*   Log telemetry events to a stream (even a JSONL file initially) to start confidence updating.

## Prompt:
Implement the config loader + router in the demo front-end.

Add a simple token-capture box wired to language_tokens matching.

Log telemetry events to a stream (even a JSONL file initially) to start confidence updating.

## Response:
**Lifehouse Liqui Fex Demo Front-end (config Loader + Router + Telemetry)**

```typescript
import React, { useEffect, useMemo, useRef, useState } from "react";

/**
 * Lifehouse LiquiFex Demo Front-End
 * - Loads a JSON config
 * - Computes module order via router rules
 * - Renders screens (entry + module screens)
 * - Token capture box that matches language_tokens and re-routes in-session
 * - Telemetry logger buffers JSONL and allows download
 *
 * Notes:
 * - This is a demo scaffold. Replace placeholder UI components with your design system.
 * - Telemetry is stored in-memory and downloadable as a .jsonl file.
 */

// ----------------------------
// 1) CONFIG (embed or fetch)
// ----------------------------

const DEMO_CONFIG = {
  schema_version: "liquifex_demo_flow_config_v1",
  flow_id: "liquifex_lifehouse_demo_v1",
  account: { name: "Lifehouse Capital" },
  constraints: {
    max_options_per_screen: 7,
    max_required_fields_per_step: 7,
    max_multi_select: { context_select: 3, pilot_metrics: 5 },
    fallback_when_uncertain: "ask_one_followup_then_default_to_module_A",
  },
  state_model: {
    inputs: { role: null, context: [], trigger: null, language_tokens: [] },
    runtime: { active_modules: [], module_order: [], depth_promotions: [], confidence_overrides: {} },
  },
  modules: {
    A_mechanics_audit: {
      id: "A_mechanics_audit",
      title: "Mechanics + Audit Trail",
      screens: ["A1_workflow_map", "A2_case_overview", "A3_decision_path", "A4_provenance_ledger", "A5_audit_export"],
    },
    B_variance_dashboard: {
      id: "B_variance_dashboard",
      title: "Variance Dashboard",
      screens: ["B1_p50_p90", "B2_drivers", "B3_tail_controls"],
    },
    C_rules_exceptions: {
      id: "C_rules_exceptions",
      title: "Rules + Exceptions",
      screens: ["C1_rules_objects", "C2_exceptions_model", "C3_versioning"],
    },
    D_artefact_pipeline: {
      id: "D_artefact_pipeline",
      title: "Artefact Pipeline",
      screens: ["D1_ingestion", "D2_review_queue"],
    },
    E_spreadsheet_migration: {
      id: "E_spreadsheet_migration",
      title: "Spreadsheet Migration",
      screens: ["E1_import_map", "E2_dualrun_exit"],
    },
    F_portability_pack: {
      id: "F_portability_pack",
      title: "Portability Pack",
      screens: ["F1_portability"],
    },
    G_pilot_blueprint: {
      id: "G_pilot_blueprint",
      title: "60-Day Pilot Blueprint",
      screens: ["G1_choose_workflow", "G2_choose_metrics", "G3_timeline"],
    },
  },
  screens: [
    {
      id: "S1_role_select",
      module: "ENTRY",
      component: "SingleSelect",
      prompt: "What role are you wearing today?",
      field: "role",
      required: true,
      options: [
        { id: "investment", label: "Investment / Portfolio" },
        { id: "operations", label: "Operations / Servicing" },
        { id: "compliance", label: "Compliance / Risk" },
        { id: "data", label: "Data / Integration" },
        { id: "procurement", label: "Procurement / Committee" },
        { id: "exec", label: "Executive sponsor" },
        { id: "other", label: "Other" },
      ],
      telemetry: [{ event: "demo.role_selected", emit_on: "submit" }],
      next: "S2_context_select",
    },
    {
      id: "S2_context_select",
      module: "ENTRY",
      component: "MultiSelect",
      prompt: "Pick your current state (choose up to 3).",
      field: "context",
      required: true,
      max_select: 3,
      options: [
        { id: "multi_carrier", label: "Multi-carrier variability" },
        { id: "multi_state", label: "Multi-state variability" },
        { id: "document_rules", label: "Rules live in PDFs/emails" },
        { id: "spreadsheet_controls", label: "Spreadsheets as controls" },
        { id: "unpredictable_ttl", label: "Unpredictable time-to-liquidity" },
        { id: "high_escalations", label: "High escalation rate" },
        { id: "vendor_dependency", label: "Vendor dependency concern" },
      ],
      telemetry: [{ event: "demo.context_selected", emit_on: "submit" }],
      next: "S3_trigger_select",
    },
    {
      id: "S3_trigger_select",
      module: "ENTRY",
      component: "SingleSelect",
      prompt: "What triggered this evaluation?",
      field: "trigger",
      required: true,
      options: [
        { id: "trapped_capital", label: "Capital trapped longer than modeled" },
        { id: "audit_friction", label: "Audit/governance friction" },
        { id: "cost_to_serve", label: "Scaling cost-to-serve" },
        { id: "exception_spike", label: "Exception spike (carrier event)" },
        { id: "committee_mandate", label: "Committee mandate (prove controls)" },
        { id: "growth", label: "Growth / expansion" },
        { id: "other", label: "Other" },
      ],
      telemetry: [{ event: "demo.trigger_selected", emit_on: "submit" }],
      next: "ROUTER",
    },
  ],
  router: {
    always_include: ["A_mechanics_audit", "G_pilot_blueprint"],
    trigger_routes: [
      {
        if: { trigger_in: ["audit_friction", "committee_mandate"] },
        then_order: ["A_mechanics_audit", "F_portability_pack", "B_variance_dashboard", "G_pilot_blueprint"],
        depth_promote: ["A_mechanics_audit", "F_portability_pack"],
      },
      {
        if: { trigger_in: ["trapped_capital"] },
        then_order: ["A_mechanics_audit", "B_variance_dashboard", "G_pilot_blueprint"],
        depth_promote: ["B_variance_dashboard"],
      },
      {
        if: { trigger_in: ["exception_spike"] },
        then_order: ["A_mechanics_audit", "C_rules_exceptions", "G_pilot_blueprint"],
        depth_promote: ["C_rules_exceptions"],
      },
      {
        if: { trigger_in: ["cost_to_serve"] },
        then_order: ["A_mechanics_audit", "C_rules_exceptions", "G_pilot_blueprint"],
        depth_promote: ["C_rules_exceptions"],
      },
      {
        if: { trigger_in: ["growth", "other"] },
        then_order: ["A_mechanics_audit", "B_variance_dashboard", "C_rules_exceptions", "G_pilot_blueprint"],
        depth_promote: ["B_variance_dashboard"],
      },
    ],
    context_inserts: [
      { if: { context_any: ["document_rules"] }, then_add: ["D_artefact_pipeline"] },
      { if: { context_any: ["spreadsheet_controls"] }, then_add: ["E_spreadsheet_migration"] },
      { if: { context_any: ["vendor_dependency"] }, then_add_front: ["F_portability_pack"] },
      { if: { context_any: ["multi_carrier", "multi_state"] }, then_ensure: ["C_rules_exceptions"] },
      { if: { context_any: ["unpredictable_ttl"] }, then_ensure: ["B_variance_dashboard"] },
    ],
    role_promotions: [
      { if: { role_in: ["investment"] }, depth_promote: ["B_variance_dashboard"] },
      { if: { role_in: ["operations"] }, depth_promote: ["C_rules_exceptions", "E_spreadsheet_migration"] },
      { if: { role_in: ["compliance"] }, depth_promote: ["A_mechanics_audit", "F_portability_pack"] },
      { if: { role_in: ["data"] }, depth_promote: ["D_artefact_pipeline", "C_rules_exceptions", "F_portability_pack"] },
      { if: { role_in: ["procurement"] }, depth_promote: ["F_portability_pack", "A_mechanics_audit"] },
    ],
    language_token_rules: [
      {
        match_any: ["mechanics", "audit", "explain", "governance"],
        then_add_front: ["A_mechanics_audit"],
        telemetry: { event: "token.triggered", token_group: "mechanics_audit" },
      },
      {
        match_any: ["lock-in", "dependency", "exit"],
        then_add_front: ["F_portability_pack"],
        telemetry: { event: "token.triggered", token_group: "dependency_exit" },
      },
    ],
  },
};

// ----------------------------
// 2) UTILITIES
// ----------------------------

function nowIso() {
  return new Date().toISOString();
}

function uniq(arr) {
  return Array.from(new Set(arr));
}

function startsWithAny(str, needles) {
  const s = str.toLowerCase();
  return needles.some((n) => s.includes(n.toLowerCase()));
}

function reorderWithFront(order, frontModules) {
  const front = frontModules.filter(Boolean);
  const remaining = order.filter((m) => !front.includes(m));
  return uniq([...front, ...remaining]);
}

function ensureModules(order, needed) {
  const o = [...order];
  for (const m of needed) if (!o.includes(m)) o.splice(o.length - 1, 0, m); // insert before last as default
  return o;
}

// ----------------------------
// 3) ROUTER (pure)
// ----------------------------

function computeModulePlan(config, inputs) {
  const { router } = config;

  // 1) seed from trigger route
  let order = [];
  let depthPromote = [];

  const trigger = inputs.trigger;
  const ctx = inputs.context || [];
  const role = inputs.role;

  const route = router.trigger_routes.find((r) => r.if?.trigger_in?.includes(trigger));
  if (route?.then_order?.length) {
    order = [...route.then_order];
    depthPromote = [...(route.depth_promote || [])];
  } else {
    order = [...router.always_include];
  }

  // 2) always include
  order = uniq([...router.always_include, ...order]);

  // 3) context inserts
  for (const rule of router.context_inserts || []) {
    const any = rule.if?.context_any;
    if (any && any.some((x) => ctx.includes(x))) {
      if (rule.then_add_front) order = reorderWithFront(order, rule.then_add_front);
      if (rule.then_add) order = uniq([...order.slice(0, -1), ...rule.then_add, order[order.length - 1]]);
      if (rule.then_ensure) order = ensureModules(order, rule.then_ensure);
    }
  }

  // 4) role promotions (only affects depthPromote list; order stays)
  for (const r of router.role_promotions || []) {
    if (r.if?.role_in?.includes(role)) depthPromote = uniq([...depthPromote, ...(r.depth_promote || [])]);
  }

  // 5) sanity: ensure last module is Pilot
  if (!order.includes("G_pilot_blueprint")) order.push("G_pilot_blueprint");
  // move pilot to end
  order = [...order.filter((m) => m !== "G_pilot_blueprint"), "G_pilot_blueprint"];

  return { module_order: order, depth_promote: depthPromote };
}

function applyLanguageTokenRules(config, inputs, currentPlan, tokenText) {
  const rules = config.router.language_token_rules || [];
  const normalized = tokenText.trim().toLowerCase();
  if (!normalized) return { updatedPlan: currentPlan, matched: [] };

  const matched = [];
  let order = [...currentPlan.module_order];

  for (const r of rules) {
    if (r.match_any && startsWithAny(normalized, r.match_any)) {
      matched.push(r);
      if (r.then_add_front?.length) {
        order = reorderWithFront(order, r.then_add_front);
      }
    }
  }

  // ensure pilot remains last
  order = [...order.filter((m) => m !== "G_pilot_blueprint"), "G_pilot_blueprint"];

  return { updatedPlan: { ...currentPlan, module_order: order }, matched };
}

// ----------------------------
// 4) TELEMETRY (JSONL buffer)
// ----------------------------

function buildTelemetryEvent({ config, sessionId, inputs, screenId, moduleId, event, metadata }) {
  return {
    timestamp: nowIso(),
    flow_id: config.flow_id,
    account: config.account?.name,
    session_id: sessionId,
    user_role: inputs.role,
    screen_id: screenId,
    module_id: moduleId,
    event,
    metadata: metadata || {},
  };
}

function downloadTextFile(filename, text) {
  const blob = new Blob([text], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

// ----------------------------
// 5) UI COMPONENTS (minimal)
// ----------------------------

function Shell({ children, left, right }) {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <div className="max-w-7xl mx-auto p-4">
        <div className="grid grid-cols-12 gap-4">
          <aside className="col-span-12 lg:col-span-3">{left}</aside>
          <main className="col-span-12 lg:col-span-6">{children}</main>
          <aside className="col-span-12 lg:col-span-3">{right}</aside>
        </div>
      </div>
    </div>
  );
}

function Card({ title, children, footer }) {
  return (
    <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
      {title ? <div className="px-4 py-3 border-b border-slate-200 font-semibold">{title}</div> : null}
      <div className="p-4">{children}</div>
      {footer ? <div className="px-4 py-3 border-t border-slate-200">{footer}</div> : null}
    </div>
  );
}

function Button({ children, onClick, variant = "primary", disabled }) {
  const base = "px-3 py-2 rounded-xl text-sm font-medium transition border";
  const styles =
    variant === "primary"
      ? "bg-slate-900 text-white border-slate-900 hover:bg-slate-800"
      : "bg-white text-slate-900 border-slate-300 hover:bg-slate-50";
  return (
    <button className={`${base} ${styles} ${disabled ? "opacity-50 cursor-not-allowed" : ""}`} onClick={onClick} disabled={disabled}>
      {children}
    </button>
  );
}

function SingleSelect({ prompt, options, value, onChange }) {
  return (
    <div className="space-y-3">
      <div className="text-base font-semibold">{prompt}</div>
      <div className="grid grid-cols-1 gap-2">
        {options.map((o) => (
          <label key={o.id} className={`flex items-center gap-3 p-3 rounded-xl border cursor-pointer ${value === o.id ? "border-slate-900" : "border-slate-200"}`}>
            <input type="radio" checked={value === o.id} onChange={() => onChange(o.id)} />
            <span>{o.label}</span>
          </label>
        ))}
      </div>
    </div>
  );
}

function MultiSelect({ prompt, options, value, maxSelect, onChange }) {
  const selected = new Set(value);
  const toggle = (id) => {
    const next = new Set(selected);
    if (next.has(id)) next.delete(id);
    else {
      if (next.size >= maxSelect) return;
      next.add(id);
    }
    onChange(Array.from(next));
  };
  return (
    <div className="space-y-3">
      <div className="flex items-end justify-between gap-4">
        <div className="text-base font-semibold">{prompt}</div>
        <div className="text-xs text-slate-500">{value.length}/{maxSelect}</div>
      </div>
      <div className="grid grid-cols-1 gap-2">
        {options.map((o) => (
          <button
            type="button"
            key={o.id}
            onClick={() => toggle(o.id)}
            className={`text-left p-3 rounded-xl border transition ${selected.has(o.id) ? "border-slate-900 bg-slate-50" : "border-slate-200 bg-white hover:bg-slate-50"}`}
          >
            <div className="font-medium">{o.label}</div>
            <div className="text-xs text-slate-500">{o.id}</div>
          </button>
        ))}
      </div>
      {value.length >= maxSelect ? <div className="text-xs text-slate-500">Selection limit reached.</div> : null}
    </div>
  );
}

function PlaceholderScreen({ title, bullets }) {
  return (
    <Card title={title}>
      <ul className="list-disc pl-5 space-y-1 text-sm text-slate-700">
        {bullets.map((b, i) => (
          <li key={i}>{b}</li>
        ))}
      </ul>
    </Card>
  );
}

// ----------------------------
// 6) APP
// ----------------------------

export default function LifehouseLiquifexDemo() {
  const config = DEMO_CONFIG;

  const sessionId = useMemo(() => `sess_${Math.random().toString(16).slice(2)}_${Date.now()}`, []);

  const [inputs, setInputs] = useState({ role: null, context: [], trigger: null, language_tokens: [] });
  const [plan, setPlan] = useState({ module_order: [], depth_promote: [] });
  const [screenQueue, setScreenQueue] = useState([]); // list of {type:'entry'|'module', id, moduleId?}
  const [idx, setIdx] = useState(0);

  // telemetry
  const [jsonl, setJsonl] = useState([]); // each item is an object
  const emit = (event, { screenId, moduleId, metadata } = {}) => {
    const ev = buildTelemetryEvent({ config, sessionId, inputs, screenId, moduleId, event, metadata });
    setJsonl((prev) => [...prev, ev]);
    // also emit to console for dev
    // eslint-disable-next-line no-console
    console.log("telemetry", ev);
  };

  // compute plan once we have entry inputs
  useEffect(() => {
    if (!inputs.role || !inputs.trigger || !(inputs.context?.length)) return;
    const computed = computeModulePlan(config, inputs);
    setPlan(computed);

    // build a screen queue: entry screens then module screens
    const entryIds = config.screens.map((s) => s.id);
    const q = [];
    for (const id of entryIds) q.push({ type: "entry", id });

    for (const mid of computed.module_order) {
      const mod = config.modules[mid];
      if (!mod) continue;
      for (const sid of mod.screens) q.push({ type: "module", id: sid, moduleId: mid });
    }
    setScreenQueue(q);

    // jump to first module screen after entry completion
    setIdx(entryIds.length);
  }, [inputs.role, inputs.trigger, inputs.context?.length]);

  // emit enter events
  const current = screenQueue[idx];
  const prevRef = useRef(null);
  useEffect(() => {
    if (!current) return;
    const key = `${current.type}:${current.id}:${current.moduleId || ""}`;
    if (prevRef.current === key) return;
    prevRef.current = key;

    emit("screen.enter", { screenId: current.id, moduleId: current.moduleId, metadata: { type: current.type } });

    if (current.type === "module") {
      emit("module.viewed", { screenId: current.id, moduleId: current.moduleId, metadata: { module_id: current.moduleId } });
    }
  }, [idx, current?.id]);

  // Token capture
  const [tokenText, setTokenText] = useState("");
  const onTokenSubmit = () => {
    const t = tokenText.trim();
    if (!t) return;

    // persist tokens
    setInputs((prev) => ({ ...prev, language_tokens: [...(prev.language_tokens || []), t] }));

    // apply token rules to module plan and rebuild remaining queue
    const { updatedPlan, matched } = applyLanguageTokenRules(config, inputs, plan, t);
    if (matched.length) {
      for (const m of matched) {
        emit(m.telemetry?.event || "token.triggered", {
          screenId: current?.id,
          moduleId: current?.moduleId,
          metadata: { token: t, token_group: m.telemetry?.token_group || "unknown" },
        });
      }
    } else {
      emit("token.captured", { screenId: current?.id, moduleId: current?.moduleId, metadata: { token: t } });
    }

    setPlan(updatedPlan);

    // rebuild future queue from current position forward
    const entryLen = config.screens.length;
    const before = screenQueue.slice(0, entryLen); // keep entry

    const rebuilt = [...before];
    for (const mid of updatedPlan.module_order) {
      const mod = config.modules[mid];
      if (!mod) continue;
      for (const sid of mod.screens) rebuilt.push({ type: "module", id: sid, moduleId: mid });
    }

    // try to keep user at same screen if still exists; otherwise keep index
    const currentKey = current ? `${current.type}:${current.id}:${current.moduleId || ""}` : null;
    let newIdx = idx;
    if (currentKey) {
      const found = rebuilt.findIndex((x) => `${x.type}:${x.id}:${x.moduleId || ""}` === currentKey);
      if (found >= 0) newIdx = found;
    }

    setScreenQueue(rebuilt);
    setIdx(newIdx);
    setTokenText("");
  };

  // navigation
  const canBack = idx > config.screens.length; // don't go back into entry via nav buttons
  const canNext = idx < screenQueue.length - 1;
  const goBack = () => {
    if (!canBack) return;
    setIdx((i) => Math.max(config.screens.length, i - 1));
  };
  const goNext = () => {
    if (!canNext) return;
    setIdx((i) => Math.min(screenQueue.length - 1, i + 1));
  };

  // download JSONL
  const downloadJsonl = () => {
    const lines = jsonl.map((o) => JSON.stringify(o));
    const text = lines.join("\n") + (lines.length ? "\n" : "");
    downloadTextFile(`telemetry_${config.flow_id}_${sessionId}.jsonl`, text);
  };

  // Entry screen renderers (from config.screens)
  const entryById = useMemo(() => {
    const map = new Map();
    for (const s of config.screens) map.set(s.id, s);
    return map;
  }, []);

  const entryScreen = current?.type === "entry" ? entryById.get(current.id) : null;

  const renderEntry = () => {
    if (!entryScreen) return null;
    const field = entryScreen.field;
    const value = inputs[field];

    const submit = () => {
      // required guard
      const ok = entryScreen.required ? (Array.isArray(value) ? value.length > 0 : !!value) : true;
      if (!ok) {
        emit("validation.failed", { screenId: entryScreen.id, moduleId: "ENTRY", metadata: { field } });
        return;
      }
      // telemetry
      for (const t of entryScreen.telemetry || []) {
        if (t.emit_on === "submit") emit(t.event, { screenId: entryScreen.id, moduleId: "ENTRY", metadata: { value } });
      }
      // move to next entry
      const entryIds = config.screens.map((s) => s.id);
      const pos = entryIds.indexOf(entryScreen.id);
      const nextId = entryScreen.next;
      if (nextId === "ROUTER") {
        // once router screen hit, build plan by setting idx to first module via useEffect
        setIdx(config.screens.length);
        return;
      }
      const nextPos = pos + 1;
      if (nextPos < entryIds.length) setIdx(nextPos);
    };

    return (
      <Card
        title="Setup"
        footer={
          <div className="flex items-center justify-between">
            <div className="text-xs text-slate-500">Step {config.screens.findIndex((s) => s.id === entryScreen.id) + 1} / {config.screens.length}</div>
            <Button onClick={submit}>Continue</Button>
          </div>
        }
      >
        {entryScreen.component === "SingleSelect" ? (
          <SingleSelect
            prompt={entryScreen.prompt}
            options={entryScreen.options}
            value={inputs[field]}
            onChange={(v) => setInputs((prev) => ({ ...prev, [field]: v }))}
          />
        ) : (
          <MultiSelect
            prompt={entryScreen.prompt}
            options={entryScreen.options}
            value={inputs[field]}
            maxSelect={entryScreen.max_select}
            onChange={(v) => setInputs((prev) => ({ ...prev, [field]: v }))}
          />
        )}
      </Card>
    );
  };

  // Module screen renderers (placeholder content; swap with real components)
  const renderModuleScreen = () => {
    if (!current || current.type !== "module") return null;
    const mid = current.moduleId;
    const screenId = current.id;

    const title = `${config.modules[mid]?.title || mid} — ${screenId}`;
    const bullets = [];

    // Minimal per-screen bullet hints
    switch (screenId) {
      case "A1_workflow_map":
        bullets.push("Show 4-node workflow: Intake → Rule Eval → Execute → Export/Audit");
        bullets.push("Ask: audit-ready always vs audit on request");
        break;
      case "A3_decision_path":
        bullets.push("Display rules fired, evidence used, alternatives rejected");
        bullets.push("Expose provenance + version diff toggles");
        break;
      case "A5_audit_export":
        bullets.push("Export: event_log_json, audit_summary, rules_snapshot, evidence_index, override_register");
        bullets.push("Emit export.generated when clicked");
        break;
      case "B1_p50_p90":
        bullets.push("Show P50/P90 time-to-liquidity; filters: workflow/carrier/state");
        break;
      case "F1_portability":
        bullets.push("Show portability pack: data export, rules+provenance, audit events, offboarding playbook");
        break;
      case "G3_timeline":
        bullets.push("Show 60-day pilot timeline with 7 deliverables");
        break;
      default:
        bullets.push("Replace placeholder with real UI component per wireframe spec");
        break;
    }

    const footer = (
      <div className="flex items-center justify-between">
        <div className="text-xs text-slate-500">Module: {mid}{plan.depth_promote?.includes(mid) ? " (depth promoted)" : ""}</div>
        <div className="flex gap-2">
          <Button variant="secondary" onClick={goBack} disabled={!canBack}>Back</Button>
          <Button onClick={goNext} disabled={!canNext}>Next</Button>
        </div>
      </div>
    );

    return (
      <Card title={title} footer={footer}>
        <PlaceholderScreen title="Presenter cues" bullets={bullets} />

        {screenId === "A5_audit_export" ? (
          <div className="mt-4 flex flex-wrap gap-2">
            <Button
              onClick={() => {
                emit("export.generated", { screenId, moduleId: mid, metadata: { export_type: "event_log_json" } });
                emit("export.generated", { screenId, moduleId: mid, metadata: { export_type: "audit_summary_pdf_html" } });
              }}
            >
              Generate audit exports
            </Button>
            <Button
              variant="secondary"
              onClick={() => emit("export.previewed", { screenId, moduleId: mid, metadata: { export_type: "audit_summary_pdf_html" } })}
            >
              Preview audit summary
            </Button>
          </div>
        ) : null}

        {screenId === "B1_p50_p90" ? (
          <div className="mt-4 flex flex-wrap gap-2">
            <Button
              variant="secondary"
              onClick={() => emit("filter.changed", { screenId, moduleId: mid, metadata: { filter: "workflow", value: "policy_loan" } })}
            >
              Filter: workflow=policy_loan
            </Button>
            <Button
              variant="secondary"
              onClick={() => emit("filter.changed", { screenId, moduleId: mid, metadata: { filter: "state", value: "US-NY" } })}
            >
              Filter: state=US-NY
            </Button>
          </div>
        ) : null}
      </Card>
    );
  };

  // Left rail: flow status
  const left = (
    <div className="space-y-4">
      <Card title="Flow">
        <div className="text-xs text-slate-500 mb-2">Account</div>
        <div className="font-semibold">{config.account.name}</div>
        <div className="mt-3 text-xs text-slate-500">Session</div>
        <div className="text-xs font-mono break-all">{sessionId}</div>

        <div className="mt-4 text-xs text-slate-500">Inputs</div>
        <pre className="text-xs bg-slate-50 border border-slate-200 rounded-xl p-2 overflow-auto">{JSON.stringify(inputs, null, 2)}</pre>

        <div className="mt-4 text-xs text-slate-500">Module plan</div>
        <div className="space-y-1">
          {(plan.module_order || []).map((m) => (
            <div key={m} className="text-sm flex items-center justify-between">
              <span className="truncate">{config.modules[m]?.title || m}</span>
              {plan.depth_promote?.includes(m) ? <span className="text-[10px] px-2 py-0.5 rounded-full bg-slate-100 border border-slate-200">depth</span> : null}
            </div>
          ))}
        </div>
      </Card>

      <Card title="Token capture">
        <div className="text-sm text-slate-700">
          Capture any live language from Lifehouse (e.g., “audit”, “mechanics”, “dependency”). Matching rules will re-route modules.
        </div>
        <div className="mt-3 flex gap-2">
          <input
            value={tokenText}
            onChange={(e) => setTokenText(e.target.value)}
            placeholder="Type token or phrase…"
            className="flex-1 px-3 py-2 rounded-xl border border-slate-300 bg-white text-sm"
            onKeyDown={(e) => {
              if (e.key === "Enter") onTokenSubmit();
            }}
          />
          <Button onClick={onTokenSubmit}>Add</Button>
        </div>
        {inputs.language_tokens?.length ? (
          <div className="mt-3">
            <div className="text-xs text-slate-500 mb-1">Captured</div>
            <div className="flex flex-wrap gap-2">
              {inputs.language_tokens.map((t, i) => (
                <span key={`${t}-${i}`} className="text-xs px-2 py-1 rounded-full bg-slate-100 border border-slate-200">
                  {t}
                </span>
              ))}
            </div>
          </div>
        ) : null}
      </Card>
    </div>
  );

  // Right rail: telemetry + download
  const right = (
    <div className="space-y-4">
      <Card
        title="Telemetry"
        footer={
          <div className="flex items-center justify-between">
            <div className="text-xs text-slate-500">{jsonl.length} events</div>
            <div className="flex gap-2">
              <Button variant="secondary" onClick={() => setJsonl([])}>Clear</Button>
              <Button onClick={downloadJsonl} disabled={!jsonl.length}>Download JSONL</Button>
            </div>
          </div>
        }
      >
        <div className="text-xs text-slate-500 mb-2">Latest</div>
        <pre className="text-xs bg-slate-50 border border-slate-200 rounded-xl p-2 h-80 overflow-auto">
          {JSON.stringify(jsonl.slice(-8), null, 2)}
        </pre>
      </Card>

      <Card title="Controls">
        <div className="flex gap-2 flex-wrap">
          <Button
            variant="secondary"
            onClick={() => {
              // reset
              setInputs({ role: null, context: [], trigger: null, language_tokens: [] });
              setPlan({ module_order: [], depth_promote: [] });
              setScreenQueue(config.screens.map((s) => ({ type: "entry", id: s.id })));
              setIdx(0);
              emit("demo.reset", { screenId: "SYSTEM", moduleId: "SYSTEM" });
            }}
          >
            Reset demo
          </Button>
          <Button
            variant="secondary"
            onClick={() => {
              if (!current) return;
              emit("note", { screenId: current.id, moduleId: current.moduleId, metadata: { note: "Manual marker" } });
            }}
          >
            Add marker
          </Button>
        </div>
        <div className="mt-3 text-xs text-slate-500">
          JSONL download is the initial telemetry stream. Replace with a POST to your ingest endpoint when ready.
        </div>
      </Card>
    </div>
  );

  // Bootstrap queue with entry screens on first render
  useEffect(() => {
    if (screenQueue.length) return;
    setScreenQueue(config.screens.map((s) => ({ type: "entry", id: s.id })));
    setIdx(0);
  }, [screenQueue.length]);

  // Render
  const content = current?.type === "entry" ? renderEntry() : renderModuleScreen();

  return <Shell left={left} right={right}>{content}</Shell>;
}

```

Implemented in the canvas file **“Lifehouse LiquiFex Demo Front-End (Config Loader + Router + Telemetry)”**:

What’s included
---------------

*   **Config loader:** Uses an embedded `DEMO_CONFIG` object (swap to `fetch()` easily).
*   **Router:** `computeModulePlan()` computes `module_order` + `depth_promote` from `role/context/trigger`.
*   **Token-capture box:** Left rail input captures phrases and runs `applyLanguageTokenRules()` to re-route modules in-session (e.g., “audit” pulls Module A forward; “dependency/exit” pulls Module F forward).
*   **Telemetry stream (JSONL):**
    *   `emit()` builds structured events and appends to an in-memory buffer.
    *   Right rail shows latest events and provides **Download JSONL** (one JSON object per line).
    *   Emits `screen.enter`, module-view events, entry submission events, token events, and sample export/filter events.

How to wire to a real telemetry stream (replace JSONL download)
---------------------------------------------------------------

In the `emit()` function, replace or augment the in-memory append with a POST:

```
fetch("/telemetry/ingest", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(ev),
});
```

Where to plug in real UI
------------------------

Module screens currently render placeholders with presenter cues; replace the `PlaceholderScreen` sections inside `renderModuleScreen()` with your real components keyed by `screenId`.

If you want confidence updating to run off telemetry (beyond routing), the right place to add it is inside `emit()` (apply per-event deltas to a `confidence` map and persist it alongside JSONL).

## Prompt:
can you do it? 

How should I implement it

## Response:
Yes.

Implementation plan (fastest path to working)
---------------------------------------------

### Architecture

*   **Front-end (this React demo):** emits telemetry events.
*   **Backend telemetry ingest:** accepts events and writes **append-only JSONL**.
*   **Confidence updater (server-side):** updates ethno-object confidence scores based on telemetry triggers and (optionally) human validations.
*   **Storage:**
    *   `telemetry/YYYY-MM-DD/<session_id>.jsonl` (immutable-ish stream)
    *   `state/confidence/<account>.json` (current confidence map snapshot)

This is the highest ROI setup: minimal complexity, audit-friendly, and easy to evolve into Kafka/S3 later.

* * *

Step 1 — Add a telemetry ingest endpoint (Node/Express)
-------------------------------------------------------

Create `server.js`:

```
import express from "express";
import fs from "fs";
import path from "path";
import crypto from "crypto";

const app = express();
app.use(express.json({ limit: "1mb" }));

const DATA_DIR = process.env.DATA_DIR || path.join(process.cwd(), "data");
const TELEMETRY_DIR = path.join(DATA_DIR, "telemetry");
const CONF_DIR = path.join(DATA_DIR, "confidence");

function ensureDir(p) {
  fs.mkdirSync(p, { recursive: true });
}

function safeStr(s) {
  return String(s || "").replace(/[^a-zA-Z0-9._-]/g, "_").slice(0, 120);
}

function isoDay(ts) {
  const d = new Date(ts || Date.now());
  const yyyy = d.getUTCFullYear();
  const mm = String(d.getUTCMonth() + 1).padStart(2, "0");
  const dd = String(d.getUTCDate()).padStart(2, "0");
  return `${yyyy}-${mm}-${dd}`;
}

// Very lightweight bayesian-ish update:
// p' = clamp(p + delta, 0.01, 0.99) then apply decay later via a scheduled job if desired
function clamp01(x) {
  return Math.max(0.01, Math.min(0.99, x));
}

function loadJson(file, fallback) {
  try {
    return JSON.parse(fs.readFileSync(file, "utf8"));
  } catch {
    return fallback;
  }
}

function saveJson(file, obj) {
  ensureDir(path.dirname(file));
  fs.writeFileSync(file, JSON.stringify(obj, null, 2), "utf8");
}

function appendJsonl(file, obj) {
  ensureDir(path.dirname(file));
  fs.appendFileSync(file, JSON.stringify(obj) + "\n", "utf8");
}

function getConfidenceFile(account) {
  return path.join(CONF_DIR, `${safeStr(account || "unknown")}.json`);
}

/**
 * Map events -> ethno-object confidence deltas.
 * Replace ids with your real EO ids.
 */
function confidenceTriggers(event) {
  const e = event?.event;
  if (!e) return [];
  switch (e) {
    case "export.generated":
      return [
        { eo: "eo_lh_0004", delta: 0.03 }, // governance/audit proof
        { eo: "eo_lh_0012", delta: 0.03 }  // variance quant relevance
      ];
    case "portability.viewed":
      return [{ eo: "eo_lh_0011", delta: 0.02 }];
    case "variance.drivers_viewed":
      return [
        { eo: "eo_lh_0007", delta: 0.02 },
        { eo: "eo_lh_0012", delta: 0.02 }
      ];
    case "token.triggered":
      return [{ eo: "eo_lh_token_salience", delta: 0.01 }];
    default:
      return [];
  }
}

app.post("/telemetry/ingest", (req, res) => {
  const event = req.body;

  // basic validation
  if (!event || typeof event !== "object") {
    return res.status(400).json({ ok: false, error: "Invalid payload" });
  }

  const timestamp = event.timestamp || new Date().toISOString();
  const sessionId = safeStr(event.session_id || crypto.randomUUID());
  const account = safeStr(event.account || "unknown");
  const day = isoDay(timestamp);

  // 1) write JSONL
  const jsonlPath = path.join(TELEMETRY_DIR, day, `${account}__${sessionId}.jsonl`);
  appendJsonl(jsonlPath, { ...event, timestamp });

  // 2) update confidence snapshot
  const confFile = getConfidenceFile(account);
  const conf = loadJson(confFile, { account, updated_at: timestamp, priors: {}, scores: {} });

  const deltas = confidenceTriggers(event);
  for (const d of deltas) {
    const key = d.eo;
    const prior = conf.scores[key] ?? 0.65; // default prior
    conf.scores[key] = clamp01(prior + d.delta);
  }
  conf.updated_at = timestamp;
  saveJson(confFile, conf);

  return res.json({ ok: true, jsonlPath, confidenceUpdated: deltas.map(d => d.eo) });
});

app.get("/confidence/:account", (req, res) => {
  const account = safeStr(req.params.account);
  const confFile = getConfidenceFile(account);
  const conf = loadJson(confFile, null);
  if (!conf) return res.status(404).json({ ok: false, error: "Not found" });
  res.json({ ok: true, confidence: conf });
});

const port = process.env.PORT || 8787;
app.listen(port, () => {
  console.log(`Telemetry server listening on http://localhost:${port}`);
});
```

Run:

```
npm i express
node server.js
```

* * *

Step 2 — Wire the front-end `emit()` to POST
--------------------------------------------

In the React file (canvas), locate `emit()` and add:

```
fetch("http://localhost:8787/telemetry/ingest", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(ev),
}).catch(() => {});
```

Keep the JSONL buffer + download in place; it’s your offline audit fallback.

* * *

Step 3 — Implement token capture “language\_tokens” matching (already done)
---------------------------------------------------------------------------

The canvas code already:

*   captures tokens into `inputs.language_tokens`
*   runs `applyLanguageTokenRules()`
*   emits `token.triggered` with a token\_group when matched
*   rebuilds the module plan + screen queue without losing your current position (if possible)

So you only need Step 2 for server-side logging.

* * *

Step 4 — Confidence updates: how to implement “correctly”
---------------------------------------------------------

You have two practical options:

### Option A (recommended now): deterministic deltas (what I wrote)

*   Pros: simple, explainable, audit-ready, no ML infra needed.
*   Cons: not “true Bayesian”; it’s a pragmatic proxy.

### Option B (next step): Beta distribution per EO

Store `(alpha, beta)` per EO:

*   prior mean = `alpha/(alpha+beta)`
*   update: success increments `alpha`, failure increments `beta`
*   map telemetry event strength to fractional increments (e.g., +0.3)

If you want Option B, say so and I’ll provide the exact code replacement.

* * *

Step 5 — File structure (recommended)
-------------------------------------

```
/app
  /src (React)
  server.js
/data
  /telemetry/2026-02-27/Lifehouse_Capital__sess_....jsonl
  /confidence/Lifehouse_Capital.json
```

* * *

What you should implement first
-------------------------------

1.  **Backend ingest + JSONL append** (Step 1)
2.  **Front-end POST in emit()** (Step 2)
3.  Confirm you see JSONL growing + confidence snapshot updating.
4.  Then replace placeholder screens with real components.

If you want, paste your preferred deployment environment (local Node, Vercel, AWS, GCP) and I’ll give the best-fit production version (auth, batching, retries, and S3/GCS storage).

## Prompt:
Backend ingest + JSONL append (Step 1)

## Response:
Backend ingest + JSONL append (Step 1) — implement now
------------------------------------------------------

Below is a complete, minimal **Node + Express** ingest service that:

*   accepts telemetry events at `POST /telemetry/ingest`
*   validates + normalizes
*   **appends** each event as a single line to a **JSONL** file:  
    `data/telemetry/YYYY-MM-DD/<account>__<session_id>.jsonl`

### 1) Create a folder + init

```
mkdir telemetry-server && cd telemetry-server
npm init -y
npm i express
```

### 2) Add `server.js`

```
import express from "express";
import fs from "fs";
import path from "path";
import crypto from "crypto";

const app = express();
app.use(express.json({ limit: "1mb" }));

const DATA_DIR = process.env.DATA_DIR || path.join(process.cwd(), "data");
const TELEMETRY_DIR = path.join(DATA_DIR, "telemetry");

/** ---------- helpers ---------- */

function ensureDir(p) {
  fs.mkdirSync(p, { recursive: true });
}

function safeStr(s) {
  // prevents path traversal / weird filenames
  return String(s || "")
    .trim()
    .replace(/[^a-zA-Z0-9._-]/g, "_")
    .slice(0, 120);
}

function isoDay(ts) {
  const d = new Date(ts || Date.now());
  if (Number.isNaN(d.getTime())) return isoDay(Date.now());
  const yyyy = d.getUTCFullYear();
  const mm = String(d.getUTCMonth() + 1).padStart(2, "0");
  const dd = String(d.getUTCDate()).padStart(2, "0");
  return `${yyyy}-${mm}-${dd}`;
}

function appendJsonl(filePath, obj) {
  ensureDir(path.dirname(filePath));
  fs.appendFileSync(filePath, JSON.stringify(obj) + "\n", "utf8");
}

/** ---------- validation ---------- */

function validateEvent(e) {
  if (!e || typeof e !== "object") return { ok: false, error: "payload_not_object" };
  if (!e.event || typeof e.event !== "string") return { ok: false, error: "missing_event" };
  // optional but recommended fields
  // session_id, account, flow_id, timestamp, etc.
  return { ok: true };
}

/** ---------- routes ---------- */

// Health check
app.get("/health", (_req, res) => res.json({ ok: true }));

// Ingest: append-only JSONL
app.post("/telemetry/ingest", (req, res) => {
  const incoming = req.body;

  const v = validateEvent(incoming);
  if (!v.ok) return res.status(400).json({ ok: false, error: v.error });

  const timestamp = incoming.timestamp || new Date().toISOString();
  const day = isoDay(timestamp);

  const account = safeStr(incoming.account || "unknown");
  const sessionId = safeStr(incoming.session_id || crypto.randomUUID());

  const filePath = path.join(TELEMETRY_DIR, day, `${account}__${sessionId}.jsonl`);

  // normalize event (add required server fields)
  const event = {
    ...incoming,
    timestamp,
    account,
    session_id: sessionId,
    _ingested_at: new Date().toISOString(),
  };

  try {
    appendJsonl(filePath, event);
    return res.json({ ok: true, file: filePath });
  } catch (err) {
    return res.status(500).json({ ok: false, error: "write_failed" });
  }
});

// Optional: read last N lines for debugging
app.get("/telemetry/tail", (req, res) => {
  const day = safeStr(req.query.day || isoDay(Date.now()));
  const account = safeStr(req.query.account || "unknown");
  const sessionId = safeStr(req.query.session_id || "");
  const n = Math.max(1, Math.min(200, Number(req.query.n || 20)));

  if (!sessionId) return res.status(400).json({ ok: false, error: "missing_session_id" });

  const filePath = path.join(TELEMETRY_DIR, day, `${account}__${sessionId}.jsonl`);
  if (!fs.existsSync(filePath)) return res.status(404).json({ ok: false, error: "not_found" });

  const text = fs.readFileSync(filePath, "utf8");
  const lines = text.trim().split("\n").slice(-n).map((l) => {
    try { return JSON.parse(l); } catch { return { parse_error: true, raw: l }; }
  });

  res.json({ ok: true, file: filePath, lines });
});

/** ---------- start ---------- */

const PORT = Number(process.env.PORT || 8787);
app.listen(PORT, () => {
  console.log(`Telemetry ingest listening on http://localhost:${PORT}`);
  console.log(`Writing JSONL under: ${TELEMETRY_DIR}`);
});
```

### 3) Enable ESM (so `import` works)

Edit `package.json` and add:

```
{
  "type": "module"
}
```

### 4) Run it

```
node server.js
```

You should see:

*   `Telemetry ingest listening on http://localhost:8787`
*   `Writing JSONL under: <...>/data/telemetry`

* * *

5) Test with curl (proves JSONL append)
---------------------------------------

```
curl -X POST http://localhost:8787/telemetry/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "event":"demo.role_selected",
    "flow_id":"liquifex_lifehouse_demo_v1",
    "account":"Lifehouse Capital",
    "session_id":"sess_test_001",
    "screen_id":"S1_role_select",
    "module_id":"ENTRY",
    "metadata":{"value":"investment"}
  }'
```

Then check:

```
cat data/telemetry/$(date -u +%F)/Lifehouse_Capital__sess_test_001.jsonl
```

You should see one JSON line per POST. Re-run the curl and the file will grow by one line each time.

* * *

Operational hardening (do next, not now)
----------------------------------------

*   rotate files by size (e.g., 50MB) and keep an index
*   add auth (API key) + IP allowlist
*   write to object storage (S3/GCS) with local buffer
*   batch ingest from front-end (reduce chatter)

If you paste your hosting target (local only vs Vercel vs AWS/GCP), I’ll provide the deployment-ready variant (including CORS and auth).

## Prompt:
Front-end POST in emit() (Step 2)

## Response:
Step 2 — Front-end POST in `emit()` (wire to ingest)
----------------------------------------------------

You already have `emit()` in the React scaffold. Modify it to:

1.  build the event object
2.  append to local JSONL buffer (keep the offline audit trail)
3.  POST to your backend `/telemetry/ingest`
4.  handle failures with a small retry/backlog (optional but recommended)

### A) Minimal change (fastest)

In the canvas React file, find:

```
const emit = (event, { screenId, moduleId, metadata } = {}) => {
  const ev = buildTelemetryEvent({ config, sessionId, inputs, screenId, moduleId, event, metadata });
  setJsonl((prev) => [...prev, ev]);
  console.log("telemetry", ev);
};
```

Replace with:

```
const TELEMETRY_URL = "http://localhost:8787/telemetry/ingest";

const emit = (event, { screenId, moduleId, metadata } = {}) => {
  const ev = buildTelemetryEvent({ config, sessionId, inputs, screenId, moduleId, event, metadata });

  // 1) local buffer (audit fallback)
  setJsonl((prev) => [...prev, ev]);

  // 2) POST to ingest (best-effort)
  fetch(TELEMETRY_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(ev),
  }).catch(() => { /* swallow in demo */ });

  console.log("telemetry", ev);
};
```

That’s enough to start writing JSONL server-side.

* * *

### B) Recommended: backlog + retry (prevents data loss)

This keeps events if the server is down, and flushes them when it comes back.

1.  Add these state variables near the telemetry section:

```
const TELEMETRY_URL = "http://localhost:8787/telemetry/ingest";
const [backlog, setBacklog] = useState([]); // unsent events
const [isFlushing, setIsFlushing] = useState(false);
```

2.  Replace `emit()` with:

```
const emit = (event, { screenId, moduleId, metadata } = {}) => {
  const ev = buildTelemetryEvent({ config, sessionId, inputs, screenId, moduleId, event, metadata });

  // local buffer
  setJsonl((prev) => [...prev, ev]);

  // enqueue for send
  setBacklog((prev) => [...prev, ev]);

  console.log("telemetry", ev);
};
```

3.  Add a flush loop (best placed under `emit()`):

```
async function postEvent(ev) {
  const r = await fetch(TELEMETRY_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(ev),
  });
  if (!r.ok) throw new Error(`ingest_failed_${r.status}`);
}

useEffect(() => {
  if (isFlushing) return;
  if (!backlog.length) return;

  let cancelled = false;

  (async () => {
    setIsFlushing(true);
    try {
      // send in order (append-only stream semantics)
      for (const ev of backlog) {
        if (cancelled) return;
        await postEvent(ev);
      }
      // if all sent, clear backlog
      setBacklog([]);
    } catch {
      // keep backlog; try again later
    } finally {
      if (!cancelled) setIsFlushing(false);
    }
  })();

  return () => {
    cancelled = true;
  };
}, [backlog, isFlushing]);
```

4.  Optional: add a timer retry so it re-attempts even if backlog doesn’t change:

```
useEffect(() => {
  const t = setInterval(() => {
    // nudge flush by re-setting backlog to itself
    setBacklog((b) => b);
  }, 3000);
  return () => clearInterval(t);
}, []);
```

* * *

CORS note (common blocker)
--------------------------

If your front-end runs on a different port (e.g., 3000) than the ingest (8787), the browser will require CORS.

### Quick fix: add CORS headers in the backend

In `server.js` (telemetry server), add before routes:

```
app.use((req, res, next) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  res.setHeader("Access-Control-Allow-Methods", "GET,POST,OPTIONS");
  if (req.method === "OPTIONS") return res.sendStatus(204);
  next();
});
```

* * *

Verification checklist
----------------------

1.  Start server: `node server.js`
2.  Run front-end and trigger any event (e.g., role selection)
3.  Confirm server writes:
    *   `data/telemetry/<UTC-date>/Lifehouse_Capital__<session>.jsonl`
4.  Open the file and confirm lines are appended.

If you tell me how you’re running the front-end (Vite, CRA, Next.js), I’ll give the exact `TELEMETRY_URL` and CORS setup that matches it.

## Prompt:
Confidence updater (server-side): updates ethno-object confidence scores based on telemetry triggers and (optionally) human validations.

## Response:
Server-side confidence updater (ethno-objects) — implement now
--------------------------------------------------------------

This adds a **confidence store** and a **deterministic + auditable** update mechanism on top of your JSONL telemetry stream.

### Data model (recommended)

*   `data/telemetry/YYYY-MM-DD/<account>__<session>.jsonl` (append-only)
*   `data/confidence/<account>.json` (current confidence snapshot)

Confidence per ethno-object uses a **Beta distribution**:

*   store: `{ alpha, beta }`
*   mean (current confidence): `alpha / (alpha + beta)`
*   updates:
    *   “supporting evidence” increments `alpha`
    *   “contradicting evidence” increments `beta`
*   advantage: mathematically grounded, explainable, and monotonic with evidence.

* * *

1) Add these files to your telemetry server
===========================================

A) `confidence.js` (engine)
---------------------------

Create `confidence.js` in the same folder as `server.js`:

```
import fs from "fs";
import path from "path";

function ensureDir(p) {
  fs.mkdirSync(p, { recursive: true });
}

function safeStr(s) {
  return String(s || "")
    .trim()
    .replace(/[^a-zA-Z0-9._-]/g, "_")
    .slice(0, 120);
}

function clamp(x, lo, hi) {
  return Math.max(lo, Math.min(hi, x));
}

function betaMean(alpha, beta) {
  const a = Math.max(1e-6, alpha);
  const b = Math.max(1e-6, beta);
  return a / (a + b);
}

/**
 * Initialize Beta prior from mean and strength.
 * strength ~ “how confident is the prior?” (higher = more inertia)
 */
function betaFromMean(mean = 0.65, strength = 10) {
  const m = clamp(mean, 0.01, 0.99);
  const s = Math.max(2, strength);
  const alpha = m * s;
  const beta = (1 - m) * s;
  return { alpha, beta };
}

/**
 * Lightweight update: add fractional pseudo-counts.
 * evidence in [0,1] where 1 is strong support, 0 is strong contradiction.
 * weight controls how big the update is.
 */
function betaUpdate({ alpha, beta }, evidence, weight) {
  const e = clamp(evidence, 0, 1);
  const w = clamp(weight, 0.01, 5); // cap for stability
  return {
    alpha: alpha + e * w,
    beta: beta + (1 - e) * w,
  };
}

function loadJson(file, fallback) {
  try {
    return JSON.parse(fs.readFileSync(file, "utf8"));
  } catch {
    return fallback;
  }
}

function saveJson(file, obj) {
  ensureDir(path.dirname(file));
  fs.writeFileSync(file, JSON.stringify(obj, null, 2), "utf8");
}

export function getConfidenceFile(DATA_DIR, account) {
  const CONF_DIR = path.join(DATA_DIR, "confidence");
  return path.join(CONF_DIR, `${safeStr(account || "unknown")}.json`);
}

/**
 * Core trigger map: telemetry event -> ethno-object evidence updates.
 * Replace EO ids with your real seed ethno-objects.
 *
 * Convention:
 * - evidence=1.0 means the event strongly supports the EO hypothesis
 * - evidence=0.0 means it contradicts it
 * - weight=0.1..2.0 controls increment size (pseudo-counts)
 */
export function confidenceTriggers(event) {
  const e = event?.event;
  if (!e) return [];

  switch (e) {
    // Governance / audit proof events
    case "export.generated":
      return [
        { eo: "eo_lh_0004", evidence: 1.0, weight: 0.6, reason: "Audit export generated (governance proof)" },
        { eo: "eo_lh_0012", evidence: 1.0, weight: 0.3, reason: "Variance telemetry touched via export context" },
      ];

    // Portability / lock-in concern
    case "portability.viewed":
      return [
        { eo: "eo_lh_0011", evidence: 1.0, weight: 0.4, reason: "Portability pack viewed (dependency risk salient)" },
      ];

    // Variance engagement
    case "variance.drivers_viewed":
      return [
        { eo: "eo_lh_0007", evidence: 1.0, weight: 0.35, reason: "Variance drivers reviewed (variance-first mindset)" },
        { eo: "eo_lh_0012", evidence: 1.0, weight: 0.35, reason: "Variance quantification engaged" },
      ];

    // Token salience — weak evidence until validated
    case "token.triggered":
      return [
        { eo: "eo_lh_token_salience", evidence: 1.0, weight: 0.1, reason: "Language token indicates salience" },
      ];

    default:
      return [];
  }
}

/**
 * Apply updates to confidence state.
 */
export function applyConfidenceUpdates({ DATA_DIR, account, event, priors }) {
  const file = getConfidenceFile(DATA_DIR, account);

  const state = loadJson(file, {
    account,
    updated_at: new Date().toISOString(),
    // priors: optional per-EO prior settings
    priors: priors || { default_mean: 0.65, default_strength: 10, per_eo: {} },
    // scores: EO -> {alpha,beta,mean,last_updated,history_tail[]}
    scores: {},
  });

  const defaultMean = state.priors?.default_mean ?? 0.65;
  const defaultStrength = state.priors?.default_strength ?? 10;

  const updates = confidenceTriggers(event);

  for (const u of updates) {
    const eo = u.eo;
    const priorCfg = state.priors?.per_eo?.[eo];

    const current = state.scores[eo] || {
      ...(priorCfg
        ? betaFromMean(priorCfg.mean ?? defaultMean, priorCfg.strength ?? defaultStrength)
        : betaFromMean(defaultMean, defaultStrength)),
      mean: null,
      last_updated: null,
      history_tail: [],
    };

    const nextBeta = betaUpdate(
      { alpha: current.alpha, beta: current.beta },
      u.evidence,
      u.weight
    );

    const nextMean = betaMean(nextBeta.alpha, nextBeta.beta);

    // keep small audit tail (last 20 updates)
    const tail = Array.isArray(current.history_tail) ? current.history_tail.slice(-19) : [];
    tail.push({
      at: new Date().toISOString(),
      event: event?.event,
      evidence: u.evidence,
      weight: u.weight,
      reason: u.reason,
      screen_id: event?.screen_id,
      module_id: event?.module_id,
      session_id: event?.session_id,
    });

    state.scores[eo] = {
      alpha: nextBeta.alpha,
      beta: nextBeta.beta,
      mean: nextMean,
      last_updated: new Date().toISOString(),
      history_tail: tail,
    };
  }

  state.updated_at = new Date().toISOString();
  saveJson(file, state);

  return { file, updates, state };
}

/**
 * Human validation endpoint semantics:
 * - label: "confirm" -> evidence=1
 * - label: "reject"  -> evidence=0
 * - label: "partial" -> evidence=0.6 (default)
 */
export function applyHumanValidation({ DATA_DIR, account, eo, label, weight = 1.0, note, context }) {
  const file = getConfidenceFile(DATA_DIR, account);
  const state = loadJson(file, {
    account,
    updated_at: new Date().toISOString(),
    priors: { default_mean: 0.65, default_strength: 10, per_eo: {} },
    scores: {},
  });

  const defaultMean = state.priors?.default_mean ?? 0.65;
  const defaultStrength = state.priors?.default_strength ?? 10;

  const current = state.scores[eo] || {
    ...betaFromMean(defaultMean, defaultStrength),
    mean: null,
    last_updated: null,
    history_tail: [],
  };

  const evidence =
    label === "confirm" ? 1.0 :
    label === "reject" ? 0.0 :
    0.6;

  const nextBeta = betaUpdate({ alpha: current.alpha, beta: current.beta }, evidence, weight);
  const nextMean = betaMean(nextBeta.alpha, nextBeta.beta);

  const tail = Array.isArray(current.history_tail) ? current.history_tail.slice(-19) : [];
  tail.push({
    at: new Date().toISOString(),
    event: "human.validation",
    evidence,
    weight,
    reason: `Human validation: ${label}`,
    note: note || null,
    context: context || null,
  });

  state.scores[eo] = {
    alpha: nextBeta.alpha,
    beta: nextBeta.beta,
    mean: nextMean,
    last_updated: new Date().toISOString(),
    history_tail: tail,
  };

  state.updated_at = new Date().toISOString();
  saveJson(file, state);

  return { file, eo, mean: nextMean, state };
}
```

* * *

B) Patch `server.js` to call the updater
----------------------------------------

In your existing `server.js`, add:

1.  At top:

```
import { applyConfidenceUpdates, applyHumanValidation } from "./confidence.js";
```

2.  Define `DATA_DIR` once (if not already):

```
const DATA_DIR = process.env.DATA_DIR || path.join(process.cwd(), "data");
```

3.  In `POST /telemetry/ingest`, after JSONL append succeeds, add:

```
// confidence update (telemetry-driven)
try {
  applyConfidenceUpdates({ DATA_DIR, account, event });
} catch {
  // do not block ingest on confidence issues
}
```

4.  Add a human validation endpoint:

```
app.post("/confidence/validate", (req, res) => {
  const { account, eo, label, weight, note, context } = req.body || {};
  if (!account || !eo || !label) {
    return res.status(400).json({ ok: false, error: "missing_account_eo_label" });
  }
  try {
    const out = applyHumanValidation({
      DATA_DIR,
      account,
      eo,
      label,
      weight: typeof weight === "number" ? weight : 1.0,
      note,
      context,
    });
    return res.json({ ok: true, mean: out.mean, file: out.file });
  } catch {
    return res.status(500).json({ ok: false, error: "validation_failed" });
  }
});
```

5.  Add a read endpoint:

```
app.get("/confidence/:account", (req, res) => {
  const account = req.params.account;
  const file = path.join(DATA_DIR, "confidence", `${account.replace(/[^a-zA-Z0-9._-]/g, "_")}.json`);
  if (!fs.existsSync(file)) return res.status(404).json({ ok: false, error: "not_found" });
  const state = JSON.parse(fs.readFileSync(file, "utf8"));
  res.json({ ok: true, confidence: state });
});
```

* * *

2) How it works (operational semantics)
=======================================

Telemetry-driven updates
------------------------

*   Every incoming telemetry event is appended to JSONL.
*   Then `confidenceTriggers(event)` maps it to EO updates.
*   Each update adjusts the EO’s Beta distribution and logs a small audit tail.

Human validation
----------------

*   Call `/confidence/validate` when a human confirms/rejects an ethno-object:
    *   `confirm` increases alpha (confidence rises)
    *   `reject` increases beta (confidence falls)
    *   `partial` is moderate support

* * *

3) Test it end-to-end
=====================

### Start server

```
node server.js
```

### Post a telemetry event that triggers confidence

```
curl -X POST http://localhost:8787/telemetry/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "event":"export.generated",
    "flow_id":"liquifex_lifehouse_demo_v1",
    "account":"Lifehouse Capital",
    "session_id":"sess_test_002",
    "screen_id":"A5_audit_export",
    "module_id":"A_mechanics_audit",
    "metadata":{"export_type":"event_log_json"}
  }'
```

### Read the confidence snapshot

```
curl http://localhost:8787/confidence/Lifehouse_Capital
```

### Human validation example

```
curl -X POST http://localhost:8787/confidence/validate \
  -H "Content-Type: application/json" \
  -d '{
    "account":"Lifehouse Capital",
    "eo":"eo_lh_0004",
    "label":"confirm",
    "weight":1.2,
    "note":"Compliance lead confirmed audit export is a gating requirement",
    "context":{"meeting":"Lifehouse demo", "date":"2026-02-27"}
  }'
```

* * *

4) What you should customize next (high leverage)
=================================================

1.  Replace EO ids in `confidenceTriggers()` with your **real seed ethno-objects**.
2.  Tune weights:
    *   telemetry weights smaller (0.1–0.6)
    *   human validations larger (0.8–2.0)
3.  Add “contradiction” triggers (e.g., if they dismiss a module, evidence=0).

If you paste your current EO list (the 10–20 seed objects), I’ll generate the exact `confidenceTriggers()` map aligned to them.

## Prompt:
explain what an EO list and suggest one for lighthouse life based on the information liquefex needs to transmit for all LS industry players

## Response:
1) What an EO list is
---------------------

**EO = Ethno-Object.**

An EO is a structured, testable hypothesis about how a stakeholder **thinks, prioritizes risk, allocates capital, or defines success**.

It is not a feature.  
It is not a persona.  
It is not a demographic.

It is:

> A belief or behavioral pattern that influences decisions in a recurring, economically meaningful way.

In LiquiFex, EO’s are used to:

*   Detect decision friction
*   Route demo emphasis
*   Adjust messaging
*   Weight confidence models
*   Prioritize roadmap
*   Predict adoption resistance

Each EO should be:

*   **Specific**
*   **Observable**
*   **Economically material**
*   **Updatable via telemetry**

* * *

2) What LiquiFex must transmit to LS industry players
-----------------------------------------------------

Across Life Settlement / Life Insurance Capital markets players (Lifehouse, capital allocators, premium finance, servicers, etc.), LiquiFex is trying to transmit 5 core ideas:

1.  Liquidity variance is the hidden risk.
2.  Auditability is a gating constraint.
3.  Rules + exceptions are infrastructure.
4.  Capital velocity matters more than averages.
5.  Portability reduces institutional risk.

Your EO list should align to those transmission goals.

* * *

3) Suggested EO List for Lifehouse Capital (LS ecosystem aligned)
=================================================================

Below is a high-signal EO list tailored for institutional life insurance capital operators and LS industry participants.

Each includes:

*   Hypothesis
*   Why it matters
*   What telemetry would confirm it

* * *

EO\_LH\_0001 — Governance-Gated Adoption
----------------------------------------

**Hypothesis:**  
No system will be adopted unless audit defensibility is proven first.

**Economic impact:**  
Adoption stalls without governance proof.

**Confirming telemetry:**

*   export.generated
*   provenance.ledger\_viewed
*   versioning.viewed
*   questions about rule source

* * *

EO\_LH\_0002 — Tail Risk > Mean Efficiency
------------------------------------------

**Hypothesis:**  
P90 variance matters more than average TTL.

**Economic impact:**  
Capital models are distorted by tail behavior.

**Confirming telemetry:**

*   variance.drivers\_viewed
*   tail\_risk.controls\_viewed
*   filter.changed (state/carrier)

* * *

EO\_LH\_0003 — Carrier Variability Is Structural
------------------------------------------------

**Hypothesis:**  
Carrier rule divergence is a permanent condition, not an exception.

**Economic impact:**  
Manual processes scale poorly.

**Confirming telemetry:**

*   rules.table\_viewed
*   questions about versioning
*   C\_rules\_exceptions module depth

* * *

EO\_LH\_0004 — Audit Artifact as Decision Object
------------------------------------------------

**Hypothesis:**  
Audit export itself is a product requirement.

**Economic impact:**  
System must generate institutional proof.

**Confirming telemetry:**

*   export.generated
*   audit\_summary\_previewed

* * *

EO\_LH\_0005 — Spreadsheet as Shadow System
-------------------------------------------

**Hypothesis:**  
Spreadsheets are currently the real control plane.

**Economic impact:**  
Dual-run cost + operational fragility.

**Confirming telemetry:**

*   spreadsheet.mapper\_viewed
*   dualrun.checklist\_viewed

* * *

EO\_LH\_0006 — Portability as Procurement Gate
----------------------------------------------

**Hypothesis:**  
Vendor dependency is a real committee blocker.

**Economic impact:**  
Deals die on lock-in risk.

**Confirming telemetry:**

*   portability.viewed
*   token: “dependency” / “exit”

* * *

EO\_LH\_0007 — Exception Volume Is Signal
-----------------------------------------

**Hypothesis:**  
Escalation rates indicate structural misalignment, not just noise.

**Economic impact:**  
Hidden cost-to-serve and capital delay.

**Confirming telemetry:**

*   exceptions.model\_viewed
*   exception\_spike trigger

* * *

EO\_LH\_0008 — Capital Velocity Is Core KPI
-------------------------------------------

**Hypothesis:**  
Time-to-liquidity drives IRR more than servicing cost.

**Economic impact:**  
Variance reduction = capital efficiency gain.

**Confirming telemetry:**

*   reduce\_p90\_ttl selected
*   variance\_reporting workflow selected

* * *

EO\_LH\_0009 — Deterministic > Black Box
----------------------------------------

**Hypothesis:**  
Probabilistic systems must remain bounded and auditable.

**Economic impact:**  
AI risk perception blocks adoption.

**Confirming telemetry:**

*   token: “mechanics” / “explain”
*   versioning.viewed
*   decision\_path.viewed

* * *

EO\_LH\_0010 — Rules Are First-Class Assets
-------------------------------------------

**Hypothesis:**  
Institutional players will treat rule sets as exportable intellectual capital.

**Economic impact:**  
Rules must be portable and versioned.

**Confirming telemetry:**

*   rules\_provenance\_export
*   rules\_snapshot\_json download

* * *

EO\_LH\_0011 — Committee Decision Friction
------------------------------------------

**Hypothesis:**  
Internal committees require cross-functional validation artifacts.

**Economic impact:**  
Sales cycles elongate without structured artifacts.

**Confirming telemetry:**

*   committee\_mandate trigger
*   portability + audit modules viewed together

* * *

EO\_LH\_0012 — Variance Quantification Changes Behavior
-------------------------------------------------------

**Hypothesis:**  
Once variance bands are visible, operational behavior shifts.

**Economic impact:**  
Measurement drives structural improvement.

**Confirming telemetry:**

*   variance.drivers\_viewed
*   threshold.updated

* * *

EO\_LH\_0013 — Human Override Is Mandatory
------------------------------------------

**Hypothesis:**  
Full automation is unacceptable; override must exist.

**Economic impact:**  
System design must embed human governance.

**Confirming telemetry:**

*   approval\_required\_for\_override toggled
*   override\_register export

* * *

EO\_LH\_0014 — Multi-State Complexity Drives Hidden Risk
--------------------------------------------------------

**Hypothesis:**  
State-specific regulatory variation is underestimated.

**Economic impact:**  
Execution unpredictability.

**Confirming telemetry:**

*   multi\_state selected
*   state filter interactions

* * *

EO\_LH\_0015 — Liquidity Infrastructure Is Under-Institutionalized
------------------------------------------------------------------

**Hypothesis:**  
LS industry liquidity workflows lack formal infrastructure.

**Economic impact:**  
Fragmentation → inefficiency → capital drag.

**Confirming telemetry:**

*   engagement across A + B + C modules
*   pilot workflow selection

* * *

4) Why this EO list works
=========================

It covers:

*   Governance
*   Variance
*   Carrier complexity
*   Portability
*   Spreadsheet migration
*   Institutional decision dynamics
*   AI risk perception
*   Capital velocity economics

It is aligned to what LiquiFex needs to transmit across **all LS industry players**, not just Lifehouse.

* * *

5) How this drives system intelligence
======================================

Each EO becomes:

*   A confidence-tracked hypothesis
*   A routing weight in demo flow
*   A messaging emphasis selector
*   A sales friction predictor
*   A roadmap prioritization signal

As telemetry accumulates, you begin to see:

*   Which EO’s dominate by firm type
*   Which EO’s correlate with pilot conversion
*   Which EO’s correlate with stall

That becomes institutional memory.

* * *

If you want next-level rigor, I can:

*   Convert this EO list into a full machine-readable EO schema
*   Add prior strengths + decay rates
*   Map each EO to explicit LiquiFex product surface areas
*   Or create an LS-industry-wide EO taxonomy beyond Lifehouse

Tell me which direction.

## Prompt:
Convert this EO list into a full machine-readable EO schema

## Response:
Machine-readable EO schema (Ethno-Object) for LiquiFex
------------------------------------------------------

This gives you:

1.  A **JSON Schema** for EO definitions
2.  A **JSON Schema** for EO evidence events (telemetry + human validation)
3.  A **complete EO catalog** for the Lifehouse list (EO\_LH\_0001–EO\_LH\_0015) in machine-readable records

* * *

1) EO Definition Schema (JSON Schema)
=====================================

```
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://liquifex.ai/schemas/eo.definition.v1.json",
  "title": "Ethno-Object Definition (EO) v1",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "eo_id",
    "name",
    "version",
    "status",
    "scope",
    "hypothesis",
    "decision_impact",
    "signals",
    "confidence_model",
    "routing_rules",
    "created_at"
  ],
  "properties": {
    "eo_id": {
      "type": "string",
      "pattern": "^EO_[A-Z0-9]+_[0-9]{4}$",
      "description": "Stable EO identifier, e.g. EO_LH_0001"
    },
    "name": { "type": "string", "minLength": 3 },
    "version": {
      "type": "string",
      "pattern": "^v[0-9]+\\.[0-9]+$",
      "description": "EO definition version"
    },
    "status": {
      "type": "string",
      "enum": ["active", "deprecated", "draft"]
    },
    "scope": {
      "type": "object",
      "additionalProperties": false,
      "required": ["industry", "account_type", "stakeholder_roles"],
      "properties": {
        "industry": { "type": "string", "description": "e.g., LS (Life Settlements) ecosystem" },
        "account_type": { "type": "string", "description": "e.g., institutional_life_insurance_capital_operator" },
        "stakeholder_roles": {
          "type": "array",
          "items": { "type": "string" },
          "minItems": 1
        },
        "applies_to_accounts": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Optional allowlist of account names"
        }
      }
    },
    "hypothesis": {
      "type": "object",
      "additionalProperties": false,
      "required": ["statement", "why_true", "why_it_matters"],
      "properties": {
        "statement": { "type": "string", "minLength": 10 },
        "why_true": { "type": "string", "minLength": 10 },
        "why_it_matters": { "type": "string", "minLength": 10 }
      }
    },
    "decision_impact": {
      "type": "object",
      "additionalProperties": false,
      "required": ["buying_criteria", "risks", "kpis"],
      "properties": {
        "buying_criteria": {
          "type": "array",
          "items": { "type": "string" },
          "minItems": 1
        },
        "risks": {
          "type": "array",
          "items": { "type": "string" }
        },
        "kpis": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "signals": {
      "type": "object",
      "additionalProperties": false,
      "required": ["telemetry_events", "language_tokens", "negative_signals"],
      "properties": {
        "telemetry_events": {
          "type": "array",
          "description": "Events that support this EO",
          "items": {
            "type": "object",
            "additionalProperties": false,
            "required": ["event", "evidence", "weight", "reason"],
            "properties": {
              "event": { "type": "string" },
              "evidence": { "type": "number", "minimum": 0, "maximum": 1 },
              "weight": { "type": "number", "minimum": 0.01, "maximum": 5 },
              "reason": { "type": "string" }
            }
          }
        },
        "language_tokens": {
          "type": "array",
          "description": "Phrases that indicate salience",
          "items": {
            "type": "object",
            "additionalProperties": false,
            "required": ["match_any", "evidence", "weight", "token_group"],
            "properties": {
              "match_any": { "type": "array", "items": { "type": "string" }, "minItems": 1 },
              "evidence": { "type": "number", "minimum": 0, "maximum": 1 },
              "weight": { "type": "number", "minimum": 0.01, "maximum": 5 },
              "token_group": { "type": "string" }
            }
          }
        },
        "negative_signals": {
          "type": "array",
          "description": "Events/tokens that contradict this EO",
          "items": {
            "type": "object",
            "additionalProperties": false,
            "required": ["kind", "match", "evidence", "weight", "reason"],
            "properties": {
              "kind": { "type": "string", "enum": ["telemetry_event", "language_token", "human_validation"] },
              "match": { "type": "string" },
              "evidence": { "type": "number", "minimum": 0, "maximum": 1 },
              "weight": { "type": "number", "minimum": 0.01, "maximum": 5 },
              "reason": { "type": "string" }
            }
          }
        }
      }
    },
    "confidence_model": {
      "type": "object",
      "additionalProperties": false,
      "required": ["type", "prior", "decay"],
      "properties": {
        "type": { "type": "string", "enum": ["beta"] },
        "prior": {
          "type": "object",
          "additionalProperties": false,
          "required": ["mean", "strength"],
          "properties": {
            "mean": { "type": "number", "minimum": 0.01, "maximum": 0.99 },
            "strength": { "type": "number", "minimum": 2, "maximum": 200 }
          }
        },
        "decay": {
          "type": "object",
          "additionalProperties": false,
          "required": ["enabled", "rate_per_period", "period_days", "floor", "ceiling"],
          "properties": {
            "enabled": { "type": "boolean" },
            "rate_per_period": { "type": "number", "minimum": 0, "maximum": 1 },
            "period_days": { "type": "integer", "minimum": 1, "maximum": 365 },
            "floor": { "type": "number", "minimum": 0.01, "maximum": 0.99 },
            "ceiling": { "type": "number", "minimum": 0.01, "maximum": 0.99 }
          }
        }
      }
    },
    "routing_rules": {
      "type": "object",
      "additionalProperties": false,
      "required": ["module_priority", "depth_promote", "message_emphasis"],
      "properties": {
        "module_priority": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Modules to move earlier when EO is high-confidence"
        },
        "depth_promote": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Modules to show deeper detail for"
        },
        "message_emphasis": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Messaging pillars to emphasize"
        }
      }
    },
    "governance": {
      "type": "object",
      "additionalProperties": false,
      "required": ["owner", "review_cadence_days"],
      "properties": {
        "owner": { "type": "string" },
        "review_cadence_days": { "type": "integer", "minimum": 7, "maximum": 365 },
        "notes": { "type": "string" }
      }
    },
    "created_at": { "type": "string", "format": "date-time" },
    "updated_at": { "type": "string", "format": "date-time" }
  }
}
```

* * *

2) EO Evidence Event Schema (telemetry + human validation)
==========================================================

```
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://liquifex.ai/schemas/eo.evidence_event.v1.json",
  "title": "EO Evidence Event v1",
  "type": "object",
  "additionalProperties": false,
  "required": ["timestamp", "account", "session_id", "source", "eo_id", "evidence", "weight"],
  "properties": {
    "timestamp": { "type": "string", "format": "date-time" },
    "account": { "type": "string" },
    "session_id": { "type": "string" },
    "source": { "type": "string", "enum": ["telemetry", "human_validation", "imported_history"] },
    "eo_id": { "type": "string" },
    "evidence": { "type": "number", "minimum": 0, "maximum": 1 },
    "weight": { "type": "number", "minimum": 0.01, "maximum": 5 },
    "reason": { "type": "string" },
    "context": {
      "type": "object",
      "additionalProperties": true,
      "description": "screen_id, module_id, token_group, notes, etc."
    }
  }
}
```

* * *

3) EO Catalog (Lifehouse list) in machine-readable records
==========================================================

```
{
  "catalog_id": "EO_CATALOG_LH_LS_v1",
  "account": "Lifehouse Capital",
  "industry": "LS_ecosystem",
  "generated_at": "2026-02-27T00:00:00Z",
  "eos": [
    {
      "eo_id": "EO_LH_0001",
      "name": "Governance-Gated Adoption",
      "version": "v1.0",
      "status": "active",
      "scope": {
        "industry": "LS_ecosystem",
        "account_type": "institutional_life_insurance_capital_operator",
        "stakeholder_roles": ["compliance", "procurement", "exec", "investment"]
      },
      "hypothesis": {
        "statement": "Adoption will not proceed unless audit defensibility is proven first.",
        "why_true": "Institutional workflows are constrained by governance, committee review, and auditability requirements.",
        "why_it_matters": "Without governance proof, pilots stall and procurement blocks conversion."
      },
      "decision_impact": {
        "buying_criteria": ["audit_export", "provenance", "versioning", "override_controls"],
        "risks": ["audit_failure", "committee_rejection"],
        "kpis": ["governance_acceptance_rate", "time_to_committee_approval"]
      },
      "signals": {
        "telemetry_events": [
          { "event": "export.generated", "evidence": 1.0, "weight": 0.6, "reason": "Audit exports indicate governance focus" },
          { "event": "provenance.ledger_viewed", "evidence": 1.0, "weight": 0.4, "reason": "Provenance review indicates audit gating" },
          { "event": "versioning.viewed", "evidence": 1.0, "weight": 0.3, "reason": "Versioning inspection indicates defensibility requirements" }
        ],
        "language_tokens": [
          { "match_any": ["audit", "governance", "defensible", "compliance"], "evidence": 1.0, "weight": 0.2, "token_group": "mechanics_audit" }
        ],
        "negative_signals": [
          { "kind": "language_token", "match": "we don't need audit", "evidence": 0.0, "weight": 0.5, "reason": "Explicitly deprioritizes governance gating" }
        ]
      },
      "confidence_model": {
        "type": "beta",
        "prior": { "mean": 0.75, "strength": 14 },
        "decay": { "enabled": true, "rate_per_period": 0.05, "period_days": 30, "floor": 0.2, "ceiling": 0.98 }
      },
      "routing_rules": {
        "module_priority": ["A_mechanics_audit", "F_portability_pack"],
        "depth_promote": ["A_mechanics_audit"],
        "message_emphasis": ["auditability_first", "provenance", "reproducibility"]
      },
      "governance": { "owner": "product_ops", "review_cadence_days": 45, "notes": "Treat audit export as primary proof artifact." },
      "created_at": "2026-02-27T00:00:00Z",
      "updated_at": "2026-02-27T00:00:00Z"
    },

    {
      "eo_id": "EO_LH_0002",
      "name": "Tail Risk Over Mean Efficiency",
      "version": "v1.0",
      "status": "active",
      "scope": {
        "industry": "LS_ecosystem",
        "account_type": "institutional_life_insurance_capital_operator",
        "stakeholder_roles": ["investment", "risk", "exec"]
      },
      "hypothesis": {
        "statement": "P90 outcomes (tail risk) matter more than average cycle time.",
        "why_true": "Institutional risk management prioritizes downside containment and predictability under stress cases.",
        "why_it_matters": "Variance reduction is the clearest institutional ROI lever."
      },
      "decision_impact": {
        "buying_criteria": ["p90_controls", "variance_drivers", "escalation_thresholds"],
        "risks": ["tail_events", "capital_drag"],
        "kpis": ["P90_time_to_liquidity", "P90_minus_P50_spread"]
      },
      "signals": {
        "telemetry_events": [
          { "event": "variance.chart_viewed", "evidence": 1.0, "weight": 0.3, "reason": "Viewing P50/P90 indicates tail focus" },
          { "event": "tail_risk.controls_viewed", "evidence": 1.0, "weight": 0.5, "reason": "Tail controls engagement indicates tail priority" }
        ],
        "language_tokens": [
          { "match_any": ["p90", "tail risk", "downside", "variance band"], "evidence": 1.0, "weight": 0.25, "token_group": "variance_tail" }
        ],
        "negative_signals": [
          { "kind": "language_token", "match": "just show the average", "evidence": 0.0, "weight": 0.3, "reason": "Deprioritizes tails" }
        ]
      },
      "confidence_model": {
        "type": "beta",
        "prior": { "mean": 0.7, "strength": 12 },
        "decay": { "enabled": true, "rate_per_period": 0.05, "period_days": 30, "floor": 0.2, "ceiling": 0.98 }
      },
      "routing_rules": {
        "module_priority": ["B_variance_dashboard"],
        "depth_promote": ["B_variance_dashboard"],
        "message_emphasis": ["variance_over_average", "tail_containment", "predictability"]
      },
      "governance": { "owner": "product", "review_cadence_days": 60, "notes": "Emphasize P90 containment in demos." },
      "created_at": "2026-02-27T00:00:00Z",
      "updated_at": "2026-02-27T00:00:00Z"
    },

    {
      "eo_id": "EO_LH_0003",
      "name": "Carrier Variability Is Structural",
      "version": "v1.0",
      "status": "active",
      "scope": {
        "industry": "LS_ecosystem",
        "account_type": "institutional_life_insurance_capital_operator",
        "stakeholder_roles": ["operations", "investment", "data"]
      },
      "hypothesis": {
        "statement": "Carrier rule divergence is permanent and must be modeled as infrastructure.",
        "why_true": "Carrier-specific processes and rulebooks change and differ by product and jurisdiction.",
        "why_it_matters": "Scaling requires rules+exceptions, not manual heroics."
      },
      "decision_impact": {
        "buying_criteria": ["rules_objects", "exceptions_model", "versioning"],
        "risks": ["operational_scaling_failure"],
        "kpis": ["exception_rate", "rule_change_lead_time"]
      },
      "signals": {
        "telemetry_events": [
          { "event": "rules.table_viewed", "evidence": 1.0, "weight": 0.45, "reason": "Rules object interest signals structural framing" },
          { "event": "exceptions.model_viewed", "evidence": 1.0, "weight": 0.35, "reason": "Exceptions model validates variability acceptance" }
        ],
        "language_tokens": [
          { "match_any": ["carrier variability", "carrier-by-carrier", "rule divergence"], "evidence": 1.0, "weight": 0.2, "token_group": "carrier_variance" }
        ],
        "negative_signals": [
          { "kind": "language_token", "match": "standardize carriers", "evidence": 0.2, "weight": 0.2, "reason": "Signals belief variability can be eliminated rather than modeled" }
        ]
      },
      "confidence_model": {
        "type": "beta",
        "prior": { "mean": 0.65, "strength": 10 },
        "decay": { "enabled": true, "rate_per_period": 0.05, "period_days": 30, "floor": 0.2, "ceiling": 0.98 }
      },
      "routing_rules": {
        "module_priority": ["C_rules_exceptions"],
        "depth_promote": ["C_rules_exceptions"],
        "message_emphasis": ["rules_as_infrastructure", "exceptions_as_first_class", "versioned_change_management"]
      },
      "governance": { "owner": "product", "review_cadence_days": 60, "notes": "" },
      "created_at": "2026-02-27T00:00:00Z",
      "updated_at": "2026-02-27T00:00:00Z"
    },

    {
      "eo_id": "EO_LH_0004",
      "name": "Audit Artifact Is the Product",
      "version": "v1.0",
      "status": "active",
      "scope": {
        "industry": "LS_ecosystem",
        "account_type": "institutional_life_insurance_capital_operator",
        "stakeholder_roles": ["compliance", "procurement", "exec"]
      },
      "hypothesis": {
        "statement": "The audit export itself is a core deliverable, not an implementation detail.",
        "why_true": "Committee and regulator-facing artifacts determine whether systems are acceptable.",
        "why_it_matters": "If exports are first-class, adoption accelerates."
      },
      "decision_impact": {
        "buying_criteria": ["audit_exports", "override_register", "rules_snapshot"],
        "risks": ["audit_deficiency"],
        "kpis": ["audit_export_usage", "audit_findings_rate"]
      },
      "signals": {
        "telemetry_events": [
          { "event": "export.panel_viewed", "evidence": 1.0, "weight": 0.25, "reason": "Export panel engagement" },
          { "event": "export.generated", "evidence": 1.0, "weight": 0.6, "reason": "Export generation indicates artifact demand" }
        ],
        "language_tokens": [
          { "match_any": ["export", "audit packet", "committee packet", "evidence trail"], "evidence": 1.0, "weight": 0.2, "token_group": "audit_artifact" }
        ],
        "negative_signals": []
      },
      "confidence_model": {
        "type": "beta",
        "prior": { "mean": 0.75, "strength": 14 },
        "decay": { "enabled": true, "rate_per_period": 0.05, "period_days": 30, "floor": 0.2, "ceiling": 0.98 }
      },
      "routing_rules": {
        "module_priority": ["A_mechanics_audit"],
        "depth_promote": ["A_mechanics_audit"],
        "message_emphasis": ["audit_packet", "exportability", "institutional_proof"]
      },
      "governance": { "owner": "product_ops", "review_cadence_days": 45, "notes": "" },
      "created_at": "2026-02-27T00:00:00Z",
      "updated_at": "2026-02-27T00:00:00Z"
    },

    {
      "eo_id": "EO_LH_0005",
      "name": "Spreadsheet Shadow Control Plane",
      "version": "v1.0",
      "status": "active",
      "scope": {
        "industry": "LS_ecosystem",
        "account_type": "institutional_life_insurance_capital_operator",
        "stakeholder_roles": ["operations", "investment", "data"]
      },
      "hypothesis": {
        "statement": "Spreadsheets currently function as the real control plane for liquidity workflows.",
        "why_true": "Operational reality often relies on spreadsheets for reconciliation, tracking, and approvals.",
        "why_it_matters": "Migration must be explicit, time-boxed, and audit-safe."
      },
      "decision_impact": {
        "buying_criteria": ["spreadsheet_import", "mapping", "dual_run_exit"],
        "risks": ["dual_run_drag", "key_person_risk"],
        "kpis": ["manual_steps", "spreadsheet_dependency_index"]
      },
      "signals": {
        "telemetry_events": [
          { "event": "spreadsheet.mapper_viewed", "evidence": 1.0, "weight": 0.5, "reason": "Spreadsheet mapping engagement" },
          { "event": "dualrun.checklist_viewed", "evidence": 1.0, "weight": 0.35, "reason": "Exit checklist engagement" }
        ],
        "language_tokens": [
          { "match_any": ["spreadsheet", "tracker", "excel", "reconciliation sheet"], "evidence": 1.0, "weight": 0.2, "token_group": "spreadsheet_control" }
        ],
        "negative_signals": []
      },
      "confidence_model": {
        "type": "beta",
        "prior": { "mean": 0.65, "strength": 10 },
        "decay": { "enabled": true, "rate_per_period": 0.05, "period_days": 30, "floor": 0.2, "ceiling": 0.98 }
      },
      "routing_rules": {
        "module_priority": ["E_spreadsheet_migration"],
        "depth_promote": ["E_spreadsheet_migration"],
        "message_emphasis": ["control_transfer", "dual_run_exit", "audit_safe_migration"]
      },
      "governance": { "owner": "solutions_eng", "review_cadence_days": 60, "notes": "" },
      "created_at": "2026-02-27T00:00:00Z",
      "updated_at": "2026-02-27T00:00:00Z"
    },

    {
      "eo_id": "EO_LH_0006",
      "name": "Portability Is Procurement Gate",
      "version": "v1.0",
      "status": "active",
      "scope": {
        "industry": "LS_ecosystem",
        "account_type": "institutional_life_insurance_capital_operator",
        "stakeholder_roles": ["procurement", "compliance", "exec"]
      },
      "hypothesis": {
        "statement": "Vendor dependency and offboarding risk are committee blockers unless mitigated upfront.",
        "why_true": "Institutions avoid lock-in where mission-critical rules and evidence trails are concerned.",
        "why_it_matters": "Portability reduces cycle time and increases win probability."
      },
      "decision_impact": {
        "buying_criteria": ["portability_pack", "offboarding_playbook", "export_specs"],
        "risks": ["vendor_lock_in", "implementation_risk"],
        "kpis": ["procurement_cycle_time", "security_review_pass_rate"]
      },
      "signals": {
        "telemetry_events": [
          { "event": "portability.viewed", "evidence": 1.0, "weight": 0.5, "reason": "Portability pack engagement" }
        ],
        "language_tokens": [
          { "match_any": ["lock-in", "dependency", "exit", "offboarding"], "evidence": 1.0, "weight": 0.25, "token_group": "dependency_exit" }
        ],
        "negative_signals": []
      },
      "confidence_model": {
        "type": "beta",
        "prior": { "mean": 0.7, "strength": 12 },
        "decay": { "enabled": true, "rate_per_period": 0.05, "period_days": 30, "floor": 0.2, "ceiling": 0.98 }
      },
      "routing_rules": {
        "module_priority": ["F_portability_pack"],
        "depth_promote": ["F_portability_pack"],
        "message_emphasis": ["portability", "exit_safety", "anti_lockin"]
      },
      "governance": { "owner": "sales_ops", "review_cadence_days": 60, "notes": "" },
      "created_at": "2026-02-27T00:00:00Z",
      "updated_at": "2026-02-27T00:00:00Z"
    },

    {
      "eo_id": "EO_LH_0007",
      "name": "Exception Volume Is Structural Signal",
      "version": "v1.0",
      "status": "active",
      "scope": {
        "industry": "LS_ecosystem",
        "account_type": "institutional_life_insurance_capital_operator",
        "stakeholder_roles": ["operations", "risk", "investment"]
      },
      "hypothesis": {
        "statement": "Escalation and exception rates indicate structural misalignment, not noise.",
        "why_true": "Exceptions cluster around rule gaps, missing evidence, and carrier/jurisdiction edge cases.",
        "why_it_matters": "Exception reduction lowers cost-to-serve and improves capital velocity."
      },
      "decision_impact": {
        "buying_criteria": ["exception_classification", "playbooks", "thresholds"],
        "risks": ["hidden_cost_to_serve", "capital_delay"],
        "kpis": ["exception_rate", "exception_resolution_time"]
      },
      "signals": {
        "telemetry_events": [
          { "event": "exceptions.model_viewed", "evidence": 1.0, "weight": 0.4, "reason": "Exceptions model engagement" },
          { "event": "variance.drivers_viewed", "evidence": 1.0, "weight": 0.25, "reason": "Drivers list often includes exceptions" }
        ],
        "language_tokens": [
          { "match_any": ["escalation", "exceptions", "triage", "playbook"], "evidence": 1.0, "weight": 0.2, "token_group": "exceptions" }
        ],
        "negative_signals": []
      },
      "confidence_model": {
        "type": "beta",
        "prior": { "mean": 0.65, "strength": 10 },
        "decay": { "enabled": true, "rate_per_period": 0.05, "period_days": 30, "floor": 0.2, "ceiling": 0.98 }
      },
      "routing_rules": {
        "module_priority": ["C_rules_exceptions"],
        "depth_promote": ["C_rules_exceptions"],
        "message_emphasis": ["exceptions_as_signal", "playbooks", "operational_scaling"]
      },
      "governance": { "owner": "solutions_eng", "review_cadence_days": 60, "notes": "" },
      "created_at": "2026-02-27T00:00:00Z",
      "updated_at": "2026-02-27T00:00:00Z"
    },

    {
      "eo_id": "EO_LH_0008",
      "name": "Capital Velocity Is Core KPI",
      "version": "v1.0",
      "status": "active",
      "scope": {
        "industry": "LS_ecosystem",
        "account_type": "institutional_life_insurance_capital_operator",
        "stakeholder_roles": ["investment", "exec"]
      },
      "hypothesis": {
        "statement": "Time-to-liquidity drives returns more than marginal servicing efficiency.",
        "why_true": "Capital trapped in process reduces redeployment and opportunity capture.",
        "why_it_matters": "Variance reduction maps directly to institutional ROI."
      },
      "decision_impact": {
        "buying_criteria": ["variance_dashboard", "ttl_controls"],
        "risks": ["opportunity_cost", "capital_drag"],
        "kpis": ["capital_velocity", "time_to_liquidity"]
      },
      "signals": {
        "telemetry_events": [
          { "event": "pilot.metrics_selected", "evidence": 1.0, "weight": 0.35, "reason": "Selecting TTL metrics indicates capital velocity focus" }
        ],
        "language_tokens": [
          { "match_any": ["capital velocity", "redeploy", "time-to-liquidity", "opportunity cost"], "evidence": 1.0, "weight": 0.25, "token_group": "capital_velocity" }
        ],
        "negative_signals": []
      },
      "confidence_model": {
        "type": "beta",
        "prior": { "mean": 0.65, "strength": 10 },
        "decay": { "enabled": true, "rate_per_period": 0.05, "period_days": 30, "floor": 0.2, "ceiling": 0.98 }
      },
      "routing_rules": {
        "module_priority": ["B_variance_dashboard"],
        "depth_promote": ["B_variance_dashboard"],
        "message_emphasis": ["capital_velocity", "variance_to_roi"]
      },
      "governance": { "owner": "sales", "review_cadence_days": 60, "notes": "" },
      "created_at": "2026-02-27T00:00:00Z",
      "updated_at": "2026-02-27T00:00:00Z"
    },

    {
      "eo_id": "EO_LH_0009",
      "name": "Deterministic Over Black Box",
      "version": "v1.0",
      "status": "active",
      "scope": {
        "industry": "LS_ecosystem",
        "account_type": "institutional_life_insurance_capital_operator",
        "stakeholder_roles": ["risk", "compliance", "data", "exec"]
      },
      "hypothesis": {
        "statement": "Probabilistic automation must be bounded; determinism and explainability are mandatory.",
        "why_true": "Institutional risk posture rejects opaque decisioning in regulated/committee-controlled workflows.",
        "why_it_matters": "Positioning must be controls-first to avoid AI-risk rejection."
      },
      "decision_impact": {
        "buying_criteria": ["explainability", "override_controls", "versioning"],
        "risks": ["ai_risk_perception", "governance_block"],
        "kpis": ["override_rate", "explainability_acceptance"]
      },
      "signals": {
        "telemetry_events": [
          { "event": "decision_path.viewed", "evidence": 1.0, "weight": 0.35, "reason": "Decision path scrutiny indicates explainability demand" },
          { "event": "versioning.viewed", "evidence": 1.0, "weight": 0.25, "reason": "Change control is often tied to non-black-box needs" }
        ],
        "language_tokens": [
          { "match_any": ["mechanics", "explain", "black box", "how does it decide"], "evidence": 1.0, "weight": 0.25, "token_group": "mechanics_audit" }
        ],
        "negative_signals": []
      },
      "confidence_model": {
        "type": "beta",
        "prior": { "mean": 0.7, "strength": 12 },
        "decay": { "enabled": true, "rate_per_period": 0.05, "period_days": 30, "floor": 0.2, "ceiling": 0.98 }
      },
      "routing_rules": {
        "module_priority": ["A_mechanics_audit"],
        "depth_promote": ["A_mechanics_audit", "C_rules_exceptions"],
        "message_emphasis": ["deterministic_controls", "bounded_ai", "human_override"]
      },
      "governance": { "owner": "product", "review_cadence_days": 60, "notes": "" },
      "created_at": "2026-02-27T00:00:00Z",
      "updated_at": "2026-02-27T00:00:00Z"
    },

    {
      "eo_id": "EO_LH_0010",
      "name": "Rules Are First-Class Assets",
      "version": "v1.0",
      "status": "active",
      "scope": {
        "industry": "LS_ecosystem",
        "account_type": "institutional_life_insurance_capital_operator",
        "stakeholder_roles": ["data", "operations", "exec"]
      },
      "hypothesis": {
        "statement": "Rule sets should be treated as exportable institutional assets with provenance and version control.",
        "why_true": "Institutional continuity requires transferability and reproducibility across vendors and teams.",
        "why_it_matters": "Exportable rules reduce lock-in risk and accelerate institutionalization."
      },
      "decision_impact": {
        "buying_criteria": ["rules_snapshot", "provenance_export", "version_diffs"],
        "risks": ["knowledge_loss", "vendor_lock_in"],
        "kpis": ["rule_reuse_rate", "rule_change_lead_time"]
      },
      "signals": {
        "telemetry_events": [
          { "event": "rules.table_viewed", "evidence": 1.0, "weight": 0.3, "reason": "Rule object interest" },
          { "event": "export.generated", "evidence": 1.0, "weight": 0.25, "reason": "Rules snapshot export is part of governance exports" }
        ],
        "language_tokens": [
          { "match_any": ["rules snapshot", "version control", "rulebook", "provenance export"], "evidence": 1.0, "weight": 0.2, "token_group": "rules_as_asset" }
        ],
        "negative_signals": []
      },
      "confidence_model": {
        "type": "beta",
        "prior": { "mean": 0.65, "strength": 10 },
        "decay": { "enabled": true, "rate_per_period": 0.05, "period_days": 30, "floor": 0.2, "ceiling": 0.98 }
      },
      "routing_rules": {
        "module_priority": ["C_rules_exceptions", "F_portability_pack"],
        "depth_promote": ["C_rules_exceptions"],
        "message_emphasis": ["rules_as_asset", "portability", "institutional_memory"]
      },
      "governance": { "owner": "data_eng", "review_cadence_days": 90, "notes": "" },
      "created_at": "2026-02-27T00:00:00Z",
      "updated_at": "2026-02-27T00:00:00Z"
    },

    {
      "eo_id": "EO_LH_0011",
      "name": "Committee Decision Friction Requires Artifacts",
      "version": "v1.0",
      "status": "active",
      "scope": {
        "industry": "LS_ecosystem",
        "account_type": "institutional_life_insurance_capital_operator",
        "stakeholder_roles": ["procurement", "compliance", "exec"]
      },
      "hypothesis": {
        "statement": "Committees require cross-functional artifacts to approve; narrative alone fails.",
        "why_true": "Institutional approvals require structured, reviewable evidence packages.",
        "why_it_matters": "LiquiFex must produce committee-ready outputs to compress cycle time."
      },
      "decision_impact": {
        "buying_criteria": ["committee_packet", "audit_exports", "portability_pack"],
        "risks": ["sales_cycle_stall"],
        "kpis": ["committee_approval_rate", "procurement_cycle_time"]
      },
      "signals": {
        "telemetry_events": [
          { "event": "demo.trigger_selected", "evidence": 1.0, "weight": 0.25, "reason": "Committee mandate selection is direct signal" },
          { "event": "portability.viewed", "evidence": 1.0, "weight": 0.25, "reason": "Portability often requested by procurement" }
        ],
        "language_tokens": [
          { "match_any": ["committee", "procurement", "security review", "vendor review"], "evidence": 1.0, "weight": 0.25, "token_group": "committee" }
        ],
        "negative_signals": []
      },
      "confidence_model": {
        "type": "beta",
        "prior": { "mean": 0.65, "strength": 10 },
        "decay": { "enabled": true, "rate_per_period": 0.05, "period_days": 30, "floor": 0.2, "ceiling": 0.98 }
      },
      "routing_rules": {
        "module_priority": ["A_mechanics_audit", "F_portability_pack"],
        "depth_promote": ["A_mechanics_audit", "F_portability_pack"],
        "message_emphasis": ["committee_ready_artifacts", "risk_mitigation", "proof_over_promises"]
      },
      "governance": { "owner": "sales_ops", "review_cadence_days": 60, "notes": "" },
      "created_at": "2026-02-27T00:00:00Z",
      "updated_at": "2026-02-27T00:00:00Z"
    },

    {
      "eo_id": "EO_LH_0012",
      "name": "Variance Quantification Changes Behavior",
      "version": "v1.0",
      "status": "active",
      "scope": {
        "industry": "LS_ecosystem",
        "account_type": "institutional_life_insurance_capital_operator",
        "stakeholder_roles": ["investment", "operations", "risk"]
      },
      "hypothesis": {
        "statement": "Once variance bands are visible, teams change workflows to reduce tail outcomes.",
        "why_true": "Measurement makes hidden drivers actionable and creates governance around variance control.",
        "why_it_matters": "Variance dashboards drive operational alignment and ROI realization."
      },
      "decision_impact": {
        "buying_criteria": ["variance_drivers", "threshold_controls"],
        "risks": ["non_actionable_reporting"],
        "kpis": ["threshold_update_rate", "variance_spread_reduction"]
      },
      "signals": {
        "telemetry_events": [
          { "event": "variance.drivers_viewed", "evidence": 1.0, "weight": 0.45, "reason": "Drivers engagement indicates actionable quant interest" },
          { "event": "threshold.updated", "evidence": 1.0, "weight": 0.5, "reason": "Changing thresholds indicates behavior change intent" }
        ],
        "language_tokens": [
          { "match_any": ["drivers", "root cause", "variance", "band"], "evidence": 1.0, "weight": 0.2, "token_group": "variance_action" }
        ],
        "negative_signals": []
      },
      "confidence_model": {
        "type": "beta",
        "prior": { "mean": 0.7, "strength": 12 },
        "decay": { "enabled": true, "rate_per_period": 0.05, "period_days": 30, "floor": 0.2, "ceiling": 0.98 }
      },
      "routing_rules": {
        "module_priority": ["B_variance_dashboard"],
        "depth_promote": ["B_variance_dashboard"],
        "message_emphasis": ["variance_drivers", "actionability", "control_loop"]
      },
      "governance": { "owner": "product", "review_cadence_days": 60, "notes": "" },
      "created_at": "2026-02-27T00:00:00Z",
      "updated_at": "2026-02-27T00:00:00Z"
    },

    {
      "eo_id": "EO_LH_0013",
      "name": "Human Override Is Mandatory",
      "version": "v1.0",
      "status": "active",
      "scope": {
        "industry": "LS_ecosystem",
        "account_type": "institutional_life_insurance_capital_operator",
        "stakeholder_roles": ["compliance", "operations", "risk", "exec"]
      },
      "hypothesis": {
        "statement": "Full automation is unacceptable; human override and approval governance must exist.",
        "why_true": "Institutions require accountable decision authority and audit trails for overrides.",
        "why_it_matters": "Override governance removes adoption blockers and reduces perceived automation risk."
      },
      "decision_impact": {
        "buying_criteria": ["approval_required_for_override", "override_register"],
        "risks": ["uncontrolled_automation"],
        "kpis": ["override_rate", "override_approval_latency"]
      },
      "signals": {
        "telemetry_events": [
          { "event": "tail_risk.controls_viewed", "evidence": 1.0, "weight": 0.2, "reason": "Override controls live here" },
          { "event": "export.generated", "evidence": 1.0, "weight": 0.25, "reason": "Override register export is part of governance proof" }
        ],
        "language_tokens": [
          { "match_any": ["override", "human in the loop", "approval", "sign-off"], "evidence": 1.0, "weight": 0.25, "token_group": "override" }
        ],
        "negative_signals": []
      },
      "confidence_model": {
        "type": "beta",
        "prior": { "mean": 0.7, "strength": 12 },
        "decay": { "enabled": true, "rate_per_period": 0.05, "period_days": 30, "floor": 0.2, "ceiling": 0.98 }
      },
      "routing_rules": {
        "module_priority": ["A_mechanics_audit", "B_variance_dashboard"],
        "depth_promote": ["A_mechanics_audit"],
        "message_emphasis": ["human_governance", "override_controls", "accountability"]
      },
      "governance": { "owner": "product", "review_cadence_days": 90, "notes": "" },
      "created_at": "2026-02-27T00:00:00Z",
      "updated_at": "2026-02-27T00:00:00Z"
    },

    {
      "eo_id": "EO_LH_0014",
      "name": "Multi-State Complexity Is Underestimated",
      "version": "v1.0",
      "status": "active",
      "scope": {
        "industry": "LS_ecosystem",
        "account_type": "institutional_life_insurance_capital_operator",
        "stakeholder_roles": ["risk", "operations", "legal", "data"]
      },
      "hypothesis": {
        "statement": "State-specific variation is an underestimated driver of delays and exceptions.",
        "why_true": "Jurisdiction rules differ and interact with carrier processes and product types.",
        "why_it_matters": "Modeling state constraints reduces surprises and tail events."
      },
      "decision_impact": {
        "buying_criteria": ["jurisdiction_applicability", "state_filters", "rules_versioning"],
        "risks": ["regulatory_mismatch", "unexpected_delays"],
        "kpis": ["state_specific_exception_rate", "state_filtered_p90"]
      },
      "signals": {
        "telemetry_events": [
          { "event": "filter.changed", "evidence": 1.0, "weight": 0.2, "reason": "State filter usage indicates state sensitivity" }
        ],
        "language_tokens": [
          { "match_any": ["state-specific", "jurisdiction", "NY regulation", "CA requirement"], "evidence": 1.0, "weight": 0.25, "token_group": "jurisdiction" }
        ],
        "negative_signals": []
      },
      "confidence_model": {
        "type": "beta",
        "prior": { "mean": 0.6, "strength": 10 },
        "decay": { "enabled": true, "rate_per_period": 0.05, "period_days": 30, "floor": 0.2, "ceiling": 0.98 }
      },
      "routing_rules": {
        "module_priority": ["C_rules_exceptions", "B_variance_dashboard"],
        "depth_promote": ["C_rules_exceptions"],
        "message_emphasis": ["jurisdiction_modeling", "predictability", "compliance_alignment"]
      },
      "governance": { "owner": "solutions_eng", "review_cadence_days": 90, "notes": "" },
      "created_at": "2026-02-27T00:00:00Z",
      "updated_at": "2026-02-27T00:00:00Z"
    },

    {
      "eo_id": "EO_LH_0015",
      "name": "Liquidity Infrastructure Is Under-Institutionalized",
      "version": "v1.0",
      "status": "active",
      "scope": {
        "industry": "LS_ecosystem",
        "account_type": "institutional_life_insurance_capital_operator",
        "stakeholder_roles": ["exec", "investment", "operations"]
      },
      "hypothesis": {
        "statement": "Liquidity workflows lack formal infrastructure; institutionalization is required to scale.",
        "why_true": "The LS ecosystem remains fragmented across carriers, documents, spreadsheets, and bespoke processes.",
        "why_it_matters": "LiquiFex positions as control-plane infrastructure, not a point tool."
      },
      "decision_impact": {
        "buying_criteria": ["end_to_end_control_plane", "auditability", "rules_exceptions_infra"],
        "risks": ["fragmentation_drag"],
        "kpis": ["portfolio_scale_supported", "process_standardization_index"]
      },
      "signals": {
        "telemetry_events": [
          { "event": "pilot.plan_viewed", "evidence": 1.0, "weight": 0.25, "reason": "Pilot blueprint implies infrastructure framing" },
          { "event": "module.viewed", "evidence": 1.0, "weight": 0.15, "reason": "Broad module engagement signals infra interest" }
        ],
        "language_tokens": [
          { "match_any": ["infrastructure", "control plane", "institutionalize", "system of record"], "evidence": 1.0, "weight": 0.2, "token_group": "infra" }
        ],
        "negative_signals": []
      },
      "confidence_model": {
        "type": "beta",
        "prior": { "mean": 0.6, "strength": 10 },
        "decay": { "enabled": true, "rate_per_period": 0.05, "period_days": 30, "floor": 0.2, "ceiling": 0.98 }
      },
      "routing_rules": {
        "module_priority": ["A_mechanics_audit", "B_variance_dashboard", "C_rules_exceptions"],
        "depth_promote": ["A_mechanics_audit", "C_rules_exceptions"],
        "message_emphasis": ["control_plane", "institutionalization", "scale"]
      },
      "governance": { "owner": "exec_sponsor", "review_cadence_days": 120, "notes": "" },
      "created_at": "2026-02-27T00:00:00Z",
      "updated_at": "2026-02-27T00:00:00Z"
    }
  ]
}
```

* * *

Implementation notes (so this schema is immediately usable)
-----------------------------------------------------------

*   **EO ids**: stable keys used by confidence store + router
*   **signals.telemetry\_events**: directly maps to your server-side `confidenceTriggers(event)` table
*   **signals.language\_tokens**: maps to your front-end `language_token_rules`
*   **routing\_rules**: lets you automatically reweight or reorder modules when EO mean crosses a threshold (e.g., mean > 0.75)

If you want, I can also output:

*   a **compiled router table** generated from the EO catalog (so EO definitions become the single source of truth), and
*   a **code generator** that exports `confidenceTriggers()` and `language_token_rules` automatically from this EO catalog JSON.

## Prompt:
a compiled router table generated from the EO catalog (so EO definitions become the single source of truth), and

a code generator that exports confidenceTriggers() and language_token_rules automatically from this EO catalog JSON.

## Response:
1) Compiled router table (generated from EO catalog)
----------------------------------------------------

### Output shape: `router.generated.json`

This is the **single source of truth** router artifact your demo can load. It’s derived from each EO’s:

*   `routing_rules.module_priority`
*   `routing_rules.depth_promote`
*   `signals.language_tokens[]`

It produces:

*   **EO-based routing policy** (when EO confidence crosses thresholds)
*   **language token rules** (front-of-queue inserts and telemetry tags)

Example (what the compiler emits):

```
{
  "schema_version": "liquifex.router_table.v1",
  "generated_at": "2026-02-27T00:00:00Z",
  "account": "Lifehouse Capital",
  "defaults": {
    "always_include": ["A_mechanics_audit", "G_pilot_blueprint"],
    "pilot_module": "G_pilot_blueprint",
    "thresholds": {
      "routing_apply_at_mean_gte": 0.75,
      "depth_promote_at_mean_gte": 0.80
    }
  },
  "eo_routing": [
    {
      "eo_id": "EO_LH_0001",
      "apply_if": { "mean_gte": 0.75 },
      "then": {
        "add_front": ["A_mechanics_audit", "F_portability_pack"],
        "depth_promote": ["A_mechanics_audit"],
        "message_emphasis": ["auditability_first", "provenance", "reproducibility"]
      }
    },
    {
      "eo_id": "EO_LH_0002",
      "apply_if": { "mean_gte": 0.75 },
      "then": {
        "add_front": ["B_variance_dashboard"],
        "depth_promote": ["B_variance_dashboard"],
        "message_emphasis": ["variance_over_average", "tail_containment", "predictability"]
      }
    }
  ],
  "language_token_rules": [
    {
      "rule_id": "tokens.mechanics_audit",
      "match_any": ["audit", "governance", "defensible", "compliance", "mechanics", "explain", "black box", "how does it decide"],
      "then_add_front": ["A_mechanics_audit"],
      "telemetry": { "event": "token.triggered", "token_group": "mechanics_audit" }
    },
    {
      "rule_id": "tokens.dependency_exit",
      "match_any": ["lock-in", "dependency", "exit", "offboarding"],
      "then_add_front": ["F_portability_pack"],
      "telemetry": { "event": "token.triggered", "token_group": "dependency_exit" }
    }
  ]
}
```

How to use it:

*   Load this router table into the front-end config loader.
*   After each telemetry batch (or at session start), fetch current EO confidence means from backend and apply `eo_routing` rules to your plan.

* * *

2) Code generator (from EO catalog JSON → confidenceTriggers() + language\_token\_rules)
----------------------------------------------------------------------------------------

### Inputs / Outputs

**Input**

*   `eo_catalog.json` (the catalog you already have: `{ catalog_id, account, eos: [...] }`)

**Outputs**

*   `router.generated.json` (compiled router table)
*   `confidenceTriggers.generated.js` (server-side event→EO evidence map)
*   `languageTokenRules.generated.js` (front-end token rules)

* * *

A) Generator script: `generate-from-eos.mjs`
============================================

```
import fs from "fs";
import path from "path";

function readJson(p) {
  return JSON.parse(fs.readFileSync(p, "utf8"));
}
function writeJson(p, obj) {
  fs.mkdirSync(path.dirname(p), { recursive: true });
  fs.writeFileSync(p, JSON.stringify(obj, null, 2), "utf8");
}
function writeText(p, text) {
  fs.mkdirSync(path.dirname(p), { recursive: true });
  fs.writeFileSync(p, text, "utf8");
}
function uniq(arr) {
  return Array.from(new Set(arr.filter(Boolean)));
}

function compileLanguageTokenRules(eos) {
  // Merge by token_group, union tokens, choose module priority union as front inserts
  const byGroup = new Map();

  for (const eo of eos) {
    const lt = eo?.signals?.language_tokens || [];
    for (const rule of lt) {
      const group = rule.token_group || "unknown";
      if (!byGroup.has(group)) {
        byGroup.set(group, { token_group: group, tokens: [], front: [], telemetry_event: "token.triggered" });
      }
      const entry = byGroup.get(group);
      entry.tokens.push(...(rule.match_any || []));
      entry.front.push(...(eo?.routing_rules?.module_priority || []));
    }
  }

  const out = [];
  for (const [group, v] of byGroup.entries()) {
    out.push({
      rule_id: `tokens.${group}`,
      match_any: uniq(v.tokens.map(t => String(t).toLowerCase())),
      then_add_front: uniq(v.front),
      telemetry: { event: v.telemetry_event, token_group: group }
    });
  }
  return out;
}

function compileRouterTable(catalog, opts = {}) {
  const eos = catalog.eos || [];
  const account = catalog.account || "unknown";

  const routing_apply_at = opts.routing_apply_at ?? 0.75;
  const depth_apply_at = opts.depth_promote_at ?? 0.80;

  const eo_routing = eos.map(eo => ({
    eo_id: eo.eo_id,
    apply_if: { mean_gte: routing_apply_at },
    then: {
      add_front: uniq(eo?.routing_rules?.module_priority || []),
      depth_promote: uniq(eo?.routing_rules?.depth_promote || []),
      message_emphasis: uniq(eo?.routing_rules?.message_emphasis || [])
    }
  }));

  return {
    schema_version: "liquifex.router_table.v1",
    generated_at: new Date().toISOString(),
    account,
    defaults: {
      always_include: ["A_mechanics_audit", "G_pilot_blueprint"],
      pilot_module: "G_pilot_blueprint",
      thresholds: {
        routing_apply_at_mean_gte: routing_apply_at,
        depth_promote_at_mean_gte: depth_apply_at
      }
    },
    eo_routing,
    language_token_rules: compileLanguageTokenRules(eos)
  };
}

function compileConfidenceTriggers(eos) {
  // Build event -> [ {eo,evidence,weight,reason} ... ] from signals.telemetry_events
  const map = new Map();

  for (const eo of eos) {
    const te = eo?.signals?.telemetry_events || [];
    for (const s of te) {
      const event = s.event;
      if (!event) continue;
      if (!map.has(event)) map.set(event, []);
      map.get(event).push({
        eo: eo.eo_id,
        evidence: s.evidence,
        weight: s.weight,
        reason: s.reason
      });
    }

    // Optional: negative signals telemetry_event -> evidence 0-ish
    const neg = eo?.signals?.negative_signals || [];
    for (const n of neg) {
      if (n.kind !== "telemetry_event") continue;
      const event = n.match;
      if (!event) continue;
      if (!map.has(event)) map.set(event, []);
      map.get(event).push({
        eo: eo.eo_id,
        evidence: n.evidence,
        weight: n.weight,
        reason: n.reason
      });
    }
  }

  // emit JS module
  const entries = Array.from(map.entries()).sort(([a],[b]) => a.localeCompare(b));
  return `// AUTO-GENERATED. Do not edit by hand.
// Source: EO catalog -> signals.telemetry_events (+negative telemetry signals)

export function confidenceTriggers(event) {
  const e = event?.event;
  if (!e) return [];
  switch (e) {
${entries.map(([eventName, updates]) => {
  const body = updates.map(u => `      { eo: ${JSON.stringify(u.eo)}, evidence: ${u.evidence}, weight: ${u.weight}, reason: ${JSON.stringify(u.reason)} },`).join("\n");
  return `    case ${JSON.stringify(eventName)}:\n      return [\n${body}\n      ];`;
}).join("\n\n")}
    default:
      return [];
  }
}
`;
}

function compileLanguageTokenRulesModule(routerTable) {
  const rules = routerTable.language_token_rules || [];
  return `// AUTO-GENERATED. Do not edit by hand.
// Source: EO catalog -> signals.language_tokens + routing_rules.module_priority

export const language_token_rules = ${JSON.stringify(rules, null, 2)};
`;
}

// -------- main --------
const catalogPath = process.argv[2] || "./eo_catalog.json";
const outDir = process.argv[3] || "./generated";

const catalog = readJson(catalogPath);
const eos = catalog.eos || [];

const routerTable = compileRouterTable(catalog, {
  routing_apply_at: 0.75,
  depth_promote_at: 0.80
});

writeJson(path.join(outDir, "router.generated.json"), routerTable);
writeText(path.join(outDir, "confidenceTriggers.generated.js"), compileConfidenceTriggers(eos));
writeText(path.join(outDir, "languageTokenRules.generated.js"), compileLanguageTokenRulesModule(routerTable));

console.log("Generated:");
console.log(" -", path.join(outDir, "router.generated.json"));
console.log(" -", path.join(outDir, "confidenceTriggers.generated.js"));
console.log(" -", path.join(outDir, "languageTokenRules.generated.js"));
```

* * *

B) Run the generator
====================

```
node generate-from-eos.mjs ./eo_catalog.json ./generated
```

You’ll get:

```
generated/router.generated.json
generated/confidenceTriggers.generated.js
generated/languageTokenRules.generated.js
```

* * *

3) Integration points
---------------------

### Server-side (confidence updater)

In your `confidence.js`, replace the handwritten trigger map with the generated one:

```
import { confidenceTriggers } from "./generated/confidenceTriggers.generated.js";
```

…and delete the manual `confidenceTriggers()` implementation.

### Front-end (token routing)

In your React config, replace `router.language_token_rules` with the generated list:

```
import { language_token_rules } from "./generated/languageTokenRules.generated.js";
```

Then use that array inside your `applyLanguageTokenRules()` logic.

### EO-based routing (confidence-driven)

Add a step that fetches account confidence and applies router table EO rules:

*   call backend `GET /confidence/<account>`
*   for each `eo_routing[]`, if `confidence.scores[eo_id].mean >= threshold`, apply:
    *   `add_front` to `module_order`
    *   `depth_promote` union into `depth_promote`

This makes EO definitions the authoritative router policy.

* * *

Optional (but high leverage)
----------------------------

If you want **true single-source-of-truth**, extend the generator to also emit:

*   `modules.generated.json` (module wiring per EO)
*   `message_emphasis.generated.json` (talk-track selection per EO)

Say “generate message emphasis artifacts too” and I’ll add that to the generator with the exact output format.

## Prompt:
modules.generated.json (module wiring per EO +
generate message emphasis artifacts too, with the goal of creating a self healing system based on the capabilities created by utilizing recursive logic and adding the ability to learn or search for information required to make a better decision

## Response:
1) `modules.generated.json` + message emphasis artifacts (single source of truth)
---------------------------------------------------------------------------------

You want the EO catalog to compile into **three runtime artifacts**:

1.  `router.generated.json`
2.  `modules.generated.json` (module wiring per EO + per-screen instrumentation)
3.  `messaging.generated.json` (message emphasis per EO + talk-track blocks)

Then runtime does:

*   observe telemetry → update EO confidence
*   recompute module plan + messaging emphasis
*   identify uncertainty gaps → ask 1 follow-up or queue a “research/search” task

This is the spine of a self-healing demo / sales system.

* * *

2) Output specs
===============

A) `modules.generated.json` (module wiring per EO)
--------------------------------------------------

Purpose: make modules, screens, and instrumentation **driven by EO definitions**, not hardcoded.

```
{
  "schema_version": "liquifex.modules_table.v1",
  "generated_at": "2026-02-27T00:00:00Z",
  "account": "Lifehouse Capital",
  "modules": {
    "A_mechanics_audit": {
      "id": "A_mechanics_audit",
      "title": "Mechanics + Audit Trail",
      "screens": ["A1_workflow_map", "A2_case_overview", "A3_decision_path", "A4_provenance_ledger", "A5_audit_export"],
      "emits": ["screen.enter", "export.generated", "export.previewed"]
    },
    "B_variance_dashboard": {
      "id": "B_variance_dashboard",
      "title": "Variance Dashboard",
      "screens": ["B1_p50_p90", "B2_drivers", "B3_tail_controls"],
      "emits": ["screen.enter", "filter.changed", "variance.drivers_viewed", "tail_risk.controls_viewed"]
    }
  },
  "eo_module_wiring": [
    {
      "eo_id": "EO_LH_0001",
      "primary_modules": ["A_mechanics_audit", "F_portability_pack"],
      "secondary_modules": ["C_rules_exceptions"],
      "depth_promote": ["A_mechanics_audit"]
    }
  ],
  "screen_instrumentation": [
    {
      "screen_id": "A5_audit_export",
      "module_id": "A_mechanics_audit",
      "default_events": [
        { "event": "export.generated", "metadata_template": { "export_type": "event_log_json" } }
      ]
    }
  ]
}
```

B) `messaging.generated.json` (talk track blocks)
-------------------------------------------------

Purpose: let the system automatically select _what to say_ based on EO confidence.

```
{
  "schema_version": "liquifex.messaging_table.v1",
  "generated_at": "2026-02-27T00:00:00Z",
  "account": "Lifehouse Capital",
  "message_blocks": {
    "auditability_first": {
      "title": "Auditability is the adoption gate",
      "one_liner": "We make every decision reproducible and exportable as an audit packet.",
      "proof_points": ["rules snapshot export", "provenance ledger", "override register"],
      "cta": "Let’s generate the committee packet for one workflow in 60 days."
    },
    "variance_over_average": {
      "title": "Variance is the real risk",
      "one_liner": "P90 is what traps capital; we reduce tail outcomes by making drivers visible and controllable.",
      "proof_points": ["P50/P90 bands", "variance drivers", "tail controls"],
      "cta": "Pick 3 variance drivers to attack in the pilot."
    }
  },
  "eo_message_emphasis": [
    {
      "eo_id": "EO_LH_0002",
      "emphasize": ["variance_over_average", "tail_containment", "predictability"],
      "deemphasize": []
    }
  ]
}
```

* * *

3) “Self-healing” layer: recursive decision logic
=================================================

You get self-healing by adding **uncertainty resolution**:

### Runtime signals

*   EO confidence below threshold on critical EO’s
*   conflicting EO evidence (some events push up, others push down)
*   missing data needed to choose modules or claims

### System response loop (recursive)

1.  compute current best plan
2.  detect uncertainty gaps
3.  **ask 1 high-yield question** OR queue an automated research task
4.  update EO confidence / plan
5.  repeat

This is where “learn or search for information” belongs.

* * *

4) Update the generator to emit both artifacts
==============================================

Add these functions to your `generate-from-eos.mjs` (in addition to what you already have).

A) `modules.generated.json` compiler
------------------------------------

```
function compileModulesGenerated(catalog) {
  const eos = catalog.eos || [];
  const account = catalog.account || "unknown";

  // Baseline module definitions for the demo (can be moved to its own registry JSON)
  const modules = {
    A_mechanics_audit: {
      id: "A_mechanics_audit",
      title: "Mechanics + Audit Trail",
      screens: ["A1_workflow_map", "A2_case_overview", "A3_decision_path", "A4_provenance_ledger", "A5_audit_export"],
      emits: ["screen.enter", "export.generated", "export.previewed"]
    },
    B_variance_dashboard: {
      id: "B_variance_dashboard",
      title: "Variance Dashboard",
      screens: ["B1_p50_p90", "B2_drivers", "B3_tail_controls"],
      emits: ["screen.enter", "filter.changed", "variance.drivers_viewed", "tail_risk.controls_viewed"]
    },
    C_rules_exceptions: {
      id: "C_rules_exceptions",
      title: "Rules + Exceptions",
      screens: ["C1_rules_objects", "C2_exceptions_model", "C3_versioning"],
      emits: ["screen.enter", "rules.table_viewed", "exceptions.model_viewed", "versioning.viewed"]
    },
    D_artefact_pipeline: {
      id: "D_artefact_pipeline",
      title: "Artefact Pipeline",
      screens: ["D1_ingestion", "D2_review_queue"],
      emits: ["screen.enter", "artefact.ingestion_viewed", "review.queue_viewed"]
    },
    E_spreadsheet_migration: {
      id: "E_spreadsheet_migration",
      title: "Spreadsheet Migration",
      screens: ["E1_import_map", "E2_dualrun_exit"],
      emits: ["screen.enter", "spreadsheet.mapper_viewed", "dualrun.checklist_viewed"]
    },
    F_portability_pack: {
      id: "F_portability_pack",
      title: "Portability Pack",
      screens: ["F1_portability"],
      emits: ["screen.enter", "portability.viewed"]
    },
    G_pilot_blueprint: {
      id: "G_pilot_blueprint",
      title: "60-Day Pilot Blueprint",
      screens: ["G1_choose_workflow", "G2_choose_metrics", "G3_timeline"],
      emits: ["screen.enter", "pilot.workflow_selected", "pilot.metrics_selected", "pilot.plan_viewed"]
    }
  };

  // Wire EO -> modules based on routing_rules
  const eo_module_wiring = eos.map((eo) => {
    const pri = uniq(eo?.routing_rules?.module_priority || []);
    const depth = uniq(eo?.routing_rules?.depth_promote || []);

    // Heuristic: secondary modules inferred from evidence signals (optional)
    const secondary = [];
    const tele = eo?.signals?.telemetry_events || [];
    for (const t of tele) {
      if (String(t.event).includes("rules") || String(t.event).includes("exceptions")) secondary.push("C_rules_exceptions");
      if (String(t.event).includes("spreadsheet")) secondary.push("E_spreadsheet_migration");
      if (String(t.event).includes("portability")) secondary.push("F_portability_pack");
      if (String(t.event).includes("variance") || String(t.event).includes("tail_risk")) secondary.push("B_variance_dashboard");
    }

    return {
      eo_id: eo.eo_id,
      primary_modules: pri,
      secondary_modules: uniq(secondary.filter(m => !pri.includes(m))),
      depth_promote: depth
    };
  });

  // Screen instrumentation (optional: can be generated from module emits)
  const screen_instrumentation = [];
  for (const m of Object.values(modules)) {
    for (const sid of m.screens) {
      screen_instrumentation.push({
        screen_id: sid,
        module_id: m.id,
        default_events: [{ event: "screen.enter" }]
      });
    }
  }

  return {
    schema_version: "liquifex.modules_table.v1",
    generated_at: new Date().toISOString(),
    account,
    modules,
    eo_module_wiring,
    screen_instrumentation
  };
}
```

B) `messaging.generated.json` compiler
--------------------------------------

```
function compileMessagingGenerated(catalog) {
  const eos = catalog.eos || [];
  const account = catalog.account || "unknown";

  // Baseline message blocks; expand over time
  const message_blocks = {
    auditability_first: {
      title: "Auditability is the adoption gate",
      one_liner: "Every decision is reproducible and exportable as a committee-ready audit packet.",
      proof_points: ["rules snapshot export", "provenance ledger", "override register"],
      cta: "Generate an audit packet for one workflow in the pilot."
    },
    provenance: {
      title: "Provenance and versioning",
      one_liner: "We show exactly what rule fired, why, and what changed over time.",
      proof_points: ["version diffs", "evidence index", "decision path"],
      cta: "Review one ruleset change end-to-end."
    },
    variance_over_average: {
      title: "Variance is the real risk",
      one_liner: "P90 is what traps capital; we make variance measurable and controllable.",
      proof_points: ["P50/P90 bands", "drivers", "tail controls"],
      cta: "Pick 3 drivers to attack."
    },
    portability: {
      title: "Portability reduces institutional risk",
      one_liner: "You can export rules, evidence, and audit logs—reducing vendor dependency.",
      proof_points: ["portability pack", "offboarding playbook", "export specs"],
      cta: "Review the offboarding playbook."
    },
    rules_as_infrastructure: {
      title: "Rules + exceptions are infrastructure",
      one_liner: "Carrier and state variation is structural—so rules must be first-class objects.",
      proof_points: ["exceptions model", "rules registry", "version control"],
      cta: "Map one carrier rule change into version control."
    },
    control_plane: {
      title: "LiquiFex as a control plane",
      one_liner: "Not a point tool—an institutional workflow control plane for liquidity operations.",
      proof_points: ["end-to-end workflow", "audit exports", "variance control loop"],
      cta: "Align on a 60-day control-plane pilot."
    }
  };

  const eo_message_emphasis = eos.map((eo) => ({
    eo_id: eo.eo_id,
    emphasize: uniq(eo?.routing_rules?.message_emphasis || []),
    deemphasize: []
  }));

  return {
    schema_version: "liquifex.messaging_table.v1",
    generated_at: new Date().toISOString(),
    account,
    message_blocks,
    eo_message_emphasis
  };
}
```

C) Emit both artifacts in `main`
--------------------------------

Add to the bottom of `generate-from-eos.mjs`:

```
const modulesGen = compileModulesGenerated(catalog);
const messagingGen = compileMessagingGenerated(catalog);

writeJson(path.join(outDir, "modules.generated.json"), modulesGen);
writeJson(path.join(outDir, "messaging.generated.json"), messagingGen);

console.log(" -", path.join(outDir, "modules.generated.json"));
console.log(" -", path.join(outDir, "messaging.generated.json"));
```

* * *

5) Runtime “self-healing” decision loop (what to implement next)
================================================================

A) Confidence → EO activation
-----------------------------

You already store Beta means per EO. Add an “activation” step:

*   active if mean ≥ 0.75
*   “uncertain” if 0.55 ≤ mean < 0.75
*   “unlikely” if mean < 0.55

B) Plan recompute (recursive)
-----------------------------

Each time an event comes in:

1.  update confidence
2.  recompute module plan from `router.generated.json` + `modules.generated.json`
3.  compute messaging emphasis from `messaging.generated.json`
4.  identify uncertainty gaps

C) Uncertainty gap detector
---------------------------

A simple first pass:

*   if **no EO mean ≥ 0.75** among top 5 EOs by weight → ask 1 follow-up
*   if **conflicting EOs** (one pushes audit-first, another pushes variance-first) → ask tie-break question
*   if demo claims require missing info (e.g., “P90 reduction ROI” requires current baseline) → generate “info request” task

D) “Learn or search” plug-in
----------------------------

For now, make it explicit and auditable:

*   a `research_queue.jsonl` written by the server when a gap is detected:
    *   `{"type":"info_request","question":"What is your current median TTL?","reason":"needed_for_roi_calc",...}`
    *   later can be replaced with a web/search connector or internal doc search, but you keep the interface stable.

This is the correct pattern for self-healing: **detect → request/learn → update**.

* * *

6) Minimal integration points (front-end)
=========================================

*   Load `modules.generated.json` and `messaging.generated.json` alongside the router table.
*   Render a “Talk Track” panel:
    *   pick top 3 emphasized blocks based on active EO means
*   When uncertain:
    *   show “1 follow-up question” UI driven by research queue (next layer)

* * *

If you want, I can also add:

*   a `questions.generated.json` artifact (1 follow-up question per EO + tie-break questions)
*   a runtime function `selectNextQuestion(confidence, eo_catalog)` that drives the self-healing loop without manual logic.

## Prompt:
both a questions.generated.json artifact (1 follow-up question per EO + tie-break questions)

a runtime function selectNextQuestion(confidence, eo_catalog) that drives the self-healing loop without manual logic.

## Response:
1) `questions.generated.json` artifact
--------------------------------------

### Purpose

A machine-readable question bank that supports:

*   **1 follow-up question per EO** (high-yield, single-shot)
*   **tie-break questions** when multiple EOs compete
*   mapping from answers → **evidence updates** (EO + evidence + weight)
*   optional fields to drive UI inputs (multiple choice, numeric, free text)

### Output shape

```
{
  "schema_version": "liquifex.questions_table.v1",
  "generated_at": "2026-02-27T00:00:00Z",
  "account": "Lifehouse Capital",
  "defaults": {
    "min_eo_mean_for_no_question": 0.75,
    "uncertainty_band": { "low": 0.55, "high": 0.75 },
    "max_questions_per_session": 6
  },
  "eo_questions": [
    {
      "eo_id": "EO_LH_0001",
      "question_id": "Q_EO_LH_0001_v1",
      "priority": 95,
      "question": "What is the minimum audit artifact your committee requires before approving a pilot (event log, decision path, rules snapshot, override register)?",
      "input_type": "multi_select",
      "options": ["event_log", "decision_path", "rules_snapshot", "override_register", "other"],
      "answer_to_evidence": [
        {
          "when": { "includes_any": ["event_log", "rules_snapshot", "override_register", "decision_path"] },
          "updates": [{ "eo_id": "EO_LH_0001", "evidence": 1.0, "weight": 1.2, "reason": "Committee requires audit artifacts" }]
        }
      ]
    }
  ],
  "tie_breakers": [
    {
      "tie_break_id": "TB_AUDIT_vs_VARIANCE_v1",
      "between_eos": ["EO_LH_0001", "EO_LH_0002", "EO_LH_0012"],
      "priority": 90,
      "question": "In a pilot decision, what blocks approval more often: (A) audit defensibility or (B) variance/tail-risk control?",
      "input_type": "single_select",
      "options": ["audit_defensibility", "variance_tail_risk", "both_equal"],
      "answer_to_evidence": [
        {
          "when": { "equals": "audit_defensibility" },
          "updates": [{ "eo_id": "EO_LH_0001", "evidence": 1.0, "weight": 1.4, "reason": "Audit is primary gate" }]
        },
        {
          "when": { "equals": "variance_tail_risk" },
          "updates": [
            { "eo_id": "EO_LH_0002", "evidence": 1.0, "weight": 1.2, "reason": "Tail risk dominates" },
            { "eo_id": "EO_LH_0012", "evidence": 1.0, "weight": 0.8, "reason": "Variance quant drives behavior" }
          ]
        },
        {
          "when": { "equals": "both_equal" },
          "updates": [
            { "eo_id": "EO_LH_0001", "evidence": 1.0, "weight": 0.8, "reason": "Audit is a gate" },
            { "eo_id": "EO_LH_0002", "evidence": 1.0, "weight": 0.8, "reason": "Tail risk is a gate" }
          ]
        }
      ]
    }
  ]
}
```

* * *

2) Generator additions: compile EO questions + tie-breakers
-----------------------------------------------------------

Add these functions to `generate-from-eos.mjs`.

### A) EO follow-up question compiler

This generates one question per EO using a policy table (editable) keyed by common EO “themes”.

```
function compileQuestionsGenerated(catalog, routerTable) {
  const eos = catalog.eos || [];
  const account = catalog.account || "unknown";

  // Theme inference from routing emphasis + tokens (deterministic, auditable)
  function inferTheme(eo) {
    const emph = (eo?.routing_rules?.message_emphasis || []).join(" ").toLowerCase();
    const tokens = (eo?.signals?.language_tokens || []).flatMap(t => t.match_any || []).join(" ").toLowerCase();

    const t = `${emph} ${tokens}`;
    if (t.includes("audit") || t.includes("governance") || t.includes("provenance")) return "audit_governance";
    if (t.includes("variance") || t.includes("p90") || t.includes("tail")) return "variance_tail";
    if (t.includes("lock") || t.includes("dependency") || t.includes("exit") || t.includes("offboarding")) return "portability";
    if (t.includes("spreadsheet") || t.includes("excel") || t.includes("dual")) return "spreadsheet";
    if (t.includes("rules") || t.includes("exceptions") || t.includes("carrier")) return "rules_exceptions";
    if (t.includes("committee") || t.includes("procurement") || t.includes("security")) return "committee";
    if (t.includes("override") || t.includes("human")) return "human_override";
    if (t.includes("jurisdiction") || t.includes("state")) return "jurisdiction";
    if (t.includes("control plane") || t.includes("infrastructure")) return "infrastructure";
    return "general";
  }

  // Question templates per theme (single best follow-up)
  const themeQuestions = {
    audit_governance: (eo) => ({
      question: "What is the minimum audit artifact your committee requires before approving a pilot (event log, decision path, rules snapshot, override register)?",
      input_type: "multi_select",
      options: ["event_log", "decision_path", "rules_snapshot", "override_register", "other"],
      answer_to_evidence: [
        {
          when: { includes_any: ["event_log", "decision_path", "rules_snapshot", "override_register"] },
          updates: [{ eo_id: eo.eo_id, evidence: 1.0, weight: 1.2, reason: "Committee requires audit artifacts" }]
        }
      ]
    }),
    variance_tail: (eo) => ({
      question: "Which metric is more important to improve in a pilot: P90 time-to-liquidity, P50 time-to-liquidity, or exception rate?",
      input_type: "single_select",
      options: ["p90_ttl", "p50_ttl", "exception_rate"],
      answer_to_evidence: [
        { when: { equals: "p90_ttl" }, updates: [{ eo_id: eo.eo_id, evidence: 1.0, weight: 1.2, reason: "Tail outcome priority" }] },
        { when: { equals: "p50_ttl" }, updates: [{ eo_id: eo.eo_id, evidence: 0.6, weight: 0.8, reason: "Median efficiency focus" }] },
        { when: { equals: "exception_rate" }, updates: [{ eo_id: eo.eo_id, evidence: 0.8, weight: 1.0, reason: "Exceptions as variance driver" }] }
      ]
    }),
    portability: (eo) => ({
      question: "Is offboarding/portability a hard requirement (must-have) or a risk mitigator (nice-to-have)?",
      input_type: "single_select",
      options: ["must_have", "nice_to_have"],
      answer_to_evidence: [
        { when: { equals: "must_have" }, updates: [{ eo_id: eo.eo_id, evidence: 1.0, weight: 1.3, reason: "Portability is a gate" }] },
        { when: { equals: "nice_to_have" }, updates: [{ eo_id: eo.eo_id, evidence: 0.6, weight: 0.7, reason: "Portability is secondary" }] }
      ]
    }),
    spreadsheet: (eo) => ({
      question: "Where does the system-of-record live today for tracking cases: spreadsheet, CRM, or internal tool?",
      input_type: "single_select",
      options: ["spreadsheet", "crm", "internal_tool", "other"],
      answer_to_evidence: [
        { when: { equals: "spreadsheet" }, updates: [{ eo_id: eo.eo_id, evidence: 1.0, weight: 1.2, reason: "Spreadsheet is the control plane" }] }
      ]
    }),
    rules_exceptions: (eo) => ({
      question: "What causes more delays: carrier rule differences, missing evidence, or internal approvals?",
      input_type: "single_select",
      options: ["carrier_rule_differences", "missing_evidence", "internal_approvals", "unknown"],
      answer_to_evidence: [
        { when: { equals: "carrier_rule_differences" }, updates: [{ eo_id: eo.eo_id, evidence: 1.0, weight: 1.1, reason: "Carrier divergence is structural" }] },
        { when: { equals: "missing_evidence" }, updates: [{ eo_id: eo.eo_id, evidence: 0.8, weight: 0.9, reason: "Evidence completeness drives exceptions" }] }
      ]
    }),
    committee: (eo) => ({
      question: "Who is the hardest approver in the buying process: compliance, procurement, or investment committee?",
      input_type: "single_select",
      options: ["compliance", "procurement", "investment_committee", "other"],
      answer_to_evidence: [
        { when: { includes_any: ["compliance", "procurement", "investment_committee"] }, updates: [{ eo_id: eo.eo_id, evidence: 1.0, weight: 1.0, reason: "Committee friction is material" }] }
      ]
    }),
    human_override: (eo) => ({
      question: "Do you require explicit human approval before any override/action is applied?",
      input_type: "single_select",
      options: ["yes_required", "sometimes", "no"],
      answer_to_evidence: [
        { when: { equals: "yes_required" }, updates: [{ eo_id: eo.eo_id, evidence: 1.0, weight: 1.2, reason: "Human override governance required" }] },
        { when: { equals: "no" }, updates: [{ eo_id: eo.eo_id, evidence: 0.2, weight: 0.8, reason: "Override governance less critical" }] }
      ]
    }),
    jurisdiction: (eo) => ({
      question: "Do state/jurisdiction differences materially change your workflow (often) or only in edge cases (rarely)?",
      input_type: "single_select",
      options: ["often", "rarely", "unknown"],
      answer_to_evidence: [
        { when: { equals: "often" }, updates: [{ eo_id: eo.eo_id, evidence: 1.0, weight: 1.1, reason: "Jurisdiction is a major driver" }] }
      ]
    }),
    infrastructure: (eo) => ({
      question: "Are you buying a point solution for a step, or a control-plane you can standardize across workflows?",
      input_type: "single_select",
      options: ["point_solution", "control_plane", "unsure"],
      answer_to_evidence: [
        { when: { equals: "control_plane" }, updates: [{ eo_id: eo.eo_id, evidence: 1.0, weight: 1.0, reason: "Infrastructure framing" }] }
      ]
    }),
    general: (eo) => ({
      question: "If LiquiFex only improved one thing in 60 days, what should it be?",
      input_type: "free_text",
      options: [],
      answer_to_evidence: [
        { when: { any: true }, updates: [{ eo_id: eo.eo_id, evidence: 0.6, weight: 0.4, reason: "General signal captured; needs interpretation" }] }
      ]
    })
  };

  const eo_questions = eos.map((eo, i) => {
    const theme = inferTheme(eo);
    const q = themeQuestions[theme](eo);
    return {
      eo_id: eo.eo_id,
      question_id: `Q_${eo.eo_id}_v1`,
      priority: 80 - i, // stable ordering; override per EO if desired
      theme,
      ...q
    };
  });

  // Tie-breaks: generate for the most common conflicts (deterministic)
  const tie_breakers = compileTieBreakersFromRouter(routerTable, eos);

  return {
    schema_version: "liquifex.questions_table.v1",
    generated_at: new Date().toISOString(),
    account,
    defaults: {
      min_eo_mean_for_no_question: 0.75,
      uncertainty_band: { low: 0.55, high: 0.75 },
      max_questions_per_session: 6
    },
    eo_questions,
    tie_breakers
  };
}
```

### B) Tie-break compiler (EO conflicts → one question)

This is rule-based: conflicts appear when EOs push different “first modules” (audit vs variance vs portability).

```
function compileTieBreakersFromRouter(routerTable, eos) {
  const eoRouting = routerTable?.eo_routing || [];

  // Identify “primary first modules” per EO
  const firsts = new Map(); // eo_id -> first module
  for (const r of eoRouting) {
    const eoId = r.eo_id;
    const front = r?.then?.add_front || [];
    firsts.set(eoId, front[0] || null);
  }

  // Group by first module
  const byFirst = new Map();
  for (const [eoId, first] of firsts.entries()) {
    if (!first) continue;
    if (!byFirst.has(first)) byFirst.set(first, []);
    byFirst.get(first).push(eoId);
  }

  // Hardcode high-value tie-break patterns
  const patterns = [
    {
      id: "TB_AUDIT_vs_VARIANCE_v1",
      groups: ["A_mechanics_audit", "B_variance_dashboard"],
      question: "In a pilot decision, what blocks approval more often: audit defensibility or variance/tail-risk control?",
      options: ["audit_defensibility", "variance_tail_risk", "both_equal"],
      map: {
        audit_defensibility: { favor: ["A_mechanics_audit"] },
        variance_tail_risk: { favor: ["B_variance_dashboard"] },
        both_equal: { favor: ["A_mechanics_audit", "B_variance_dashboard"] }
      }
    },
    {
      id: "TB_AUDIT_vs_PORTABILITY_v1",
      groups: ["A_mechanics_audit", "F_portability_pack"],
      question: "What is the bigger committee blocker: audit defensibility or vendor lock-in/offboarding risk?",
      options: ["audit_defensibility", "vendor_lockin", "both_equal"],
      map: {
        audit_defensibility: { favor: ["A_mechanics_audit"] },
        vendor_lockin: { favor: ["F_portability_pack"] },
        both_equal: { favor: ["A_mechanics_audit", "F_portability_pack"] }
      }
    }
  ];

  // Convert favored modules to EO updates (favor all EOs whose first module matches)
  const tieBreakers = [];
  for (const p of patterns) {
    const eosA = (byFirst.get(p.groups[0]) || []);
    const eosB = (byFirst.get(p.groups[1]) || []);
    const between = Array.from(new Set([...eosA, ...eosB]));
    if (between.length < 2) continue;

    tieBreakers.push({
      tie_break_id: p.id,
      between_eos: between,
      priority: 90,
      question: p.question,
      input_type: "single_select",
      options: p.options,
      answer_to_evidence: p.options.map((opt) => {
        const favorModules = p.map[opt].favor;
        const favoredEOs = favorModules.flatMap(m => byFirst.get(m) || []);
        return {
          when: { equals: opt },
          updates: favoredEOs.map(eo_id => ({
            eo_id,
            evidence: 1.0,
            weight: 1.2,
            reason: `Tie-break favored: ${opt}`
          }))
        };
      })
    });
  }

  return tieBreakers;
}
```

### C) Emit `questions.generated.json` in `main`

In `generate-from-eos.mjs` after you build `routerTable`:

```
const questionsGen = compileQuestionsGenerated(catalog, routerTable);
writeJson(path.join(outDir, "questions.generated.json"), questionsGen);
console.log(" -", path.join(outDir, "questions.generated.json"));
```

* * *

3) Runtime function: `selectNextQuestion(confidence, eo_catalog)`
-----------------------------------------------------------------

### Inputs expected

*   `confidence`: snapshot from server, containing `scores[eo_id].mean`
*   `eo_catalog`: the generated questions artifact OR EO catalog + questions artifact
*   optional `askedQuestionIds` list and `sessionState` to prevent loops

### Output

A single “next best question” object, or `null` if not needed.

```
/**
 * confidence: { scores: { [eo_id]: { mean: number } } }
 * questionsTable: { defaults, eo_questions[], tie_breakers[] }
 * askedQuestionIds: string[]
 */
export function selectNextQuestion(confidence, questionsTable, askedQuestionIds = []) {
  const scores = confidence?.scores || {};
  const defaults = questionsTable?.defaults || {};
  const eoQuestions = questionsTable?.eo_questions || [];
  const tieBreakers = questionsTable?.tie_breakers || [];

  const MIN_NO_Q = defaults.min_eo_mean_for_no_question ?? 0.75;
  const band = defaults.uncertainty_band ?? { low: 0.55, high: 0.75 };
  const LOW = band.low ?? 0.55;
  const HIGH = band.high ?? 0.75;

  // If any EO is confidently “active”, no question required (unless conflicts exist)
  const means = Object.entries(scores).map(([eo_id, v]) => ({
    eo_id,
    mean: typeof v?.mean === "number" ? v.mean : null
  })).filter(x => x.mean !== null);

  const top = means.sort((a, b) => b.mean - a.mean).slice(0, 6);

  const hasStrong = top.some(x => x.mean >= MIN_NO_Q);

  // Conflict detection: two or more EOs in the uncertainty band but close to each other
  const inBand = top.filter(x => x.mean >= LOW && x.mean < HIGH);
  const conflictLikely =
    inBand.length >= 2 && Math.abs(inBand[0].mean - inBand[1].mean) <= 0.08;

  // 1) Tie-breaker first if conflict likely
  if (conflictLikely) {
    const bandIds = new Set(inBand.map(x => x.eo_id));

    const candidates = tieBreakers
      .filter(tb => (tb.between_eos || []).some(eo => bandIds.has(eo)))
      .filter(tb => !askedQuestionIds.includes(tb.tie_break_id))
      .sort((a, b) => (b.priority ?? 0) - (a.priority ?? 0));

    if (candidates.length) return { kind: "tie_break", ...candidates[0] };
  }

  // 2) If no strong EO, pick the highest priority EO question among uncertain EOs
  if (!hasStrong) {
    const uncertain = top.filter(x => x.mean >= LOW && x.mean < HIGH);
    const uncertainIds = new Set(uncertain.map(x => x.eo_id));

    const candidates = eoQuestions
      .filter(q => uncertainIds.has(q.eo_id))
      .filter(q => !askedQuestionIds.includes(q.question_id))
      .sort((a, b) => (b.priority ?? 0) - (a.priority ?? 0));

    if (candidates.length) return { kind: "eo_question", ...candidates[0] };
  }

  // 3) If strong exists but we still want “self-healing” data: pick a question for the #1 EO
  // Only do this if you want continuous improvement even after routing is decided.
  // Comment this block out if you want fewer interruptions.
  const best = top[0];
  if (best && best.mean >= MIN_NO_Q) {
    const q = eoQuestions
      .filter(x => x.eo_id === best.eo_id)
      .filter(x => !askedQuestionIds.includes(x.question_id))
      .sort((a, b) => (b.priority ?? 0) - (a.priority ?? 0))[0];

    if (q) return { kind: "eo_question", ...q };
  }

  return null;
}
```

* * *

4) Applying answers (no manual logic)
-------------------------------------

When the user answers, you do:

1.  Find the selected question in `questions.generated.json`
2.  Evaluate `answer_to_evidence[]` conditions
3.  Emit **EO evidence events** to backend `/confidence/validate` (or a new `/confidence/evidence` endpoint) using the `updates[]` payload.

### Evaluator (deterministic)

```
export function mapAnswerToEvidence(question, answer) {
  const rules = question?.answer_to_evidence || [];
  const updates = [];

  for (const r of rules) {
    const when = r.when || {};
    const ok =
      when.any === true ||
      (when.equals !== undefined && answer === when.equals) ||
      (Array.isArray(when.includes_any) && Array.isArray(answer) && answer.some(a => when.includes_any.includes(a))) ||
      (Array.isArray(when.includes_any) && typeof answer === "string" && when.includes_any.includes(answer));

    if (ok) updates.push(...(r.updates || []));
  }

  return updates;
}
```

Then POST each update to your backend:

```
fetch("http://localhost:8787/confidence/validate", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    account: "Lifehouse Capital",
    eo: update.eo_id,
    label: update.evidence >= 0.8 ? "confirm" : "partial",
    weight: update.weight,
    note: update.reason,
    context: { question_id: question.question_id, answer }
  })
});
```

* * *

5) Why this qualifies as “self-healing”
---------------------------------------

*   The system asks questions only when **confidence is insufficient** or **conflicting**
*   Answers are translated into evidence using a **generated rule map**
*   Evidence updates confidence → confidence changes routing + messaging → recursion closes the loop
*   Over time, telemetry + answers reduce uncertainty, decreasing future questions and improving decisions

If you want the system to “search for information required to make a better decision,” the next clean step is to add a third question type:

*   `kind: "research_task"` with `query_templates[]` (e.g., internal doc lookup, prior pilot baseline extraction)
*   the runtime can enqueue these into `research_queue.jsonl` when uncertainty persists after 1–2 questions

## Prompt:
add: kind: "research_task" with query_templates[] (e.g., internal doc lookup, prior pilot baseline extraction)

## Response:
1) Extend `questions.generated.json` to support `kind: "research_task"`
-----------------------------------------------------------------------

### Add a third section: `research_tasks[]`

This is **machine-readable automation work** the system can queue when:

*   EO confidence stays in the uncertainty band after 1–2 questions
*   the system needs baseline data to compute ROI or choose modules
*   tie-break remains unresolved

#### Updated artifact shape

```
{
  "schema_version": "liquifex.questions_table.v1",
  "generated_at": "2026-02-27T00:00:00Z",
  "account": "Lifehouse Capital",
  "defaults": {
    "min_eo_mean_for_no_question": 0.75,
    "uncertainty_band": { "low": 0.55, "high": 0.75 },
    "max_questions_per_session": 6,
    "max_research_tasks_per_session": 3
  },
  "eo_questions": [ /* ... */ ],
  "tie_breakers": [ /* ... */ ],
  "research_tasks": [
    {
      "task_id": "RT_LH_BASELINE_TTL_v1",
      "priority": 95,
      "requires": {
        "any_eo_in_band": ["EO_LH_0002", "EO_LH_0008", "EO_LH_0012"]
      },
      "goal": "Acquire baseline time-to-liquidity distribution to quantify variance ROI.",
      "query_templates": [
        {
          "source": "internal_docs",
          "template": "Lifehouse baseline time-to-liquidity P50 P90 distribution current process",
          "qdf": 5
        },
        {
          "source": "prior_pilots",
          "template": "LiquiFex pilot baseline TTL metrics (P50,P90) LS portfolio",
          "qdf": 3
        }
      ],
      "output_schema_hint": {
        "expected_fields": ["p50_days", "p90_days", "sample_size", "as_of_date", "workflow_scope"]
      },
      "evidence_on_success": [
        {
          "updates": [
            { "eo_id": "EO_LH_0002", "evidence": 1.0, "weight": 0.6, "reason": "Baseline variance data required/used" },
            { "eo_id": "EO_LH_0012", "evidence": 1.0, "weight": 0.6, "reason": "Variance quantification operationalized" }
          ]
        }
      ]
    }
  ]
}
```

* * *

2) Generator changes: emit `research_tasks[]`
---------------------------------------------

Add to `generate-from-eos.mjs`:

### A) Research task compiler (policy-driven, deterministic)

```
function compileResearchTasksGenerated(catalog) {
  const eos = catalog.eos || [];

  // Helper: find EO ids by theme from message emphasis/tokens
  function eosByTheme(themeIncludes) {
    const out = [];
    for (const eo of eos) {
      const emph = (eo?.routing_rules?.message_emphasis || []).join(" ").toLowerCase();
      const tokens = (eo?.signals?.language_tokens || []).flatMap(t => t.match_any || []).join(" ").toLowerCase();
      const t = `${emph} ${tokens}`;
      if (themeIncludes.some(k => t.includes(k))) out.push(eo.eo_id);
    }
    return Array.from(new Set(out));
  }

  const varianceEOs = eosByTheme(["variance", "p90", "tail", "capital velocity", "drivers"]);
  const auditEOs = eosByTheme(["audit", "governance", "provenance", "committee"]);
  const portabilityEOs = eosByTheme(["lock", "dependency", "exit", "offboarding"]);
  const spreadsheetEOs = eosByTheme(["spreadsheet", "excel", "dual"]);

  const tasks = [
    {
      task_id: "RT_LH_BASELINE_TTL_v1",
      priority: 95,
      requires: { any_eo_in_band: varianceEOs.slice(0, 8) },
      goal: "Acquire baseline time-to-liquidity distribution to quantify variance ROI.",
      query_templates: [
        { source: "internal_docs", template: "Lifehouse baseline time-to-liquidity P50 P90 distribution current process", qdf: 5 },
        { source: "prior_pilots", template: "LiquiFex pilot baseline TTL metrics (P50,P90) LS portfolio", qdf: 3 }
      ],
      output_schema_hint: { expected_fields: ["p50_days", "p90_days", "sample_size", "as_of_date", "workflow_scope"] },
      evidence_on_success: [
        { updates: varianceEOs.slice(0, 3).map(eo_id => ({ eo_id, evidence: 1.0, weight: 0.6, reason: "Baseline variance data required/used" })) }
      ]
    },
    {
      task_id: "RT_LH_AUDIT_REQUIREMENTS_v1",
      priority: 90,
      requires: { any_eo_in_band: auditEOs.slice(0, 8) },
      goal: "Extract Lifehouse committee/procurement audit artifact requirements (what must be in the packet).",
      query_templates: [
        { source: "internal_docs", template: "Lifehouse committee requirements audit packet evidence trail override register rules snapshot", qdf: 5 },
        { source: "prior_pilots", template: "audit packet requirements institutional LS buyer procurement compliance", qdf: 3 }
      ],
      output_schema_hint: { expected_fields: ["required_artifacts", "reviewers", "approval_sequence", "security_requirements"] },
      evidence_on_success: [
        { updates: auditEOs.slice(0, 3).map(eo_id => ({ eo_id, evidence: 1.0, weight: 0.6, reason: "Audit requirements confirmed" })) }
      ]
    },
    {
      task_id: "RT_LH_PORTABILITY_CONCERNS_v1",
      priority: 85,
      requires: { any_eo_in_band: portabilityEOs.slice(0, 8) },
      goal: "Determine offboarding/portability constraints and acceptable export formats/specs.",
      query_templates: [
        { source: "internal_docs", template: "Lifehouse vendor offboarding requirements portability export formats rules evidence audit logs", qdf: 5 },
        { source: "prior_pilots", template: "portability pack offboarding playbook requirements institutional buyer", qdf: 3 }
      ],
      output_schema_hint: { expected_fields: ["required_exports", "formats", "retention_policy", "handoff_process"] },
      evidence_on_success: [
        { updates: portabilityEOs.slice(0, 2).map(eo_id => ({ eo_id, evidence: 1.0, weight: 0.5, reason: "Portability constraints clarified" })) }
      ]
    },
    {
      task_id: "RT_LH_CURRENT_SOR_v1",
      priority: 80,
      requires: { any_eo_in_band: spreadsheetEOs.slice(0, 8) },
      goal: "Confirm current system-of-record and spreadsheet dependence for workflow tracking.",
      query_templates: [
        { source: "internal_docs", template: "Lifehouse system of record workflow tracking spreadsheet tracker reconciliation", qdf: 5 },
        { source: "prior_pilots", template: "LS operations spreadsheet control plane reconciliation dual run", qdf: 3 }
      ],
      output_schema_hint: { expected_fields: ["current_sor", "key_spreadsheets", "manual_steps", "dual_run_constraints"] },
      evidence_on_success: [
        { updates: spreadsheetEOs.slice(0, 2).map(eo_id => ({ eo_id, evidence: 1.0, weight: 0.5, reason: "Spreadsheet control-plane confirmed" })) }
      ]
    }
  ];

  return tasks;
}
```

### B) Add tasks into `compileQuestionsGenerated()`

In `compileQuestionsGenerated(...)`, add:

```
const research_tasks = compileResearchTasksGenerated(catalog);

return {
  schema_version: "liquifex.questions_table.v1",
  generated_at: new Date().toISOString(),
  account,
  defaults: { /* existing defaults */ max_research_tasks_per_session: 3 },
  eo_questions,
  tie_breakers,
  research_tasks
};
```

* * *

3) Runtime: update `selectNextQuestion(...)` to return `research_task`
----------------------------------------------------------------------

### Updated selector logic (no manual heuristics beyond policy)

Key behavior:

*   If conflict likely → tie-break question
*   If no strong EO → EO follow-up question
*   If you’ve already asked enough questions OR uncertainty persists → return a research\_task

```
export function selectNextQuestion(confidence, questionsTable, askedIds = [], sessionState = {}) {
  const scores = confidence?.scores || {};
  const defaults = questionsTable?.defaults || {};
  const eoQuestions = questionsTable?.eo_questions || [];
  const tieBreakers = questionsTable?.tie_breakers || [];
  const researchTasks = questionsTable?.research_tasks || [];

  const MIN_NO_Q = defaults.min_eo_mean_for_no_question ?? 0.75;
  const band = defaults.uncertainty_band ?? { low: 0.55, high: 0.75 };
  const LOW = band.low ?? 0.55;
  const HIGH = band.high ?? 0.75;

  const maxQ = defaults.max_questions_per_session ?? 6;
  const maxRT = defaults.max_research_tasks_per_session ?? 3;

  const askedCount = sessionState.questions_asked_count ?? 0;
  const researchCount = sessionState.research_tasks_queued_count ?? 0;

  const means = Object.entries(scores)
    .map(([eo_id, v]) => ({ eo_id, mean: typeof v?.mean === "number" ? v.mean : null }))
    .filter(x => x.mean !== null)
    .sort((a, b) => b.mean - a.mean);

  const top = means.slice(0, 6);
  const hasStrong = top.some(x => x.mean >= MIN_NO_Q);

  const inBand = top.filter(x => x.mean >= LOW && x.mean < HIGH);
  const conflictLikely = inBand.length >= 2 && Math.abs(inBand[0].mean - inBand[1].mean) <= 0.08;

  // 1) tie-break first
  if (conflictLikely && askedCount < maxQ) {
    const bandIds = new Set(inBand.map(x => x.eo_id));
    const tb = tieBreakers
      .filter(t => (t.between_eos || []).some(eo => bandIds.has(eo)))
      .filter(t => !askedIds.includes(t.tie_break_id))
      .sort((a, b) => (b.priority ?? 0) - (a.priority ?? 0))[0];
    if (tb) return { kind: "tie_break", ...tb };
  }

  // 2) EO question if uncertainty and question budget remains
  if ((!hasStrong || inBand.length) && askedCount < maxQ) {
    const inBandIds = new Set(inBand.map(x => x.eo_id));
    const q = eoQuestions
      .filter(q => inBandIds.has(q.eo_id))
      .filter(q => !askedIds.includes(q.question_id))
      .sort((a, b) => (b.priority ?? 0) - (a.priority ?? 0))[0];
    if (q) return { kind: "eo_question", ...q };
  }

  // 3) research_task if uncertainty persists OR question budget exceeded
  // (deterministic: choose highest priority task whose requires.any_eo_in_band matches)
  if (researchCount < maxRT) {
    const inBandIds = new Set(inBand.map(x => x.eo_id));
    const rt = researchTasks
      .filter(t => !askedIds.includes(t.task_id))
      .filter(t => {
        const req = t.requires || {};
        const any = req.any_eo_in_band || [];
        return any.some(eo => inBandIds.has(eo));
      })
      .sort((a, b) => (b.priority ?? 0) - (a.priority ?? 0))[0];

    if (rt) return { kind: "research_task", ...rt };
  }

  return null;
}
```

* * *

4) Executing a `research_task`: enqueue to `research_queue.jsonl`
-----------------------------------------------------------------

### Server-side endpoint: `POST /research/enqueue`

Add to your Node server:

```
app.post("/research/enqueue", (req, res) => {
  const task = req.body;
  if (!task?.task_id || !task?.account || !task?.session_id) {
    return res.status(400).json({ ok: false, error: "missing_task_id_account_session_id" });
  }

  const day = isoDay(task.timestamp || Date.now());
  const filePath = path.join(DATA_DIR, "research_queue", day, "research_queue.jsonl");

  const record = {
    ...task,
    timestamp: task.timestamp || new Date().toISOString(),
    status: "queued"
  };

  try {
    appendJsonl(filePath, record);
    return res.json({ ok: true, file: filePath });
  } catch {
    return res.status(500).json({ ok: false, error: "enqueue_failed" });
  }
});
```

### Front-end action

When `selectNextQuestion(...)` returns `kind: "research_task"`:

*   emit telemetry `research_task.queued`
*   POST the task (including `query_templates`) to `/research/enqueue`

Example payload:

```
await fetch("http://localhost:8787/research/enqueue", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    task_id: rt.task_id,
    account: config.account,
    session_id: sessionId,
    goal: rt.goal,
    query_templates: rt.query_templates,
    output_schema_hint: rt.output_schema_hint
  })
});
```

* * *

5) Optional: auto-apply evidence when research completes
--------------------------------------------------------

When a human (or later, an automated search worker) completes the task, they POST:

*   the extracted baseline fields
*   and the `evidence_on_success[]` updates to confidence

Add endpoint: `POST /research/complete`

*   appends to `research_results.jsonl`
*   applies confidence updates (calls your beta updater) using the task’s `evidence_on_success`

This closes the self-healing loop: **detect gap → research → update confidence → recompute routing**.

* * *

6) What you get with this addition
----------------------------------

*   A third decision lever besides “ask user”:
    *   **ask user** when answer is quick and high-signal
    *   **research task** when answer requires data pull or internal lookup
*   Auditability: every research decision is logged as JSONL
*   Extensibility: you can later route `query_templates` to:
    *   internal docs (Google Drive)
    *   prior pilot databases
    *   CRM notes
    *   or web search (public validation)

If you want the next step, say: **“add /research/complete and auto-evidence application”** and I’ll provide the exact server code and the JSONL formats for results and evidence.

## Prompt:
add /research/complete and auto-evidence application

## Response:
Add `/research/complete` + auto-evidence application (server-side)
------------------------------------------------------------------

This closes the loop:

1.  runtime queues research task → `research_queue.jsonl`
2.  human/worker completes task → POST `/research/complete`
3.  server appends results → `research_results.jsonl`
4.  server auto-applies `evidence_on_success[]` to EO confidence (Beta updates)
5.  confidence snapshot updates immediately

Below is drop-in code.

* * *

1) Add helpers (if not already present)
=======================================

In `server.js`, ensure you have these helpers (or equivalent):

```
import fs from "fs";
import path from "path";

function ensureDir(p) {
  fs.mkdirSync(p, { recursive: true });
}

function isoDay(ts) {
  const d = new Date(ts || Date.now());
  const yyyy = d.getUTCFullYear();
  const mm = String(d.getUTCMonth() + 1).padStart(2, "0");
  const dd = String(d.getUTCDate()).padStart(2, "0");
  return `${yyyy}-${mm}-${dd}`;
}

function appendJsonl(filePath, obj) {
  ensureDir(path.dirname(filePath));
  fs.appendFileSync(filePath, JSON.stringify(obj) + "\n", "utf8");
}

function safeStr(s) {
  return String(s || "")
    .trim()
    .replace(/[^a-zA-Z0-9._-]/g, "_")
    .slice(0, 120);
}
```

* * *

2) Add Beta confidence “evidence apply” function
================================================

If your server already imports and uses `applyHumanValidation()` (label-based), add a direct evidence endpoint function so you don’t have to map evidence→label.

Create `confidence_evidence.js` (or add into `confidence.js`), using your existing Beta state storage approach.

### `confidence_evidence.js`

```
import fs from "fs";
import path from "path";

function ensureDir(p) {
  fs.mkdirSync(p, { recursive: true });
}

function safeStr(s) {
  return String(s || "")
    .trim()
    .replace(/[^a-zA-Z0-9._-]/g, "_")
    .slice(0, 120);
}

function clamp(x, lo, hi) {
  return Math.max(lo, Math.min(hi, x));
}

function betaMean(alpha, beta) {
  const a = Math.max(1e-6, alpha);
  const b = Math.max(1e-6, beta);
  return a / (a + b);
}

function betaFromMean(mean = 0.65, strength = 10) {
  const m = clamp(mean, 0.01, 0.99);
  const s = Math.max(2, strength);
  return { alpha: m * s, beta: (1 - m) * s };
}

function betaUpdate({ alpha, beta }, evidence, weight) {
  const e = clamp(evidence, 0, 1);
  const w = clamp(weight, 0.01, 5);
  return {
    alpha: alpha + e * w,
    beta: beta + (1 - e) * w
  };
}

function loadJson(file, fallback) {
  try {
    return JSON.parse(fs.readFileSync(file, "utf8"));
  } catch {
    return fallback;
  }
}

function saveJson(file, obj) {
  ensureDir(path.dirname(file));
  fs.writeFileSync(file, JSON.stringify(obj, null, 2), "utf8");
}

export function getConfidenceFile(DATA_DIR, account) {
  return path.join(DATA_DIR, "confidence", `${safeStr(account || "unknown")}.json`);
}

/**
 * Apply direct evidence updates (telemetry/research/human) to EO confidence state.
 * updates: [{ eo_id, evidence, weight, reason }]
 */
export function applyEvidenceUpdates({ DATA_DIR, account, source, session_id, updates, context }) {
  const file = getConfidenceFile(DATA_DIR, account);

  const state = loadJson(file, {
    account,
    updated_at: new Date().toISOString(),
    priors: { default_mean: 0.65, default_strength: 10, per_eo: {} },
    scores: {}
  });

  const defaultMean = state.priors?.default_mean ?? 0.65;
  const defaultStrength = state.priors?.default_strength ?? 10;

  const applied = [];

  for (const u of updates || []) {
    const eo = u.eo_id;
    if (!eo) continue;

    const current = state.scores[eo] || {
      ...betaFromMean(defaultMean, defaultStrength),
      mean: null,
      last_updated: null,
      history_tail: []
    };

    const next = betaUpdate(
      { alpha: current.alpha, beta: current.beta },
      u.evidence,
      u.weight
    );

    const mean = betaMean(next.alpha, next.beta);

    const tail = Array.isArray(current.history_tail) ? current.history_tail.slice(-19) : [];
    tail.push({
      at: new Date().toISOString(),
      source: source || "unknown",
      session_id: session_id || null,
      evidence: u.evidence,
      weight: u.weight,
      reason: u.reason || null,
      context: context || null
    });

    state.scores[eo] = {
      alpha: next.alpha,
      beta: next.beta,
      mean,
      last_updated: new Date().toISOString(),
      history_tail: tail
    };

    applied.push({ eo_id: eo, mean });
  }

  state.updated_at = new Date().toISOString();
  saveJson(file, state);

  return { file, applied, state };
}
```

* * *

3) Add `/research/complete` endpoint in `server.js`
===================================================

In `server.js`, import:

```
import { applyEvidenceUpdates } from "./confidence_evidence.js";
```

Add the endpoint:

```
app.post("/research/complete", (req, res) => {
  const body = req.body || {};

  const account = body.account;
  const session_id = body.session_id;
  const task_id = body.task_id;

  if (!account || !session_id || !task_id) {
    return res.status(400).json({ ok: false, error: "missing_account_session_id_task_id" });
  }

  const timestamp = body.timestamp || new Date().toISOString();
  const day = isoDay(timestamp);

  // 1) append research result record
  const resultsPath = path.join(DATA_DIR, "research_results", day, "research_results.jsonl");

  const record = {
    timestamp,
    account,
    session_id,
    task_id,
    status: "completed",
    goal: body.goal || null,
    // raw extracted output (should match output_schema_hint if possible)
    output: body.output || null,
    // optionally include the templates used + sources
    resolved_queries: body.resolved_queries || null,
    // evidence plan from generator or provided by client
    evidence_on_success: body.evidence_on_success || null,
    // freeform notes
    notes: body.notes || null
  };

  try {
    appendJsonl(resultsPath, record);
  } catch {
    return res.status(500).json({ ok: false, error: "write_results_failed" });
  }

  // 2) auto-apply evidence
  // Evidence format supported:
  // - evidence_on_success: [{ updates: [{ eo_id, evidence, weight, reason }, ...] }, ...]
  // OR directly: evidence_updates: [{ eo_id, evidence, weight, reason }, ...]
  let updates = [];

  if (Array.isArray(body.evidence_updates)) {
    updates = body.evidence_updates;
  } else if (Array.isArray(body.evidence_on_success)) {
    for (const block of body.evidence_on_success) {
      if (Array.isArray(block?.updates)) updates.push(...block.updates);
    }
  }

  let applied = [];
  if (updates.length) {
    try {
      const out = applyEvidenceUpdates({
        DATA_DIR,
        account,
        source: "research_task",
        session_id,
        updates,
        context: {
          task_id,
          goal: body.goal || null,
          output_schema_hint: body.output_schema_hint || null
        }
      });
      applied = out.applied;
    } catch {
      // do not fail completion if confidence update fails
    }
  }

  return res.json({
    ok: true,
    results_file: resultsPath,
    evidence_applied: applied
  });
});
```

* * *

4) Payload contract for `/research/complete`
============================================

### Minimal

```
{
  "account": "Lifehouse Capital",
  "session_id": "sess_123",
  "task_id": "RT_LH_BASELINE_TTL_v1",
  "output": {
    "p50_days": 41,
    "p90_days": 97,
    "sample_size": 842,
    "as_of_date": "2026-02-15",
    "workflow_scope": "policy_loan_to_settlement"
  },
  "evidence_updates": [
    { "eo_id": "EO_LH_0002", "evidence": 1.0, "weight": 0.6, "reason": "Baseline TTL collected" },
    { "eo_id": "EO_LH_0012", "evidence": 1.0, "weight": 0.6, "reason": "Variance quant operationalized" }
  ]
}
```

### Using generator-provided blocks

```
{
  "account": "Lifehouse Capital",
  "session_id": "sess_123",
  "task_id": "RT_LH_BASELINE_TTL_v1",
  "goal": "Acquire baseline time-to-liquidity distribution to quantify variance ROI.",
  "output_schema_hint": {
    "expected_fields": ["p50_days","p90_days","sample_size","as_of_date","workflow_scope"]
  },
  "output": { "p50_days": 41, "p90_days": 97, "sample_size": 842, "as_of_date": "2026-02-15", "workflow_scope": "..." },
  "evidence_on_success": [
    {
      "updates": [
        { "eo_id": "EO_LH_0002", "evidence": 1.0, "weight": 0.6, "reason": "Baseline variance data required/used" }
      ]
    }
  ],
  "notes": "Extracted from internal workflow report"
}
```

* * *

5) Test with curl
=================

```
curl -X POST http://localhost:8787/research/complete \
  -H "Content-Type: application/json" \
  -d '{
    "account":"Lifehouse Capital",
    "session_id":"sess_test_003",
    "task_id":"RT_LH_BASELINE_TTL_v1",
    "output":{"p50_days":41,"p90_days":97,"sample_size":842,"as_of_date":"2026-02-15","workflow_scope":"case_to_liquidity"},
    "evidence_updates":[
      {"eo_id":"EO_LH_0002","evidence":1.0,"weight":0.6,"reason":"Baseline TTL collected"},
      {"eo_id":"EO_LH_0012","evidence":1.0,"weight":0.6,"reason":"Variance quant operationalized"}
    ]
  }'
```

Then verify:

*   `data/research_results/<day>/research_results.jsonl` has the record
*   `data/confidence/Lifehouse_Capital.json` has updated EO means

* * *

6) Recommended hardening (next)
===============================

*   add `status: failed` path for research tasks
*   add idempotency key: `{task_id, session_id}` to avoid double-apply
*   include `worker_id` and `source_ref` fields
*   add `GET /research/queue/tail` for operational visibility

If you want idempotency now, say “add idempotency guard” and I’ll provide the exact implementation (append-only safe with a lightweight index).

## Prompt:
add idempotency guard

## Response:
Add idempotency guard for `/research/complete` (append-only safe)
-----------------------------------------------------------------

Goal: prevent double-applying evidence if the same `{account, session_id, task_id}` is submitted twice (retries, UI double-click, worker replay).

### Approach

*   Compute an **idempotency key**: `account|session_id|task_id`
*   Maintain a tiny **processed index file** per day (or global) storing keys that have been applied:
    *   `data/research_index/processed_keys.jsonl` (append-only)
*   On `/research/complete`:
    1.  check if key already processed → return `ok: true, idempotent_replay: true` without re-applying
    2.  else write result + apply evidence + append key to processed index

This is robust enough for Step 1/2. If you later need concurrency safety across multiple processes, you’d move to SQLite/Postgres with a unique constraint.

* * *

1) Add helper functions to `server.js`
======================================

Add near your helpers:

```
import crypto from "crypto";

function makeIdempotencyKey({ account, session_id, task_id }) {
  const raw = `${String(account)}|${String(session_id)}|${String(task_id)}`;
  // hash keeps it short + safe
  return crypto.createHash("sha256").update(raw).digest("hex");
}

function processedIndexPath(DATA_DIR) {
  return path.join(DATA_DIR, "research_index", "processed_keys.jsonl");
}

function hasProcessedKey(DATA_DIR, key) {
  const idxPath = processedIndexPath(DATA_DIR);
  if (!fs.existsSync(idxPath)) return false;

  // For Step 1, linear scan is fine (index will remain small early).
  // If it grows, add an in-memory cache or per-day index.
  const lines = fs.readFileSync(idxPath, "utf8").split("\n");
  for (const line of lines) {
    if (!line.trim()) continue;
    try {
      const obj = JSON.parse(line);
      if (obj.key === key) return true;
    } catch {
      // ignore corrupt line
    }
  }
  return false;
}

function markProcessedKey(DATA_DIR, entry) {
  const idxPath = processedIndexPath(DATA_DIR);
  appendJsonl(idxPath, entry);
}
```

* * *

2) Patch `/research/complete` to enforce idempotency
====================================================

Replace your existing `/research/complete` handler with this version (or apply the edits inline):

```
app.post("/research/complete", (req, res) => {
  const body = req.body || {};

  const account = body.account;
  const session_id = body.session_id;
  const task_id = body.task_id;

  if (!account || !session_id || !task_id) {
    return res.status(400).json({ ok: false, error: "missing_account_session_id_task_id" });
  }

  const idemKey = makeIdempotencyKey({ account, session_id, task_id });

  // 0) Idempotency check (fast-fail)
  try {
    if (hasProcessedKey(DATA_DIR, idemKey)) {
      return res.json({
        ok: true,
        idempotent_replay: true,
        idempotency_key: idemKey,
        evidence_applied: []
      });
    }
  } catch {
    // If index read fails, do not block; proceed (best effort)
  }

  const timestamp = body.timestamp || new Date().toISOString();
  const day = isoDay(timestamp);

  // 1) append research result record
  const resultsPath = path.join(DATA_DIR, "research_results", day, "research_results.jsonl");

  const record = {
    timestamp,
    account,
    session_id,
    task_id,
    idempotency_key: idemKey,
    status: "completed",
    goal: body.goal || null,
    output: body.output || null,
    resolved_queries: body.resolved_queries || null,
    evidence_on_success: body.evidence_on_success || null,
    notes: body.notes || null
  };

  try {
    appendJsonl(resultsPath, record);
  } catch {
    return res.status(500).json({ ok: false, error: "write_results_failed" });
  }

  // 2) compute evidence updates
  let updates = [];

  if (Array.isArray(body.evidence_updates)) {
    updates = body.evidence_updates;
  } else if (Array.isArray(body.evidence_on_success)) {
    for (const block of body.evidence_on_success) {
      if (Array.isArray(block?.updates)) updates.push(...block.updates);
    }
  }

  // 3) apply evidence updates
  let applied = [];
  if (updates.length) {
    try {
      const out = applyEvidenceUpdates({
        DATA_DIR,
        account,
        source: "research_task",
        session_id,
        updates,
        context: {
          task_id,
          goal: body.goal || null,
          output_schema_hint: body.output_schema_hint || null
        }
      });
      applied = out.applied;
    } catch {
      // do not fail completion if confidence update fails
    }
  }

  // 4) Mark idempotency key as processed ONLY after write + (attempted) apply
  try {
    markProcessedKey(DATA_DIR, {
      key: idemKey,
      account,
      session_id,
      task_id,
      timestamp: new Date().toISOString(),
      results_file: resultsPath,
      applied_count: applied.length
    });
  } catch {
    // Best effort; if this fails, a retry may double-apply.
    // Next hardening step is atomic persistence (sqlite) or fs lock.
  }

  return res.json({
    ok: true,
    idempotent_replay: false,
    idempotency_key: idemKey,
    results_file: resultsPath,
    evidence_applied: applied
  });
});
```

* * *

3) Operational behavior
=======================

*   First call completes normally and writes:
    *   `research_results.jsonl`
    *   `processed_keys.jsonl`
    *   confidence state updates
*   Retry with same `{account, session_id, task_id}` returns:
    *   `ok: true`
    *   `idempotent_replay: true`
    *   no evidence re-application

* * *

4) Known limitation (tell-it-like-it-is)
========================================

This is **single-process safe** and “good enough” for Step 1.  
If you run multiple server instances concurrently, a race can still double-apply.

### Upgrade path (when needed)

*   Replace processed index with **SQLite** and enforce `UNIQUE(idempotency_key)`; apply evidence inside a transaction.

If you want that upgrade now, say “move idempotency to sqlite” and I’ll provide the complete minimal SQLite implementation (schema + transaction logic) while keeping the same endpoint contract.

## Prompt:
move idempotency to sqlite

## Response:
Move `/research/complete` idempotency to SQLite (transactional, multi-instance safe)
------------------------------------------------------------------------------------

This replaces the JSONL “processed index” with a SQLite table that enforces **UNIQUE(idempotency\_key)** and applies evidence inside a **single transaction**.

### What you get

*   Retry-safe across UI double clicks, network retries, worker replays
*   Multi-process safe (within SQLite locking semantics)
*   Audit trail remains JSONL (append-only), but idempotency is enforced by DB

* * *

1) Install a SQLite driver
==========================

Pick one:

### Option A (recommended): `better-sqlite3` (sync, simple, reliable)

```
npm i better-sqlite3
```

### Option B: `sqlite3` (async)

```
npm i sqlite3
```

Below I’ll implement **better-sqlite3** (cleanest for an ingestion server). If you want `sqlite3`, say so and I’ll translate.

* * *

2) Create `idempotency_db.js`
=============================

```
import fs from "fs";
import path from "path";
import crypto from "crypto";
import Database from "better-sqlite3";

function ensureDir(p) {
  fs.mkdirSync(p, { recursive: true });
}

export function makeIdempotencyKey({ account, session_id, task_id }) {
  const raw = `${String(account)}|${String(session_id)}|${String(task_id)}`;
  return crypto.createHash("sha256").update(raw).digest("hex");
}

export function openIdempotencyDb(DATA_DIR) {
  const dbDir = path.join(DATA_DIR, "sqlite");
  ensureDir(dbDir);
  const dbPath = path.join(dbDir, "liquifex_demo.db");

  const db = new Database(dbPath);
  db.pragma("journal_mode = WAL");     // better concurrency
  db.pragma("synchronous = NORMAL");   // good tradeoff for demo

  db.exec(`
    CREATE TABLE IF NOT EXISTS research_completions (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      idempotency_key TEXT NOT NULL UNIQUE,
      account TEXT NOT NULL,
      session_id TEXT NOT NULL,
      task_id TEXT NOT NULL,
      created_at TEXT NOT NULL,
      results_file TEXT,
      evidence_applied_json TEXT
    );

    CREATE INDEX IF NOT EXISTS idx_research_completions_account
      ON research_completions(account);

    CREATE INDEX IF NOT EXISTS idx_research_completions_session
      ON research_completions(session_id);
  `);

  const insertCompletion = db.prepare(`
    INSERT INTO research_completions (
      idempotency_key, account, session_id, task_id, created_at, results_file, evidence_applied_json
    ) VALUES (
      @idempotency_key, @account, @session_id, @task_id, @created_at, @results_file, @evidence_applied_json
    )
  `);

  const getCompletion = db.prepare(`
    SELECT idempotency_key, account, session_id, task_id, created_at, results_file, evidence_applied_json
    FROM research_completions
    WHERE idempotency_key = ?
  `);

  return { db, dbPath, insertCompletion, getCompletion };
}
```

* * *

3) Patch `/research/complete` to use SQLite idempotency
=======================================================

In `server.js`:

### A) import + init once

At top:

```
import { openIdempotencyDb, makeIdempotencyKey } from "./idempotency_db.js";
```

After `DATA_DIR` is defined:

```
const idem = openIdempotencyDb(DATA_DIR);
console.log("SQLite idempotency DB:", idem.dbPath);
```

### B) Replace `/research/complete` with transactional version

This version:

*   checks if completion exists → returns prior result (idempotent replay)
*   otherwise:
    *   writes research results JSONL
    *   applies evidence updates
    *   inserts a completion row (UNIQUE constraint ensures no duplicates)
*   All in one `better-sqlite3` transaction.

```
app.post("/research/complete", (req, res) => {
  const body = req.body || {};

  const account = body.account;
  const session_id = body.session_id;
  const task_id = body.task_id;

  if (!account || !session_id || !task_id) {
    return res.status(400).json({ ok: false, error: "missing_account_session_id_task_id" });
  }

  const idempotency_key = makeIdempotencyKey({ account, session_id, task_id });

  // 0) fast-path: already processed
  const existing = idem.getCompletion.get(idempotency_key);
  if (existing) {
    let priorApplied = [];
    try { priorApplied = JSON.parse(existing.evidence_applied_json || "[]"); } catch {}
    return res.json({
      ok: true,
      idempotent_replay: true,
      idempotency_key,
      results_file: existing.results_file || null,
      evidence_applied: priorApplied
    });
  }

  const timestamp = body.timestamp || new Date().toISOString();
  const day = isoDay(timestamp);

  const resultsPath = path.join(DATA_DIR, "research_results", day, "research_results.jsonl");

  // 1) compute evidence updates
  let updates = [];
  if (Array.isArray(body.evidence_updates)) {
    updates = body.evidence_updates;
  } else if (Array.isArray(body.evidence_on_success)) {
    for (const block of body.evidence_on_success) {
      if (Array.isArray(block?.updates)) updates.push(...block.updates);
    }
  }

  // 2) transaction: write JSONL + apply evidence + insert completion row
  const tx = idem.db.transaction(() => {
    // Re-check inside transaction in case of race between processes
    const again = idem.getCompletion.get(idempotency_key);
    if (again) return { replay: true, row: again };

    // Append research result (audit trail)
    const record = {
      timestamp,
      account,
      session_id,
      task_id,
      idempotency_key,
      status: "completed",
      goal: body.goal || null,
      output: body.output || null,
      resolved_queries: body.resolved_queries || null,
      evidence_on_success: body.evidence_on_success || null,
      notes: body.notes || null
    };
    appendJsonl(resultsPath, record);

    // Apply evidence updates to EO confidence state
    let applied = [];
    if (updates.length) {
      const out = applyEvidenceUpdates({
        DATA_DIR,
        account,
        source: "research_task",
        session_id,
        updates,
        context: {
          task_id,
          goal: body.goal || null,
          output_schema_hint: body.output_schema_hint || null
        }
      });
      applied = out.applied || [];
    }

    // Insert completion row (unique key enforces idempotency)
    idem.insertCompletion.run({
      idempotency_key,
      account,
      session_id,
      task_id,
      created_at: new Date().toISOString(),
      results_file: resultsPath,
      evidence_applied_json: JSON.stringify(applied)
    });

    return { replay: false, applied, results_file: resultsPath };
  });

  try {
    const out = tx();

    if (out.replay) {
      let priorApplied = [];
      try { priorApplied = JSON.parse(out.row.evidence_applied_json || "[]"); } catch {}
      return res.json({
        ok: true,
        idempotent_replay: true,
        idempotency_key,
        results_file: out.row.results_file || null,
        evidence_applied: priorApplied
      });
    }

    return res.json({
      ok: true,
      idempotent_replay: false,
      idempotency_key,
      results_file: out.results_file,
      evidence_applied: out.applied
    });
  } catch (err) {
    // If insert failed due to unique constraint (race), treat as replay
    if (String(err?.message || "").toLowerCase().includes("unique")) {
      const row = idem.getCompletion.get(idempotency_key);
      let priorApplied = [];
      try { priorApplied = JSON.parse(row?.evidence_applied_json || "[]"); } catch {}
      return res.json({
        ok: true,
        idempotent_replay: true,
        idempotency_key,
        results_file: row?.results_file || null,
        evidence_applied: priorApplied
      });
    }

    return res.status(500).json({ ok: false, error: "research_complete_failed" });
  }
});
```

* * *

4) Add a lookup endpoint (optional but useful)
==============================================

```
app.get("/research/completions/:account", (req, res) => {
  const account = req.params.account;
  const rows = idem.db
    .prepare("SELECT account, session_id, task_id, created_at, results_file FROM research_completions WHERE account = ? ORDER BY created_at DESC LIMIT 100")
    .all(account);
  res.json({ ok: true, rows });
});
```

* * *

5) Notes on correctness and edge cases
======================================

### JSONL write + DB transaction

*   SQLite transaction does not make the filesystem append atomic, but it **does** prevent evidence double-apply because:
    *   the unique insert is the authoritative gate
    *   the handler re-checks inside the DB transaction
*   Worst-case failure mode: JSONL record written but DB insert fails → later retry could write JSONL again. Evidence still won’t double-apply once DB insert succeeds. If you want “exactly once write” for JSONL too, you’d store the research output in SQLite instead of JSONL or write JSONL after the insert (tradeoff: you lose record on crash between insert and write).

### Concurrency

*   WAL mode supports multiple readers and serialized writers.
*   This is sufficient for your Step 1/2 deployment.

* * *

6) Quick test
=============

```
curl -X POST http://localhost:8787/research/complete \
  -H "Content-Type: application/json" \
  -d '{
    "account":"Lifehouse Capital",
    "session_id":"sess_test_004",
    "task_id":"RT_LH_BASELINE_TTL_v1",
    "output":{"p50_days":40,"p90_days":95,"sample_size":800,"as_of_date":"2026-02-15","workflow_scope":"case_to_liquidity"},
    "evidence_updates":[
      {"eo_id":"EO_LH_0002","evidence":1.0,"weight":0.6,"reason":"Baseline TTL collected"},
      {"eo_id":"EO_LH_0012","evidence":1.0,"weight":0.6,"reason":"Variance quant operationalized"}
    ]
  }'
```

Run it twice; second response should return `idempotent_replay: true`.

* * *

If you want the highest-integrity version (exactly-once for both DB + JSONL), the next step is: **store research results in SQLite and generate JSONL exports from DB** (append-only export job).



---
Powered by [ChatGPT Exporter](https://www.chatgptexporter.com)