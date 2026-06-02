# Why Stage 5 — Industry Processes (1-minute read)

**Stage 5 collapses what would be days of org-process discovery into minutes** by loading a curated industry-template catalog and asking the operator to triage it.

Every industry has a small set of canonical processes that 80% of operators run some variant of: a real-estate operator runs listings + showings + offer-management + closing; a hospitality operator runs bookings + check-in + concierge + checkout; an agency runs proposal + onboarding + delivery + retainer-renewal. These canonical processes are well-documented across the industry. The platform carries a catalog per industry + sub-vertical and loads the relevant slice for each operator.

**Triaging the catalog is structurally cheaper than discovering processes from scratch.** Three buttons per catalog entry — *Applies*, *Doesn't Apply*, *Modify* — let the operator review 30-40 catalog entries in 10-15 minutes. Without the catalog, the operator would interview their team, audit their tooling, and draft each process by hand — typically 12-30 hours of consulting-equivalent work. The PPIM signature reflects this: avg **12-30 hours of consulting equivalent saved** at Stage 5.

Each catalog entry binds to Variable Registry tags **industry** and **sub_vertical**. Those tags are what make the catalog operator-portable: a new operator selects industry + sub_vertical, the catalog filters to their relevant entries, and triage begins. The same catalog substrate serves every operator in the same vertical without bespoke per-operator authoring.

The triage outcomes route forward:

- **Applies** — the process is adopted as-is. HME inherits the canonical workflow definition.
- **Doesn't Apply** — the process is marked irrelevant. HME skips it.
- **Modify** — the process is partially relevant. The entry forks into Stage 6 (Org Processes) as a starting point for org-specific codification.

The Stage 5 activation gate requires `uncategorized_count == 0` — every catalog entry has been triaged. The platform won't advance to Stage 6 with un-triaged entries because the org-process discovery in Stage 6 depends on knowing which industry processes are in-scope.

If you only remember one thing: **Stage 5 buys you 12-30 hours by triaging a curated catalog instead of discovering processes from scratch. The catalog is operator-portable because it's tagged by industry + sub_vertical.**
