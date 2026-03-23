"""Small side-by-side comparison for the richer baseline scenario."""

from __future__ import annotations

from pathlib import Path
import re
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from experiments.baseline_synthetic_experiment import build_baseline_experiment_summary
from uxsim_emissions import EmissionModelKind

TOTAL_CO2_PATTERN = re.compile(r"^Total CO2: ([0-9.]+) g over ([0-9.]+) m$")


def build_baseline_model_comparison_summary() -> list[str]:
    average_speed_lines = build_baseline_experiment_summary(
        model_kind=EmissionModelKind.AVERAGE_SPEED
    )
    speed_acceleration_lines = build_baseline_experiment_summary(
        model_kind=EmissionModelKind.SPEED_ACCELERATION
    )

    average_speed_total, average_speed_distance_m = _extract_total_summary(
        average_speed_lines
    )
    speed_acceleration_total, speed_acceleration_distance_m = _extract_total_summary(
        speed_acceleration_lines
    )

    return [
        "Scenario: baseline-two-link",
        f"Average-speed CO2: {average_speed_total:.2f} g",
        f"Average-speed intensity: {_intensity_g_per_km(average_speed_total, average_speed_distance_m):.2f} g/km",
        f"Speed-acceleration CO2: {speed_acceleration_total:.2f} g",
        f"Speed-acceleration intensity: {_intensity_g_per_km(speed_acceleration_total, speed_acceleration_distance_m):.2f} g/km",
        f"Difference: {speed_acceleration_total - average_speed_total:.2f} g",
        "Note: this compact comparison is intended as a same-scenario model check.",
    ]


def _extract_total_summary(lines: list[str]) -> tuple[float, float]:
    for line in lines:
        match = TOTAL_CO2_PATTERN.match(line)
        if match is not None:
            return float(match.group(1)), float(match.group(2))

    raise ValueError("Could not find total CO2 line in baseline summary")


def _intensity_g_per_km(co2_g: float, distance_m: float) -> float:
    if distance_m <= 0:
        return 0.0
    return co2_g / (distance_m / 1000.0)


if __name__ == "__main__":
    print("\n".join(build_baseline_model_comparison_summary()))
