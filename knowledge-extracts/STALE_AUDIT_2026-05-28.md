---
name: knowledge-extracts-stale-audit-2026-05-28
description: Audit of every .md file in knowledge-extracts/ — staleness, source xlsx state, downstream consumers, disposition.
audit_date: 2026-05-28
auditor: Claude Opus 4.7 + Todd
---

# Knowledge Extracts Audit — 2026-05-28

## Method

For each extract in `knowledge-extracts/`:
1. Compared extract mtime to source xlsx mtime (grep'd `~/Desktop` + `~/Documents` for filename pattern).
2. Grep'd all service-repo code (`gigaton-*`, `intelligence-silo`, `gigaton-gateway`, `Carmen-Beach-Properties`, etc.) for the extract's slug — counts external references.
3. Determined disposition: **REFRESH**, **ARCHIVE**, or **INGEST**.

## Headline finding

**ZERO of the 11 extracts are referenced anywhere outside `master-knowledge-base/` itself.** They are orphaned knowledge.

The original intent (per `scripts/xlsx_to_knowledge.py` header comment: *"structured Markdown knowledge files consumable by AI intelligence systems (Claude, GPT, RAG pipelines)"*) was that these would be picked up by ingestion into a RAG layer. That ingestion never happened — the intelligence-silo Q&A pipeline (shipped 2026-05-28 across PRs #46/#49/#50-#53) does not have these in its FAISS index.

## Per-file audit

| Extract | mtime | Source xlsx | xlsx mtime | Extl refs | Disposition |
|---------|-------|-------------|------------|-----------|-------------|
| `brand-voice-data-dictionary.md` | 2026-04-01 | NOT FOUND on disk | — | 0 | ARCHIVE — source missing; restore from Drive backup before re-extracting |
| `carmen-beach-affiliate-model.md` | 2026-05-19 | NOT FOUND on disk | — | 0 | ARCHIVE + INGEST |
| `carmen-beach-agent-costing.md` | 2026-05-19 | `~/Desktop/Solutiions/CarmenBeach_Costing_Calculator_Governed.xlsx` | 2025-11-10 | 0 | INGEST (extract newer than source) |
| `carmen-beach-occupancy-roi.md` | 2026-04-01 | NOT FOUND on disk | — | 0 | ARCHIVE + INGEST |
| `carmen-beach-pricing.md` | 2026-05-19 | NOT FOUND on disk | — | 0 | ARCHIVE + INGEST |
| `claude-tool-education-roi.md` | 2026-04-01 | NOT FOUND on disk | — | 0 | ARCHIVE + INGEST |
| `gigaton-company-valuation.md` | 2026-04-01 | NOT FOUND on disk | — | 0 | ARCHIVE + INGEST |
| `gigaton-playa-dag-model.md` | 2026-05-16 | NOT FOUND on disk | — | 0 | INGEST |
| `liquifex-pilot1-roi.md` | 2026-05-16 | NOT FOUND on disk | — | 0 | INGEST |
| `liquifex-scenario-forecasting.md` | 2026-05-16 | `~/Desktop/Liquifex Contacts - Mike Gaurino/LiqueFex_Scenario_Forecasting_Calculator.xlsx` | 2026-03-02 | 0 | INGEST (extract newer than source) |
| `sales-os-catalog.md` | 2026-05-16 | NOT FOUND on disk | — | 0 | INGEST |

## Why nothing is ARCHIVE-only

Even if the source xlsx is missing, the .md extract is *itself* a piece of doctrine + reference data the Q&A pipeline can answer from. We don't want to throw that away — we want to either:

- **Ingest** it into intel-silo so users can ask *"what's the playa DAG model say about ADR vs occupancy?"* and get a cited answer.
- **Archive** the extract metadata (path + sha256) before deletion so we can prove provenance.

So the policy is: **all 11 .md extracts move into the ingest pass of `scripts/ingest_mkb_to_silo.sh`** (category=`extract`, operator_id=`gigaton`). Their source xlsx files are tracked separately in this audit; missing sources become a Todd-action ("locate or regenerate from Drive").

## Source xlsx — missing-on-disk register

These workbooks were named in `xlsx_to_knowledge.py`'s `WORKBOOK_REGISTRY` but not found on disk during this audit. They likely live in Drive or were moved during the Desktop cleanup (`gigaton-cleanup-2026-05-27/`). Locate before next refresh:

- `Sales_Operating_System.xlsx`
- `Brand_Voice_Data_Dictionary.xlsx`
- `gigaton_playa_roisummary.xlsx`
- `CarmenBeach_Pricing_Calculator.xlsx`
- `CarmenBeach_Affiliate_Growth_Calculator.xlsx`
- `Occupancy_Marketing_ROI_Calculator.xlsx`
- `LiquiFex_Pilot1_Calculator_Restructured.xlsx`
- `company_valuation_model.xlsx`
- `claude_tool_education_roi_calculator.xlsx`

Found on disk:
- `CarmenBeach_Costing_Calculator_Governed.xlsx` (`~/Desktop/Solutiions/`)
- `LiqueFex_Scenario_Forecasting_Calculator.xlsx` (`~/Desktop/Liquifex Contacts - Mike Gaurino/`)

## Follow-up tasks

1. ✅ This audit committed.
2. ⏳ Run `scripts/ingest_mkb_to_silo.sh` first time to onboard all extracts into the Q&A pipeline (LEARNING_LOOP step 2). After this, `/v1/qa/ask "what's the carmen-beach agent cost structure?"` returns the .md extract with citation.
3. ⏳ Todd: locate the 9 missing xlsx sources in Drive or recreate. Once located, `scripts/launchagents/com.gigaton.knowledge-extracts-refresh.plist` (weekly Sunday 05:00 UTC) will keep extracts fresh.
4. ⏳ Patch `scripts/xlsx_to_knowledge.py` to search `~/Documents/Claude/Projects/` and `~/Library/CloudStorage/GoogleDrive-*/` in addition to `~/Desktop` so file moves don't break the refresh.
