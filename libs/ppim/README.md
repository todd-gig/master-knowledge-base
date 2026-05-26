# `libs/ppim` — Cross-engine PPIM signature validators

Single source of truth for PPIM (Predictably Profitable Interaction Management)
signature invariants. Imported by every Gigaton engine that stamps, carries,
or reads the `ppim_attribution_chain` field.

Anchor docs:
- `master_project_plan.md` §"foundational_goal_gigaton_engineered_brand_experience"
- `master-knowledge-base/runbooks/Phase3_Spec_B_PPIM_attribution_chain.md` (this feature)

## Why this lives in `master-knowledge-base/libs/`

The chain is a **cross-cutting** contract: gateway stamps it, HME carries it,
decision-engine reads it. If each repo implemented its own validator the four
invariants would drift the moment one engine shipped a fix the others didn't
mirror. Hosting the validator here — alongside the canonical PPIM-signature
doctrine doc — keeps every consumer pinned to the same invariant set.

## The `ppim_attribution_chain` shape

```jsonc
{
  "ppim_operator_id": "cbp-walking-tour",
  "ppim_attribution_chain": [
    "cbp-walking-tour",   // [0]  leaf  — operator-of-record
    "cbp",                // [1]  parent
    "gigaton-root"        // [-1] platform sentinel (always last)
  ]
}
```

**Ordering:** leaf-first → root-last. Element `[0]` always equals
`ppim_operator_id`. Element `[-1]` always equals the `GIGATON_ROOT` sentinel.

## The four invariants

| ID | Invariant | Enforced by |
|----|-----------|-------------|
| I-1 | TERMINATED — `chain[-1] == "gigaton-root"` | `is_terminated` |
| I-2 | LEAF-OF-RECORD — `chain[0] == operator_id` | `leaf_matches_operator` |
| I-3 | DEPTH-CAP — `1 <= len(chain) <= 10` | `is_within_depth_cap` |
| I-4 | NO-SELF-ATTRIB — root may not synthesise a multi-hop chain | `has_no_self_attribution` |

`validate_chain(chain, operator_id)` runs all four and returns
`(valid: bool, reason: str)`.

`repair_chain(chain, operator_id)` is the fail-soft companion: given an
almost-valid chain (missing sentinel, depth overflow, leaf-mismatch from
a stale cache), it returns a guaranteed-valid chain following the six
repair rules in the module docstring. **It never raises.** Callers log a
warning whenever the returned chain differs from the input.

## Import pattern

From any consumer repo that vendors `master-knowledge-base/libs/`:

```python
from libs.ppim import (
    GIGATON_ROOT,
    validate_chain,
    repair_chain,
)

ok, reason = validate_chain(["cbp-walking-tour", "cbp", "gigaton-root"], "cbp-walking-tour")
assert ok, reason

# Stamp-time fail-soft (gateway middleware):
chain = repair_chain(uae_response.get("chain"), operator_id="cbp-walking-tour")
```

The `libs.ppim` package has zero third-party dependencies — pure stdlib —
specifically so it can be vendored into a Cloud Run engine's deploy bundle
without pulling in the rest of `master-knowledge-base`.

## Tests

```bash
cd /Users/admin/Documents/GitHub/master-knowledge-base
python3 -m pytest libs/ppim/tests/ -q
```

Tests cover every predicate, every repair rule, and the composite validator
+ idempotency of `repair_chain(repair_chain(x))`.
