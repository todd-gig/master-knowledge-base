# Merge Into Main App Migration Chain

Use the `101_`, `102_`, and `103_` migrations as additive migrations inside your existing application migration sequence.

## Recommendation
- keep these migrations idempotent
- place them after tenant/core auth tables
- do not duplicate payment tables elsewhere
