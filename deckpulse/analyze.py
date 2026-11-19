"""Local analysis that mirrors the KQL explore queries for DeckPulse."""

from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ALERT_OCCUPANCY_PCT = 88.0


@dataclass(frozen=True)
class Reading:
    timestamp: str
    gate_id: str
    deck: str
    occupancy_pct: float
    wait_seconds: float
    throughput_per_min: float
    status: str


def load_readings(path: Path) -> list[Reading]:
    rows: list[Reading] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for raw in reader:
            rows.append(
                Reading(
                    timestamp=raw["Timestamp"],
                    gate_id=raw["GateId"],
                    deck=raw["Deck"],
                    occupancy_pct=float(raw["OccupancyPct"]),
                    wait_seconds=float(raw["WaitSeconds"]),
                    throughput_per_min=float(raw["ThroughputPerMin"]),
                    status=raw["Status"],
                )
            )
    return rows


def summarize_by_deck(rows: list[Reading]) -> list[dict[str, Any]]:
    totals: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        totals[row.deck].append(row.occupancy_pct)
    summary = [
        {
            "deck": deck,
            "avg_occupancy_pct": round(sum(levels) / len(levels), 2),
            "readings": len(levels),
        }
        for deck, levels in totals.items()
    ]
    summary.sort(key=lambda item: item["avg_occupancy_pct"], reverse=True)
    return summary


def alert_rows(rows: list[Reading]) -> list[Reading]:
    return sorted(
        [row for row in rows if row.status == "ALERT"],
        key=lambda row: row.timestamp,
    )


def alerts_by_deck(rows: list[Reading]) -> list[dict[str, Any]]:
    counts: dict[str, int] = defaultdict(int)
    for row in alert_rows(rows):
        counts[row.deck] += 1
    ranked = [{"deck": deck, "alerts": count} for deck, count in counts.items()]
    ranked.sort(key=lambda item: item["alerts"], reverse=True)
    return ranked


def build_report(rows: list[Reading]) -> dict[str, Any]:
    alerts = alert_rows(rows)
    by_deck = summarize_by_deck(rows)
    alert_rank = alerts_by_deck(rows)
    peak = max(rows, key=lambda row: row.occupancy_pct)
    return {
        "row_count": len(rows),
        "alert_count": len(alerts),
        "ok_count": len(rows) - len(alerts),
        "alert_rate": round(100.0 * len(alerts) / len(rows), 2) if rows else 0.0,
        "deck_summary": by_deck,
        "alerts_by_deck": alert_rank,
        "peak_gate": peak.gate_id,
        "peak_occupancy_pct": peak.occupancy_pct,
        "peak_deck": peak.deck,
        "peak_timestamp": peak.timestamp,
        "first_alerts": alerts[:8],
        "alert_threshold_pct": ALERT_OCCUPANCY_PCT,
        "preview": rows[:10],
    }
