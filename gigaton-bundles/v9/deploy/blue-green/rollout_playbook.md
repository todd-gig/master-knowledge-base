# Blue-Green Rollout Playbook

1. Deploy green environment.
2. Run readiness checks.
3. Run integration tests.
4. Run cutover gate script.
5. Compare metrics against blue.
6. Shift traffic gradually or atomically.
7. Monitor error rate and latency.
8. Roll back to blue if health or correctness degrades.
