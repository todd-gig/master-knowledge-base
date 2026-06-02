# Why Stage 7 — Human-assigned + Automated Processes (1-minute read)

**A process without an owner is a process that doesn't run.** That's the operator-facing motto for Stage 7.

By the end of Stage 6, you have 10+ codified org processes. Each one is a candidate workflow — but a candidate is not yet a running workflow. Without an accountable human or a scored automation candidate, codified workflows sit in HME as inert definitions. Operators routinely under-execute because work isn't owned: nobody knows it's their job, nobody runs it, the work falls through the cracks.

**After Stage 7 every codified workflow has either:**

- **A human accountable** (one or more Stage 2 people assigned via drag-and-drop), or
- **An automation candidate scored** by the Decision Execution Engine (queued for human review, approved, or rejected).

No exceptions. The activation gate predicate is `unassigned_initiative_count == 0`. **False**: a process cannot legitimately leave Stage 7 without either an owner OR an automation candidate score. Every codified workflow must have a routing decision.

The PPIM signature quantifies the value as **avg $40k+/yr work-falls-through-cracks recovered**. That number reflects what operators actually lose when codified work sits unowned: customer requests that don't get followed up, vendor invoices that don't get paid on time, escalations that don't reach the escalation target, periodic compliance work that gets missed in busy weeks. Stage 7 closes the loop.

The two paths through Stage 7 are complementary, not competing:

- **Human ownership** is the right answer for high-judgment work that is hard to automate, or low-volume work where automation isn't worth the lift.
- **Automation** is the right answer for repetitive, deterministic work where the cost-benefit favors letting the engine handle it.

The decision-engine scores each unassigned workflow for automation likelihood; the operator approves, rejects, or queues for human owner. The platform tries to make the obvious calls obvious, and the judgment calls explicit.

If you only remember one thing: **no process leaves Stage 7 without either a human accountable or an automation candidate score. That structural rule is what makes the operator's work surface complete.**
