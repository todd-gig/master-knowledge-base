# Deployment Guide v5

## Objective
Deploy a Claude project and local operator layer with:
- doctrine memory
- automated client overlay generation
- retrieval calibration
- lifecycle-governed memory
- a functional local dashboard

## Execution flow
1. Upload the root JSON and markdown files into the Claude project.
2. Use `system_prompt_contract.v5.md` as the primary instruction layer.
3. Use `claude_bootstrap.v5.md` as the startup layer.
4. Generate client overlays with `scripts/generate_namespace.py`.
5. Calibrate retrieval using `scripts/calibrate_retrieval.py`.
6. Run `scripts/run_demo.py` for a full sample path.
7. Run the dashboard locally to inspect namespaces, calibration state, and registry coverage.

## ROI logic
This package reduces manual client setup, tightens ranking quality, and creates an operator loop that compounds over time.
