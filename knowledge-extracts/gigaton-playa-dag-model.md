---
title: gigaton-playa-dag-model
project: gigaton-engine
source_file: gigaton_playa_roisummary.xlsx
description: Causal DAG model for Playa del Carmen property ROI: exogenous market inputs, operator-controlled treatments, and outcome coefficients
extracted: 2026-04-01
tags:
  - dag
  - causal
  - playa-del-carmen
  - roi
  - occupancy
  - revenue
  - gigaton
type: xlsx-knowledge-extract
---

# Causal DAG model for Playa del Carmen property ROI: exogenous market inputs, operator-controlled treatments, and outcome coefficients

**Source**: `gigaton_playa_roisummary.xlsx`
**Project**: `gigaton-engine`
**Extracted**: 2026-04-01


## DAG_Nodes

| Node | Type | Description | Parents |
| --- | --- | --- | --- |
| Seasonality_Index | Exogenous | Seasonal demand strength for Playa del Carmen (0–1 index) |  |
| Macro_Demand_Index | Exogenous | Overall tourism demand / arrivals index | Seasonality_Index |
| Market_Supply_Index | Exogenous | Relative number of competing listings in the area |  |
| Media_Quality_Index | Treatment | Quality of photos, 3D tours, video, Bella content (0–10) |  |
| Listing_Price_Relative | Treatment | Listing price indexed to market median (e.g., 1.05 = 5% higher) |  |
| Marketing_Impressions | Treatment | Paid + organic impressions per period |  |
| Response_Time_Min | Treatment | Median WhatsApp response time in minutes |  |
| Partner_Agency_Score | Treatment | Quality/strength of partner agencies (0–10) |  |
| Listing_Visibility_Index | Mediator | Visibility / ranking on platforms (0–10) | Macro_Demand_Index, Market_Supply_Index, Marketing_Impressions, Media_Quality_Index |
| Lead_Volume | Mediator | Number of inbound inquiries (per property / period) | Listing_Visibility_Index, Marketing_Impressions, Partner_Agency_Score |
| Lead_Quality_Score | Mediator | Average quality/intent of leads (0–10) | Media_Quality_Index, Partner_Agency_Score, Listing_Price_Relative |
| Conversion_Rate | Mediator | Probability an inquiry becomes a booking | Lead_Quality_Score, Listing_Price_Relative, Response_Time_Min, Media_Quality_Index |
| Avg_Length_of_Stay | Mediator | Average nights per booking | Lead_Quality_Score, Seasonality_Index |
| Nightly_Rate_Realized | Mediator | Average realized nightly rate after discounts | Listing_Price_Relative, Macro_Demand_Index, Market_Supply_Index |
| Occupancy_Rate | Mediator | Share of nights occupied in the period | Lead_Volume, Conversion_Rate, Avg_Length_of_Stay, Market_Supply_Index |
| Operating_Cost_per_Booking | Mediator | Marginal operating cost per booking (cleaning, water, ops) | Service_Quality_Index |
| Service_Quality_Index | Mediator | Quality of integrated services (water, maintenance, concierge) | Partner_Agency_Score |
| Monthly_Gross_Revenue | Outcome | Total booking revenue per property per month | Occupancy_Rate, Nightly_Rate_Realized |
| Monthly_Contribution_Margin | Outcome | Gross revenue minus variable costs | Monthly_Gross_Revenue, Operating_Cost_per_Booking |
| Monthly_Net_Profit | Outcome | Contribution margin minus fixed costs and commissions | Monthly_Contribution_Margin, Fixed_Costs |
| Fixed_Costs | Exogenous | Fixed costs per property (rent, platform fees, base labor) |  |

## Conv_Coeffs

| Variable | Beta |
| --- | --- |
| Intercept | 0 |
| Lead_Quality_Score | 0 |
| Listing_Price_Relative | 0 |
| Response_Time_Min | 0 |
| Media_Quality_Index | 0 |

## Occ_Coeffs

| Variable | Beta |
| --- | --- |
| Intercept | 0 |
| Lead_Volume | 0 |
| Conversion_Rate | 0 |
| Avg_Length_of_Stay | 0 |
| Market_Supply_Index | 0 |

## Rev_Coeffs

| Variable | Beta |
| --- | --- |
| Intercept | 0 |
| Occupancy_Rate | 0 |
| Nightly_Rate_Realized | 0 |

## Scenarios

| Variable | Value |
| --- | --- |
| Seasonality_Index | 0.7 |
| Macro_Demand_Index | 0.7 |
| Market_Supply_Index | 1 |
| Media_Quality_Index | 7 |
| Listing_Price_Relative | 1 |
| Marketing_Impressions | 10000 |
| Response_Time_Min | 10 |
| Partner_Agency_Score | 7 |
| Lead_Quality_Score (derived or assumed) | 6 |

## Channel_Scenario

| Global Assumptions |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Nights_per_Month | 30 |  |  |  |  |  |  |
| Variable_Cost_per_Booked_Night | 600 |  |  |  |  |  |  |
| Fixed_Costs_Per_Month | 20000 |  |  |  |  |  |  |
| Base_Occupancy_Single_Channel | 0.45 |  |  |  |  |  |  |
| Uplift_per_Additional_Channel | 0.05 |  |  |  |  |  |  |
| Gigaton_Intelligence_Extra_Uplift | 0.1 |  |  |  |  |  |  |
| Baseline_Nightly_Rate | 1800 |  |  |  |  |  |  |
| Gigaton_Nightly_Rate_Uplift | 0.05 |  |  |  |  |  |  |


| Scenario | Channels | Nightly_Rate | Resulting_Occupancy | Booked_Nights | Gross_Revenue | Variable_Costs | Fixed_Costs |
| Baseline – 1 channel | 1 |  |  |  |  |  |  |
| Manual multi-channel | 3 |  |  |  |  |  |  |
| Gigaton orchestrated multi-channel | 6 |  |  |  |  |  |  |

## Owner_Summary

| Gigaton Property Performance Summary |  |
| --- | --- |

| Baseline Profit |  |
| Gigaton Profit |  |
| Monthly Profit Increase |  |
| ROI vs Baseline |  |

| Explanation |  |
| 1. Baseline = single-channel distribution.
2. Gigaton = multi-channel + AI orchestration.
3. Profit Increase = Gigaton - Baseline.
4. ROI shows uplift efficiency. |  |
