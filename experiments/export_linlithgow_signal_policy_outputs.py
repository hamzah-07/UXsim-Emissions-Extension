"""Write Linlithgow signal-policy CSV outputs to generated files."""

from __future__ import annotations

import csv
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from experiments.linlithgow_signal_policy_comparison import (
    build_linlithgow_signal_policy_delta_rows,
    build_linlithgow_signal_policy_rows,
)

DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "outputs" / "linlithgow_signal_policy"


def export_linlithgow_signal_policy_outputs(
    output_dir: Path | str = DEFAULT_OUTPUT_DIR,
) -> dict[str, Path]:
    """Write the current Linlithgow signal-policy CSV tables."""

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    summary_rows = build_linlithgow_signal_policy_rows()
    delta_rows = build_linlithgow_signal_policy_delta_rows(summary_rows)

    summary_csv_path = output_path / "linlithgow_signal_policy_summary.csv"
    delta_csv_path = output_path / "linlithgow_signal_policy_deltas.csv"

    _write_summary_csv(summary_csv_path, summary_rows)
    _write_delta_csv(delta_csv_path, delta_rows)

    return {
        "signal_policy_summary_csv": summary_csv_path,
        "signal_policy_deltas_csv": delta_csv_path,
    }


def _write_summary_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "variant",
                "signal_policy",
                "model_kind",
                "runtime_seconds",
                "total_co2_g",
                "distance_m",
                "intensity_g_per_km",
                "average_delay_s",
            ]
        )
        for row in rows:
            writer.writerow(
                [
                    row["variant"],
                    row["signal_policy"],
                    row["model_kind"],
                    row["runtime_seconds"],
                    row["total_co2_g"],
                    row["distance_m"],
                    row["intensity_g_per_km"],
                    row["average_delay_s"],
                ]
            )


def _write_delta_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "variant",
                "model_kind",
                "fixed_time_total_co2_g",
                "responsive_total_co2_g",
                "delta_total_co2_g",
                "fixed_time_intensity_g_per_km",
                "responsive_intensity_g_per_km",
                "delta_intensity_g_per_km",
                "fixed_time_average_delay_s",
                "responsive_average_delay_s",
                "delta_average_delay_s",
            ]
        )
        for row in rows:
            writer.writerow(
                [
                    row["variant"],
                    row["model_kind"],
                    row["fixed_time_total_co2_g"],
                    row["responsive_total_co2_g"],
                    row["delta_total_co2_g"],
                    row["fixed_time_intensity_g_per_km"],
                    row["responsive_intensity_g_per_km"],
                    row["delta_intensity_g_per_km"],
                    row["fixed_time_average_delay_s"],
                    row["responsive_average_delay_s"],
                    row["delta_average_delay_s"],
                ]
            )


if __name__ == "__main__":
    exported = export_linlithgow_signal_policy_outputs()
    for name, path in exported.items():
        print(f"{name}: {path}")
