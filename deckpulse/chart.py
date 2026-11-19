"""Write a simple alert-count chart for DeckPulse."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


def write_alert_chart(report: dict[str, Any], path: Path) -> Path:
    ranked = report["alerts_by_deck"]
    decks = [item["deck"] for item in ranked]
    counts = [item["alerts"] for item in ranked]

    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8.2, 4.2))
    bars = ax.bar(decks, counts, color="#C45C26", edgecolor="#7A3414", width=0.62)
    ax.set_title("ALERT readings by deck")
    ax.set_ylabel("ALERT count")
    ax.set_xlabel("Deck")
    ax.set_ylim(0, max(counts) * 1.25 if counts else 1)
    for bar, count in zip(bars, counts):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.8,
            str(count),
            ha="center",
            va="bottom",
            fontsize=10,
        )
    fig.tight_layout()
    fig.savefig(path, dpi=140)
    plt.close(fig)
    return path
