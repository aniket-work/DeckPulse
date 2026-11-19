"""ASCII brief helpers for DeckPulse."""

from __future__ import annotations

from typing import Any


def format_ascii_table(report: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("DeckPulse parking-garage gate telemetry brief")
    lines.append(
        f"rows={report['row_count']} alerts={report['alert_count']} "
        f"ok={report['ok_count']} alert_rate={report['alert_rate']:.2f}%"
    )
    lines.append(f"threshold OccupancyPct > {report['alert_threshold_pct']}")
    lines.append("")
    lines.append(f"{'DECK':<10} {'AVG_PCT':>8} {'READINGS':>9}")
    for item in report["deck_summary"]:
        lines.append(
            f"{item['deck']:<10} {item['avg_occupancy_pct']:>8.2f} {item['readings']:>9}"
        )
    lines.append("")
    lines.append(f"{'DECK':<10} {'ALERTS':>8}")
    for item in report["alerts_by_deck"]:
        lines.append(f"{item['deck']:<10} {item['alerts']:>8}")
    lines.append("")
    lines.append(
        f"peak {report['peak_gate']} @ {report['peak_occupancy_pct']:.2f}% "
        f"({report['peak_deck']}) {report['peak_timestamp']}"
    )
    if report["alerts_by_deck"]:
        top = report["alerts_by_deck"][0]
        lines.append(f"watch first: {top['deck']} ({top['alerts']} ALERT)")
    lines.append("")
    lines.append("first ALERT rows")
    lines.append(f"{'TIMESTAMP':<22} {'GATE':<10} {'DECK':<10} {'OCC%':>8}")
    for row in report["first_alerts"]:
        lines.append(
            f"{row.timestamp:<22} {row.gate_id:<10} {row.deck:<10} "
            f"{row.occupancy_pct:>8.2f}"
        )
    return "\n".join(lines)
