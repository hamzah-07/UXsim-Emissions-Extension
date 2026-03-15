"""Write reusable Linlithgow analysis tables to generated CSV files."""

from __future__ import annotations

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from experiments.linlithgow_analysis_table import build_linlithgow_analysis_rows
from experiments.linlithgow_link_hotspot_validation import (
    build_linlithgow_link_hotspot_rows,
)

DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "outputs" / "linlithgow_analysis"


def export_linlithgow_analysis_outputs(
    output_dir: Path | str = DEFAULT_OUTPUT_DIR,
) -> dict[str, Path]:
    """Write the current Linlithgow analysis tables to generated CSV files."""

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    analysis_rows = build_linlithgow_analysis_rows()
    hotspot_rows = build_linlithgow_link_hotspot_rows()

    run_table_path = output_path / "linlithgow_run_summary.csv"
    hotspot_table_path = output_path / "linlithgow_link_hotspots.csv"

    _write_run_summary_csv(run_table_path, analysis_rows)
    _write_hotspot_csv(hotspot_table_path, hotspot_rows)

    return {
        "run_summary_csv": run_table_path,
        "link_hotspots_csv": hotspot_table_path,
    }


def _write_run_summary_csv(
    path: Path,
    rows: list[dict[str, str]],
) -> None:
    lines = [
        "scenario_name,variant,model_kind,runtime_seconds,total_co2_g,distance_m,intensity_g_per_km,average_delay_s"
    ]
    for row in rows:
        lines.append(
            ",".join(
                [
                    row["scenario_name"],
                    row["variant"],
                    row["model_kind"],
                    row["runtime_seconds"],
                    row["total_co2_g"],
                    row["distance_m"],
                    row["intensity_g_per_km"],
                    row["average_delay_s"],
                ]
            )
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_hotspot_csv(
    path: Path,
    rows: list[dict[str, object]],
) -> None:
    lines = ["variant,rank,link_id,highway,co2_g"]
    for row in rows:
        lines.append(
            ",".join(
                [
                    str(row["variant"]),
                    str(row["rank"]),
                    str(row["link_id"]),
                    str(row["highway"]),
                    f"{float(row['co2_g']):.2f}",
                ]
            )
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    exported = export_linlithgow_analysis_outputs()
    for name, path in exported.items():
        print(f"{name}: {path}")
