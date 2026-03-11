---
name: sim-quant-automation
description: 'Automate simulation quant research jobs in Python using akshare and akquant. Use for collecting market data, saving analysis datasets to xlsx, and generating markdown reports.'
argument-hint: 'Describe market universe, timeframe, factors, and output folder'
user-invocable: true
disable-model-invocation: false
---

# Sim Quant Automation

This skill runs a repeatable simulation-quant workflow for Python projects using `akshare` and `akquant`, then produces:

1. Python execution scripts for the pipeline
2. Data outputs saved as `.xlsx`
3. A summary report saved as `.md`

## When to Use

- You need a fast batch job for daily or ad-hoc quant simulation data pulls.
- You want consistent outputs for research handoff (`data + report`).
- You need a single command workflow that can be reused in CI or scheduled tasks.

## Inputs to Collect

Before running, confirm:

1. Target market universe (for example `A-share`, `ETF`, or a custom symbol list).
2. Snapshot date or backtest window.
3. Output folder path.
4. Report language (`zh` or `en`).

## Procedure

1. Validate dependencies in the active Python environment: `akshare`, `akquant`, `pandas`, `openpyxl`.
2. Run [pipeline script](./scripts/run_sim_quant_pipeline.py) with the desired output directory.
   - Default: AkQuant-first with AkShare fallback
   - AkShare-only mode: `--no-akquant`
3. Confirm output artifacts exist:
   - `market_snapshot_YYYYMMDD.xlsx`
   - `sim_quant_report_YYYYMMDD.md`
4. If needed, enrich the report by adding your strategy-specific KPIs.

## Decision Points

1. If `akquant` project connectors are configured, augment the snapshot with strategy metadata.
2. If `akquant` is unavailable, continue with the `akshare`-only path.
3. If dataframe columns differ from expected names, normalize columns in the collector script before report generation.

## Completion Checks

1. Pipeline exits without exceptions.
2. `.xlsx` contains non-empty tabular data with expected columns.
3. `.md` report includes run timestamp, row count, and top movers table.
4. `.md` report includes turnover ranking, factor score overview (when columns exist), and signal summary.

## Resources

- [Pipeline entrypoint](./scripts/run_sim_quant_pipeline.py)
- [Data collection module](./scripts/collect_market_data.py)
- [Markdown report module](./scripts/build_markdown_report.py)

## Example Prompts

- `/sim-quant-automation Generate a daily A-share snapshot job and save outputs under outputs/daily`
- `/sim-quant-automation Run AkShare-only mode and produce xlsx + markdown report`
- `/sim-quant-automation Add factor columns ending with _score and include them in the markdown summary`

## Annotations
- Ask user for whether to use a venv or not, and if so, which one. If not, run in the current environment.
