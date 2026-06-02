---
name: foundational-goal-maximize-human-superpowers
description: "Co-equal foundational doctrine alongside PPIM. Every Gigaton system, engine, surface, and ingest pipeline exists to maximize human superpowers — multiply what one human operator can do, perceive, decide, and execute. Established 2026-05-26 by Todd as the success metric for the Intelligence Layer."
metadata: 
  node_type: memory
  type: feedback
  established: 2026-05-26
  status: ACTIVE — load-bearing on every architecture decision
  lifecycle_state: canonical
  originSessionId: 82f42574-fcf9-4248-a749-0cfccc81094e
promoted_from: foundational_goal_maximize_human_superpowers.md
promoted_at: 2026-06-02T20:13:25Z
---

# Foundational Goal — Maximize Human Superpowers

## The sentence

> **Every Gigaton capability exists to maximize human superpowers — to multiply what a single human operator can do, perceive, decide, and execute.**

Pairs with [[foundational_goal_gigaton_engineered_brand_experience]] (PPIM = the WHAT). This memory establishes the WHO it's for and HOW we measure success: **did this make the human more capable, more leveraged, more accurate, faster?**

## Why this matters

PPIM tells us what to build (predictably profitable interaction management). This tells us the success criterion at the human layer: every artifact, every UI, every engine, every Q&A response should leave the human MORE capable than before — not just informed, not just served, but amplified.

This is what differentiates "an AI tool that answers questions" from "an intelligence layer that turns one operator into an organization." The former is utility; the latter is leverage.

## How to apply

When designing or reviewing any capability, ask in order:

1. **Does this give the human a new superpower they didn't have?** (perception they couldn't see, decisions they couldn't make in time, actions they couldn't execute alone)
2. **Does it compound — does using it today make tomorrow's use easier or more powerful?** (memory accumulates, skill embeddings sharpen, dispatch routes improve)
3. **Does it preserve human agency at the decision point?** Per [[wave2_intel_2_meta_doctrine]] INTEL-2: system decides ASAP, escalates only on novel/high-cost/user-tagged decisions — but the human always *can* override.
4. **Does it teach?** Real-time coaching loop ([[wave2_intelligence_layer_ti_agent_matrix]] § 7) — every interaction should leave the operator more skilled, not more dependent.
5. **Is the leverage measurable?** If you can't show the human did 10x what they could do solo, you haven't built a superpower yet — you've built a feature.

## How this shapes the Q&A pipeline (and every ingest path)

Every piece of information ingested into Gigaton MUST flow through the FULL intelligence stack — not just embed + retrieve. Concretely, every ingest + every Q&A must apply:

| Capability | Source | Purpose for human superpower |
|---|---|---|
| **10 Intelligence Dimensions scoring** | `intelligence-silo/core/intelligence/dimensions.py` (SUBJECT/TRAINING/EDUCATION/SCIENCE/KNOWLEDGE/STRATEGY/SUCCESS/TOOLS/INFORMATION/EXPERIENCE) | Qualify every chunk — what dimensions does this strengthen? Which are gaps? |
| **Language conversion** | LLM router (gateway `app/llm_router/`) + Claude/Gemini native translation | Operators read source-language original AND working-language summary; nothing lost in monolingual filter |
| **Alt-referencing (cross-source)** | Connector catalog (`connector-api` Pattern A, 15 providers), alt AI tools registry, gignet-orchestrator topic | Every answer cross-checks against alternatives — alternate ingested sources, alternate LLMs, alternate vendor data — to surface disagreement |
| **Existing memory referencing** | Memory hierarchy (working/episodic/semantic/procedural), auto-memory `~/.claude/projects/-Users-admin/memory/`, Ti memory network v3 | Every Q&A loads relevant prior conversations, decisions, and learnings — answer is informed by everything the system has ever known |
| **Information qualification** | Trust assessor SLM (T0-T4 tiers) + Penrose 8-metric scoreboard + principles_filter + Critic phase | Every claim is scored: trust tier, source authority, doctrine alignment, falsifiability — operator sees the qualification, not just the claim |
| **Ti Agent Matrix dispatch** | persona-engine 9 OrgPersonas → 63-role expansion, skill_vectors cosine match | Every question routes to the right specialist ensemble — operator effectively has CFO+CMO+CISO+... advising in parallel |
| **Variable Registry binding** | persona-engine First Principles Variable Registry (50 seed vars) | Answers ground in operator-specific context (brand voice, pricing, market) not generic responses |
| **Axiom Registry check** | decision-engine `axioms.yaml` (23 axioms) | Answer cannot violate ratified doctrine; if it would, surface the conflict to the human |
| **Penrose falsification scoreboard update** | decision-engine `/v1/penrose/scoreboard` (8 metrics) | Every interaction emits a falsification signal — strengthens or weakens our model of what works |
| **Ethnographic frames projection** | `~/.claude/skills/ethnographic-research/` + future `core/intelligence/ethnographic_frames.py` | Behavioral/cultural/contextual nuance, not just literal text match |
| **Web-research backfill** | EO `self_heal.spawn_research_task` + Anthropic native `web_search` tool | When ingest has gaps, system fills them — operator never gets "I don't know" if the answer exists somewhere |
| **Self-Engineered HR signal** | HME utilization sweep, gaps → recruiting loop | Repeated operator gaps surface as hiring signal (human or agent) — the platform extends the operator's team |

## Source of truth

[[wave2_intelligence_layer_ti_agent_matrix]] INTEL-1 sentence: *"create real-time coaching + feedback + intelligence-utilization-to-qualify-information environment."*

That sentence operationalizes this memory. Every architecture decision should be testable against: *does it qualify information for the human, and does it leave them more capable?*

## Anti-patterns

- Any Q&A path that returns chunks-with-citations without applying the qualification stack = leak; rebuild.
- Any UI surface that hides the qualification (trust tier, dispatch ensemble, principles check) = "AI tool" not "superpower amplifier."
- Any engine that scales by reducing human agency at the decision point = inverse of the goal; refactor or kill.
- Any ingest path that drops information through a single-language or single-source filter = data loss against superpower.
