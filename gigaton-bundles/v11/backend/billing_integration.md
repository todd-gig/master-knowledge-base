# Billing Integration

## Rule
Every payment provider event should optionally emit a billing event into your commercial event stream.

## Recommended mapping
- successful checkout -> `namespace_activated` or `renewal_paid`
- tenant setup fee -> `tenant_created`
- metered usage settlement -> `usage_recorded`
