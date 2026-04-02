---
title: carmen-beach-agent-costing
project: Carmen-Beach-Properties
source_file: CarmenBeach_Costing_Calculator_Governed.xlsx
description: Governed compensation model for Carmen Beach AI agent roles: Photographer, Listing Agent, Leasing Agent, Property Management Agent, Tenant Management
extracted: 2026-04-01
tags:
  - carmen-beach
  - costing
  - agent-compensation
  - governance
type: xlsx-knowledge-extract
---

# Governed compensation model for Carmen Beach AI agent roles: Photographer, Listing Agent, Leasing Agent, Property Management Agent, Tenant Management

**Source**: `CarmenBeach_Costing_Calculator_Governed.xlsx`
**Project**: `Carmen-Beach-Properties`
**Extracted**: 2026-04-01


## Config

| Parameter | Value | Notes |
| --- | --- | --- |
| Complexity increment per level | 0.05 | Applied to (Complexity-1) in multiplier |
| Skill increment per level | 0.03 | Applied to (Skill-1) in multiplier |
| Quality sensitivity factor | 0.5 | Quality_Mult = 1 + ((Quality-80)/20)*factor; cap >=0.5 |
| Outcome bonus multiplier | 50 | Outcome_Bonus = Value_Weight * Outcome_Score * multiplier/100 * Variable_Rate |
| SLA miss penalty (fraction) | 0.15 | If SLA_Met == FALSE then Total_Comp *= (1 - penalty) |
| Default base rate per hour (USD) | 25 | Used if Base_Rate not specified per task |
| Default variable rate percent (0-1) | 0.1 | Used if Variable_Rate not specified per task |

## Governance

| List | Value |
| --- | --- |
| Owners | Marketing Lead |
| Owners | Sales Lead |
| Owners | Ops Lead |
| Owners | CX Lead |
| Owners | Revenue Manager |
| Owners | Creative Director |
| Owners | Distribution Manager |
| Owners | Owner Relations |
| Approvers | GM Playa |
| Approvers | COO |
| Approvers | CFO |
| Approvers | Legal |
| Approvers | Brand QA |
| Tooling | Google Drive |
| Tooling | Google Sheets |
| Tooling | Google Calendar |
| Tooling | ClickUp |
| Tooling | Gmail |
| Tooling | HubSpot |
| Tooling | Airbnb |
| Tooling | VRBO |
| Tooling | Booking.com |
| Tooling | Matterport |
| Tooling | DJI Fly |
| Tooling | Adobe Lightroom |
| Tooling | Premiere Pro |
| Tooling | MongoDB |
| Tooling | BigQuery |

## Causal_Matrix

| Task_ID | Outcome_ID | Causal_Link_Type | Expected_Impact_0to1 | Lag_Days | Confidence_0to1 | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| T-PH-001 | O1 | direct | 0.3 | 7 | 0.7 |  |
| T-PH-002 | O1 | direct | 0.3 | 7 | 0.7 |  |
| T-PH-003 | O1 | direct | 0.3 | 7 | 0.7 |  |
| T-PH-004 | O1 | direct | 0.3 | 7 | 0.7 |  |
| T-PH-005 | O1 | direct | 0.3 | 7 | 0.7 |  |
| T-PH-006 | O1 | direct | 0.3 | 7 | 0.7 |  |
| T-PH-007 | O1 | direct | 0.3 | 7 | 0.7 |  |
| T-PH-008 | O1 | direct | 0.3 | 7 | 0.7 |  |
| T-PH-009 | O1 | direct | 0.3 | 7 | 0.7 |  |
| T-PH-010 | O1 | direct | 0.3 | 7 | 0.7 |  |
| T-PH-011 | O1 | direct | 0.3 | 7 | 0.7 |  |
| T-PH-012 | O1 | direct | 0.3 | 7 | 0.7 |  |
| T-LA-001 | O1 | direct | 0.3 | 3 | 0.7 |  |
| T-LA-002 | O1 | direct | 0.3 | 3 | 0.7 |  |
| T-LA-003 | O1 | direct | 0.3 | 3 | 0.7 |  |
| T-LA-004 | O1 | direct | 0.3 | 3 | 0.7 |  |
| T-LA-005 | O1 | direct | 0.3 | 3 | 0.7 |  |
| T-LA-006 | O1 | direct | 0.3 | 3 | 0.7 |  |
| T-LA-007 | O1 | direct | 0.3 | 3 | 0.7 |  |
| T-LA-008 | O1 | direct | 0.3 | 3 | 0.7 |  |
| T-LA-009 | O1 | direct | 0.3 | 3 | 0.7 |  |
| T-LA-010 | O1 | direct | 0.3 | 3 | 0.7 |  |
| T-LA-011 | O1 | direct | 0.3 | 3 | 0.7 |  |
| T-LA-012 | O1 | direct | 0.3 | 3 | 0.7 |  |
| T-LE-001 | O1 | direct | 0.5 | 3 | 0.7 |  |
| T-LE-002 | O1 | direct | 0.5 | 3 | 0.7 |  |
| T-LE-003 | O1 | direct | 0.5 | 3 | 0.7 |  |
| T-LE-004 | O1 | direct | 0.5 | 3 | 0.7 |  |
| T-LE-005 | O1 | direct | 0.5 | 3 | 0.7 |  |
| T-LE-006 | O1 | direct | 0.5 | 3 | 0.7 |  |
| T-LE-007 | O1 | direct | 0.5 | 3 | 0.7 |  |
| T-LE-008 | O1 | direct | 0.5 | 3 | 0.7 |  |
| T-LE-009 | O1 | direct | 0.5 | 3 | 0.7 |  |
| T-LE-010 | O1 | direct | 0.5 | 3 | 0.7 |  |
| T-LE-011 | O1 | direct | 0.5 | 3 | 0.7 |  |
| T-LE-012 | O1 | direct | 0.5 | 3 | 0.7 |  |
| T-PM-001 | O1 | direct | 0.3 | 3 | 0.7 |  |
| T-PM-002 | O1 | direct | 0.3 | 3 | 0.7 |  |
| T-PM-003 | O1 | direct | 0.3 | 3 | 0.7 |  |
| T-PM-004 | O1 | direct | 0.3 | 3 | 0.7 |  |
| T-PM-005 | O1 | direct | 0.3 | 3 | 0.7 |  |
| T-PM-006 | O1 | direct | 0.3 | 3 | 0.7 |  |
| T-PM-007 | O1 | direct | 0.3 | 3 | 0.7 |  |
| T-PM-008 | O1 | direct | 0.3 | 3 | 0.7 |  |
| T-PM-009 | O1 | direct | 0.3 | 3 | 0.7 |  |
| T-PM-010 | O1 | direct | 0.3 | 3 | 0.7 |  |
| T-PM-011 | O1 | direct | 0.3 | 3 | 0.7 |  |
| T-PM-012 | O1 | direct | 0.3 | 3 | 0.7 |  |
| T-TM-001 | O1 | direct | 0.3 | 3 | 0.6 |  |
| T-TM-002 | O1 | direct | 0.3 | 3 | 0.6 |  |
| T-TM-003 | O1 | direct | 0.3 | 3 | 0.6 |  |
| T-TM-004 | O1 | direct | 0.3 | 3 | 0.6 |  |
| T-TM-005 | O1 | direct | 0.3 | 3 | 0.6 |  |
| T-TM-006 | O1 | direct | 0.3 | 3 | 0.6 |  |
| T-TM-007 | O1 | direct | 0.3 | 3 | 0.6 |  |
| T-TM-008 | O1 | direct | 0.3 | 3 | 0.6 |  |
| T-TM-009 | O1 | direct | 0.3 | 3 | 0.6 |  |
| T-TM-010 | O1 | direct | 0.3 | 3 | 0.6 |  |
| T-TM-011 | O1 | direct | 0.3 | 3 | 0.6 |  |
| T-TM-012 | O1 | direct | 0.3 | 3 | 0.6 |  |

## Summary_Role

| Role | Effort_Cost_USD | Outcome_Bonus_USD | Total_Comp_USD | Efficiency_Ratio |
| --- | --- | --- | --- | --- |
| Leasing Agent | 0 | 0 | 0 | 0 |
| Listing Agent | 0 | 0 | 0 | 0 |
| Photographer | 0 | 0 | 0 | 0 |
| Property Management Agent | 0 | 0 | 0 | 0 |
| Tenant Management | 0 | 0 | 0 | 0 |

## Summary_Outcome

| Outcome_ID | Effort_Cost_USD | Outcome_Bonus_USD | Total_Comp_USD | Efficiency_Ratio |
| --- | --- | --- | --- | --- |
| O1 | 0 | 0 | 0 | 0 |
