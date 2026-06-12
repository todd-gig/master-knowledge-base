---
type: provenance-registry
established: 2026-05-27
version: v0
source: docs/governance/comp_payout_structure_v1.md §3.7
status: ACTIVE — registry scaffold for knowledge-extraction source provenance
ppim_interaction: audit trail for every doctrine/CBP pattern derived from a knowledge-extraction source
ppim_economics: none directly — these sources receive NO compensation (see §3.7)
ppim_predictability: HIGH — deterministic tag convention
ppim_brand_dimension: integrity + auditability (every borrowed pattern is traceable to origin)
ppim_attribution_chain: [provenance_registry, knowledge-extracts, master-knowledge-base, gigaton-root]
---

# Knowledge-Extraction Provenance Registry

## Purpose

This registry is the audit trail for **work-product origins**. Per
`docs/governance/comp_payout_structure_v1.md` §3.7, every pattern that is
**derived from a knowledge-extraction source** (Kollosche, McGrath, Medvidi,
CareRev) and **applied to platform doctrine or to Carmen Beach Properties (CBP)**
must carry a `provenance.source` tag so the borrowed pattern is traceable back
to where it came from.

These sources are **read-only registries of work-product origins** — they are
**NOT compensation rows** and receive **no payout** from the comp/payout
governance doc. If any of the four ever becomes an active deal, it gets its own
`§3.X` compensation row at that time; until then, this registry only records
provenance.

## The `provenance.source` tag convention

Tag any derived artifact (a doctrine doc, a pricing template, a process model, a
CBP config, etc.) with a `provenance.source` value of the form:

```
provenance.source: <source>/<work-product-slug>_<version-or-period>
```

Examples:

```
provenance.source: kollosche/pricing_template_v2_2024-Q4
provenance.source: mcgrath/listing_pipeline_v1_2024-Q3
provenance.source: medvidi/patient_acquisition_funnel_2025-Q1
provenance.source: carerev/shift_matching_cadence_v1_2024-Q4
```

Format rules:

- **`<source>`** — lowercase source key: one of `kollosche`, `mcgrath`,
  `medvidi`, `carerev` (the four current sources below).
- **`<work-product-slug>`** — short, hyphen/underscore-delimited descriptor of
  the specific work-product the pattern was lifted from.
- **`<version-or-period>`** — a version (`v2`) and/or a period (`2024-Q4`) so the
  provenance pins a specific vintage of the source material.
- A pattern derived from **multiple** sources carries multiple `provenance.source`
  tags (one per origin).

## Current knowledge-extraction sources (per §3.7)

| Source | Vertical | Work-product captured | Applied to |
|---|---|---|---|
| **Kollosche** | AU luxury real estate | Pricing structures, contract templates, agent comp models, listing-quality patterns | CBP / `playadelcarmen.homes` real estate business model |
| **McGrath** | Real estate placement / sales | Listing pipelines, closing patterns, sales-process automation | CBP / `playadelcarmen.homes` real estate business model |
| **Medvidi** | Healthcare patient acquisition | Service-industry frameworks, human management systems, acquisition / process logic | Platform doctrine — services / HR / acquisition workflows |
| **CareRev** | Per-shift healthcare staffing marketplace | Supply-side acquisition patterns, matching algorithms, cadence models | Platform doctrine — services / HR / acquisition workflows |

## Out of scope

- **Integra-CCS** — explicitly OUT OF SCOPE. No active deal and no
  knowledge-extraction value identified (dropped 2026-05-26 per §3.7). Do not add
  Integra-CCS provenance records here.

## Provenance record shape

Each derived pattern that draws on a source should be recorded here (or carry the
tag inline in its own frontmatter). The canonical record shape is in
[`_template.yaml`](./_template.yaml). Minimal example:

```yaml
provenance.source: kollosche/pricing_template_v2_2024-Q4
derived_artifact: docs/governance/comp_payout_structure_v1.md  # where the pattern was applied
applied_to: CBP                                                # CBP | platform-doctrine
pattern: "agent compensation model — tiered split structure"
extracted_on: 2026-05-26
notes: "Informed CBP §3.1 owner rev-share top-quartile positioning."
```

## See also

- `docs/governance/comp_payout_structure_v1.md` §3.7 — source of truth for this registry
- `[[entity_hierarchy_for_namespace_seed_2026_05_26]]` — entity hierarchy (these 4 are knowledge sources, not operators)
