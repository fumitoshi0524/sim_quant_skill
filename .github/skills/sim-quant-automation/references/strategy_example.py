import pandas as pd
import numpy as np
from akquant import Strategy, run_backtest

'''
Here we use random data for demonstration.
In a real scenario, you could replace this with actual historical price data.
'''
def generate_data():
    dates = pd.date_range(start="2023-01-01", end="2023-12-31")
    n = len(dates)
    price = 100 * np.cumprod(1 + np.random.normal(0.0005, 0.02, n))
    return pd.DataFrame({
        "date": dates,
        "open": price, "high": price * 1.01, "low": price * 0.99, "close": price,
        "volume": 10000,
        "symbol": "600000"
    })


class MyStrategy(Strategy):
    def on_bar(self, bar):
        position = self.get_position(bar.symbol)
        if position == 0:
            self.buy(symbol=bar.symbol, quantity=100)
        elif position > 0:
            self.sell(symbol=bar.symbol, quantity=100)

df = generate_data()
result = run_backtest(
    strategy=MyStrategy,  
    data=df,              
    symbol="600000",     
    initial_cash=500_000.0,       
    commission_rate=0.0003 
)

print(f"Total Return: {result.metrics.total_return_pct:.2f}%")
print(f"Sharpe Ratio: {result.metrics.sharpe_ratio:.2f}")
print(f"Max Drawdown: {result.metrics.max_drawdown_pct:.2f}%")

print(result.metrics_df)
print(result.trades_df)
print(result.positions_df)
