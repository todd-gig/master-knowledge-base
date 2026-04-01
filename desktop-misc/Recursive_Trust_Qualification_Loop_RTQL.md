# Recursive Trust Qualification Loop (RTQL)

## Core Name
**Recursive Trust Qualification Loop (RTQL)**

## Alternate Names
- First-Principles Trust Engine (FPTE)
- Trust-to-Truth Qualification Loop (TTQL)
- Recursive Signal Certification Framework (RSCF)
- First-Principles Input Validation Loop (FPIVL)

## Recommended Official Name
Use **Recursive Trust Qualification Loop (RTQL)** as the canonical name.

Why this name:
- **Recursive**: outputs are fed back into the system for re-qualification.
- **Trust**: the system is centered on trust-weighted acceptance of inputs.
- **Qualification**: not all inputs deserve equal standing.
- **Loop**: the process compounds over time and continuously improves.

---

## Purpose
RTQL is a core decision system for evaluating any input, claim, observation, source, artifact, or research output before it is allowed to influence strategy, scoring, knowledge, ontology, or decision-making.

Its purpose is to:
1. filter noise,
2. qualify usable signals,
3. certify strong signals,
4. route uncertainty into research,
5. identify genuinely new information,
6. extract first principles when possible,
7. recursively feed validated knowledge back into the system.

RTQL should be treated as a **foundational logic layer** inside any value matrix, scoring engine, research pipeline, ontology engine, or agentic reasoning framework.

---

## Core Operating Principle
**No input should materially influence decision-making until it has been trust-qualified.**

Corollaries:
- repeated exposure alone does not equal truth,
- authority alone does not equal trust,
- novelty alone does not equal value,
- consensus alone does not equal first principles,
- only repeated, independent, explainable, replicable, and adversarially robust signals should be promoted.

---

## Canonical Process Flow

```text
Raw Input
-> Qualification
-> Certification
-> Research
-> New Information Detection
-> First-Principles Identification
-> Re-Qualification
-> Knowledge Core / Value Matrix / Decision System
```

More explicit loop:

```text
Input
-> Qualified?
-> Certified?
-> Research Required?
-> New Information?
-> First-Principles Candidate?
-> Re-insert as higher-trust input
```

---

## Rule of 7 Logic
RTQL uses a 7-checkpoint trust discipline.

### Seven Core Checkpoints
1. Provenance
2. Source Integrity
3. Repeated Exposure
4. Independence of Confirmation
5. Mechanistic Explainability
6. Replicability
7. Adversarial Robustness

Interpretation:
- passing checkpoints 1 to 4 makes an input **Qualified**,
- passing checkpoints 5 to 7 makes it **Certified**,
- passing novelty and decomposition tests may elevate it to **Research-Grade** or **First-Principles Candidate**.

---

## Smooth Number Scoring Logic
To avoid false precision, scoring should use coarse stable increments.

### Allowed Scores
```text
0, 1, 2, 3, 4, 5, 6, 8, 10, 12
```

This forces clearer classification and reduces score gaming.

---

## Trust Dimensions
Each input should be scored across 7 dimensions.

### 1. Source Integrity
How credible and auditable is the source?

### 2. Exposure Count
How many meaningful exposures has the signal survived?

### 3. Independence of Confirmation
Are confirmations independent or merely echoes?

### 4. First-Principles Explainability
Can the claim be reduced to a mechanism rather than narrative?

### 5. Replicability
Can another competent operator reproduce the outcome?

### 6. Adversarial Robustness
Can the claim survive attempts to break, spoof, manipulate, or game it?

### 7. Novelty Yield
Does this input produce materially new information?

---

## Trust Stages

### Stage 0: Noise
The input is unverifiable, low-integrity, or too weak to matter.

### Stage 1: Weak Signal
The input may be worth monitoring but cannot influence decisions.

### Stage 2: Qualified
The input has cleared minimum trust thresholds and may enter structured validation.

### Stage 3: Certification Gap
The input is promising but lacks mechanism, replication, or robustness.

### Stage 4: Certified
The input is strong enough for controlled operational use.

### Stage 5: Research-Grade
The input is certified and materially adds insight or improves the model.

### Stage 6: First-Principles Candidate
The input appears to express an irreducible causal rule, variable, or governing constraint.

---

## Stage Gates

### Qualification Gate
Minimum conditions:
- identifiable source,
- provenance or auditability present,
- source integrity above threshold,
- repeated exposure threshold met,
- independent confirmations threshold met.

Suggested minimum thresholds:
- Source Integrity >= 4
- Exposure Count >= 3
- Independence >= 4

If any of these fail, the input does not become Qualified.

### Certification Gate
Minimum conditions:
- mechanism can be explained,
- result can be replicated,
- claim survives adversarial challenge.

Suggested minimum thresholds:
- Explainability >= 6
- Replicability >= 6
- Adversarial Robustness >= 6

### New Information Gate
A certified input counts as genuinely new only if at least one is true:
- it materially changes a prior,
- it reveals a hidden variable,
- it improves predictive or decision quality,
- it compresses multiple observations into a simpler mechanism.

### First-Principles Gate
A research-grade insight is a first-principles candidate only if it:
- expresses a causal mechanism,
- remains true after narrative removal,
- remains true after authority removal,
- survives context shift,
- is irreducible without losing explanatory power.

---

## Decision Tree

```text
START
  |
  v
Is input identifiable and attributable?
  |-- No -> Noise
  |-- Yes -> Continue

Does source integrity meet threshold?
  |-- No -> Weak Signal
  |-- Yes -> Continue

Has exposure threshold been met?
  |-- No -> Track only
  |-- Yes -> Continue

Are confirmations independent?
  |-- No -> Echo Signal / Hold
  |-- Yes -> Qualified

Can the claim be mechanistically explained?
  |-- No -> Research: explanation gap
  |-- Yes -> Continue

Can the result be replicated?
  |-- No -> Research: replication gap
  |-- Yes -> Continue

Does it survive adversarial testing?
  |-- No -> Quarantine / downgrade
  |-- Yes -> Certified

Does it produce materially new information?
  |-- No -> Certified Knowledge
  |-- Yes -> Continue

Does it reveal an irreducible causal rule or governing variable?
  |-- No -> Research-Grade Insight
  |-- Yes -> First-Principles Candidate
```

---

## Core Labels
Use these exact normalized labels whenever possible:

- `noise`
- `weak_signal`
- `echo_signal`
- `qualified`
- `certification_gap`
- `certified`
- `research_grade`
- `first_principles_candidate`
- `axiom_candidate`

For principle classification:
- `derived`
- `pattern`
- `mechanism`
- `principle`
- `axiom_candidate`

---

## Implementation Rules for Claude
Claude should implement RTQL as a mandatory upstream filter before allowing any input to materially affect:
- scoring,
- valuation,
- strategy,
- ontology design,
- automation rules,
- memory systems,
- policy rules,
- decision recommendations.

### Mandatory Behavioral Contract
Claude should:
1. classify the input,
2. score it across trust dimensions,
3. identify the stage,
4. explain why the input is or is not promotable,
5. route uncertainty into explicit research tasks,
6. refuse to elevate low-trust novelty,
7. recursively re-ingest validated outputs.

Claude should not:
- treat consensus as proof,
- treat confidence as evidence,
- treat repetition from the same source as independence,
- treat eloquence as mechanism,
- treat novelty as value without trust,
- treat authority as first principles.

---

## RTQL Pseudocode

```python
def classify_input(x):
    if not x.is_identifiable or not x.has_provenance:
        return "noise"

    if x.source_integrity < 4:
        return "weak_signal"

    if x.exposure_count < 3:
        return "weak_signal"

    if x.independence < 4:
        return "echo_signal"

    if x.explainability < 6:
        return "certification_gap:explainability"

    if x.replicability < 6:
        return "certification_gap:replicability"

    if x.adversarial_robustness < 6:
        return "certification_gap:robustness"

    if x.novelty_yield < 6:
        return "certified"

    if not x.reveals_causal_mechanism:
        return "research_grade"

    if not x.is_irreducible:
        return "research_grade"

    if not x.survives_authority_removal:
        return "research_grade"

    if not x.survives_context_shift:
        return "research_grade"

    return "first_principles_candidate"
```

---

## Data Model

```yaml
input_record:
  input_id: string
  claim: string
  source: string
  timestamp: datetime
  source_integrity: number
  exposure_count: number
  independence: number
  explainability: number
  replicability: number
  adversarial_robustness: number
  novelty_yield: number
  trust_stage: string
  principle_label: string
  reveals_causal_mechanism: boolean
  is_irreducible: boolean
  survives_authority_removal: boolean
  survives_context_shift: boolean
  research_tasks: list
  notes: string
```

---

## Research Routing Logic
If an input fails promotion, Claude should generate the minimum viable next-step research action.

### Failure Modes and Actions
- low provenance -> request or locate source trail
- low exposure -> monitor for repeat appearances
- low independence -> find cross-domain confirmation
- low explainability -> decompose into causal variables
- low replicability -> specify a replication protocol
- low robustness -> design red-team or gaming tests
- low novelty -> store as operational knowledge, not model-changing knowledge

---

## First-Principles Extraction Questions
Claude should use these questions to test for first principles:

1. What must be true for this claim to hold?
2. What assumptions is the claim resting on?
3. Which variables are irreducible?
4. What is causal versus merely correlated?
5. What survives when authority is stripped away?
6. What survives under context shift?
7. What cannot be removed without breaking the explanation?

---

## Integration with the Value Matrix
RTQL should sit upstream of any value system.

### Governing Rule
**Value should be trust-adjusted before use.**

Conceptually:

```text
Adjusted Value = Raw Value x Trust Multiplier
```

Suggested trust multipliers:
- noise -> 0.00 to 0.25
- weak_signal -> 0.25 to 0.50
- qualified -> 1.00
- certified -> 1.25
- research_grade -> 1.50
- first_principles_candidate -> 2.00

This prevents low-trust inputs from inflating value calculations.

---

## Minimal Prompting Instruction for Claude
Use the following instruction as a reusable system or developer layer:

```text
Apply the Recursive Trust Qualification Loop (RTQL) to all material inputs before allowing them to influence conclusions, recommendations, scoring, memory, ontology, or strategy. Score the input across source integrity, exposure count, independence, explainability, replicability, adversarial robustness, and novelty yield. Determine whether the input is noise, weak_signal, echo_signal, qualified, certification_gap, certified, research_grade, or first_principles_candidate. If the input fails promotion, generate explicit research actions required to advance it. Never confuse repetition with independence, authority with truth, novelty with value, or narrative with mechanism.
```

---

## Short Definition
**Recursive Trust Qualification Loop (RTQL)** is a trust-weighted, stage-gated logic system that filters raw inputs into qualified, certified, research-grade, and first-principles knowledge through repeated, independent, explainable, replicable, and adversarially robust validation.

---

## Executive Summary
RTQL is the governance layer that determines whether information deserves influence. It is built to convert raw inputs into trustworthy knowledge, prevent contamination from weak signals, and recursively improve the quality of strategic and analytical reasoning over time.
