from __future__ import annotations

from datetime import datetime

import pandas as pd


def build_report(snapshot: pd.DataFrame, trade_date: str, source: str) -> str:
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row_count = len(snapshot)

    lines: list[str] = []
    lines.append(f"# Sim Quant Snapshot Report - {trade_date}")
    lines.append("")
    lines.append(f"Generated at: `{generated_at}`")
    lines.append(f"Data source: `{source}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Universe size: `{row_count}`")

    if "pct_change" in snapshot.columns:
        leaders = snapshot.sort_values("pct_change", ascending=False).head(10)
        laggards = snapshot.sort_values("pct_change", ascending=True).head(10)

        lines.append("- Metric: `pct_change`")
        lines.append("")
        lines.append("## Top 10 Gainers")
        lines.append("")
        lines.extend(_markdown_table(leaders, ["symbol", "name", "last", "pct_change"]))
        lines.append("")
        lines.append("## Top 10 Losers")
        lines.append("")
        lines.extend(_markdown_table(laggards, ["symbol", "name", "last", "pct_change"]))
    else:
        lines.append("- Note: `pct_change` column not found, so ranking tables were skipped.")

    if "turnover" in snapshot.columns:
        turnover_top = snapshot.sort_values("turnover", ascending=False).head(10)
        lines.append("")
        lines.append("## Top 10 Turnover")
        lines.append("")
        lines.extend(_markdown_table(turnover_top, ["symbol", "name", "turnover", "pct_change"]))

    factor_cols = [c for c in snapshot.columns if c.lower().endswith("_score") or "factor" in c.lower()]
    if factor_cols:
        lines.append("")
        lines.append("## Factor Score Overview")
        lines.append("")
        for col in factor_cols:
            series = pd.to_numeric(snapshot[col], errors="coerce")
            lines.append(f"- `{col}` mean: `{series.mean():.4f}`")
            lines.append(f"- `{col}` std: `{series.std():.4f}`")

    lines.append("")
    lines.append("## Simple Strategy Signal Summary")
    lines.append("")
    lines.extend(_simple_signal_summary(snapshot))

    lines.append("")
    lines.append("## Data Quality Checks")
    lines.append("")
    lines.append(f"- Non-empty dataset: `{'yes' if row_count > 0 else 'no'}`")
    lines.append(f"- Columns: `{', '.join(snapshot.columns.astype(str).tolist())}`")
    lines.append("")

    return "\n".join(lines)


def _markdown_table(df: pd.DataFrame, columns: list[str]) -> list[str]:
    available = [c for c in columns if c in df.columns]
    if not available:
        return ["No matching columns available for table rendering."]

    view = df[available].copy()
    header = "| " + " | ".join(available) + " |"
    sep = "| " + " | ".join(["---"] * len(available)) + " |"
    rows = ["| " + " | ".join(str(v) for v in row) + " |" for row in view.to_numpy().tolist()]
    return [header, sep, *rows]


def _simple_signal_summary(snapshot: pd.DataFrame) -> list[str]:
    if "pct_change" not in snapshot.columns:
        return ["- Signals skipped: `pct_change` column not found."]

    pct = pd.to_numeric(snapshot["pct_change"], errors="coerce").fillna(0.0)
    buy = int((pct >= 2.0).sum())
    sell = int((pct <= -2.0).sum())
    hold = int(len(pct) - buy - sell)
    return [
        "- Rule: `BUY if pct_change >= 2`, `SELL if pct_change <= -2`, else `HOLD`",
        f"- BUY count: `{buy}`",
        f"- HOLD count: `{hold}`",
        f"- SELL count: `{sell}`",
    ]
