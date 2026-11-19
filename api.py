#!/usr/bin/env python3
"""Small FastAPI surface for the DeckPulse brief."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from deckpulse.analyze import build_report, load_readings

ROOT = Path(__file__).resolve().parent
CSV_PATH = ROOT / "data" / "gate_telemetry.csv"
STATIC = ROOT / "static"

app = FastAPI(title="DeckPulse", version="0.1.0")
if STATIC.exists():
    app.mount("/static", StaticFiles(directory=STATIC), name="static")


@app.get("/api/brief")
def api_brief() -> dict:
    rows = load_readings(CSV_PATH)
    report = build_report(rows)
    return {
        "row_count": report["row_count"],
        "alert_count": report["alert_count"],
        "ok_count": report["ok_count"],
        "alert_rate": report["alert_rate"],
        "alert_threshold_pct": report["alert_threshold_pct"],
        "deck_summary": report["deck_summary"],
        "alerts_by_deck": report["alerts_by_deck"],
        "peak_gate": report["peak_gate"],
        "peak_occupancy_pct": report["peak_occupancy_pct"],
        "peak_deck": report["peak_deck"],
        "peak_timestamp": report["peak_timestamp"],
        "first_alerts": [
            {
                "timestamp": row.timestamp,
                "gate_id": row.gate_id,
                "deck": row.deck,
                "occupancy_pct": row.occupancy_pct,
            }
            for row in report["first_alerts"]
        ],
    }


@app.get("/")
def dashboard() -> FileResponse:
    return FileResponse(STATIC / "dashboard.html")
