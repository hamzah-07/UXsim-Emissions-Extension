"""Build a reusable Linlithgow results table for later analysis outputs."""

from __future__ import annotations

import csv
from io import StringIO
from pathlib import Path
import re
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from experiments.linlithgow_town_centre_experiment import (
    build_linlithgow_town_centre_summary,
)
from uxsim_emissions import EmissionModelKind
from uxsim_emissions.scenarios import TownCentreVariant

SCENARIO_PATTERN = re.compile(r"^Scenario: (.+)$")
RUNTIME_PATTERN = re.compile(r"^Runtime: ([0-9.]+) s$")
TOTAL_CO2_PATTERN = re.compile(r"^Total CO2: ([0-9.]+) g over ([0-9.]+) m$")
INTENSITY_PATTERN = re.compile(r"^Emission intensity: ([0-9.]+) g/km$")
AVERAGE_DELAY_PATTERN = re.compile(r"^Average delay: ([0-9.]+) s$")


def build_linlithgow_analysis_rows() -> list[dict[str, str]]:
    """Collect headline Linlithgow results for both models and variants."""

    rows: list[dict[str, str]] = []

    # Keep the row order stable so downstream tables and figures read
    # consistently across repeated exports.
    for variant in (TownCentreVariant.BASELINE, TownCentreVariant.PEAK_DEMAND):
        for model_kind in (
            EmissionModelKind.AVERAGE_SPEED,
            EmissionModelKind.SPEED_ACCELERATION,
        ):
            metrics = _extract_metrics(
                build_linlithgow_town_centre_summary(
                    model_kind=model_kind,
                    variant=variant,
                )
            )
            rows.append(
                {
                    "scenario_name": metrics["scenario_name"],
                    "variant": variant.value,
                    "model_kind": model_kind.value,
                    "runtime_seconds": f"{float(metrics['runtime_seconds']):.3f}",
                    "total_co2_g": f"{float(metrics['total_co2_g']):.2f}",
                    "distance_m": f"{float(metrics['distance_m']):.1f}",
                    "intensity_g_per_km": f"{float(metrics['intensity_g_per_km']):.2f}",
                    "average_delay_s": f"{float(metrics['average_delay_s']):.2f}",
                }
            )

    return rows


def build_linlithgow_analysis_csv_lines() -> list[str]:
    """Render the Linlithgow analysis rows as CSV lines."""

    fieldnames = [
        "scenario_name",
        "variant",
        "model_kind",
        "runtime_seconds",
        "total_co2_g",
        "distance_m",
        "intensity_g_per_km",
        "average_delay_s",
    ]
    buffer = StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(build_linlithgow_analysis_rows())
    return buffer.getvalue().strip().splitlines()


def _extract_metrics(lines: list[str]) -> dict[str, str | float]:
    metrics: dict[str, str | float] = {
        "scenario_name": "",
        "runtime_seconds": 0.0,
        "total_co2_g": 0.0,
        "distance_m": 0.0,
        "intensity_g_per_km": 0.0,
        "average_delay_s": 0.0,
    }

    for line in lines:
        scenario_match = SCENARIO_PATTERN.match(line)
        if scenario_match is not None:
            metrics["scenario_name"] = scenario_match.group(1)
            continue

        runtime_match = RUNTIME_PATTERN.match(line)
        if runtime_match is not None:
            metrics["runtime_seconds"] = float(runtime_match.group(1))
            continue

        total_match = TOTAL_CO2_PATTERN.match(line)
        if total_match is not None:
            metrics["total_co2_g"] = float(total_match.group(1))
            metrics["distance_m"] = float(total_match.group(2))
            continue

        intensity_match = INTENSITY_PATTERN.match(line)
        if intensity_match is not None:
            metrics["intensity_g_per_km"] = float(intensity_match.group(1))
            continue

        delay_match = AVERAGE_DELAY_PATTERN.match(line)
        if delay_match is not None:
            metrics["average_delay_s"] = float(delay_match.group(1))

    return metrics


if __name__ == "__main__":
    print("\n".join(build_linlithgow_analysis_csv_lines()))
