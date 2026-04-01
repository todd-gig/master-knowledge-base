# V12 Payments Execution Test Plan

## Required checks
- auto selects Stripe by default
- explicit provider override works
- session creation returns normalized object
- intent creation returns normalized object
- repository lookup is tenant-aware
- webhook path accepts both providers
- billing bridge maps normalized success events
