"""Compare fixed-time and responsive Linlithgow signal policies across models."""

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

RUNTIME_PATTERN = re.compile(r"^Runtime: ([0-9.]+) s$")
TOTAL_CO2_PATTERN = re.compile(r"^Total CO2: ([0-9.]+) g over ([0-9.]+) m$")
INTENSITY_PATTERN = re.compile(r"^Emission intensity: ([0-9.]+) g/km$")
AVERAGE_DELAY_PATTERN = re.compile(r"^Average delay: ([0-9.]+) s$")


def build_linlithgow_signal_policy_comparison_summary(
    *,
    variant: TownCentreVariant | str = TownCentreVariant.BASELINE,
) -> list[str]:
    """Build a compact cross-model comparison for Linlithgow signal policies."""

    variant_value = TownCentreVariant(variant)
    lines = [
        "Scenario family: linlithgow-town-centre-signal-policies",
        f"Demand variant: {variant_value.value}",
    ]
    # Keep the output to one summary line per run so the comparison is easy to
    # drop into notes or a dissertation draft before we build richer exports.
    for signals_label, use_fixed_time_signals, use_responsive_signals in (
        ("fixed_time", True, False),
        ("responsive", False, True),
    ):
        for model_kind in (
            EmissionModelKind.AVERAGE_SPEED,
            EmissionModelKind.SPEED_ACCELERATION,
        ):
            metrics = _extract_metrics(
                build_linlithgow_town_centre_summary(
                    model_kind=model_kind,
                    variant=variant_value,
                    use_fixed_time_signals=use_fixed_time_signals,
                    use_responsive_signals=use_responsive_signals,
                )
            )
            lines.append(
                f"{signals_label} / {model_kind.value}: "
                f"{metrics['total_co2_g']:.2f} g, "
                f"{metrics['intensity_g_per_km']:.2f} g/km, "
                f"delay {metrics['average_delay_s']:.2f} s, "
                f"runtime {metrics['runtime_seconds']:.3f} s"
            )
    return lines


def _extract_metrics(lines: list[str]) -> dict[str, float]:
    metrics = {
        "runtime_seconds": 0.0,
        "total_co2_g": 0.0,
        "intensity_g_per_km": 0.0,
        "average_delay_s": 0.0,
    }
    for line in lines:
        runtime_match = RUNTIME_PATTERN.match(line)
        if runtime_match is not None:
            metrics["runtime_seconds"] = float(runtime_match.group(1))
            continue
        total_match = TOTAL_CO2_PATTERN.match(line)
        if total_match is not None:
            metrics["total_co2_g"] = float(total_match.group(1))
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
    print("\n".join(build_linlithgow_signal_policy_comparison_summary()))
