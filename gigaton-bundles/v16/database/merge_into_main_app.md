# Merge Into Main App Migration Chain

Add `201_`, `202_`, and `203_` after your V15 payment migrations.

## Notes
- `203_` assumes `payment_events` already exists.
- If your migration runner does not support idempotent ALTER TABLE checks, gate it in code or collapse this into a fresh table definition for new environments.
