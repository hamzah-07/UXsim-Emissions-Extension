"""Write Linlithgow signal-policy outputs to generated files."""

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
    """Write the current Linlithgow signal-policy CSV tables, figure, and note."""

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    summary_rows = build_linlithgow_signal_policy_rows()
    delta_rows = build_linlithgow_signal_policy_delta_rows(summary_rows)

    summary_csv_path = output_path / "linlithgow_signal_policy_summary.csv"
    delta_csv_path = output_path / "linlithgow_signal_policy_deltas.csv"
    figure_path = output_path / "linlithgow_signal_policy_co2_chart.svg"
    summary_md_path = output_path / "linlithgow_signal_policy_summary.md"

    _write_summary_csv(summary_csv_path, summary_rows)
    _write_delta_csv(delta_csv_path, delta_rows)
    figure_path.write_text(
        _build_co2_chart_svg(summary_rows),
        encoding="utf-8",
    )
    summary_md_path.write_text(
        _build_signal_policy_summary_markdown(summary_rows, delta_rows),
        encoding="utf-8",
    )

    return {
        "signal_policy_summary_csv": summary_csv_path,
        "signal_policy_deltas_csv": delta_csv_path,
        "signal_policy_co2_chart_svg": figure_path,
        "signal_policy_summary_md": summary_md_path,
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


def _build_co2_chart_svg(rows: list[dict[str, str]]) -> str:
    width = 980
    height = 420
    chart_height = 250
    chart_top = 80
    chart_left = 80
    bar_width = 85
    gap = 24
    colours = {
        "fixed_time": "#6B8E5F",
        "responsive": "#C7663A",
    }
    variant_labels = {
        ("baseline", "average_speed"): "Base avg",
        ("baseline", "speed_acceleration"): "Base VT",
        ("peak_demand", "average_speed"): "Peak avg",
        ("peak_demand", "speed_acceleration"): "Peak VT",
    }

    max_co2 = max(float(row["total_co2_g"]) for row in rows)
    bars: list[str] = []
    labels: list[str] = []
    for index, row in enumerate(rows):
        total_co2 = float(row["total_co2_g"])
        bar_height = 0.0 if max_co2 <= 0 else chart_height * (total_co2 / max_co2)
        x = chart_left + index * (bar_width + gap)
        y = chart_top + chart_height - bar_height
        bars.append(
            f'<rect x="{x}" y="{y:.1f}" width="{bar_width}" height="{bar_height:.1f}" fill="{colours[row["signal_policy"]]}" />'
        )
        bars.append(
            f'<text x="{x + bar_width / 2:.1f}" y="{y - 8:.1f}" text-anchor="middle" font-size="13">{total_co2:.0f}</text>'
        )
        labels.append(
            f'<text x="{x + bar_width / 2:.1f}" y="{chart_top + chart_height + 24}" text-anchor="middle" font-size="12">{variant_labels[(row["variant"], row["model_kind"])]}</text>'
        )
        labels.append(
            f'<text x="{x + bar_width / 2:.1f}" y="{chart_top + chart_height + 40}" text-anchor="middle" font-size="11">{row["signal_policy"]}</text>'
        )

    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            '<rect width="100%" height="100%" fill="#F6F2E8" />',
            '<text x="490" y="34" text-anchor="middle" font-size="24" font-family="Georgia, serif">Linlithgow Signal Policy CO2 Comparison</text>',
            '<text x="490" y="58" text-anchor="middle" font-size="14">Fixed-time and responsive signal policies across baseline and peak-demand cases</text>',
            f'<line x1="{chart_left}" y1="{chart_top + chart_height}" x2="{width - 40}" y2="{chart_top + chart_height}" stroke="#333" stroke-width="2" />',
            f'<line x1="{chart_left}" y1="{chart_top}" x2="{chart_left}" y2="{chart_top + chart_height}" stroke="#333" stroke-width="2" />',
            *bars,
            *labels,
            '<text x="28" y="205" transform="rotate(-90 28 205)" text-anchor="middle" font-size="14">Total CO2 (g)</text>',
            '<rect x="690" y="46" width="16" height="16" fill="#6B8E5F" />',
            '<text x="714" y="59" font-size="13">Fixed-time</text>',
            '<rect x="800" y="46" width="16" height="16" fill="#C7663A" />',
            '<text x="824" y="59" font-size="13">Responsive</text>',
            "</svg>",
        ]
    )


def _build_signal_policy_summary_markdown(
    summary_rows: list[dict[str, str]],
    delta_rows: list[dict[str, str]],
) -> str:
    lines = [
        "# Linlithgow Signal Policy Summary",
        "",
        "## Run-Level Comparison",
        "",
        "| Demand variant | Signal policy | Model | Runtime (s) | Total CO2 (g) | Distance (m) | Intensity (g/km) | Average delay (s) |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in summary_rows:
        lines.append(
            "| "
            + " | ".join(
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
            + " |"
        )

    lines.extend(
        [
            "",
            "## Responsive Minus Fixed-Time Deltas",
            "",
            "| Demand variant | Model | Delta CO2 (g) | Delta intensity (g/km) | Delta delay (s) |",
            "| --- | --- | ---: | ---: | ---: |",
        ]
    )
    for row in delta_rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    row["variant"],
                    row["model_kind"],
                    row["delta_total_co2_g"],
                    row["delta_intensity_g_per_km"],
                    row["delta_average_delay_s"],
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Read-Out",
            "",
            "- The responsive policy is compared against the same fixed-time baseline under both the baseline and peak-demand Linlithgow demand profiles.",
            "- The delay reduction is clearer than the CO2 reduction, especially under peak demand, which makes the heavier-demand case the stronger signal-control stress test.",
            "- The chart and delta table together give the dissertation one compact emissions comparison and one compact intervention-effect summary.",
        ]
    )
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    exported = export_linlithgow_signal_policy_outputs()
    for name, path in exported.items():
        print(f"{name}: {path}")
