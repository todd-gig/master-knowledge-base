# Blue-Green Rollout Playbook

1. Deploy green environment.
2. Run readiness checks.
3. Run smoke tests.
4. Compare metrics against blue.
5. Shift traffic gradually or atomically.
6. Monitor error rate and latency.
7. Roll back to blue if health or correctness degrades.
