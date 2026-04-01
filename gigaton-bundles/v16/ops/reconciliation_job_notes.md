# Reconciliation Job Notes

The reconciliation job scans local payments in unstable statuses and compares them against provider state.

## Purpose
Reduce payment status drift when webhooks are delayed, dropped, or fail downstream processing.
