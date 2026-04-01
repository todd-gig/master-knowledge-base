# Client Onboarding Generator

## Purpose
Use this generator to create a client-specific overlay without breaking Gigaton global doctrine.

## Input form
- Client name:
- Industry:
- Business model:
- Primary revenue motion:
- Top 3 objectives:
- Key constraints:
- Preferred terminology:
- Success metrics:
- Decision rights map:

## Output set
1. `client_namespace.json`
2. `client_onboarding_brief.md`
3. `client_memory_overlay.md`
4. `client_scoring_weights.json`

## Rules
- Always inherit from `global`.
- Never override foundational doctrine.
- Prefer the minimum viable overlay.
- Only introduce client-specific weights when there is a measurable business case.
