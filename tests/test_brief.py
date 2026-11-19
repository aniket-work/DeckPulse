from __future__ import annotations

from pathlib import Path

from deckpulse.analyze import alert_rows, build_report, load_readings

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "data" / "gate_telemetry.csv"


def test_sample_has_six_thousand_rows() -> None:
    rows = load_readings(CSV)
    assert len(rows) == 6_000


def test_alert_threshold_and_counts_are_stable() -> None:
    rows = load_readings(CSV)
    report = build_report(rows)
    alerts = alert_rows(rows)
    assert report["alert_count"] == len(alerts)
    assert all(row.occupancy_pct > 88.0 for row in alerts)
    assert all(row.status == "ALERT" for row in alerts)
    assert report["row_count"] == 6_000
    assert report["alert_count"] > 0
    assert report["alerts_by_deck"][0]["alerts"] >= report["alerts_by_deck"][-1]["alerts"]


def test_deck_summary_covers_four_decks() -> None:
    rows = load_readings(CSV)
    report = build_report(rows)
    decks = {item["deck"] for item in report["deck_summary"]}
    assert decks == {"Plaza", "River", "Midtown", "Campus"}
    assert sum(item["readings"] for item in report["deck_summary"]) == 6_000
