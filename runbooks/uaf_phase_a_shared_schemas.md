# UAF Phase A — Shared Schemas (`SignalEvent` + `IDPProfile`)

> **Status:** Locked contract for Phase A. Source of truth for cross-repo wire shapes.
> **Authored:** 2026-05-28
> **Owners:** UAF-C (this doc) — locks contracts between UAF-A (gateway) + UAF-B (UAE IDP resolver)
> **Related:** [`runbooks/2026_05_26_universal_acquisition_framework.md`](2026_05_26_universal_acquisition_framework.md) (full UAF spec — Phase A is the first concrete buildout)

---

## 1. Purpose

The Universal Acquisition Framework (UAF) Phase A builds the shared substrate underneath all 5 user categories (`customer`, `client`, `talent`, `affiliate`, `alt_user`). Two endpoints ship in parallel:

- **`gateway POST /v1/acquisition/signal`** — captures every pre-IDP signal (web visit, doc fetch, referral click, intro DM, ad impression, language hint, etc.). Built by sibling agent **UAF-A**.
- **`UAE POST /v1/idp/resolve`** — resolves a `SignalEvent` (or candidate identity bundle) into an `IDPProfile`, merging across channels. Built by sibling agent **UAF-B**.

Because the two services ship from different repos on the same day, **the wire shape must be agreed once and locked here**. This doc IS that contract. Any field change is a coordinated PR landing in both consumers + a bump of this doc.

**Sibling PRs that consume this contract:**

- Gateway (UAF-A): adds `/v1/acquisition/signal` route + Firestore writer for `unauthenticated_signals` collection. PR # — `TBD`.
- UAE (UAF-B): adds `idp_profiles` table + `alembic` migration + `/v1/idp/resolve` endpoint + Pydantic models. PR # — `TBD`.

Out of scope: NeedsProfile inference (intel-silo), OfferSet matcher (intel-silo), UI Auto-Gen Renderer (gigaton-ui-system). Each ships in a later phase with its own runbook (see §7).

---

## 2. `SignalEvent`

Captured by the gateway and written to Firestore (`unauthenticated_signals` collection). Also the body shape posted to `POST /v1/acquisition/signal`.

### 2.1 Field-by-field

| Field | Type | Optional? | Semantics | Allowed values / format |
|---|---|---|---|---|
| `event_type` | `string` (enum) | **required** | What kind of contact this is | `web_visit`, `doc_fetch`, `referral_click`, `intro_dm`, `ad_impression`, `email_open`, `email_click`, `call_inbound`, `form_submit`, `chat_message`, `api_probe`, `other` |
| `channel` | `string` (enum) | **required** | Surface the signal arrived on | `web`, `email`, `sms`, `whatsapp`, `voice`, `slack`, `gmail_inbound`, `linkedin`, `referral`, `ad`, `api`, `other` |
| `page_url` | `string` (URL) | optional | Full URL incl. query string. Required for `event_type=web_visit \| doc_fetch \| form_submit`. | RFC 3986 URI; max 2048 chars |
| `referrer` | `string` (URL) | optional | `document.referrer` or upstream link. Empty string normalized to `null`. | RFC 3986 URI; max 2048 chars |
| `device_fingerprint` | `string` | optional | Stable per-device hash from client SDK (or `null` if server-side capture). | opaque hex/base64 string, max 128 chars |
| `geo` | `object` | optional | Server-derived (Cloudflare headers / IP geo). Never client-set. | see §2.2 |
| `geo.country` | `string` | optional | ISO 3166-1 alpha-2 | e.g. `"US"`, `"MX"` |
| `geo.region` | `string` | optional | ISO 3166-2 subdivision OR free text fallback | e.g. `"US-FL"`, `"MX-ROO"` |
| `geo.city` | `string` | optional | Free text | e.g. `"Playa del Carmen"` |
| `language` | `string` (ISO 639-1) | optional | Two-letter language code from `Accept-Language` or client SDK. | e.g. `"en"`, `"es"`, `"fr"` |
| `intent_hint` | `string` | optional | Lightweight intent label set by capturing surface (e.g. `"pricing_page"`, `"affiliate_signup_click"`, `"book_demo"`, `"download_pdf"`). Free-form but encouraged set documented at §2.3. | max 64 chars, `[a-z0-9_]+` recommended |
| `timestamp` | `string` (RFC 3339) | **required** | Client-asserted event time. UAE resolver uses this for ordering; `accepted_at` is the trust anchor. | `2026-05-28T14:32:01.123Z` |
| `visitor_token` | `string` | **required** | Anonymous visitor cookie / SDK-generated UUID v4. Stable across page loads for the same browser/device. | UUID v4 string |
| `utm` | `object` | optional | Marketing attribution bag. All sub-fields optional. | see §2.4 |
| `utm.source` | `string` | optional | `utm_source` query param | max 128 chars |
| `utm.medium` | `string` | optional | `utm_medium` | max 128 chars |
| `utm.campaign` | `string` | optional | `utm_campaign` | max 128 chars |
| `utm.term` | `string` | optional | `utm_term` | max 128 chars |
| `utm.content` | `string` | optional | `utm_content` | max 128 chars |
| `operator_id` | `string` | **required** | Which Gigaton operator this signal belongs to (top-level entity in [[entity_hierarchy_for_namespace_seed_2026_05_26]]). Set by gateway based on `X-Client-Namespace` or domain mapping. NOT client-overridable. | UAE `client_namespaces.namespace_id` |
| `signal_id` | `string` (UUID v4) | server-generated | Server assigns on accept. Idempotency key for the Firestore doc. | UUID v4 string |
| `accepted_at` | `string` (RFC 3339) | server-generated | Gateway wall-clock at accept time. Always trusted over `timestamp`. | RFC 3339 timestamp w/ ms |

### 2.2 `geo` semantics

- Sourced from Cloudflare `cf.country` / `cf.region` / `cf.city` headers when behind CF; otherwise from MaxMind lookup at gateway.
- Never client-set; gateway strips any `geo` object provided in the request body.
- All three sub-fields optional independently. Profile may have `country` only, etc.

### 2.3 Recommended `intent_hint` vocabulary

Free-form, but the matcher in Phase B+ will key off common labels. Bias toward this set:

- `pricing_page`, `book_demo`, `start_trial`, `talk_to_sales`
- `affiliate_signup_click`, `talent_apply_click`
- `download_pdf`, `view_case_study`, `play_demo_video`
- `support_inquiry`, `partnership_inquiry`, `vendor_inquiry`, `regulator_inquiry`
- `unknown`

### 2.4 `utm` capture

- All sub-fields trimmed to 128 chars; longer values truncated server-side.
- Empty strings normalized to absent (not stored).
- Lowercase normalization NOT applied (preserves campaign casing for attribution).

### 2.5 JSON example (request body to `POST /v1/acquisition/signal`)

```json
{
  "event_type": "web_visit",
  "channel": "web",
  "page_url": "https://playadelcarmen.homes/properties/oceanview-2br?utm_source=google&utm_medium=cpc",
  "referrer": "https://www.google.com/",
  "device_fingerprint": "fp_8a4b2c9d1e",
  "language": "en",
  "intent_hint": "pricing_page",
  "timestamp": "2026-05-28T14:32:01.123Z",
  "visitor_token": "8d3f1e2a-5b6c-4d7e-8f90-1a2b3c4d5e6f",
  "utm": {
    "source": "google",
    "medium": "cpc",
    "campaign": "pdc_spring_2026"
  }
}
```

### 2.6 Firestore document shape (after gateway accept)

Same as §2.5, plus:

```json
{
  "signal_id": "f1e2d3c4-b5a6-4978-8b6c-5d4e3f2a1b0c",
  "accepted_at": "2026-05-28T14:32:01.847Z",
  "geo": { "country": "US", "region": "US-FL", "city": "Miami" },
  "operator_id": "cbp"
}
```

Collection path: `unauthenticated_signals/{signal_id}`.
Doc TTL: 90 days (Firestore TTL policy on `accepted_at` + 90d).

### 2.7 Endpoint contract — `POST /v1/acquisition/signal`

- **Auth:** none (this endpoint is intentionally unauthenticated; that is the point of pre-IDP signal capture). Rate-limited per IP + per `visitor_token`.
- **Namespace resolution:** gateway maps incoming host → `operator_id` via existing namespace resolver. If unresolvable, signal is dropped with 204 (NOT 4xx — we never want to leak operator topology).
- **Response 200:** `{ "signal_id": "<uuid>", "accepted_at": "<rfc3339>" }`.
- **Response 204:** silent drop (rate-limit, unknown namespace, malformed body). Never returns 4xx to client to avoid probing.
- **Idempotency:** `(visitor_token, timestamp, event_type, page_url)` tuple deduped within a 5-minute window; duplicate calls return the same `signal_id`.

---

## 3. `IDPProfile`

UAE table `idp_profiles` and Pydantic model returned by `POST /v1/idp/resolve`.

### 3.1 Field-by-field

| Field | Type | Optional? | Semantics |
|---|---|---|---|
| `idp_id` | `string` (UUID v4) | **required** | Primary key. Stable across merges (oldest profile's `idp_id` wins on merge). |
| `operator_id` | `string` | **required** | Owning operator namespace. Profiles are operator-scoped; no cross-operator merging in Phase A. |
| `primary_identity` | `string \| null` | optional | Best-known identifier. Format: same `<kind>:<value>` encoding as `alt_identities` (§4). `null` until at least one email or auth_subject lands. |
| `alt_identities` | `list[string]` | **required** (may be empty list) | All known identifiers for this profile across channels. See §4. Stored as Postgres `text[]` with GIN index. |
| `provisional_category_vector` | `dict[str, float]` | **required** | Confidence over the 5 categories: `{customer, client, talent, affiliate, alt_user}`. Sum need not equal 1.0 (multi-category overlap allowed). **Stays empty `{}` in Phase A** — populated by Needs Inference in a later phase. |
| `signal_count` | `int` | **required** | Number of `SignalEvent`s currently associated. Monotonic. |
| `first_seen_at` | `string` (RFC 3339) | **required** | Server timestamp of first signal. |
| `last_seen_at` | `string` (RFC 3339) | **required** | Server timestamp of most recent signal. |
| `resolved` | `bool` | **required** | `true` once any email or `auth_subject` alt_identity is attached; `false` otherwise. See §5. |
| `created_at` | `string` (RFC 3339) | **required** | Row creation time. |
| `updated_at` | `string` (RFC 3339) | **required** | Last mutation time. |

### 3.2 Postgres DDL sketch (for UAE migration)

```sql
CREATE TABLE idp_profiles (
  idp_id                        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  operator_id                   TEXT NOT NULL REFERENCES client_namespaces(namespace_id),
  primary_identity              TEXT,
  alt_identities                TEXT[] NOT NULL DEFAULT '{}',
  provisional_category_vector   JSONB NOT NULL DEFAULT '{}'::jsonb,
  signal_count                  INTEGER NOT NULL DEFAULT 0,
  first_seen_at                 TIMESTAMPTZ NOT NULL,
  last_seen_at                  TIMESTAMPTZ NOT NULL,
  resolved                      BOOLEAN NOT NULL DEFAULT FALSE,
  created_at                    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at                    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_idp_profiles_alt_identities  ON idp_profiles USING GIN (alt_identities);
CREATE INDEX idx_idp_profiles_operator        ON idp_profiles (operator_id);
CREATE INDEX idx_idp_profiles_operator_last   ON idp_profiles (operator_id, last_seen_at DESC);
```

Composite uniqueness: at most one profile per `(operator_id, alt_identity)` is enforced in application code by the resolver, not by a unique constraint (because `alt_identities` is a multi-value array). The merge rule in §5 keeps this invariant.

### 3.3 Pydantic model sketch (for UAE service)

```python
from typing import Literal
from datetime import datetime
from pydantic import BaseModel, Field

CategoryKey = Literal["customer", "client", "talent", "affiliate", "alt_user"]

class IDPProfile(BaseModel):
    idp_id: str
    operator_id: str
    primary_identity: str | None = None
    alt_identities: list[str] = Field(default_factory=list)
    provisional_category_vector: dict[CategoryKey, float] = Field(default_factory=dict)
    signal_count: int = 0
    first_seen_at: datetime
    last_seen_at: datetime
    resolved: bool = False
    created_at: datetime
    updated_at: datetime
```

---

## 4. `alt_identities` encoding

Every identifier stored as a single string in the form `<kind>:<value>`.

### 4.1 Kinds

| Kind | Value semantics | Normalization |
|---|---|---|
| `email` | RFC 5322 mailbox addr-spec | lowercase the domain; preserve local-part case; strip surrounding whitespace |
| `phone` | E.164 phone number | strip non-digits except leading `+`; reject if not E.164 valid |
| `device` | Device fingerprint from client SDK | take as-is from `SignalEvent.device_fingerprint` |
| `visitor` | Visitor token (browser-scoped UUID) | take as-is from `SignalEvent.visitor_token` |
| `auth_subject` | OIDC `sub` claim from an authenticated session (Firebase Auth, Google OAuth, etc.) | preserve issuer prefix when ambiguous, e.g. `auth_subject:firebase:abc123` |

### 4.2 Examples

```
email:todd.cx@turtleisland.solutions
email:hello@playadelcarmen.homes
phone:+15551234567
device:fp_8a4b2c9d1e
visitor:8d3f1e2a-5b6c-4d7e-8f90-1a2b3c4d5e6f
auth_subject:firebase:9X0fJk2L3mN4
auth_subject:google:117289746124983748312
```

### 4.3 Order / dedup invariants

- Stored sorted lexicographically; reads are order-stable.
- Dedup on exact match (post-normalization).
- An identifier appears in at most one `IDPProfile` per `operator_id`. If a second signal arrives with an alt_identity that already exists on another profile, the resolver merges per §5.

---

## 5. Resolution rules

### 5.1 Match (no new profile created)

A `SignalEvent` (or identity bundle posted to `/v1/idp/resolve`) **matches** an existing `IDPProfile` when ANY of the following candidate identifiers, after normalization, is already present in that profile's `alt_identities`, scoped to the same `operator_id`:

- the `visitor_token` (always present on a `SignalEvent`),
- the `device_fingerprint` (if present),
- any provided `email` / `phone` / `auth_subject` candidate (typically supplied via the `/v1/idp/resolve` body when a form / auth flow gives them up).

On match: the resolver appends any new alt_identities to the existing profile, increments `signal_count`, updates `last_seen_at` and `updated_at`, recomputes `resolved` (§5.3), and returns the existing `idp_id`.

### 5.2 Cross-profile merge

If a candidate identifier set spans two existing profiles (e.g. profile A has `visitor:X` + `device:Y`; profile B has `email:Z`; a new signal arrives with `visitor:X` AND `email:Z`):

- **Merge ONLY when at least one identifier in the spanning set is `email:` or `auth_subject:`** (i.e. an authenticated / strongly-asserted identifier).
- The older profile (by `created_at`) wins: keeps its `idp_id`, absorbs the other profile's `alt_identities`, sums `signal_count`, takes min `first_seen_at` + max `last_seen_at`, ORs `resolved`, and unions any non-empty `provisional_category_vector` (max per category).
- The younger profile row is soft-deleted (marked with a tombstone; not in scope for Phase A schema, tracked via [[uaf_phase_a_followups]] in Phase B).
- If the spanning set contains ONLY weak identifiers (`visitor`, `device`), **do NOT merge** — this is the §5.4 privacy guard. Instead, leave both profiles distinct; record an internal warning and continue with the older profile.

### 5.3 `resolved` flip

`resolved` becomes `true` the moment any of the following lands on a profile:

- any `email:*` alt_identity, OR
- any `auth_subject:*` alt_identity.

Never flips back to `false`. Phone numbers alone do NOT flip `resolved` in Phase A (they are weaker than email/auth and we lack TFV in this scope).

### 5.4 Privacy guard

> **Never cross-merge two profiles without at least one authenticated identifier (`email:` or `auth_subject:`) in the spanning set.**

This prevents two unrelated browsers behind the same shared device from being silently fused into a single profile, and it prevents fingerprint-only correlation from creating ambient identity graphs. The guard is an explicit invariant of the resolver — must be unit-tested in UAF-B's PR.

### 5.5 Endpoint contract — `POST /v1/idp/resolve`

- **Auth:** internal-only. Requires gateway-issued service-to-service token; rejects external callers with 401.
- **Body:** an `IDPResolveRequest` containing:
  - `operator_id` (required),
  - `signal_id` (optional — points back to a `SignalEvent`),
  - `candidate_identities` (required, non-empty list of `<kind>:<value>` strings).
- **Response 200:** the full `IDPProfile` (new or matched), plus a `created: bool` flag indicating whether the call resulted in a new row.
- **Response 409:** returned only when a merge attempt violates the §5.4 privacy guard AND the caller did not opt-in via `allow_weak_merge: false` (which is the default). Caller may inspect and retry with stronger candidates.

---

## 6. Wire integration

### 6.1 Phase A (this PR cohort) — synchronous capture only

```
┌──────────┐         ┌─────────┐         ┌──────────┐
│ Browser  │────1───▶│ Gateway │────2───▶│ Firestore│
│ / SDK    │  POST   │         │  write  │  doc     │
└──────────┘ /signal └─────────┘         └──────────┘
                          │
                          └── returns {signal_id, accepted_at}
```

1. Client posts `SignalEvent` body (§2.5) to `gateway POST /v1/acquisition/signal`.
2. Gateway:
   - resolves `operator_id` from request host / `X-Client-Namespace`,
   - server-fills `geo`, `signal_id`, `accepted_at`,
   - writes Firestore doc at `unauthenticated_signals/{signal_id}` (§2.6),
   - returns `200 { signal_id, accepted_at }` or `204` (silent drop per §2.7).

**No UAE write happens in Phase A from this path.** Signals accumulate in Firestore; IDP resolution is invoked on demand.

### 6.2 Phase A — on-demand resolution

Other surfaces that need a profile (e.g. an authenticated form submit, an inbound email handler, a chat session start) call:

```
┌──────────────┐                ┌──────┐                ┌──────────┐
│ Other        │──── POST ─────▶│ UAE  │── read/write ─▶│ idp_     │
│ service /    │ /v1/idp/resolve│      │                │ profiles │
│ worker       │                └──────┘                └──────────┘
└──────────────┘                   │
                                   └── returns IDPProfile + created flag
```

The caller supplies `operator_id` + `candidate_identities` (any mix of `visitor:`, `device:`, `email:`, `phone:`, `auth_subject:`). UAE matches per §5.1, merges per §5.2 (subject to §5.4), updates the row, returns the profile.

### 6.3 Phase B (NOT in this PR cohort) — Pub/Sub fan-out

In a later phase, gateway will also emit a `acquisition.signal_received` Pub/Sub message on every accept, and a UAE worker will subscribe + call `/v1/idp/resolve` to keep profiles continuously hot. That worker, the topic, and the subscription are out of scope for Phase A and tracked in the follow-on runbook.

```
┌─────────┐  3a. write   ┌──────────┐
│ Gateway │─────────────▶│Firestore │
│         │  3b. publish ┌──────────┐
│         │─────────────▶│Pub/Sub   │── (Phase B) ─▶ UAE worker ─▶ POST /v1/idp/resolve
└─────────┘  acquisition.│signal_   │
             signal_     │received  │
             received    └──────────┘
```

---

## 7. Out of scope for Phase A

Each ships in its own runbook in a subsequent phase:

- **`NeedsProfile` inference** — `intelligence-silo/core/intelligence/needs_inference.py`. Consumes accumulated `SignalEvent`s for an `IDPProfile` and emits the 10-Intelligence-Dimensions + ethnographic-frames bundle. Will populate `provisional_category_vector` on the profile.
- **`OfferSet` matcher** — `intelligence-silo/core/intelligence/offer_matcher.py`. Ranks Gigaton superpowers against `NeedsProfile` weighted by `gigaton_promotion_priorities.yaml`. Emits the `OfferSet` the UI Auto-Gen Renderer consumes.
- **UI Auto-Gen Renderer** — `gigaton-ui-system/components/auto/*` + `lib/autoUiComposer.ts`. Composes the visible surface (HeroCard / FunctionalityProof / CTAStrip / DispatchedAdvisor / QualificationDashboard).
- **Pub/Sub `acquisition.signal_received` topic + UAE worker** — see §6.3.
- **Cross-operator profile linking** — Phase A scopes profiles strictly to `operator_id`. Cross-operator graph (when one person is a `customer` of CBP and a `talent` candidate for Gigaton) is deliberately deferred.
- **Soft-delete tombstones for merged-away profiles** — sketched in §5.2 but not in the Phase A migration.
- **TFV (toll-free verification) phone trust** — needed before `phone:` alt_identities can flip `resolved`.

---

## 8. PR links

Filled in as sibling agents open PRs:

- Gateway PR (UAF-A — `/v1/acquisition/signal` route + Firestore writer): **TBD**
- UAE PR (UAF-B — `idp_profiles` migration + `/v1/idp/resolve` endpoint + Pydantic models): **TBD**
- This doc PR (UAF-C — shared schemas): see PR cover.

When both sibling PRs are open, update this section + reference this doc from each PR description. Any change to a wire shape after both sibling PRs open requires a coordinated 3-PR bump (schemas doc + both consumers).

---

## Appendix A — Why these specific fields

- `visitor_token` is **required** even though it is weak, because every other identifier may be absent on a first-touch signal. The visitor_token is the minimum viable correlation key.
- `event_type` and `channel` are split because the SAME `event_type` can arrive on multiple `channel`s (a `form_submit` can come from `web` or `whatsapp`).
- `intent_hint` is intentionally free-form rather than a hard enum, because intent vocabularies will evolve per category and per operator. The recommended set (§2.3) is guidance; the matcher in Phase B+ will key off observed labels and surface novel ones.
- `language` is captured at signal time (not derived from profile later) because operators serve multiple-language audiences and the per-signal language is what drives surface choices for that interaction.
- `operator_id` is server-set, never client-set, because the entire multi-tenant isolation model ([[mcp_multi_tenant_namespace_blocker_2026_05_26]]) depends on it being un-spoofable.

## Appendix B — Open questions parked for Phase B

1. **`provisional_category_vector` decay** — when do stale category confidences fade? Likely an exponential decay on `last_seen_at`. Not modeled in Phase A schema (just `{}`).
2. **Cross-operator graph at `gigaton` root operator** — does the top-level `gigaton` operator see a unified profile across all sub-operators? Per [[entity_hierarchy_for_namespace_seed_2026_05_26]] this is plausible but blocked on the namespace seed PR.
3. **Per-signal PII redaction** — `page_url` may contain PII in query strings. Phase A stores raw; Phase B should add a redaction layer before Firestore write.
4. **`device_fingerprint` provenance** — first-party SDK only, or accept third-party fingerprinting libraries? Phase A treats it as opaque; policy call deferred.
