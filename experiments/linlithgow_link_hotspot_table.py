"""Build a reusable Linlithgow hotspot table for later analysis outputs."""

from __future__ import annotations

import csv
from io import StringIO
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from experiments.linlithgow_link_hotspot_validation import (
    build_linlithgow_link_hotspot_rows,
)


def build_linlithgow_link_hotspot_csv_lines() -> list[str]:
    """Render the top Linlithgow link hotspots as CSV lines."""

    fieldnames = [
        "variant",
        "rank",
        "link_id",
        "highway",
        "co2_g",
    ]
    buffer = StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(
        {
            **row,
            "co2_g": f"{float(row['co2_g']):.2f}",
        }
        for row in build_linlithgow_link_hotspot_rows()
    )
    return buffer.getvalue().strip().splitlines()


if __name__ == "__main__":
    print("\n".join(build_linlithgow_link_hotspot_csv_lines()))
