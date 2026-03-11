from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

repo_root = Path(__file__).resolve().parents[2]
skill_scripts = repo_root / '.github' / 'skills' / 'sim-quant-automation' / 'scripts'
sys.path.insert(0, str(skill_scripts))

from build_markdown_report import build_report
from collect_market_data import fetch_snapshot_with_fallback

out_dir = repo_root / 'results' / 'example_factor'
out_dir.mkdir(parents=True, exist_ok=True)

snapshot = fetch_snapshot_with_fallback(prefer_akquant=True)
df = snapshot.dataframe.copy()

if 'pct_change' not in df.columns:
    raise ValueError("Required column 'pct_change' not found in snapshot dataframe.")
if 'turnover' not in df.columns:
    raise ValueError("Required column 'turnover' not found in snapshot dataframe.")

pct = pd.to_numeric(df['pct_change'], errors='coerce')
turnover_log = pd.to_numeric(df['turnover'], errors='coerce').fillna(0.0).map(np.log1p)

pct_std = pct.std()
if pd.isna(pct_std) or float(pct_std) == 0.0:
    momentum = pd.Series([0.0] * len(df), index=df.index, dtype='float64')
else:
    momentum = (pct - pct.mean()) / pct_std

liq_std = turnover_log.std()
if pd.isna(liq_std) or float(liq_std) == 0.0:
    liquidity = pd.Series([0.0] * len(df), index=df.index, dtype='float64')
else:
    liquidity = (turnover_log - turnover_log.mean()) / liq_std

df['momentum_score'] = momentum
df['liquidity_score'] = liquidity
df['composite_factor_score'] = 0.6 * df['momentum_score'] + 0.4 * df['liquidity_score']

xlsx_path = out_dir / f'factor_snapshot_{snapshot.trade_date}.xlsx'
report_path = out_dir / f'factor_report_{snapshot.trade_date}.md'

df.to_excel(xlsx_path, index=False)
report_path.write_text(build_report(df, snapshot.trade_date, snapshot.source), encoding='utf-8')

print(f'Saved dataset: {xlsx_path}')
print(f'Saved report:  {report_path}')

