# Prompt Suggestor + Saved Prompts + Entity / Action Color-Coding — Assessment

**Date**: 2026-05-26
**Author**: investigation thread (Opus 4.7) for Todd
**Type**: investigation + spec (no code)
**Goal**: verify the "most human development + instant system alignment from
initial use" surface for new operators; identify what's spec'd, what's built,
what's a stub, what's missing.

---

## 0. TL;DR — top-line findings

1. There is **no `PromptSuggestor` component** anywhere. A
   `PLACEHOLDER_PROMPTS` array of 5 hard-coded strings inside `ChatPage.tsx`
   is the entire "suggested prompts" surface today.
2. There is **no saved-prompts / favorites / starred-prompt feature**
   anywhere (UI, backend, schema). MISSING end-to-end.
3. **The richest available source for suggested prompts is already seeded
   but not consumed**: `persona-engine` ships 9 OrgPersonas × ~5
   `example_questions` each (~45 high-quality, role-scoped prompts) at
   `api/executive_org_personas/seed/executive_org_personas.yaml`.
   These reach `gigaton-gateway` (routed at
   `gigaton-gateway/api/routing_table.py:204-211`) but **no FE caller
   exists** — `gigaton-ui-system/services/personaClient.ts` exposes
   `getOrg`/`upsertOrg`/etc. but NOT `listExecutivePersonas`.
4. **Entity color-coding** is MISSING from the schema and the UI. The
   `client_namespaces` table (UAE) has no `brand_color` / `palette` /
   `theme` column. Every operator renders in the same purple chrome
   (`#662D91`) inherited from Gigaton chat. The entity selector in
   `ChatPage.tsx:54-60` is a plain `<select>` with no visual differentiator.
5. **Action/task status colors** partially exist as ad-hoc per-page maps —
   `ConnectorsPage.tsx:150-157`, `ConnectorWhatsAppPage.tsx:66`,
   `ConnectorGmailPage.tsx:58`, `ConnectorStripePage.tsx:44`,
   `ConnectorGoogleCalendarPage.tsx:57`, `AdminReviewQueuePage.tsx:333-336`,
   onboarding `ProviderCredentialPanel.tsx:75`. **No shared `StatusPill`
   primitive** — each page reimplements the palette inline.

---

## 1. Prompt Suggestor — current state

### 1A. What exists

| Artifact | Path | Lines | What it does |
|---|---|---|---|
| `PLACEHOLDER_PROMPTS` | `gigaton-ui-system/pages/ChatPage.tsx` | 62-68 | Hard-coded `string[]` of 5 prompts (rotational placeholder + first-load grid) |
| First-load grid | `gigaton-ui-system/pages/ChatPage.tsx` | 310-321 | Renders `PLACEHOLDER_PROMPTS.slice(0, 4)` as 4 clickable cards when `messages.length === 0` |
| Random placeholder | `gigaton-ui-system/pages/ChatPage.tsx` | 78-80 | Picks one of 5 prompts as the textarea `placeholder` attr |
| OrgPersona `example_questions` (seed) | `persona-engine/api/executive_org_personas/seed/executive_org_personas.yaml` | 43-48, 83-88, 123-128, 165-170, 207-212, 249-254, 290-295, 331-336, 373-378 | 9 personas × 5 questions each = 45 high-quality role-scoped prompts |
| OrgPersona schema field | `persona-engine/api/executive_org_personas/schema.py` | 79 | `example_questions: list[str]` (validated 3-5 per persona) |
| OrgPersona list endpoint | `persona-engine/api/executive_org_personas/endpoints.py` | 34, 38-55 | `GET /v1/executive-personas` returns `{items, count}` |
| Gateway route to persona-engine | `gigaton-gateway/api/routing_table.py` | 204-211 | `/v1/executive-personas` + `/v1/executive-personas/` → `persona-engine` |

### 1B. What is stub vs functional

| Capability | State | Evidence |
|---|---|---|
| Show suggested prompts on first chat load | FUNCTIONAL (degenerate) | `ChatPage.tsx:310-321` — but only 4 hard-coded strings, none operator-scoped, none persona-derived |
| Operator-scoped suggestions | MISSING | no fetch, no service, no context wiring |
| Persona-derived suggestions | MISSING (data ready, consumer absent) | `personaClient.ts:165-189` only ships `getOrg`/`upsertOrg`/`patchOrg`; no `listExecutivePersonas` method |
| Suggestions that adapt over time | MISSING | no usage/coaching graduation hooks in chat surface |
| Suggestions surfaced after first turn | MISSING | grid disappears as soon as `messages.length > 0` |
| Suggestions inside onboarding | INDIRECT | `ChatOnboardingOrchestrator.tsx:177-216` renders affordance-specific buttons (`MultipleChoiceAffordance`, etc.) — but those are intent-driven, not prompt-suggestions |

### 1C. Is it surfaced in chat today?

**Yes — degenerately.** Per `ChatPage.tsx:300-322`, when `messages.length === 0`
the user sees a 2×2 grid of 4 hard-coded prompts. Click → populates input
(not auto-send). On second turn the surface is gone forever for that session.

There is no:
- per-operator personalization
- persona-aware ranking
- "show me other prompts" affordance
- graduation / fade-out as operator demonstrates competence

---

## 2. Saved Prompts — current state

### 2A. What exists

**MISSING.** Comprehensive grep across `gigaton-ui-system/`, `decision-engine/`,
`master-knowledge-base/`, `persona-engine/`, `user-access-engine/`,
`intelligence-silo/`, `gigaton-gateway/` for:

- `saved prompt`, `saved_prompt`, `saved-prompt`
- `favorite prompt`, `favorite_prompt`, `prompt_favorite`
- `starred prompt`, `starred_prompt`
- `prompt librar`, `prompt_libr`
- `bookmark prompt`, `prompt bookmark`

→ **zero matches** for any UI component, hook, service, schema, route, or
runbook.

### 2B. Adjacent functionality that is NOT a saved-prompt feature

- `ReviewQueue` (`AdminReviewQueuePage.tsx`) — saves DRIFT / review items,
  not user prompts.
- `OAuth credentials` persistence — saves provider creds, not prompts.
- `Connector status` cache — saves connector state, not prompts.

### 2C. Closest existing primitive (could be repurposed)

- `client_namespaces.decision_preferences` JSONB
  (`user-access-engine/api/models/client_namespaces.py:101`) is the
  natural home for per-operator prompt favorites — but is currently used
  for decision-engine routing preferences only.

---

## 3. Color-coding — current state

### 3A. Entity color-coding (operator → palette)

**MISSING from schema.** `client_namespaces` ORM
(`user-access-engine/api/models/client_namespaces.py:54-134`) has NO column
for `brand_color`, `palette`, `theme`, `accent`, or `chrome`. Fields present:

```
namespace_id, parent_entity_id, display_name, business_goals,
voice_brand_logic_ref (text ref — opaque), workflows, stakeholders,
integrations, offer_catalog_ref, revenue_model, decision_preferences,
memory_filter, retrieval_policy, governance_overlays,
first_principle_variable_overrides, multi_axis_tags, lifecycle_state,
parent_operator_id, created_at, updated_at
```

`voice_brand_logic_ref` is a text reference to an external brand doc — not
a typed color/palette.

**MISSING from UI.** Entity selector at `ChatPage.tsx:279-287` is an
unstyled `<select>`. Selected entity is stored in state
(`ChatPage.tsx:75`, `setEntityContext`) and sent in the chat request body
(`ChatPage.tsx:166`) — but is never used to mutate any visual style.

The single chrome color `#662D91` (Gigaton purple) is hard-coded across:
- `ChatPage.tsx:268, 302, 311 (border), 362, 376` (chat surface)
- `NavRail.tsx:42-43, 69` (left rail background, active circle)
- `DashboardPage.tsx:157, 219-222, 258, 300, 303, 316, 334, 349` (dashboard buttons)

Every operator — Gigaton, PDC, Ti Solutions, LiquiFex, InContekst, Multipli,
Carmen Beach DMS, etc. — sees the identical purple shell.

### 3B. Action / task status color-coding

**Partial — uncoordinated.** Status palettes are duplicated across pages:

| File | Lines | Pattern |
|---|---|---|
| `ConnectorsPage.tsx` | 150-157 | `connected=emerald, disconnected=white, testing=sky, failed=red, pending=amber` |
| `ConnectorWhatsAppPage.tsx` | 66 | `pending=amber` (same hex token, redeclared) |
| `ConnectorGmailPage.tsx` | 58 | same redeclared |
| `ConnectorStripePage.tsx` | 44 | same redeclared |
| `ConnectorGoogleCalendarPage.tsx` | 57 | same redeclared |
| `AdminReviewQueuePage.tsx` | 333-336 | `pending_review=amber, rerun_pending=purple, rerun_complete=purple` |
| `ProviderCredentialPanel.tsx` | 75-... | `StatusPill` (local component, not exported) |

**Action/task entities specifically.** `services/reviewApi.ts:247` declares
`status: 'queued' | 'in_progress' | 'complete'` but no page color-maps that
triplet. Tasks emitted via the chat-orchestrator onboarding flow
(`ChatOnboardingOrchestrator.tsx`) carry status implicitly via
`current_stage_actions_completed[]` (state) but DOM does not show colored
chips for queued vs completed individual actions inside the chat bubble.

There is no `OnboardingActionStatus`, `TaskCard`, `ActionChip`, or
`ActionQueue` component. The closest is `OnboardingSidePanel.tsx` (tier
progress, not action status).

### 3C. Where this matters most

1. **Chat header** (`ChatPage.tsx:266-296`) — single most-visited surface
   for a new operator; entity selector at line 279 is the natural place
   to render the entity's color as a chip + tint the chrome accent.
2. **Nav rail** (`NavRail.tsx:42, 69`) — active circle background uses
   `#662D91`; should pick up the active entity color.
3. **Action affordances inside chat** (`ChatOnboardingOrchestrator.tsx:215`)
   — each stage's open action is a chat bubble; needs status color
   (pending/in-progress/blocked/done) for the "operator just glanced at
   chat — what do I owe Gigaton?" scan.
4. **Side panel** (`OnboardingSidePanel.tsx`) — shows tier progress; should
   surface per-action status chips matching the action queue colors.

---

## 4. New-operator onboarding flow — "instant alignment from first use"

### 4A. The flow today

When a new operator hits `/chat` for the first time
(`ChatPage.tsx:252-411`):

1. `<NavRail>` renders with all circles greyed-out except `chat`
   (`onboarding_v1.yaml:84-90`).
2. `<ChatOnboardingOrchestrator>` mounts unconditionally
   (`ChatPage.tsx:329-336`); shows "Loading your onboarding plan…"
   (`ChatOnboardingOrchestrator.tsx:165-174`).
3. Manifest + state load → stage-0 opens with `opening_message` from
   `onboarding_v1.yaml:950-954` ("Welcome to Gigaton…").
4. The next open action's affordance renders (`AFFORDANCE_COMPONENTS`,
   `ChatOnboardingOrchestrator.tsx:53-67`).
5. In parallel, the empty-state `PLACEHOLDER_PROMPTS` grid renders
   (`ChatPage.tsx:300-322`) — **collision risk**: the onboarding
   orchestrator and the empty-state grid display simultaneously when
   `messages.length === 0`. The grid is 4 generic prompts unrelated to
   the operator's onboarding stage.

### 4B. What new operators DO see

- Welcome message (manifest-driven, generic — same for every operator).
- Affordance for stage-0 trust-scope action (typed by `affordance_resolution`
  in `onboarding_v1.yaml:883-946`).
- 4 generic prompts: "What pricing strategy should I use for a 2BR…",
  "Score this lead…", "Draft a property description for Casa Azul…",
  "Explain the RTQL trust tier system." — **all PDC/real-estate biased.**
  A LiquiFex operator or Multipli operator gets the same 4 vacation-rental
  prompts — concretely off-brand.

### 4C. What new operators DON'T see

| Cue | State | Why it matters |
|---|---|---|
| Their entity color / brand chip | MISSING | "Whose Gigaton is this?" answered only by the `<select>` text |
| Persona-relevant suggested prompts | MISSING | 45 persona-tuned prompts sit unused in persona-engine |
| Saved prompts | MISSING | no one has ever saved one — feature absent |
| Action status color | INCONSISTENT | varies per page; chat-orchestrator action bubbles have no status chip |
| "Try one of these" graduated suggestions | MISSING | once `messages.length > 0`, suggestions vanish forever |

---

## 5. Gaps + recommendations

### 5A. What works today (concrete)

- `ChatPage.tsx:300-322` — first-load empty-state grid (4 prompts, click
  to populate, not auto-send). Demonstrates the affordance pattern;
  needs operator-scoping + persona-scoping.
- `ChatOnboardingOrchestrator.tsx:177-235` — chat-first directed
  affordance dispatch is shipped and working; the muscle for "render an
  in-chat suggestion card the user can click" is already there.
- `persona-engine/api/executive_org_personas/seed/executive_org_personas.yaml`
  — 45 role-scoped prompts are seeded, validated by the
  `example_questions: list[str]` field
  (`api/executive_org_personas/schema.py:79`).
- `persona-engine/api/executive_org_personas/endpoints.py:38-55` +
  gateway routing (`gigaton-gateway/api/routing_table.py:204-211`) —
  endpoint reachable from FE today.
- `ConnectorsPage.tsx:150-157` — best-in-class shared `STATUS_PILL`
  pattern; can be extracted as the canonical primitive.

### 5B. What is stub / partial

- `PLACEHOLDER_PROMPTS` — hard-coded 5 strings, PDC-biased; no
  persona/operator scoping.
- Per-page status palettes — same hex tokens redeclared 6 times.
- Entity selector — functional state binding, zero visual brand cue.
- `voice_brand_logic_ref` (`client_namespaces`) — text reference, opaque,
  not a typed color palette.

### 5C. What is completely missing

1. `PromptSuggestor` component (any form).
2. `useSuggestedPrompts(operatorId, primaryPersonaId)` hook.
3. `personaClient.listExecutivePersonas()` method.
4. Saved-prompts schema (column / table).
5. Saved-prompts UI (star button on user message, "saved" panel).
6. `client_namespaces.brand_color` (or `theme_token`) column.
7. `EntityChip` component (color + name).
8. `useEntityTheme(namespaceId)` hook.
9. Shared `StatusPill` primitive in `gigaton-ui-system/components/`.
10. `ActionStatus` chip inside the onboarding orchestrator action bubble.

### 5D. Proposed minimum viable feature set

A scope tuned to "most human development + instant alignment from first
use" — five capabilities, NOT a full prompt-library product:

#### MVP-1. Persona-derived suggested prompts on first chat load

- New `useSuggestedPrompts(operatorId)` hook:
  - Fetches operator's primary persona from `client_namespaces`
    (or defaults to `ceo` when unknown).
  - Calls `GET /v1/executive-personas/{primary_persona_id}` → uses
    that record's `example_questions[]` (3-5 prompts).
  - Optionally calls `/v1/executive-personas?tag=axis:executive` to get
    a 2nd-pass blend of cross-functional questions for breadth.
- New `<PromptSuggestor>` component:
  - Renders 3 prompts on `messages.length === 0` (replaces the 4-card
    grid in `ChatPage.tsx:310-321`).
  - Renders a collapsed "Try a prompt" pill ABOVE the input box after
    `messages.length > 0` — click to re-expand. **This is the
    graduation surface.**

#### MVP-2. Saved prompts (per-operator favorites)

- New UAE alembic migration: `0017_saved_prompts.py` adds table
  `saved_prompts (id PK, namespace_id FK, user_id, prompt_text,
  created_at, last_used_at, use_count, tags JSONB)`.
- New persona-engine OR gateway routes: `GET/POST/DELETE
  /v1/operators/{namespace_id}/saved-prompts`.
- New `<SaveAsPromptButton>` (a star icon) on user `<MessageBubble>`.
- New `<SavedPromptsDrawer>` accessible from chat header (alphabet icon).

#### MVP-3. Entity color column on `client_namespaces`

- New UAE alembic migration: `0018_namespace_brand_color.py`
  adds `brand_color text` (hex, validated `^#[0-9A-Fa-f]{6}$`),
  `brand_color_accent text` (lighter shade for hover/active),
  `brand_secondary_color text` (optional 2nd entity-cue chip), all
  nullable, defaulting to NULL (root operators stay on Gigaton purple
  until overridden).
- Seed migration patches the existing 5-6 namespaces with proposed
  colors (see §5F).
- Gateway `/v1/operators/{namespace_id}/persona` already returns the
  namespace blob — no new route needed; FE reads the colors from it.

#### MVP-4. Entity color rendered in chat header + nav rail

- New `<EntityChip namespaceId={selectedEntity} />` component:
  rendered to the right of the entity `<select>` in
  `ChatPage.tsx:279-287`.
- `<NavRail>` (`components/NavRail.tsx:42, 69`) reads
  `useEntityTheme(activeNamespaceId)` and tints the active circle
  background + accent border with the operator's color.
- Chat send button (`ChatPage.tsx:376`) tints with operator color.

#### MVP-5. Shared `<StatusPill>` + per-action status in chat-orchestrator

- New `gigaton-ui-system/components/StatusPill.tsx` consolidating the
  per-page palettes:
  - `done / complete` → emerald
  - `in_progress / testing / running` → sky
  - `pending / queued / waiting` → amber
  - `blocked / failed / needs_reauth` → red
  - `idle / disconnected / unknown` → neutral-white
- Migrate `ConnectorsPage.tsx:150-157` and the four `Connector*Page.tsx`
  files to import from this primitive (purely cosmetic — no behavior
  change).
- Wire `<StatusPill>` into `ChatOnboardingOrchestrator.tsx:215` so each
  open action shows its status alongside the affordance.

### 5E. Implementation roadmap (5 small PRs, dependency-ordered)

| # | PR | Repo | Est. LOC | Blocks on |
|---|---|---|---|---|
| 1 | `shared StatusPill primitive + retire per-page palettes` | gigaton-ui-system | ~120 (new component + 6 file migrations) | nothing |
| 2 | `namespace brand_color column + seed existing 5 ops` | user-access-engine | ~180 (alembic 0017 + seed 0018 + model update + tests) | nothing |
| 3 | `EntityChip + useEntityTheme + tint chat header / nav rail / send` | gigaton-ui-system | ~200 | PR #2 |
| 4 | `useSuggestedPrompts hook + PromptSuggestor + persona client method` | gigaton-ui-system | ~220 (component + hook + service method + ChatPage wire) | nothing (persona-engine endpoint already shipped via PR #12) |
| 5 | `saved_prompts table + CRUD routes + SaveAsPromptButton + SavedPromptsDrawer` | user-access-engine + gigaton-gateway + gigaton-ui-system | ~350 (migration + 3 routes + 2 components + drawer + tests) | PRs #1, #3 (uses StatusPill + EntityChip) |

**Wave 2 coaching-graduation bridge.** Once MVP-1 ships, the same
`example_questions` payload should:
1. Feed the Wave-2 Ti Agent Matrix (per
   `persona-engine/api/executive_org_personas/seed/executive_org_personas.yaml:54-58`
   ppim_signature `decision` / `strategic_optionality`) so the
   prompt-suggestor's "What did the operator click last week?" telemetry
   becomes input to per-persona competence scoring.
2. Decay / "graduate away" once the operator demonstrates competence —
   the suggestion list shortens, then collapses, then disappears, per
   the master plan's tier_5_live autonomy gate
   (`master-knowledge-base/manifests/onboarding_v1.yaml:75-79`).
3. Persist saved prompts AS evidence in `capabilities_verified[]` on
   the operator's HumanPersona record
   (`persona-engine/services/personaClient.ts` HumanPersona type,
   `capabilities_verified` field) — closes the loop with the trust-tier
   system.

### 5F. Color palette + UX details (concrete)

**Entity color seed (proposed)** — applied via alembic 0018 against
the 6 namespaces in production:

| namespace_id | display_name | brand_color | accent | rationale |
|---|---|---|---|---|
| `gigaton` | Gigaton AI | `#662D91` | `#7B35AA` | current canonical purple (preserve) |
| `carmen-beach` (PDC) | Carmen Beach Properties | `#0E8FB3` | `#16ABCC` | PDC ocean teal — already used in `playadelcarmen.homes` chrome |
| `ti-solutions` | Ti Solutions | `#1F4F7A` | `#2D6FA8` | Ti slate-blue (managed-services gravitas) |
| `liquefex` | LiqueFex | `#2BB673` | `#3FCC8A` | financial green (portfolio scenarios) |
| `multipli` | Multipli | `#E2792B` | `#F18B40` | vendor-growth orange (energy / growth) |
| `incontekst` | InContekst | `#7E22CE` | `#9B3FE0` | violet variant (sits under Gigaton root) |

Additional placeholders for the entity hierarchy in
`/Users/admin/.claude/projects/-Users-admin/memory/entity_hierarchy_for_namespace_seed_2026_05_26.md`:

| namespace_id | brand_color | accent |
|---|---|---|
| `cbp-walking-tour` | `#F4A53A` | `#F9BC68` |
| `cbp-dms` | `#34708C` | `#4A8FAE` |
| `kollosche` | `#0B2545` | `#13396B` |
| `medvidi` | `#C2185B` | `#D8417F` |
| `mcgrath` | `#8B0000` | `#A82020` |
| `carerev` | `#0EA5E9` | `#22B2F0` |
| `integra-ccs` | `#475569` | `#5B6B7E` |

The 13-entity palette stays a 14-color set (Gigaton + 13 leaves) — meets
Todd's "instant brand alignment" directive without auto-generation.

**Action / task status palette (canonical)** — to land in MVP-5:

| status | bg | text | border | symbol |
|---|---|---|---|---|
| `done` / `complete` / `connected` | `bg-emerald-500/20` | `text-emerald-200` | `border-emerald-400/40` | check |
| `in_progress` / `running` / `testing` | `bg-sky-500/20` | `text-sky-200` | `border-sky-400/40` | spinner |
| `pending` / `queued` / `waiting` | `bg-amber-500/20` | `text-amber-200` | `border-amber-400/40` | clock |
| `blocked` / `failed` / `needs_reauth` | `bg-red-500/20` | `text-red-200` | `border-red-400/40` | x-circle |
| `idle` / `disconnected` / `unknown` | `bg-white/10` | `text-white/60` | `border-white/20` | dot |

Matches the de-facto palette already used in `ConnectorsPage.tsx:150-157`,
preserves muscle memory.

**First-load chat UX (with MVPs 1-5 shipped)**:

```
┌────────────────────────────────────────────────────────────────┐
│  [G] Gigaton AI · Decision-engine augmented · claude            │
│        ┌──────────────────┐ ┌─── color chip ───┐                │
│        │ PDC          ▾  │ │ ░░ #0E8FB3       │ [New chat]     │
│        └──────────────────┘ └──────────────────┘                │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Welcome to Gigaton, PDC.                                        │
│  Pick a starting question — or just type.                        │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ How does this change our 3-year revenue trajectory?     │    │  ← from CEO persona
│  └─────────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ What's the fully-loaded cost and measurable payback?    │    │  ← from CFO persona
│  └─────────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Which BFT variable does this move?                      │    │  ← from CXOO persona
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ▸ Saved prompts (3)                                  ▸ More    │
│                                                                  │
├────────────────────────────────────────────────────────────────┤
│  Stage 0 — Trust + Scope · [pending] ●                          │  ← StatusPill
│  (onboarding affordance renders here)                            │
└────────────────────────────────────────────────────────────────┘
```

---

## 6. Decisions Todd needs to make (gate before any PR)

1. **Migration timing.** Per
   `/Users/admin/.claude/projects/-Users-admin/memory/migration_is_value_blocking_2026_05_25.md`,
   the GCP carmen-beach → gigaton-platform engine migration is value-
   blocking. PRs #2 + #5 touch UAE schema; they should go AFTER
   migration soak (not during) to avoid alembic head-divergence between
   the two GCP projects.
2. **Persona for "primary persona unknown" default.** Proposal: `ceo`
   (broadest decision-lens) for any operator whose `client_namespaces`
   has no `primary_persona_id`. Alternative: rotate through all 9 on
   each load.
3. **Saved prompts scope.** Per-user (every operator's user has their
   own list) OR per-namespace (every member of operator X shares one
   list)? Proposal: per-user, namespace-scoped (composite key
   `namespace_id + user_id`).
4. **Entity color editability.** Read-only seed (Todd sets via
   alembic) OR self-serve (operator picks during stage-3 brand)?
   Proposal: seeded today, self-serve added in a later PR after the
   stage-3 brand binding lands (per `onboarding_v1.yaml:62-66`
   tier_2_personalized).
5. **Coaching-graduation telemetry hookup.** Wire MVP-1 click events
   into HME `SuggestedPromptClicked` / `SuggestedPromptDismissed` /
   `SuggestedPromptGraduated` event types now, or defer to a separate
   Wave-2 PR? Proposal: emit minimal `SuggestedPromptClicked` from day
   one (lightweight) and defer graduation logic.

---

## 7. Out of scope (deliberately deferred)

- Prompt versioning / branching / forking.
- Cross-operator prompt sharing (saved prompts of operator A visible to
  operator B).
- Public prompt marketplace.
- Prompt analytics dashboard (click-through, conversion rate per
  prompt).
- AI-suggested prompt generation (LLM-generated suggestions based on
  operator's recent decisions).
- i18n of suggested prompts (currently EN-only — Spanish for PDC
  comes in via the existing `primary_language` field and is its own PR
  per the gigaton-ui-system bilingual-ready directive).

---

## 8. Verification checklist (for the reviewer)

Run these to validate the findings above before approving any of the 5
proposed PRs:

```bash
# 1. Confirm only PLACEHOLDER_PROMPTS is the suggestor surface:
grep -rn "suggest\|favorite\|starred\|saved.*prompt" \
  /Users/admin/Documents/GitHub/gigaton-ui-system/{components,pages,hooks,services} \
  --include="*.tsx" --include="*.ts" | grep -v "suggested_depth\|suggested_channels\|suggested_profile"

# 2. Confirm no saved-prompts schema:
grep -rln "saved_prompt\|favorite_prompt\|starred_prompt" \
  /Users/admin/Documents/GitHub/user-access-engine \
  /Users/admin/Documents/GitHub/intelligence-silo \
  /Users/admin/Documents/GitHub/persona-engine

# 3. Confirm client_namespaces has no color column:
grep -n "brand_color\|namespace_color\|theme_token\|palette" \
  /Users/admin/Documents/GitHub/user-access-engine/api/models/client_namespaces.py \
  /Users/admin/Documents/GitHub/user-access-engine/alembic/versions/*.py

# 4. Confirm 45 example_questions exist:
grep -c "example_questions:" \
  /Users/admin/Documents/GitHub/persona-engine/api/executive_org_personas/seed/executive_org_personas.yaml
# expect: 9

# 5. Confirm gateway route to executive-personas is live:
grep -n "executive-personas" \
  /Users/admin/Documents/GitHub/gigaton-gateway/api/routing_table.py
# expect: lines 204-211 (or similar)

# 6. Confirm persona-engine endpoint:
curl -s https://api.gigaton.ai/v1/executive-personas | head -c 500
# expect: {"items":[...9...],"count":9}
```

---

## 9. Cross-references

- `/Users/admin/.claude/projects/-Users-admin/memory/master_project_plan.md`
  — §5 deterministic spine + §6 operating rules (the 10-question gate +
  source-authority hierarchy apply to PR #2 + PR #5 since they touch
  schema).
- `/Users/admin/.claude/projects/-Users-admin/memory/universal_connector_hub_architecture.md`
  — `brand_dimensions` extensibility (system-proposable) is the natural
  long-term home for entity color once self-serve editing arrives.
- `/Users/admin/.claude/projects/-Users-admin/memory/entity_hierarchy_for_namespace_seed_2026_05_26.md`
  — 13-leaf namespace tree; entity-color seed in §5F mirrors this list.
- `/Users/admin/Documents/GitHub/master-knowledge-base/manifests/onboarding_v1.yaml`
  — stage-3 brand binding (tier_2_personalized) is the gate for any
  operator-self-serve brand-color affordance.
- `/Users/admin/.claude/projects/-Users-admin/memory/stage_5_variance_aware_self_healing_spec.md`
  — Wave-2 variance model is the substrate for "graduate away
  suggestions as competence is demonstrated."

---

## 10. Top 3 critical gaps + top 3 quick wins

**Top 3 critical gaps**

1. The 45 high-quality persona-scoped suggested prompts already shipped
   in `persona-engine` are **completely invisible to the FE** — no
   consumer exists. This is the single biggest "instant alignment"
   miss.
2. **No entity color anywhere in the schema or the UI.** Every operator
   sees identical Gigaton purple chrome — "Whose Gigaton is this?" is
   not visually answered.
3. **Saved-prompts feature does not exist** end-to-end. Operators have
   no way to capture a working prompt, no way to recall it, no
   evidence-of-competence trail tied to it.

**Top 3 quick wins**

1. **PR #1 (StatusPill primitive)** — ~120 LOC, zero schema impact,
   immediately retires 6 redeclared palettes and gives the chat-
   orchestrator action bubble its missing status chip.
2. **PR #4 (persona-derived suggested prompts)** — ~220 LOC, the
   persona-engine endpoint + 45 prompts are LIVE; the FE work is just
   the consumer. Replaces PDC-biased placeholder grid with
   operator-relevant prompts on first chat load. Delivers Todd's
   "instant alignment" directive in one PR.
3. **PR #2 (brand_color column + seed)** — ~180 LOC, low-risk schema
   add (nullable column), seeds the 6 known namespaces with the colors
   in §5F. Foundation for PR #3 (visible entity chip).

---

End of assessment.
