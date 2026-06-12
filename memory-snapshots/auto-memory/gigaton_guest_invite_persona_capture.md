---
name: User Access Engine — invite, onboarding, persona-driven access (Gigaton platform-wide)
description: Backlog spec — new sibling engine to decision-engine/gigaton-engine. Owns user lifecycle, org lifecycle, forced onboarding UI, persona capture, and automatic access computation across every Gigaton project. Replaces the earlier "GuestInvite + auth-gateway" framing.
type: project
established: 2026-05-08 by Todd
revised: 2026-05-08 — scope corrected from "guest invite service" to "platform-wide User Access Engine" per Todd
revised: 2026-05-08 (later) — added re-evaluation cadence, full org-digital-twin schema, Network Intelligence Layer, automated product-dev pipeline with todd/matt dual-signer routing
revised: 2026-05-08 (later still) — added managementMode (MANAGED vs EXEMPT) — gigaton.ai users are exempt from access management but receive same post-deploy upgrade notifications as managed users, in service of org mission to support human development
originSessionId: d8eb5668-0e1b-438d-860c-4ac2c18dd357
lifecycle_state: active
state_set_at: 2026-05-19
state_set_by: auto-migration-concept-8
promoted_from: gigaton_guest_invite_persona_capture.md
promoted_at: 2026-06-02T20:13:25Z
---
## SMEN Alignment (canonical doctrine — see `smen_doctrine.md`)

This engine implements **two SMEN layers**:

- **Memory Layer**: owns the canonical `HumanPersona` row (life logs, digital exhaust, domain history, permissioned embeddings) — replicates a read-model to `intelligence-silo` for AI use; canonical row never leaves the user's sovereignty (per "Human-Centric Data Ownership: user-owned identity containers with zero-knowledge boundaries")
- **Experience Layer**: persona digital twin + Org persona digital twin + trust graph (CxGuy Trust×Value×Priority cap mechanic) = state tracking, preference modeling, relationship graphs, contextual continuity

**Canonical principles this engine must respect:**
- User Sovereignty — cryptographically-enforced permissioning, revocable access (Open Decision: design how revocation cascades to silo read-models)
- Data-as-Asset — the persona is an *appreciating asset* belonging to the user; engine is steward, not owner
- Connect–Create–Thrive–Evolve mantra — Steps 1–6 of the wizard map roughly to Connect (Identity, Context, Trust) → Create (Capabilities) → Thrive (Intent) → Evolve (re-eval cadence + adaptive questioning)

## Status

**GOVERNANCE LOCKED 2026-05-08.** All 12 architectural decisions resolved with WHY lines per the always-record-WHY rule. Spec is canonical and ready to build against.

**Implementation status**: NOT YET BUILT — engine code does not exist. Multi-deploy-window scaffold-and-ship plan:
- **2026-05-08 19:00 CT deploy**: governance lock-in (this spec); optional empty-repo scaffold (`user-access-engine` repo + README + spec + cloudbuild stub)
- **2026-05-11 (Mon)**: FastAPI app + schema migration + empty Cloud Run + healthcheck
- **2026-05-13 (Wed)**: Org onboarding wizard + GuestInvite + Google OAuth callback
- **Subsequent windows**: user verification wizard with pre-population → persona schema → access computation → adaptive re-eval scheduler → Network Intelligence Layer in decision-engine → notification system → thin client adoption per project (Carmen Beach Phase 4 retiring its hardcoded role enum, then SIE / gigaton-engine / decision-engine)

## Why

Identity + access is a security boundary that must be co-located with onboarding (because onboarding IS data collection for the access decision) and reusable by every Gigaton project. Putting it in `gigaton-engine` (pricing) confuses concerns; a thin `auth-gateway` underspecifies the work. The right artifact is an **engine** that automatically computes a user's access from their captured persona × their org's profile × current platform state — no manual permission grants. This implements the Engine Artifact Doctrine literally: `completion = f(user, org, platform.intelligence, resources.available)`.

## Scope (responsibilities)

1. **User lifecycle** — invite → onboarding → active → suspended → expired
2. **Org lifecycle** — provisioning, org persona capture, member management, org-level access defaults
3. **Onboarding UIs** — both org-onboarding wizard and user-onboarding wizard (forced, gated, can't reach platform until complete)
4. **Persona capture** — canonical write of HumanPersona; replicates a read-model to intelligence-silo for AI use
5. **Access computation** — `f(persona, orgProfile, platformState) → capabilitySet`, audit-grade reasoning attached to every decision
6. **Continuous re-evaluation** — persona/org/platform changes trigger recomputation
7. **Audit log** — every access decision recorded with reasoning

## Repo and naming

- New repo: `user-access-engine` (sibling to `decision-engine`, `gigaton-engine`, `intelligence-silo`, `drift-sentinel`)
- Stack: Python/FastAPI to match decision-engine; Cloud Run; Cloud SQL; Secret Manager for OAuth client secrets

## Data model (v0)

### Org (organizational digital twin — full entity graph, not flat profile)

Core fields: `id, name, createdAt, status, gigatonRelationship { contractedProjects[], billingTier, overridePolicies[], firstTouchSource }`

Entity groups (each captured during org onboarding + maintained via re-evaluation):

| Group | Captures |
|---|---|
| **People** | Employee directory, roles, reporting lines; each employee = a User with their own captured persona |
| **Processes** | Workflows, decision-making chains, approval routes, recurring rituals, SOPs |
| **TechStack** | Tools per category (CRM, dialer, comms, storage, dev, analytics), live integrations, deprecation candidates |
| **Needs** | Current pain points, desired outcomes, KPIs/OKRs, blocked work |
| **Constraints** | Regulatory, budget, geographic, data-residency, contracted obligations |
| **Resources** | Team capacity, skills available, time-of-day windows, languages |
| **MarketContext** | Industry, size band, competitors, market position |

Schema approach: typed core fields + JSONB sub-documents per entity group + a foreign-key `OrgRelationship` table for the people graph. Don't force every field rigid — value is in capturing the messy real shape.

Outputs the org persona drives:
- **Personalized access** — what functionalities each user gets
- **Personalized UI** — what each user *sees* on the platform (5-person startup ≠ 500-person regulated org; org without Drive integration doesn't see Drive widgets)
- **Inputs to Network Intelligence Layer** (see below)

### User
- `id, googleEmail, googleSub, displayName, avatarUrl, primaryOrgId, status [INVITED|ONBOARDING|ACTIVE|SUSPENDED|EXPIRED], inviterUserId (nullable for org-admin seats), createdAt, lastActiveAt, managementMode [MANAGED|EXEMPT]`
- **`managementMode = EXEMPT`** when email matches `*@gigaton.ai` (auto-set at creation; manually overridable). EXEMPT users skip onboarding wizard, persona capture (optional), re-eval cadence, and forced UI flows. They receive default native full access (`tier: internal_full`).
- **`managementMode = MANAGED`** for everyone else — full lifecycle applies.

### GuestInvite
- `id, inviterUserId, orgId, inviteeEmail, token, status [PENDING|CONSUMED|EXPIRED|REVOKED], attachedArtifactIds[], createdAt, consumedAt`
- Cap: ≤5 outstanding open invites per inviter
- Token expiry: 14 days unconsumed

### HumanPersona
- Canonical row owned by user-access-engine; replicated read-model to intelligence-silo
- Identity: `userId, googleEmail, displayName, avatarUrl`
- Context: `role, organizationName, industry, country, timezone, languages[]`
- Capabilities: `domainExpertise[], toolsUsedDaily[], decisionCategories[]`
- Preferences: `syncAsync, register, availabilityWindows, channels[]`
- Trust: `relationshipToInviter, yearsKnown, declaredTrust (capped by inviter trust)`
- Intent: `goalsOnPlatform, constraints, definitionOfSuccess`
- Meta: `status [PENDING|COMPLETE], completedAt, lastUpdatedAt`

### Capability / Policy
- `Policy { id, expression, projectScope, requires (predicate over persona+org+platform), grants (capability list), reasoning }`
- `CapabilityGrant { userId, capability, projectScope, grantedByPolicyId, grantedAt, ttl }`

### AuditLog
- `actorId, action, target, decision, reasoning, policiesEvaluated[], timestamp`

## Onboarding flows

### Stage 1 — Organization onboarding (precedes any user onboarding into that org)

1. Org provisioned (Todd at platform level, or partner self-serve later)
2. Org-onboarding wizard captures org persona (industry/size/zones/contracted projects/billing/default-access)
3. Org admin seat provisioned (one human user; their persona is captured via Stage 2)
4. Org becomes ACTIVE; eligible to invite members

### Stage 2 — User onboarding (within an org context)

**Persona is pre-populated BEFORE the invite is sent.** The wizard is a verification + gap-fill flow, not cold interrogation.

**Pre-population sources (in priority order, highest confidence first):**
1. **Inviter manual input** — relationship context, declared trust, intent, why-inviting (the inviter's tacit knowledge that the invitee couldn't easily articulate themselves)
2. **Org persona inheritance** — invitee's org defaults: industry, geographic zones, contracted projects, default-member-access profile
3. **Automated research / scraping** — public LinkedIn (name, role, current org, location, languages), public publications/talks, public web presence, Google profile metadata once OAuth completes
4. **Cross-references** — if invitee email appears in any existing platform data (Carmen Beach inquiry log, SalesOS catalog, etc.), pull what's known

**Each pre-populated field carries a `sourceConfidence` tag** (`USER_CONFIRMED` > `INVITER_ASSERTED` > `ORG_INHERITED` > `RESEARCH_SCRAPED` > `INFERRED`). Wizard surfaces low-confidence fields preferentially for verification.

**User flow:**
1. Invite issued with attached pre-populated persona draft
2. Recipient → Google OAuth → email match check; OAuth metadata enriches identity fields
3. Forced 6-step **verification + gap-fill** wizard (cannot reach any platform route until Qualified):
   - Step 1: Identity — confirm Google-pulled values (email, name, avatar) ✓ / edit
   - Step 2: Context — confirm or edit pre-populated role, org, industry, country, timezone, languages
   - Step 3: Capabilities — confirm or edit pre-populated expertise/tools/decisions; user adds gap items
   - Step 4: Preferences — user-only (rarely pre-populatable) — sync/async, register, availability, channels
   - Step 5: Trust — confirm pre-populated relationship-to-inviter, years known; declared trust (capped by inviter)
   - Step 6: Intent — pre-populated from inviter's "why-inviting" if provided; user confirms/edits/adds
4. Adaptive questioning: any field flagged low-confidence after Step 6 prompts a verification follow-up
5. On Qualified: persona stored canonically, replicated to intelligence-silo, **Access Engine computes capability set automatically**
6. User lands in platform with pre-provisioned access on the right projects at the right tier

**Why pre-population**: cold-form data collection has high abandonment and low data quality (users guess or skip); pre-populated drafts reduce cognitive load to verification, dramatically increasing completion rates and accuracy. Inviter pre-population captures relationship context the invitee couldn't easily articulate. Automated research pulls public signals the user might forget. Source confidence tagging lets the wizard target verification where it matters.

### Continuous persona re-evaluation cadence (REQUIRED)

Front-loaded calibration window, then steady-state monthly:

- Onboarding complete = Day 0
- Reviews fire at: **D+3, D+5, D+8, D+10, D+12, D+15** (6 calibration touchpoints)
- After D+15: every **30 days** automatically (D+45, D+75, D+105, ...)

**Implementation**:
- Each User has `nextReviewAt` field; daily Cloud Scheduler scans and dispatches due reviews
- Three persona-qualification states (the system tracks current state, not "review mode"):
  - **Asked** — base wizard question set has been surfaced; answers received; persona partially populated
  - **Inferred** — system has analyzed prior answers + behavioral signals + cross-references (org persona, inviter context) to identify **next questions targeted at closing gaps or qualifying/verifying earlier answers**. Adaptive questioning, not automated skipping. The wave-2 questions are produced by question-generation logic, not pulled from a fixed list.
  - **Qualified** — persona has met the **minimum onboarding requirement**: sufficient fields populated, internal consistency checks pass, behavioral signals match self-reported persona, critical gaps closed or explicitly accepted. Access computation can proceed with confidence.

**Why:** the goal of the re-eval loop is qualification accuracy, not automation. Reducing human input is a side-effect of better questions, not the objective. An "Auto silent inference" mode (which this spec previously contained) was rejected by Todd 2026-05-08 because silently propagating inferences risks compounding errors that downstream intelligence systems then treat as ground truth. The maturity is in *which* questions get asked, not in *whether* the user is asked.

**How adaptive questioning works:**
- Each review cycle, the engine computes a gap map (fields below confidence threshold, internal-consistency conflicts, behavior-vs-stated mismatches, fields that should now exist given platform tenure)
- Question-generation logic produces 2–5 follow-ups targeted at the highest-impact gaps
- User answers feed forward; persona advances toward Qualified
- Once Qualified, re-evals continue at the 30-day cadence but ask fewer/narrower questions unless new gaps appear (e.g., user changed orgs, role, project assignment)
- Each review writes a new `PersonaRevision` row (full history retained)
- Access auto-recomputes after every revision; audit logged
- User can manually trigger an early review at any time

### Continuous access re-evaluation triggers (in addition to scheduled)

- Persona update → recompute that user's capabilities
- Org persona/policy change → recompute every member of that org
- New project added to platform-registry → eligible users gain access automatically (no admin intervention)

## Consumer integration

Every Gigaton project imports a thin client:

```python
access = UserAccessClient(base_url=ACCESS_ENGINE_URL)
caps = access.capabilities_for(user_id, project="carmen-beach")
if access.can_do(user_id, action="property.create", project="carmen-beach"):
    ...
```

Carmen Beach Phase 3's hardcoded 5-role enum (`super_admin|admin|editor|operations|viewer`) gets retired in favor of engine-computed capabilities. Same for any role/permission code in SIE, gigaton-engine, decision-engine.

## Value-matrix climb (must clear all 3 in one release)

- **Functionality**: org onboarding + user invite + Google SSO + forced wizard + persona stored + access computed
- **Capability**: every Gigaton project pulls dynamic capabilities from a single engine; persona feeds Trust × Value × Priority ranker; org/persona/platform state changes propagate automatically
- **Super-ability enabled**: a Gigaton operator onboards an organization and its users such that the platform AI is **already calibrated to that human and that org from minute one** — no permission paperwork, no "tell me about yourself" friction, no role-assignment by hand. The engine does what would otherwise require an IT admin + an HRIS + a manual permissions review.

## User management modes (MANAGED vs EXEMPT)

The engine treats two user classes differently for **access management** but identically for **value delivery via upgrade notifications**.

| | MANAGED (non `@gigaton.ai`) | EXEMPT (`@gigaton.ai`) |
|---|---|---|
| Onboarding wizard | Forced — gates platform access | Skipped — full access at creation |
| Persona capture | Required | Optional (opt-in strengthens own notifications) |
| Access computation | Dynamic, persona-driven | Native `internal_full` (fast path, bypasses policy engine) |
| Re-eval cadence | Required (D+3/5/8/10/12/15 → 30d) | Skipped |
| Restricted UI | Yes | No |
| Audit logging | Yes | **Yes — exempt from constraints, not accountability** |
| Post-deploy upgrade notifications | Yes | **Yes — same engine, same algorithm** |

**Auto-detection rule**: email match `*@gigaton.ai` → EXEMPT at account creation. Manual override available for edge cases (contractor with gigaton.ai alias who should be MANAGED).

**Why the symmetry on notifications**: internal team members ship features and don't use them — they're the platform's blindest users. Per org mission to support human development, no user (internal or external) should fall behind on their own platform. Building the platform doesn't exempt you from receiving its leverage.

## Post-deploy upgrade notification system (runs for ALL users, both modes)

After every platform deploy, the Network Intelligence Layer evaluates which users would benefit from each shipped feature and pushes a "platform upgrade available" notification.

| Signal source | MANAGED | EXEMPT |
|---|---|---|
| Captured persona | ✓ | Optional (if user opted in) |
| Org persona digital twin | ✓ | N/A (Gigaton internal) |
| Behavioral signals | ✓ | ✓ |
| Role / team / project assignments | Inferred from persona | Pulled from gigaton-internal directory |
| Recent platform activity | ✓ | ✓ |
| Doctrine-relevance | Indirect | Direct (they author doctrine) |

Same algorithm, same notification pipeline, same UI surface. Different input sources. One engine, two modes.

Notification content: what shipped, why it benefits this user given their context, how to activate. Channel choice respects user preferences (in-platform badge / email / etc.).

## Gamification design layer (REQUIRED — applies across all human-operated surfaces)

Per the universal feedback rule "always include gamification when architecting human-operated systems," the user-access-engine surfaces incorporate the following mechanics. **All gamification mechanics in this engine MUST emit events to the Human Management Engine** (see `human_management_engine.md`) — gamification is the instrumented input feeding user analysis, coaching, management, and supervisor tasks. UI mechanic + event emitter ship together; neither alone is sufficient.

### Onboarding wizard
- **Progress bar with qualification state**: shows percent complete + current state (Asked / Inferred / Qualified) + which fields verified vs. pending
- **Source confidence visualization**: each pre-populated field shows a confidence badge — confirming a field upgrades it to `USER_CONFIRMED` and visually rewards the action
- **Capability unlock preview**: live counter of platform capabilities unlocked as fields are verified ("verifying your role unlocks 4 more features")
- **Completion celebration**: on reaching Qualified, surface a clear "you're in" moment with the list of platform capabilities now active for the user

### Re-eval cadence (D+3, 5, 8, 10, 12, 15, then 30d)
- **Streaks**: visible counter of consecutive completed re-evals; missed re-evals nudged with stakes-light reminders, not penalties
- **Persona-quality tier**: (Bronze / Silver / Gold / Platinum) based on field coverage × source-confidence depth × verification recency
- **Capability rewards tied to depth**: highest-tier persona unlocks Network Intelligence cross-org introductions, advanced AI assistance modes
- **Behavioral-vs-stated reconciliation**: when a flag fires, frame as "we noticed your work pattern looks like X — shall we update your profile?" not as a correctness audit

### Org persona digital twin
- **Org completeness score** + entity-group sub-scores (People X% / Processes Y% / TechStack Z% / ...)
- **Org tier**: org-level analog of persona tier — incentivizes admins to keep the org digital twin current
- **Network Intelligence visibility**: high-completeness orgs see richer cross-org signal (privacy-aware); incentive to invest in completeness

### Post-deploy upgrade notifications
- **Highlights what they unlock**, not just what shipped: "feature X is now available — your persona qualifies you for these 3 specific use cases"
- **EXEMPT users**: notifications celebrate adoption ("you shipped this — try it") without nagging

### What NOT to gamify (per the gamification feedback rule)

- Decision quality on Todd/Matt sign-off surfaces (don't pit speed against judgment)
- Trust scores in ways that incentivize gaming (declared trust is qualitative + inviter-anchored, not action-count-driven)
- Permission grants and security-sensitive flows (no confetti on access escalations)
- Compliance / audit / regulatory data (accuracy first, satisfaction second)

**Why:** gamification leverages intrinsic motivation to drive engagement and data quality; the bar is "does it make the human better at the work they came here to do." Cold persona-capture forms have high abandonment; gamified verification flows complete at much higher rates with better data accuracy. Aligns with org mission of supporting human development — the platform should make engagement satisfying, not extractive.

## Network Intelligence Layer (lives in decision-engine, NOT in user-access-engine)

Purpose: turn the aggregate of all org+user personas into automated product-development opportunity signal.

Responsibilities:
- **Aggregation**: cluster orgs/users by similarity (industry × size × tech stack × needs)
- **Gap detection**: identify functionality requests, pain points, or feature usage patterns appearing across N orgs above threshold
- **Cross-org introductions**: surface "orgs in your network that solved problem X" patterns (privacy-aware)
- **Opportunity scoring**: rank proposals by reach × impact × cost-to-build

Data flow: reads persona via the silo synced read-model (read-only). User-access-engine retains canonical persona ownership.

## Automated product-development pipeline with dual-signer routing

The flywheel closes here. Network Intelligence Layer emits product proposals → wraps each as a Decision Certificate (existing decision-engine pattern) → routes to a human signer based on decision class.

### Decision class → signer routing

| Decision class | Signer |
|---|---|
| Architecture, doctrine, platform direction, new engine artifact, schema changes | **todd@gigaton.ai** |
| Operational, feature prioritization, customer-facing changes, marketing | **matt@gigaton.ai** |
| High-stakes, irreversible, doctrine-touching | **Both** |
| Low-risk, high-confidence, reversible | Auto-approve (logged, no human in loop) — **DEFERRED to future internal intelligence systems; not a v0 capability. All decisions require a human signer until then.** |

### Sign-off mechanism

- Each pending certificate enters HUMAN approval queue
- Notification (email + UI badge); UI shows certificate, evidence, impact, signer's required action
- On signed certificate → propagates into build pipeline:
  - **v1**: auto-generate PRD + spec + ClickUp/GitHub issue routed to the right repo
  - **v2**: agent generates first PR draft against the right repo
  - **v3**: full agentic implementation with human review only at PR

This maps to the existing Decision Routing Framework maturity ladder (v1 → v3.2). The new piece is the dual-signer routing.

## Resolved decisions (locked 2026-05-08)

1. ~~**Org persona schema anchor**~~ **RESOLVED**: anchor to **Carmen Beach owner model** (operational fields) + **Ti Solutions client model** (industry/size/billing dimensions), then extend with the People/Processes/TechStack/Needs/Constraints/Resources/MarketContext groups. *Why: these are the most concretely-defined real-world entities in the existing codebase — start from working schemas to reduce greenfield invention and preserve data already collected from real orgs.*
2. ~~**HumanPersona storage owner**~~ **RESOLVED**: `user-access-engine` owns the canonical row; replicates a read-model to `intelligence-silo`. *Why: keeps sensitive identity behind the auth boundary (single audit point, single schema-evolution authority); silo gets eventual-consistency read access without write access (CQRS); avoids two-master sync conflicts.*
3. ~~**Policy expression**~~ **RESOLVED**: hybrid — code defines available rule shapes (predicates + capability sets); data binds them to orgs (which rules apply at what tier). *Why: code-only requires a developer for every org-policy change (high-friction); data-only invites unsafe expressiveness (admin-authored DSL = attack surface); hybrid mirrors OPA/Cedar — developers ship safe primitives, admins compose them via UI.*
4. ~~**OAuth scope**~~ **RESOLVED**: minimal `openid email profile` for v0. *Why: smallest viable scope to verify identity; richer scopes (Drive, Gmail, Calendar) get requested later as opt-in capability grants tied to specific features; reduces friction at first consent screen and minimizes blast radius if a token leaks.*
5. ~~**Trust cap mechanic v0**~~ **RESOLVED**: manual seed — Todd = 1.0, Matt = 1.0; initial guests default to 0.5 unless Todd/Matt explicitly raise. Computed CxGuy Trust×Value×Priority replaces seeded trust once `cxguy-methodology` is integrated. *Why: persona Step 5 (declared trust capped by inviter) requires an inviter trust score to exist; CxGuy is a separate repo not yet integrated; manual seeding gives a working v0 without blocking on cross-repo work; the swap to computed trust is contained when CxGuy lands.*
6. ~~**Migration plan for Carmen Beach Phase 3 roles**~~ **REVISED 2026-05-09 per Todd directive**: Carmen Beach Phase 3 **integrates with gignet platform from the start** — does NOT ship a hardcoded enum first. UAE v0 ships stub capability-check + audit-log endpoints on Mon 2026-05-11; Phase 3 wires its thin client to those stubs immediately. Migration is iterative as UAE matures, not phased. *Why (revised): Phase 3 shipping its own hardcoded RBAC creates Phase 4 migration debt that contradicts SMEN sovereignty (Carmen Beach must not own user identity logic — that belongs to platform per the Gigaton-Owned vs Vertical-Owned Scope Doctrine, `gigaton_scope_doctrine.md`). Integrating from the start means thin-client calls can be stubbed initially and matured in place; aligns with the rule that engines NOT specific to real-estate / Playa-del-Carmen are Gigaton-owned and consumed BY gignet platform + intelligence platform > portal.* (Prior resolution from 2026-05-08 — ship hardcoded enum first, migrate Phase 4 — is superseded.)
7. ~~**Re-eval mode threshold**~~ **RESOLVED**: progression is **Asked → Inferred → Qualified**. The maturity is in *which* questions get asked (adaptive questioning targeting gaps + verification of prior answers), not in whether the user is asked. *Why: silently auto-inferring persona fields risks compounding errors that downstream intelligence systems treat as ground truth; better questions close gaps faster than removing the human from the loop. Reducing human input is a side-effect of better questions, not the objective.*
   - **Sub-question RESOLVED**: persona is **pre-populated before invite send** (inviter manual + org inheritance + automated research/scraping + cross-references) and the wizard becomes a verification + gap-fill flow. Each field carries a `sourceConfidence` tag (`USER_CONFIRMED` > `INVITER_ASSERTED` > `ORG_INHERITED` > `RESEARCH_SCRAPED` > `INFERRED`); adaptive questioning prioritizes verification of low-confidence fields. *Why: cold-form data collection has high abandonment and low data quality; pre-populated drafts reduce cognitive load to verification, dramatically increasing completion rates and accuracy. Inviter pre-population captures relationship context the invitee couldn't easily articulate; automated research pulls public signals the user might forget; source-confidence tagging directs verification effort where it matters.*
8. ~~**Network Intelligence privacy boundary**~~ **RESOLVED**: anonymized signal by default; opt-in identity disclosure per org for cross-org introductions. *Why: aggregate patterns ("3 orgs in your sector solved problem X with feature Y") deliver high value without revealing identities; identity disclosure is a privacy escalation requiring explicit consent; opt-in unlocks "introduce me to org Z" once that org has marked itself discoverable.*
9. ~~**Auto-approve threshold for product-dev decisions**~~ **DEFERRED**: governed by future internal platform intelligence systems. Until those land, all product-dev decisions require a human signer per the Todd/Matt routing matrix. *Why: setting the auto-approve bar requires platform-level confidence calibration that doesn't exist yet — the system must observe many decision/outcome pairs before earning the right to skip humans. Defining the threshold prematurely would be guessing; future internal intelligence will derive it empirically.*
10. ~~**EXEMPT user notification default channel**~~ **RESOLVED**: in-platform badge + weekly email digest of post-deploy notifications. **No Slack auto-posts.** Per-user configurable. *Why: in-platform badge is non-intrusive and visible at next platform login; weekly email digest reduces interruption while ensuring nothing is missed; the existing Slack-is-user-level-only feedback memory explicitly prohibits Slack auto-posts from background jobs.*
11. ~~**EXEMPT contractor edge case**~~ **RESOLVED**: default `*@gigaton.ai` → EXEMPT. Override flag `forcedManagementMode = MANAGED` available via admin UI; **only Todd or Matt can flip the mode**. Any flip writes to `audit_log` with a required WHY field. *Why: auto-detection is a heuristic and real-world contractor patterns need an escape hatch; restricting flip authority to dual-signers prevents accidental mode changes on sensitive accounts; required WHY field makes mode flips intelligible to downstream intelligence systems per the always-record-WHY rule.*
12. ~~**EXEMPT default access scope**~~ **RESOLVED**: `internal_full` is broad by default but excludes a small explicitly-tagged "restricted" capability set: billing portal, secrets management, compliance audit logs, contractual data on partner orgs, production-data destructive operations. Restricted capabilities require explicit grant from Todd or Matt. *Why: full access for internal team eliminates friction on the 99% of features; restricting the sensitive set protects against insider error or compromise on irreversible operations; matches principle of least privilege without imposing onboarding overhead.*

## Minimum onboarding requirement (RESOLVED 2026-05-08 — gates `Qualified` state)

The bar to advance from `Inferred` → `Qualified` is **three-pronged**. All three must be satisfied; failure on any one keeps the user in `Inferred` with adaptive questioning continuing.

### Prong 1 — Profile qualifications

- **Mandatory fields**: identity (email, name, role, primary org), context (industry, country, timezone), capability (≥3 expertise tags), trust (relationship to inviter), intent (≥1 platform goal)
- **Consistency predicates**: org claimed in Step 2 must match invitation org OR be flagged for human review; languages claimed must include ≥1 supported by platform UI; declared trust ≤ inviter's trust cap
- **Behavioral-vs-stated tolerance**: at D+3 review N/A (no behavioral data yet); from D+5, claimed expertise X with zero engagement on X-related features after 7 days → re-qualification flag (re-ask, not auto-demote)

### Prong 2 — System-value matching (≥10 Gigaton systems identified as value-providers)

The Access Engine must identify **no fewer than 10 Gigaton systems/features** that match this user's persona as value-providers before they reach `Qualified`. This is proof the platform actually serves them, not just admits them.

**Architectural placement**: a new sub-component — **Gigaton System-to-User Matcher** — lives **inside `user-access-engine`** (not in decision-engine's Network Intelligence Layer; that's cross-org pattern detection, this is individual-user qualification).

**Inputs**:
- The user's persona (capabilities, role, intent, context, preferences, language, expertise)
- The user's org persona (industry, contracted projects, tech stack, needs, constraints)
- The **Gigaton System Registry** — a queryable catalog of every shippable Gigaton system, feature, or capability with metadata: applicable_personas, applicable_orgs, value_proposition, prerequisites, surface_routes
- Inviter trust score and intent (the inviter's "why-inviting" feeds intent matching)

**Output**: ranked list of ≥10 Gigaton systems with a per-system match score and a one-sentence value rationale. Stored as `UserValueMatchSet` (history retained — feeds re-eval).

**If <10 matches found**: persona stays `Inferred`. Engine triggers adaptive questioning to enrich the persona until ≥10 matches surface OR escalates to human review (Todd or Matt) for an inviter who keeps inviting users the platform can't serve.

### Prong 3 — Intelligence audit

All relevant Gigaton intelligence must be surfaced and applied to the user's context before they reach `Qualified`.

**Baseline audit** (every user):
- Canonical first principles (per `gigaton_canonical_first_principles.md` — 7 non-negotiables, 15 principles, 8 ethos filters, 17 frameworks, 12 anti-patterns)
- Drift Sentinel doctrine conformance — this user's planned access does not violate doctrine
- CxGuy methodology Trust×Value×Priority ranker once integrated

**User addon audits** (extensible framework):
- Example named by Todd: **"uniqueness value vs alt network entity detractor"** — for this user, the engine evaluates what makes them uniquely valuable to the network AND what alternatives exist that detract from their value relative to those alternatives. Output: a uniqueness-value score with reasoning.
- Future addons: org-specific audits (the user's org may require its own intelligence overlay), vertical-specific audits (real estate, life settlements, MMM), regulatory audits (compliance-bound contexts)

**Audit framework is extensible**: each audit is a named module with `(persona, orgPersona, platformState) → AuditResult { passed, findings[], score }`. Engine composes baseline + applicable addons; all must pass for `Qualified`.

### Why (composite)

A user qualification gate built only on data completeness is the wrong bar — it tells you the platform knows them, but says nothing about whether the platform can serve them or whether platform doctrine has been honored. The three-prong bar enforces:

- **Prong 1** ensures the persona is *trustworthy enough to act on* (data quality)
- **Prong 2** ensures the platform *actually delivers value to this user* — if the engine can't surface 10 systems that benefit them, the platform shouldn't admit them yet (prevents dead-weight users; forces the engine to work hard for every user; aligns with org mission to support human development)
- **Prong 3** ensures the platform's *intelligence and doctrine apply* to this user's context — first principles aren't optional; user-specific addons capture the value-vs-alternatives framing that distinguishes Gigaton from generic platforms

Combined: a user reaches `Qualified` only when the platform has demonstrated value, applied doctrine, and earned the right to grant them access — not merely collected enough data.

### Gamification surface for the requirement

Per the always-include-gamification rule, the wizard surfaces all three prongs visibly during onboarding:

- **Profile qualifications** — percent fields verified, source-confidence breakdown
- **System-value matching** — live counter ("we've identified 14 Gigaton systems that will benefit you"); each new match unlocked surfaces a one-line value rationale; user feels the platform working for them in real time
- **Intelligence audit** — visible audit checklist (first principles ✓, drift conformance ✓, uniqueness-value score: +47); audits earn badges on completion
- **Qualified celebration** — clear "you're in" moment on reaching `Qualified`, surfacing the matched systems and the audit score as the proof of platform fit

### Open implementation sub-tasks (handled during v0 build)

- Build the **Gigaton System Registry** (queryable catalog) — likely seeds from existing tool/integration registry + platform-state metadata
- Build the **User-System Matcher** algorithm (rules-based first; ML-augmented later)
- Implement the audit framework (baseline + addon plugin pattern)
- Implement the "uniqueness value vs alt network entity detractor" addon as the first non-baseline audit
- Final tuning of all three prongs against real onboarding telemetry once v0 is live
7. ~~**Re-eval mode threshold**~~ **RESOLVED 2026-05-08**: progression is **Asked → Inferred → Qualified** (not Asked → Inferred → Auto). The maturity is in *which* questions get asked (adaptive questioning targeting gaps + verification of prior answers), not in whether the user is asked. Goal = qualification accuracy, not automation. *Why: silently auto-inferring persona fields risks compounding errors that downstream intelligence systems treat as ground truth; better questions close gaps faster than removing the human from the loop. Reducing human input is a side-effect of better questions, not the objective.* Remaining sub-question: define the **minimum onboarding requirement** quantitatively — which fields are mandatory, what consistency-check predicates must pass, what behavioral-vs-stated mismatch tolerance is acceptable.
8. **Network Intelligence privacy boundary** — when surfacing "orgs in your network that solved problem X," is org identity revealed or anonymized? Opt-in per org?
9. ~~**Auto-approve threshold for product-dev decisions**~~ **DEFERRED 2026-05-08**: governed by future internal platform intelligence systems to be integrated later. Until those land, **all product-dev decisions require a human signer** per the routing matrix (Todd / Matt / both). Auto-approve is not a v0 capability. *Why: setting the auto-approve bar requires platform-level confidence calibration that doesn't exist yet — the system must observe many decision/outcome pairs before it has earned the right to skip humans. Defining the threshold prematurely would be guessing; future internal intelligence will derive it empirically from decision-outcome correlation.*
10. **EXEMPT user notification preferences** — default channel (in-platform badge / email / Slack-equivalent) for `@gigaton.ai` users? Note Slack-is-user-level-only feedback memory — system shouldn't auto-post to Slack from background jobs.
11. **EXEMPT contractor edge case** — is there a contractor pattern where someone has a `@gigaton.ai` alias but should be MANAGED (e.g., a contracted advisor)? Define the manual-override path and who can flip the mode.
12. **EXEMPT default access scope** — does `internal_full` mean literally every capability across every project, or does it still respect role boundaries within Gigaton (e.g., billing/finance restricted to specific employees)?

## How to apply

When this lands in deployment planning or someone asks "where does invite/auth/onboarding/access live in the Gigaton platform?" — point at this spec. Do not conflate with the Carmen Beach AffiliateInvite (different layer, different purpose). Treat user-access-engine as a sibling to decision-engine — same artifact class, same deployment pattern.
