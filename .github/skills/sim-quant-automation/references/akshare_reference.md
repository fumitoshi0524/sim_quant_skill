# AkShare Reference (for `sim-quant-automation`)

## Official Documentation

- Main site: `https://akshare.akfamily.xyz/`
- GitHub repo: `https://github.com/akfamily/akshare`

## Install / Environment

Use the project environment toolchain (recommended: `uv`):

```powershell
uv sync
uv run python -c "import akshare as ak; print(ak.__version__)"
```

## API Discovery Patterns

```python
import akshare as ak

# list available API names
api_names = [n for n in dir(ak) if not n.startswith("_")]

# search by domain
stock_apis = [n for n in api_names if n.startswith("stock_")]
macro_apis = [n for n in api_names if n.startswith("macro_")]
index_apis = [n for n in api_names if n.startswith("index_")]
```

## Commonly Used API Families

### A-share snapshot / history

- `stock_zh_a_spot_em()` — A-share real-time snapshot
- `stock_zh_a_hist(...)` — daily history
- `stock_zh_a_hist_min_em(...)` — minute-level history

### Macro data (China)

- `macro_china_pmi()`
- `macro_china_cpi_monthly()`
- `macro_china_gdp_yearly()`

### Index / components

- `index_component_sw(...)`
- `index_analysis_daily_sw(...)`

### Funds / ETFs

- `fund_etf_category_sina()`
- `fund_aum_hist_em()`

## Practical Notes

- Many endpoints return Chinese column names; normalize columns before downstream analysis.
- Date argument formats vary by endpoint (`YYYYMMDD`, `YYYY-MM-DD`, etc.); verify via docs/examples.
- Handle network instability with retries when running batch jobs.
- Always persist raw pulls and processed outputs separately when reproducibility matters.

## Skill Usage Guidance

When using this skill:

1. Choose APIs based on task objective (snapshot, factor, macro, backtest input).
2. Write a task-specific script in the requested output folder.
3. Export at least one `.xlsx` + one `.md` report.
4. Include data source APIs in the markdown report.
