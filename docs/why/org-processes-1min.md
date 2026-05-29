# Why Stage 6 — Organization Processes (1-minute read)

**Industry templates carry you 60-80% of the way; the remaining 20-40% is operator-specific.** Stage 6 is where that 20-40% gets codified.

Stage 5 (Industry Processes) loaded a curated catalog and asked you to triage it; that catalog is broad-and-shallow by design. It captures what most operators in your vertical do. It does **not** capture the operator-specific variations — your team's escalation paths, your in-house naming, the carve-outs you've negotiated, the workflows you run that nobody else does.

After Stage 6, **HME (human-management-engine) knows what your team actually does and can automate or assign**. Specifically, HME now has:

- A codified workflow per operator-specific process, structured as inputs, steps, outputs, and escalation triggers.
- A draft escalation path per process — when does this workflow escalate to a human, and to whom.
- A workflow type tag per initiative — `org_process` for codified-by-Stage-6 workflows.

Without Stage 6, HME's view of the operator's work is the catalog-level view — accurate for the shared 60-80%, blank for the remaining 20-40%. The platform can recommend against the catalog, but it cannot route Stage 7 assignments (humans + automations) against work that isn't codified.

**True**: Stage 6 is what enables HME to automate OR assign work. The platform can only assign work it can describe; Stage 6 supplies the description for the operator-specific portion of the work.

The activation gate requires **`org_initiatives_with_workflow_type >= 10`** — at least 10 codified org processes. Ten is the floor below which Stage 7's assignment surface looks empty; above ten, the platform has enough work to populate the assignment carousel and start scoring automation candidates.

Stage 6 inherits proposed workflows from two sources: your Stage 1 documentation bundle and your meeting transcripts (if connected). The platform extracts candidate workflows; you accept, edit, or reject each one. This makes Stage 6 cheaper than discovery-from-scratch but more bespoke than Stage 5's catalog triage.

If you only remember one thing: **Stage 5 captured the shared 60-80%; Stage 6 captures the operator-specific 20-40%. Together they give HME a complete enough picture of your work to route Stage 7's assignments.**
