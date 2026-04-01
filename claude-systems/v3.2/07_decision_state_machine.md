---
title: Decision State Machine
version: 3.0
status: active
category: state-machine
tags: [state-machine, process]
---

# States
1. `intake`
2. `normalize`
3. `classify`
4. `score`
5. `route`
6. `execute`
7. `review_exception`
8. `review_human`
9. `log`
10. `evaluate_codification`
11. `close`

# Transition Rules
- intake -> normalize
- normalize -> classify
- classify -> score
- score -> route
- route -> execute
- execute -> review_exception if exception exists
- execute -> review_human if human review required
- execute -> log if successful
- review_exception -> review_human or log
- review_human -> log
- log -> evaluate_codification
- evaluate_codification -> close
