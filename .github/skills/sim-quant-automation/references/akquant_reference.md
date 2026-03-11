# AKQuant Reference (for `sim-quant-automation`)

## Official Documentation

- Docs (CN/EN): `https://akquant.akfamily.xyz/`
- GitHub repo: `https://github.com/akfamily/akquant`
- PyPI package: `https://pypi.org/project/akquant/`

## Install / Environment

```powershell
uv sync
uv run python -c "import akquant; print('akquant imported')"
```

## Typical Usage Positioning

Use AKQuant when you need:

- Strategy/backtest engine abstractions
- Performance metrics and risk statistics
- Strategy class lifecycle (`on_bar`, order handling, position management)

Use AkShare + pandas when you only need data ingestion and lightweight analysis.

## API Discovery Patterns

```python
import akquant

names = [n for n in dir(akquant) if not n.startswith("_")]
print(names[:100])
```

Commonly visible interfaces include objects like:

- `Strategy`
- `BacktestConfig` / `BacktestResult`
- indicators such as `SMA`, `EMA`, `RSI`, `MACD`
- order/risk related classes (`OrderType`, `OrderStatus`, `RiskConfig`, etc.)

## Minimal Backtest Skeleton

```python
import akquant as aq
import akshare as ak
from akquant import Strategy

df = ak.stock_zh_a_hist(symbol="600000", start_date="20240101", end_date="20241231", adjust="")

class DemoStrategy(Strategy):
    def on_bar(self, bar):
        pass

result = aq.run_backtest(
    data=df,
    strategy=DemoStrategy,
    initial_cash=100000.0,
    symbol="600000",
)
print(result)
```

## Practical Notes

- AKQuant APIs may evolve quickly; verify current signatures in official docs/examples.
- Keep strategy logic and data-prep logic separated for easier debugging.
- In mixed workflows, use AkShare for data pull and AKQuant for simulation/performance layers.

## Skill Usage Guidance

When users request strategy simulation:

1. Pull and normalize data first (usually with AkShare).
2. Build a task-specific AKQuant strategy script.
3. Run backtest and export:
   - tabular results to `.xlsx`
   - summary/KPI narrative to `.md`
