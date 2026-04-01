---
title: Pricing Formula Spec
tags: [pricing, formulas]
status: spec
---

# Pricing Formula Spec

## Core Formula Set

### Gross Margin
```text
Gross Margin % = (Revenue - Direct Cost) / Revenue
```

### Contribution Margin
```text
Contribution Margin = Revenue - Variable Cost
```

### CAC Payback
```text
CAC Payback Months = CAC / Monthly Gross Profit
```

### Discount Impact
```text
Discounted Price = Base Price * (1 - Discount Rate)
```

### Floor Price
```text
Floor Price = Total Cost / (1 - Minimum Acceptable Margin)
```

## Rules
- Never recommend a price below floor price without explicit approval.
- Flag any scenario where gross margin < minimum acceptable margin.
- Separate setup work from recurring delivery whenever possible.
