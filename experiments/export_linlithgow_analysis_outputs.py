"""Write reusable Linlithgow analysis tables and figures to generated files."""

from __future__ import annotations

import csv
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
    """Write the current Linlithgow analysis tables and figures."""

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    analysis_rows = build_linlithgow_analysis_rows()
    hotspot_rows = build_linlithgow_link_hotspot_rows()

    run_table_path = output_path / "linlithgow_run_summary.csv"
    hotspot_table_path = output_path / "linlithgow_link_hotspots.csv"
    figure_path = output_path / "linlithgow_intensity_chart.svg"
    summary_path = output_path / "linlithgow_analysis_summary.md"

    _write_run_summary_csv(run_table_path, analysis_rows)
    _write_hotspot_csv(hotspot_table_path, hotspot_rows)
    figure_path.write_text(
        _build_intensity_chart_svg(analysis_rows),
        encoding="utf-8",
    )
    summary_path.write_text(
        _build_analysis_summary_markdown(analysis_rows, hotspot_rows),
        encoding="utf-8",
    )

    return {
        "run_summary_csv": run_table_path,
        "link_hotspots_csv": hotspot_table_path,
        "intensity_chart_svg": figure_path,
        "analysis_summary_md": summary_path,
    }


def _write_run_summary_csv(
    path: Path,
    rows: list[dict[str, str]],
) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "scenario_name",
                "variant",
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


def _write_hotspot_csv(
    path: Path,
    rows: list[dict[str, object]],
) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["variant", "rank", "link_id", "highway", "co2_g"])
        for row in rows:
            writer.writerow(
                [
                    str(row["variant"]),
                    str(row["rank"]),
                    str(row["link_id"]),
                    str(row["highway"]),
                    f"{float(row['co2_g']):.2f}",
                ]
            )


def _build_intensity_chart_svg(rows: list[dict[str, str]]) -> str:
    width = 760
    height = 360
    chart_height = 220
    chart_top = 60
    chart_left = 70
    bar_width = 120
    gap = 35
    colours = {
        "average_speed": "#4E7A5D",
        "speed_acceleration": "#B35C3B",
    }

    max_intensity = max(float(row["intensity_g_per_km"]) for row in rows)
    bars: list[str] = []
    labels: list[str] = []

    for index, row in enumerate(rows):
        intensity = float(row["intensity_g_per_km"])
        bar_height = 0.0 if max_intensity <= 0 else chart_height * (
            intensity / max_intensity
        )
        x = chart_left + index * (bar_width + gap)
        y = chart_top + chart_height - bar_height
        fill = colours[row["model_kind"]]
        label = (
            "Baseline avg"
            if row["variant"] == "baseline" and row["model_kind"] == "average_speed"
            else "Baseline VT"
            if row["variant"] == "baseline"
            else "Peak avg"
            if row["model_kind"] == "average_speed"
            else "Peak VT"
        )
        bars.append(
            f'<rect x="{x}" y="{y:.1f}" width="{bar_width}" height="{bar_height:.1f}" fill="{fill}" />'
        )
        bars.append(
            f'<text x="{x + bar_width / 2:.1f}" y="{y - 8:.1f}" text-anchor="middle" font-size="14">{intensity:.2f}</text>'
        )
        labels.append(
            f'<text x="{x + bar_width / 2:.1f}" y="{chart_top + chart_height + 24}" text-anchor="middle" font-size="13">{label}</text>'
        )

    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            '<rect width="100%" height="100%" fill="#F8F5EE" />',
            '<text x="380" y="32" text-anchor="middle" font-size="22" font-family="Georgia, serif">Linlithgow Emission Intensity</text>',
            f'<line x1="{chart_left}" y1="{chart_top + chart_height}" x2="{width - 40}" y2="{chart_top + chart_height}" stroke="#333" stroke-width="2" />',
            f'<line x1="{chart_left}" y1="{chart_top}" x2="{chart_left}" y2="{chart_top + chart_height}" stroke="#333" stroke-width="2" />',
            *bars,
            *labels,
            '<text x="26" y="174" transform="rotate(-90 26 174)" text-anchor="middle" font-size="14">g/km</text>',
            '<rect x="540" y="46" width="16" height="16" fill="#4E7A5D" />',
            '<text x="564" y="59" font-size="13">Average-speed</text>',
            '<rect x="640" y="46" width="16" height="16" fill="#B35C3B" />',
            '<text x="664" y="59" font-size="13">Speed-acceleration</text>',
            "</svg>",
        ]
    )


def _build_analysis_summary_markdown(
    analysis_rows: list[dict[str, str]],
    hotspot_rows: list[dict[str, object]],
) -> str:
    baseline_hotspots = [row for row in hotspot_rows if row["variant"] == "baseline"][:3]
    peak_hotspots = [row for row in hotspot_rows if row["variant"] == "peak_demand"][:3]

    lines = [
        "# Linlithgow Analysis Summary",
        "",
        "## Run-Level Comparison",
        "",
        "| Variant | Model | Runtime (s) | Total CO2 (g) | Distance (m) | Intensity (g/km) | Average delay (s) |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in analysis_rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    row["variant"],
                    row["model_kind"],
                    row["runtime_seconds"],
                    row["total_co2_g"],
                    row["distance_m"],
                    row["intensity_g_per_km"],
                    row["average_delay_s"],
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Top Link Hotspots",
            "",
            "### Baseline",
            "",
        ]
    )
    for row in baseline_hotspots:
        lines.append(
            f"- Rank {row['rank']}: `{row['link_id']}` ({row['highway']}), {float(row['co2_g']):.2f} g CO2"
        )

    lines.extend(
        [
            "",
            "### Peak Demand",
            "",
        ]
    )
    for row in peak_hotspots:
        lines.append(
            f"- Rank {row['rank']}: `{row['link_id']}` ({row['highway']}), {float(row['co2_g']):.2f} g CO2"
        )

    lines.extend(
        [
            "",
            "## Read-Out",
            "",
            "- Peak demand increases total CO2 and average delay for both current models.",
            "- The average-speed model remains higher than the current speed-acceleration path in both tracked variants.",
            "- Peak-demand hotspots intensify on plausible gateway and corridor links, which gives the case study both network-level and spatially differentiated analysis outputs.",
        ]
    )

    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    exported = export_linlithgow_analysis_outputs()
    for name, path in exported.items():
        print(f"{name}: {path}")
