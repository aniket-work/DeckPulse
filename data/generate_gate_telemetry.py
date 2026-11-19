#!/usr/bin/env python3
"""Generate the synthetic parking-garage gate telemetry CSV used by DeckPulse.

Running this script with the default options reproduces
data/gate_telemetry.csv exactly: 6,000 rows, seed 19, one reading every
30 seconds starting at 2026-11-01T00:00:00Z.
"""

from __future__ import annotations

import argparse
import csv
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

SEED = 19
ROW_COUNT = 6_000
INTERVAL = timedelta(seconds=30)
START_TIME = datetime(2026, 11, 1, tzinfo=timezone.utc)
GATES = [f"gate-{i:03d}" for i in range(1, 21)]
DECKS = ["Plaza", "River", "Midtown", "Campus"]
SPIKE_PROBABILITY = 0.013
SPIKE_OFFSET_PCT = 22.0
ALERT_OCCUPANCY_PCT = 88.0
COLUMNS = [
    "Timestamp",
    "GateId",
    "Deck",
    "OccupancyPct",
    "WaitSeconds",
    "ThroughputPerMin",
    "Status",
]


def build_rows(seed: int = SEED, row_count: int = ROW_COUNT) -> list[tuple]:
    """Return telemetry rows that match the bundled sample when defaults are used."""
    rng = random.Random(seed)
    deck_of = {gate: rng.choice(DECKS) for gate in GATES}

    rows: list[tuple] = []
    timestamp = START_TIME
    for _ in range(row_count):
        gate = rng.choice(GATES)
        occupancy = round(min(100.0, max(5.0, rng.gauss(62, 14))), 2)
        if rng.random() < SPIKE_PROBABILITY:
            occupancy = round(min(100.0, occupancy + SPIKE_OFFSET_PCT), 2)
        wait_seconds = round(max(0.0, rng.gauss(45, 25) + max(0.0, occupancy - 70) * 1.8), 1)
        throughput = round(max(0.5, rng.gauss(12, 3) - max(0.0, occupancy - 80) * 0.15), 2)
        status = "ALERT" if occupancy > ALERT_OCCUPANCY_PCT else "OK"
        rows.append(
            (
                timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
                gate,
                deck_of[gate],
                occupancy,
                wait_seconds,
                throughput,
                status,
            )
        )
        timestamp += INTERVAL
    return rows


def write_csv(path: Path, rows: list[tuple]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\r\n")
        writer.writerow(COLUMNS)
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "gate_telemetry.csv",
        help="Output CSV path (defaults to data/gate_telemetry.csv).",
    )
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--rows", type=int, default=ROW_COUNT)
    args = parser.parse_args()

    rows = build_rows(seed=args.seed, row_count=args.rows)
    write_csv(args.output, rows)
    alerts = sum(1 for row in rows if row[-1] == "ALERT")
    print(f"Wrote {len(rows)} rows to {args.output} ({alerts} ALERT)")


if __name__ == "__main__":
    main()
