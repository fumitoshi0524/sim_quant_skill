from __future__ import annotations

import argparse
from pathlib import Path

from build_markdown_report import build_report
from collect_market_data import fetch_snapshot_with_fallback


def main() -> None:
    parser = argparse.ArgumentParser(description="Run sim quant snapshot pipeline with AkShare/AkQuant-compatible outputs")
    parser.add_argument("--output-dir", default="outputs", help="Directory for xlsx and markdown outputs")
    parser.add_argument("--no-akquant", action="store_true", help="Disable AkQuant attempt and use AkShare directly")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    snapshot = fetch_snapshot_with_fallback(prefer_akquant=not args.no_akquant)

    xlsx_path = output_dir / f"market_snapshot_{snapshot.trade_date}.xlsx"
    report_path = output_dir / f"sim_quant_report_{snapshot.trade_date}.md"

    snapshot.dataframe.to_excel(xlsx_path, index=False)

    report = build_report(snapshot.dataframe, snapshot.trade_date, snapshot.source)
    report_path.write_text(report, encoding="utf-8")

    print(f"Saved dataset: {xlsx_path}")
    print(f"Saved report:  {report_path}")


if __name__ == "__main__":
    main()
