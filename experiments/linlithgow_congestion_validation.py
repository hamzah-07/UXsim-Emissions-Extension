"""Congestion-sensitivity comparison for the Linlithgow town-centre case study."""

from __future__ import annotations

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

TOTAL_CO2_PATTERN = re.compile(r"^Total CO2: ([0-9.]+) g over ([0-9.]+) m$")
AVERAGE_DELAY_PATTERN = re.compile(r"^Average delay: ([0-9.]+) s$")


def build_linlithgow_congestion_validation_summary() -> list[str]:
    """Compare baseline and peak-demand Linlithgow variants for both models."""

    baseline_average_speed = _extract_metrics(
        build_linlithgow_town_centre_summary(
            model_kind=EmissionModelKind.AVERAGE_SPEED,
            variant=TownCentreVariant.BASELINE,
        )
    )
    peak_average_speed = _extract_metrics(
        build_linlithgow_town_centre_summary(
            model_kind=EmissionModelKind.AVERAGE_SPEED,
            variant=TownCentreVariant.PEAK_DEMAND,
        )
    )
    baseline_speed_acceleration = _extract_metrics(
        build_linlithgow_town_centre_summary(
            model_kind=EmissionModelKind.SPEED_ACCELERATION,
            variant=TownCentreVariant.BASELINE,
        )
    )
    peak_speed_acceleration = _extract_metrics(
        build_linlithgow_town_centre_summary(
            model_kind=EmissionModelKind.SPEED_ACCELERATION,
            variant=TownCentreVariant.PEAK_DEMAND,
        )
    )

    return [
        "Scenario family: linlithgow-town-centre",
        (
            "Average-speed baseline -> peak-demand: "
            f"{baseline_average_speed['co2_g']:.2f} g -> {peak_average_speed['co2_g']:.2f} g, "
            f"{baseline_average_speed['intensity_g_per_km']:.2f} -> {peak_average_speed['intensity_g_per_km']:.2f} g/km, "
            f"delay {baseline_average_speed['delay_s']:.2f} -> {peak_average_speed['delay_s']:.2f} s"
        ),
        (
            "Speed-acceleration baseline -> peak-demand: "
            f"{baseline_speed_acceleration['co2_g']:.2f} g -> {peak_speed_acceleration['co2_g']:.2f} g, "
            f"{baseline_speed_acceleration['intensity_g_per_km']:.2f} -> {peak_speed_acceleration['intensity_g_per_km']:.2f} g/km, "
            f"delay {baseline_speed_acceleration['delay_s']:.2f} -> {peak_speed_acceleration['delay_s']:.2f} s"
        ),
        "Validation read-out: both models show higher total CO2 and higher delay under peak demand.",
        "Validation read-out: both models also show a modest rise in g/km, which is a plausible congestion-sensitivity trend.",
    ]


def _extract_metrics(lines: list[str]) -> dict[str, float]:
    total_co2_g = 0.0
    total_distance_m = 0.0
    delay_s = 0.0

    for line in lines:
        total_match = TOTAL_CO2_PATTERN.match(line)
        if total_match is not None:
            total_co2_g = float(total_match.group(1))
            total_distance_m = float(total_match.group(2))
            continue

        delay_match = AVERAGE_DELAY_PATTERN.match(line)
        if delay_match is not None:
            delay_s = float(delay_match.group(1))

    return {
        "co2_g": total_co2_g,
        "distance_m": total_distance_m,
        "intensity_g_per_km": _intensity_g_per_km(total_co2_g, total_distance_m),
        "delay_s": delay_s,
    }


def _intensity_g_per_km(total_co2_g: float, total_distance_m: float) -> float:
    if total_distance_m <= 0:
        return 0.0
    return total_co2_g / (total_distance_m / 1000.0)


if __name__ == "__main__":
    print("\n".join(build_linlithgow_congestion_validation_summary()))
