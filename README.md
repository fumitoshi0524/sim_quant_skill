# Sim Quant Automation Skill Repository

This repository shares a reusable GitHub Copilot skill: `sim-quant-automation`.

For each user task, the agent should create a task-specific workflow/script and output reproducible artifacts such as:

- `.xlsx` datasets
- `.md` analysis reports
- optional charts/backtest summaries

## Skill Location

- Skill entry: `.github/skills/sim-quant-automation/SKILL.md`
- Example scripts: `.github/skills/sim-quant-automation/scripts/`
- Reference docs:
  - `.github/skills/sim-quant-automation/references/akshare_reference.md`
  - `.github/skills/sim-quant-automation/references/akquant_reference.md`

## How to Share and Use

Copy `.github/skills/sim-quant-automation` into your supported skill directory (project-level or global-level), then invoke:

```text
/sim-quant-automation <your quant task request>
```

## Prompt Examples

- `/sim-quant-automation Build a CSI300 factor analysis job for 2022-01 to 2024-12, export xlsx + markdown under results/csi300_factor`
- `/sim-quant-automation Fetch PMI and CPI series from 2019-01 to 2024-12 and produce xlsx with line charts under results/macro_dashboard`
- `/sim-quant-automation Use akshare for data and akquant for backtest, then summarize KPIs in markdown under results/strategy_eval`

## Existing Example Results

Generated sample outputs are under `.\results`:

- `results\example_daily\`
- `results\example_akshare_only\`
- `results\example_factor\`

