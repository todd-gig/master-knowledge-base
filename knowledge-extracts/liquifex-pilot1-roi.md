---
title: liquifex-pilot1-roi
project: liquifex
source_file: LiquiFex_Pilot1_Calculator_Restructured.xlsx
description: LiquiFex Pilot 1 ROI calculator: $500M AUM portfolio across 4, 6, and 12-month liquidity scenarios
extracted: 2026-04-01
tags:
  - liquifex
  - pilot
  - roi
  - aum
  - liquidity
type: xlsx-knowledge-extract
---

# LiquiFex Pilot 1 ROI calculator: $500M AUM portfolio across 4, 6, and 12-month liquidity scenarios

**Source**: `LiquiFex_Pilot1_Calculator_Restructured.xlsx`
**Project**: `liquifex`
**Extracted**: 2026-04-01


## Inputs

| LiquiFex Pilot 1 ROI & Liquidity Calculator — Master Inputs |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |

| Edit BLUE cells only. All scenario and timeline tabs reference these inputs. |  |  |  |  |  |  |  |

| Input Category | Variable | Value | Notes / Guidance |  |  |  |  |
| Portfolio Basics |  |  |  |  |  |  |  |
|  | Number of policies | 25 |  |  |  |  |  |
|  | Total AUM of policies ($) | 500000000 |  |  |  |  |  |
|  | FTC‑eligible fraction of AUM (%) | 0.6 |  |  |  |  |  |
|  | Avg policy duration (years) | 6 |  |  |  |  |  |
| Baseline Return Profile |  |  |  |  |  |  |  |
|  | Baseline MOIC over duration (x) | 1.6 |  |  |  |  |  |
|  | Baseline annual friction/drag (bps of AUM) | 150 |  |  |  |  |  |
|  | Baseline annual operating cost (bps of AUM) | 50 |  |  |  |  |  |
| LiquiFex Uplift Drivers |  |  |  |  |  |  |  |
|  | Capital velocity factor vs baseline (x) | 2 |  |  |  |  |  |
|  | Incremental IRR uplift from arbitrage/actuarial drift (%) | 0.02 |  |  |  |  |  |
|  | Friction reduction vs baseline (bps) | 50 |  |  |  |  |  |
|  | Operating cost reduction vs baseline (bps) | 15 |  |  |  |  |  |
|  | FTC annual turnover on eligible notional (x) | 1.5 |  |  |  |  |  |
| LiquiFex Commercials |  |  |  |  |  |  |  |
|  | Upfront sponsored pilot fee ($) | 750000 |  |  |  |  |  |
|  | Performance fee on FTC turnover (bps) | 35 |  |  |  |  |  |

| Derived (auto) |  |  |  |  |  |  |  |
|  | Baseline IRR (annualized, from MOIC & duration) |  | Uses MOIC and average duration as a simple annualization proxy. |  |  |  |  |
|  | Implied IRR uplift (annualized, proxy) |  | Proxy: uplift from velocity + arbitrage + bps savings converted to %. |  |  |  |  |
|  | LiquiFex IRR (annualized, proxy) |  | Baseline IRR plus implied uplift. |  |  |  |  |

## 4 Month

| LiquiFex Pilot 1 — 4 Month Scenario |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |

| Calculator Outputs |  |  |  |  |  |  |

| Metric | Value | Formula / Driver |  |  |  |  |
| Pilot length (months) | 4 | Fixed for this tab |  |  |  |  |
| Liquidity enabled ($) |  | AUM × FTC-eligible fraction |  |  |  |  |
| Baseline IRR (annualized) |  | From Inputs (MOIC & duration) |  |  |  |  |
| LiquiFex IRR (annualized, proxy) |  | Baseline IRR + implied uplift |  |  |  |  |
| IRR uplift (annualized, proxy) |  | Velocity + arbitrage + bps savings |  |  |  |  |
| Annual gross profit uplift ($/yr) |  | AUM × IRR uplift |  |  |  |  |
| Annual direct cost savings ($/yr) |  | AUM × (friction+ops bps reduction) |  |  |  |  |
| LiquiFex performance fee ($/yr) |  | Eligible notional × turnover × perf bps |  |  |  |  |
| Net uplift ($/yr) after LiquiFex perf fee |  | Net incremental profit after LiquiFex perf fee |  |  |  |  |
| Pilot net uplift ($) net of upfront fee |  | Net uplift over pilot duration minus upfront fee |  |  |  |  |
| Payback period (months) for upfront fee |  | Upfront fee / monthly net uplift |  |  |  |  |

| Project Scope (phases, milestones, activities, responsibilities) |  |  |  |  |  |  |

| Phase | Milestone | Activities | Tasks | Responsibility (RACI-lite) | Requirements / Inputs | Obligations & Commitments |
| Phase 1: Governance & Tranche Lock | M1: Pilot charter signed + tranche locked | Establish operating model + legal/compliance boundaries | • Define pilot success criteria + reporting cadence
• Select tranche (policy IDs, AUM, servicer)
• Confirm no-policy-transfer constraints
• Define allowed FTC structures (bands, slices)
• Counterparty whitelist + KYC/AML onboarding plan | LiquiFex: Platform design + controls
Sponsor: tranche selection + approvals
Servicer: data feeds
Legal/Compliance: sign-off | Policy schedule, cashflow projections, premium schedules, servicer reports, valuation method, approved counterparties list | Sponsor provides clean data + timely approvals; LiquiFex commits to closed-loop controls; both commit to weekly steering committee |
| Phase 2: Build & Integrate Execution Rails | M2: FTC issuance + escrow/settlement rails live (UAT) | Deploy core infrastructure in controlled test mode | • Configure FTC registry + issuance rules
• Integrate actuarial revaluation inputs
• Configure fractional/sub-fractional slicing
• Stand up escrow + settlement workflows
• UAT: issuance, retirement, transfers, audit logs | LiquiFex: build/integrations
Sponsor Ops: test execution
Escrow agent: operational readiness
Compliance: control testing | APIs / files for valuation updates, settlement instructions, escrow account setup, audit requirements | LiquiFex delivers UAT-ready environment; sponsor allocates SMEs for testing; escrow agent confirms SOPs + SLAs |
| Phase 3: Go‑Live (Limited) + First Liquidity Events | M3: First live FTC issuance + first secondary trade settled | Activate live capital with strict risk limits | • Issue FTCs against tranche (initial notional cap)
• Execute first trades (representation-only)
• Validate settlement finality + reconciliations
• Implement exception handling + break-glass procedures
• Publish first weekly performance pack | LiquiFex: execution + monitoring
Sponsor Trading/Ops: trade approval
Finance: reconciliation
Compliance: surveillance | Signed trading rules, caps/limits, approved counterparties, settlement cutoffs, reconciliation templates | Sponsor commits to minimum activity thresholds; LiquiFex commits to uptime + monitoring; both commit to rapid issue triage |
| Phase 4: Scale + Optimization | M4: Capital recycling demonstrated + repeatable weekly cycle | Increase liquidity depth and capture arbitrage density | • Expand issuance bands/slices
• Increase turnover to target
• Continuous repricing (actuarial drift)
• Measure capital velocity vs baseline
• Optimize fees/drag via process tuning | LiquiFex: optimization
Sponsor: volume + counterparties
Actuary: model updates
Ops: process automation | Turnover targets, updated valuation curves, governance approvals for new structures, ops playbooks | Sponsor maintains liquidity program participation; LiquiFex delivers enhancements in sprint cadence; shared KPI governance |
| Phase 5: Closeout + Expansion Decision | M5: Board-ready results + expansion term sheet | Quantify uplift and lock long-term rollout economics | • Final KPI analysis (IRR uplift, velocity, costs)
• Validate neutrality (no policy/carrier/reg changes)
• Security/compliance attestation package
• Expansion playbook + pricing
• Elect ROFR / exclusivity window | LiquiFex: reporting + commercial proposal
Sponsor: investment committee decision
Legal: contract expansion
Ops: BAU transition | Pilot KPI dataset, audit logs, compliance outputs, term sheet templates, expansion scope | Sponsor commits to go/no-go date; LiquiFex commits to expansion readiness plan + SLA proposal |

## 6 Month

| LiquiFex Pilot 1 — 6 Month Scenario |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |

| Calculator Outputs |  |  |  |  |  |  |

| Metric | Value | Formula / Driver |  |  |  |  |
| Pilot length (months) | 6 | Fixed for this tab |  |  |  |  |
| Liquidity enabled ($) |  | AUM × FTC-eligible fraction |  |  |  |  |
| Baseline IRR (annualized) |  | From Inputs (MOIC & duration) |  |  |  |  |
| LiquiFex IRR (annualized, proxy) |  | Baseline IRR + implied uplift |  |  |  |  |
| IRR uplift (annualized, proxy) |  | Velocity + arbitrage + bps savings |  |  |  |  |
| Annual gross profit uplift ($/yr) |  | AUM × IRR uplift |  |  |  |  |
| Annual direct cost savings ($/yr) |  | AUM × (friction+ops bps reduction) |  |  |  |  |
| LiquiFex performance fee ($/yr) |  | Eligible notional × turnover × perf bps |  |  |  |  |
| Net uplift ($/yr) after LiquiFex perf fee |  | Net incremental profit after LiquiFex perf fee |  |  |  |  |
| Pilot net uplift ($) net of upfront fee |  | Net uplift over pilot duration minus upfront fee |  |  |  |  |
| Payback period (months) for upfront fee |  | Upfront fee / monthly net uplift |  |  |  |  |

| Project Scope (phases, milestones, activities, responsibilities) |  |  |  |  |  |  |

| Phase | Milestone | Activities | Tasks | Responsibility (RACI-lite) | Requirements / Inputs | Obligations & Commitments |
| Phase 1: Governance & Tranche Lock | M1: Pilot charter signed + tranche locked | Establish operating model + legal/compliance boundaries | • Define pilot success criteria + reporting cadence
• Select tranche (policy IDs, AUM, servicer)
• Confirm no-policy-transfer constraints
• Define allowed FTC structures (bands, slices)
• Counterparty whitelist + KYC/AML onboarding plan | LiquiFex: Platform design + controls
Sponsor: tranche selection + approvals
Servicer: data feeds
Legal/Compliance: sign-off | Policy schedule, cashflow projections, premium schedules, servicer reports, valuation method, approved counterparties list | Sponsor provides clean data + timely approvals; LiquiFex commits to closed-loop controls; both commit to weekly steering committee |
| Phase 2: Build & Integrate Execution Rails | M2: FTC issuance + escrow/settlement rails live (UAT) | Deploy core infrastructure in controlled test mode | • Configure FTC registry + issuance rules
• Integrate actuarial revaluation inputs
• Configure fractional/sub-fractional slicing
• Stand up escrow + settlement workflows
• UAT: issuance, retirement, transfers, audit logs | LiquiFex: build/integrations
Sponsor Ops: test execution
Escrow agent: operational readiness
Compliance: control testing | APIs / files for valuation updates, settlement instructions, escrow account setup, audit requirements | LiquiFex delivers UAT-ready environment; sponsor allocates SMEs for testing; escrow agent confirms SOPs + SLAs |
| Phase 3: Go‑Live (Limited) + First Liquidity Events | M3: First live FTC issuance + first secondary trade settled | Activate live capital with strict risk limits | • Issue FTCs against tranche (initial notional cap)
• Execute first trades (representation-only)
• Validate settlement finality + reconciliations
• Implement exception handling + break-glass procedures
• Publish first weekly performance pack | LiquiFex: execution + monitoring
Sponsor Trading/Ops: trade approval
Finance: reconciliation
Compliance: surveillance | Signed trading rules, caps/limits, approved counterparties, settlement cutoffs, reconciliation templates | Sponsor commits to minimum activity thresholds; LiquiFex commits to uptime + monitoring; both commit to rapid issue triage |
| Phase 4: Scale + Optimization | M4: Capital recycling demonstrated + repeatable weekly cycle | Increase liquidity depth and capture arbitrage density | • Expand issuance bands/slices
• Increase turnover to target
• Continuous repricing (actuarial drift)
• Measure capital velocity vs baseline
• Optimize fees/drag via process tuning | LiquiFex: optimization
Sponsor: volume + counterparties
Actuary: model updates
Ops: process automation | Turnover targets, updated valuation curves, governance approvals for new structures, ops playbooks | Sponsor maintains liquidity program participation; LiquiFex delivers enhancements in sprint cadence; shared KPI governance |
| Phase 5: Closeout + Expansion Decision | M5: Board-ready results + expansion term sheet | Quantify uplift and lock long-term rollout economics | • Final KPI analysis (IRR uplift, velocity, costs)
• Validate neutrality (no policy/carrier/reg changes)
• Security/compliance attestation package
• Expansion playbook + pricing
• Elect ROFR / exclusivity window | LiquiFex: reporting + commercial proposal
Sponsor: investment committee decision
Legal: contract expansion
Ops: BAU transition | Pilot KPI dataset, audit logs, compliance outputs, term sheet templates, expansion scope | Sponsor commits to go/no-go date; LiquiFex commits to expansion readiness plan + SLA proposal |

## 12 Month

| LiquiFex Pilot 1 — 12 Month Scenario |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |

| Calculator Outputs |  |  |  |  |  |  |

| Metric | Value | Formula / Driver |  |  |  |  |
| Pilot length (months) | 12 | Fixed for this tab |  |  |  |  |
| Liquidity enabled ($) |  | AUM × FTC-eligible fraction |  |  |  |  |
| Baseline IRR (annualized) |  | From Inputs (MOIC & duration) |  |  |  |  |
| LiquiFex IRR (annualized, proxy) |  | Baseline IRR + implied uplift |  |  |  |  |
| IRR uplift (annualized, proxy) |  | Velocity + arbitrage + bps savings |  |  |  |  |
| Annual gross profit uplift ($/yr) |  | AUM × IRR uplift |  |  |  |  |
| Annual direct cost savings ($/yr) |  | AUM × (friction+ops bps reduction) |  |  |  |  |
| LiquiFex performance fee ($/yr) |  | Eligible notional × turnover × perf bps |  |  |  |  |
| Net uplift ($/yr) after LiquiFex perf fee |  | Net incremental profit after LiquiFex perf fee |  |  |  |  |
| Pilot net uplift ($) net of upfront fee |  | Net uplift over pilot duration minus upfront fee |  |  |  |  |
| Payback period (months) for upfront fee |  | Upfront fee / monthly net uplift |  |  |  |  |

| Project Scope (phases, milestones, activities, responsibilities) |  |  |  |  |  |  |

| Phase | Milestone | Activities | Tasks | Responsibility (RACI-lite) | Requirements / Inputs | Obligations & Commitments |
| Phase 1: Governance & Tranche Lock | M1: Pilot charter signed + tranche locked | Establish operating model + legal/compliance boundaries | • Define pilot success criteria + reporting cadence
• Select tranche (policy IDs, AUM, servicer)
• Confirm no-policy-transfer constraints
• Define allowed FTC structures (bands, slices)
• Counterparty whitelist + KYC/AML onboarding plan | LiquiFex: Platform design + controls
Sponsor: tranche selection + approvals
Servicer: data feeds
Legal/Compliance: sign-off | Policy schedule, cashflow projections, premium schedules, servicer reports, valuation method, approved counterparties list | Sponsor provides clean data + timely approvals; LiquiFex commits to closed-loop controls; both commit to weekly steering committee |
| Phase 2: Build & Integrate Execution Rails | M2: FTC issuance + escrow/settlement rails live (UAT) | Deploy core infrastructure in controlled test mode | • Configure FTC registry + issuance rules
• Integrate actuarial revaluation inputs
• Configure fractional/sub-fractional slicing
• Stand up escrow + settlement workflows
• UAT: issuance, retirement, transfers, audit logs | LiquiFex: build/integrations
Sponsor Ops: test execution
Escrow agent: operational readiness
Compliance: control testing | APIs / files for valuation updates, settlement instructions, escrow account setup, audit requirements | LiquiFex delivers UAT-ready environment; sponsor allocates SMEs for testing; escrow agent confirms SOPs + SLAs |
| Phase 3: Go‑Live (Limited) + First Liquidity Events | M3: First live FTC issuance + first secondary trade settled | Activate live capital with strict risk limits | • Issue FTCs against tranche (initial notional cap)
• Execute first trades (representation-only)
• Validate settlement finality + reconciliations
• Implement exception handling + break-glass procedures
• Publish first weekly performance pack | LiquiFex: execution + monitoring
Sponsor Trading/Ops: trade approval
Finance: reconciliation
Compliance: surveillance | Signed trading rules, caps/limits, approved counterparties, settlement cutoffs, reconciliation templates | Sponsor commits to minimum activity thresholds; LiquiFex commits to uptime + monitoring; both commit to rapid issue triage |
| Phase 4: Scale + Optimization | M4: Capital recycling demonstrated + repeatable weekly cycle | Increase liquidity depth and capture arbitrage density | • Expand issuance bands/slices
• Increase turnover to target
• Continuous repricing (actuarial drift)
• Measure capital velocity vs baseline
• Optimize fees/drag via process tuning | LiquiFex: optimization
Sponsor: volume + counterparties
Actuary: model updates
Ops: process automation | Turnover targets, updated valuation curves, governance approvals for new structures, ops playbooks | Sponsor maintains liquidity program participation; LiquiFex delivers enhancements in sprint cadence; shared KPI governance |
| Phase 5: Closeout + Expansion Decision | M5: Board-ready results + expansion term sheet | Quantify uplift and lock long-term rollout economics | • Final KPI analysis (IRR uplift, velocity, costs)
• Validate neutrality (no policy/carrier/reg changes)
• Security/compliance attestation package
• Expansion playbook + pricing
• Elect ROFR / exclusivity window | LiquiFex: reporting + commercial proposal
Sponsor: investment committee decision
Legal: contract expansion
Ops: BAU transition | Pilot KPI dataset, audit logs, compliance outputs, term sheet templates, expansion scope | Sponsor commits to go/no-go date; LiquiFex commits to expansion readiness plan + SLA proposal |
