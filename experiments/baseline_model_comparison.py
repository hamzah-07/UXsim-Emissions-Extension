"""Small side-by-side comparison for the richer baseline scenario."""

from __future__ import annotations

from pathlib import Path
import re
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from experiments.baseline_synthetic_experiment import build_baseline_experiment_summary

TOTAL_CO2_PATTERN = re.compile(r"^Total CO2: ([0-9.]+) g over")


def build_baseline_model_comparison_summary() -> list[str]:
    average_speed_lines = build_baseline_experiment_summary(model_kind="average_speed")
    speed_acceleration_lines = build_baseline_experiment_summary(
        model_kind="speed_acceleration"
    )

    average_speed_total = _extract_total_co2(average_speed_lines)
    speed_acceleration_total = _extract_total_co2(speed_acceleration_lines)

    return [
        "Scenario: baseline-two-link",
        f"Average-speed CO2: {average_speed_total:.2f} g",
        f"Speed-acceleration CO2: {speed_acceleration_total:.2f} g",
        f"Difference: {speed_acceleration_total - average_speed_total:.2f} g",
    ]


def _extract_total_co2(lines: list[str]) -> float:
    for line in lines:
        match = TOTAL_CO2_PATTERN.match(line)
        if match is not None:
            return float(match.group(1))

    raise ValueError("Could not find total CO2 line in baseline summary")


if __name__ == "__main__":
    print("\n".join(build_baseline_model_comparison_summary()))
