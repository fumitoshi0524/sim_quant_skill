---
name: sim-quant-automation
description: 'General-purpose quant research automation with AkShare and AKQuant. Build task-specific scripts, datasets, charts, and markdown reports.'
argument-hint: 'Describe objective, market universe, timeframe, factors/strategy, and output folder'
user-invocable: true
disable-model-invocation: false
---

# Sim Quant Automation

This skill is a **general quant analysis skill** for Python projects using `akshare` and `akquant`.

It should not be limited to one fixed pipeline file.  
For each task, the agent should create a **task-specific script/workflow** and produce reproducible outputs.

## When to Use

- Market data collection and cleaning
- Factor/indicator construction
- Strategy backtest experiments
- Exportable research handoff (`xlsx + markdown + optional chart`)

## Inputs to Collect

Before running, confirm:

1. Research objective (snapshot, factor study, backtest, macro analysis, etc.)
2. Target universe (A-share, ETF, futures, macro series, custom symbols)
3. Time range / frequency
4. Required indicators, factors, or strategy logic
5. Output folder and deliverables (`xlsx`, `md`, chart types)
6. Environment choice (venv/uv/current env)

## Procedure

1. Validate dependencies in the chosen environment: `akshare`, `akquant`, `pandas`, `openpyxl` (plus task-specific packages).
2. Use the reference docs under `./references/` to pick APIs and design data flow.
3. Create a task-specific runner script (for example `results/<task_name>/run_<task_name>.py`) instead of hardcoding one entrypoint.
4. Execute the task and generate artifacts in the requested output directory.
5. Produce at minimum:
   - one `.xlsx` dataset
   - one `.md` report
6. If requested, include charting (Excel line/bar chart or plotted images) and strategy KPI summaries.
7. Validate output quality (non-empty data, expected columns/range, readable report).

## Decision Points

1. Prefer `akshare` for data ingestion; use `akquant` when backtesting/execution abstractions are needed.
2. If `akquant` is unavailable, continue in `akshare + pandas` mode.
3. If schemas differ, normalize columns explicitly before analysis/reporting.
4. For every new user task, generate or update a dedicated script so the workflow is reproducible.

## Completion Checks

1. Workflow exits without exceptions.
2. Output folder contains required files (`.xlsx`, `.md`, optional chart/image files).
3. Data in `.xlsx` matches requested universe/time window and is non-empty.
4. `.md` report records source APIs, assumptions, and key quantitative findings.

## Resources

- [AkShare reference](./references/akshare_reference.md)
- [AKQuant reference](./references/akquant_reference.md)
- [Example pipeline entrypoint](./scripts/run_sim_quant_pipeline.py)
- [Example data collector](./scripts/collect_market_data.py)
- [Example report module](./scripts/build_markdown_report.py)

## Example Prompts

- `/sim-quant-automation Build a CSI300 factor analysis job for 2022-01 to 2024-12 and export xlsx + markdown under results/csi300_factor`
- `/sim-quant-automation Fetch China macro indicators (PMI, CPI) and create a charted xlsx report under results/macro_dashboard`
- `/sim-quant-automation Use akshare for data + akquant for backtest, then summarize performance metrics in markdown`

## Annotations
- Ask user which environment to use (venv/uv/current env) before installation or execution.
- Do not restrict execution to `./scripts/run_sim_quant_pipeline.py`; treat that file as an example only.
- For each concrete user task, create a task-specific runnable script/workflow.
