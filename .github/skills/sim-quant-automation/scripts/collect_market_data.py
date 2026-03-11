from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

import akshare as ak
import pandas as pd


@dataclass
class MarketSnapshot:
    trade_date: str
    dataframe: pd.DataFrame
    source: str


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    rename_map = {
        "代码": "symbol",
        "名称": "name",
        "最新价": "last",
        "涨跌幅": "pct_change",
        "涨跌额": "change",
        "成交量": "volume",
        "成交额": "turnover",
    }
    out = df.rename(columns=rename_map).copy()
    keep = [c for c in ["symbol", "name", "last", "pct_change", "change", "volume", "turnover"] if c in out.columns]
    if keep:
        out = out[keep]
    return out


def fetch_a_share_snapshot() -> MarketSnapshot:
    raw = ak.stock_zh_a_spot_em()
    snapshot = _normalize_columns(raw)
    trade_date = datetime.now().strftime("%Y%m%d")
    return MarketSnapshot(trade_date=trade_date, dataframe=snapshot, source="akshare")


def fetch_snapshot_with_fallback(prefer_akquant: bool = True) -> MarketSnapshot:
    if prefer_akquant:
        akquant_df = _try_fetch_from_akquant()
        if akquant_df is not None and not akquant_df.empty:
            trade_date = datetime.now().strftime("%Y%m%d")
            return MarketSnapshot(trade_date=trade_date, dataframe=_normalize_columns(akquant_df), source="akquant")
    return fetch_a_share_snapshot()


def _try_fetch_from_akquant() -> pd.DataFrame | None:
    try:
        import akquant  # type: ignore
    except Exception:
        return None

    # Probe common callable names to keep compatibility across akquant variants.
    candidates = ("market_snapshot", "get_market_snapshot", "stock_zh_a_spot")
    for name in candidates:
        fn: Any = getattr(akquant, name, None)
        if callable(fn):
            try:
                result = fn()
                if isinstance(result, pd.DataFrame):
                    return result
            except Exception:
                continue
    return None
