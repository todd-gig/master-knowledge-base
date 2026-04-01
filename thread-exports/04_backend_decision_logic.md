    ---
    title: Backend Decision Logic
    tags:
      - backend-logic
  - rules
  - routing
type: logic-note
    status: draft
    created: 2026-03-26
    updated: 2026-03-26
    purpose: >
      Formalize explicit and inferred decision logic from the visible thread.
    ---
# Backend Decision Logic

## Explicit rules

### Org span rules
- Executive span: 7 direct reports.
- Mid-layer span: 3-5 direct reports.
- Lead span: up to 3 direct reports.

### Executive coverage set
- CEO
- CTO
- Chief Experience & Operations Officer
- Chief Information Systems Officer
- Chief Data Officer
- Chief Talent Officer
- CFO
- CMO
- CRO
- Chief Environment Officer
- Chief Policy Officer / Chief Political Advisor

### Team design rules
- assign the fewest roles necessary
- preserve human supervision
- identify what can be automated vs AI-augmented vs human-reviewed vs human-approved vs human-owned
- do not stop at department labels; decompose to atomic skills

### File routing logic
- Always load root instruction file first.
- Load skill ontology when skills/capabilities/qualifications are requested.
- Load team structure rules when ownership, reporting lines, or supervision are requested.
- Load negotiation framework when influence, alignment, value exchange, terms, or objections are involved.
- Load output template before generating final response unless format is overridden.

## Inferred state machine

1. Intake request
2. Define problem
3. Define desired outcome
4. Detect whether skills, team structure, negotiation, or all three are needed
5. Load relevant logic modules
6. Map capabilities -> skills -> roles -> supervisors
7. Add certification layers if readiness matters
8. Add negotiation staffing and sequence if approvals/counterparties exist
9. Separate automation vs human-critical ownership
10. Format final output

## Confidence logic (inferred)
- High confidence: user explicitly requested the artifact or logic branch.
- Medium confidence: logic is strongly implied by task type.
- Low confidence: role, threshold, or governance detail not directly stated.

## Exception policy (inferred)
- If user requests a different format, output template is optional.
- If problem is simple and no counterparties exist, negotiation framework may be skipped.
- If no skills decomposition is required, ontology can remain implicit.
