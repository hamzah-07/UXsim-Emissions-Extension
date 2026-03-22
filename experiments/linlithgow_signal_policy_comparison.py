"""Compare fixed-time and responsive Linlithgow signal policies across models."""

from __future__ import annotations

from collections import defaultdict
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


def build_linlithgow_signal_policy_rows() -> list[dict[str, str]]:
    """Build structured signal-policy rows across tracked demand variants."""

    rows: list[dict[str, str]] = []
    for variant_value in (
        TownCentreVariant.BASELINE,
        TownCentreVariant.PEAK_DEMAND,
    ):
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
                rows.append(
                    {
                        "variant": variant_value.value,
                        "signal_policy": signals_label,
                        "model_kind": model_kind.value,
                        "runtime_seconds": f"{metrics['runtime_seconds']:.3f}",
                        "total_co2_g": f"{metrics['total_co2_g']:.2f}",
                        "distance_m": f"{metrics['distance_m']:.1f}",
                        "intensity_g_per_km": f"{metrics['intensity_g_per_km']:.2f}",
                        "average_delay_s": f"{metrics['average_delay_s']:.2f}",
                    }
                )
    return rows


def build_linlithgow_signal_policy_delta_rows(
    rows: list[dict[str, str]] | None = None,
) -> list[dict[str, str]]:
    """Build fixed-time versus responsive deltas for each variant and model."""

    rows = build_linlithgow_signal_policy_rows() if rows is None else rows
    grouped_rows: dict[tuple[str, str], dict[str, dict[str, str]]] = defaultdict(dict)
    for row in rows:
        grouped_rows[(row["variant"], row["model_kind"])][row["signal_policy"]] = row

    delta_rows: list[dict[str, str]] = []
    for (variant, model_kind), policy_rows in grouped_rows.items():
        fixed_time = policy_rows["fixed_time"]
        responsive = policy_rows["responsive"]
        delta_rows.append(
            {
                "variant": variant,
                "model_kind": model_kind,
                "fixed_time_total_co2_g": fixed_time["total_co2_g"],
                "responsive_total_co2_g": responsive["total_co2_g"],
                "delta_total_co2_g": _difference(
                    responsive["total_co2_g"],
                    fixed_time["total_co2_g"],
                ),
                "fixed_time_intensity_g_per_km": fixed_time["intensity_g_per_km"],
                "responsive_intensity_g_per_km": responsive["intensity_g_per_km"],
                "delta_intensity_g_per_km": _difference(
                    responsive["intensity_g_per_km"],
                    fixed_time["intensity_g_per_km"],
                ),
                "fixed_time_average_delay_s": fixed_time["average_delay_s"],
                "responsive_average_delay_s": responsive["average_delay_s"],
                "delta_average_delay_s": _difference(
                    responsive["average_delay_s"],
                    fixed_time["average_delay_s"],
                ),
            }
        )
    return delta_rows


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
    # The variant line lets the same helper report the baseline and heavier
    # demand stress cases without changing the row structure below.
    for row in build_linlithgow_signal_policy_rows():
        if row["variant"] != variant_value.value:
            continue
        lines.append(
            f"{row['signal_policy']} / {row['model_kind']}: "
            f"{row['total_co2_g']} g, "
            f"{row['intensity_g_per_km']} g/km, "
            f"delay {row['average_delay_s']} s, "
            f"runtime {row['runtime_seconds']} s"
        )
    return lines


def _extract_metrics(lines: list[str]) -> dict[str, float]:
    metrics = {
        "runtime_seconds": 0.0,
        "total_co2_g": 0.0,
        "distance_m": 0.0,
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


def _difference(left: str, right: str) -> str:
    return f"{float(left) - float(right):.2f}"


if __name__ == "__main__":
    print("\n".join(build_linlithgow_signal_policy_comparison_summary()))
