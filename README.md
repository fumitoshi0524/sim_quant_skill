# Sim Quant Skill Demo Repo

This repository shares a reusable GitHub Copilot skill: `sim-quant-automation`.

The skill helps you run simulation-quant data jobs with `akshare` / `akquant` and generate:

- `.xlsx` datasets
- `.md` summary reports

Skill definition: `.github/skills/sim-quant-automation/SKILL.md`

## Environment

This project uses `uv` for dependency and environment management.

```powershell
uv sync
```

Then run examples with `uv run ...` so commands execute inside the project environment.

## Example Commands

Run from repository root:

### Skill prompts (recommended)

- `/sim-quant-automation Generate a daily A-share snapshot job and save outputs under results/example_daily`
- `/sim-quant-automation Run AkShare-only mode and produce xlsx + markdown report under results/example_akshare_only`
- `/sim-quant-automation Add factor columns ending with _score and include them in the markdown summary, output to results/example_factor`

### Equivalent local CLI command

```powershell
uv run python .\.github\skills\sim-quant-automation\scripts\run_sim_quant_pipeline.py --output-dir <RESULT_DIR> [--no-akquant]
```

### Factor-enriched example script

```powershell
uv run python .\results\example_factor\run_factor_example.py
```

## Output Layout

All example artifacts are stored under `.\results`:

- `results\example_daily\`
- `results\example_akshare_only\`
- `results\example_factor\`

Each example produces an `.xlsx` data file and a `.md` report.

