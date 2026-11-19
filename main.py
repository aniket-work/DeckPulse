#!/usr/bin/env python3
"""Print the DeckPulse parking-garage telemetry brief."""

from __future__ import annotations

import argparse
from pathlib import Path

from deckpulse.analyze import build_report, load_readings
from deckpulse.chart import write_alert_chart
from deckpulse.report import format_ascii_table

ROOT = Path(__file__).resolve().parent
DEFAULT_CSV = ROOT / "data" / "gate_telemetry.csv"


def main() -> None:
    parser = argparse.ArgumentParser(description="DeckPulse telemetry brief")
    parser.add_argument(
        "--csv",
        type=Path,
        default=DEFAULT_CSV,
        help="Path to gate_telemetry.csv",
    )
    parser.add_argument(
        "--chart",
        default="",
        help="Optional path for the ALERT-by-deck chart",
    )
    args = parser.parse_args()

    rows = load_readings(args.csv)
    report = build_report(rows)
    print(format_ascii_table(report))
    if args.chart:
        chart_path = Path(args.chart)
        write_alert_chart(report, chart_path)
        print(f"chart: {chart_path}")
    print("[SUCCESS] brief written — laptop mirror of the Eventhouse explore path")


if __name__ == "__main__":
    main()
