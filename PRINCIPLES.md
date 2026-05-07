---
title: Principles — What We Won't Compromise On
owner: todd@gigaton.ai
last-reviewed: 2026-05-07
review-cadence: quarterly
---

These are non-negotiable. Anything that violates a principle requires an explicit, documented exception in `decisions/` signed by both CODEOWNERS.

## 1. Single source of truth

Every fact lives in exactly one place. Cross-references point back to that place. If you find duplicate truth, file a chore to merge it. The list of authoritative sources is in `master-knowledge-base/AUTHORITATIVE_SOURCES.md`.

## 2. Reversibility

Every action has a documented rollback. If you can't write the rollback in two sentences, the action needs review before it ships. This applies to deploys, schema migrations, customer messages, and decisions.

## 3. Audit trail

Every non-trivial action is logged with: who, what, when, why, what changed. Logs are append-only. The trail must reconstruct any state at any point in time. No silent edits to production.

## 4. Reviewability

No solo prod changes. Two CODEOWNERS on every production repo. SIE auto-approval only for T0-trust items with a complete certificate chain. Any human override is logged in `/sie-audit`.

## 5. Data ownership

Customer and prospect data belongs to the customer. We hold it in trust. PII never appears in logs, URLs, or third-party LLM context windows without explicit per-record consent. Retention is documented per data class in `POLICY.md`.

## 6. Security at the boundary

Trust internal traffic; verify at the edge. Every public endpoint requires auth. Internal services (e.g. intelligence-silo) run with `--ingress=internal-and-cloud-load-balancing`. Secrets come from Secret Manager only.

## 7. Cost discipline

Every service has a documented monthly cost ceiling. Alerts fire at 80%. No service runs without `--min-instances=0` unless there's a documented latency requirement.

## 8. Time-box the unknown

Research and POCs get a fixed time budget (default: 1 week). At the end, the work either becomes a planned project or gets archived. No half-finished work lingering on `wip/*` branches.

## 9. Documentation is part of the product

Code without docs is unfinished. Every production service has a CLAUDE.md, a README, and a `/health` + `/version` endpoint. New users hit `START_HERE.md` and find what they need.

## 10. Daily rhythm

The 19:00 CT deploy is sacred. It's how we know the system is alive. Skipping it means the system isn't actually working, and we should find out why immediately.
