"""Plain-text summaries for small experiment runs."""

from .results import ExperimentRunResult


def build_experiment_summary_lines(result: ExperimentRunResult) -> list[str]:
    """Summarise a run result into readable text lines."""

    total_co2_g = result.totals.total_sample.pollutants_g.get("co2", 0.0)
    total_distance_m = result.totals.total_sample.distance_m
    snapshots_captured_count = result.snapshots_captured_count or len(result.snapshots)
    intervals_computed_count = (
        result.intervals_computed_count or len(result.interval_results)
    )
    lines = [
        f"Scenario: {result.scenario_name}",
        f"Snapshots captured: {snapshots_captured_count}",
        f"Intervals computed: {intervals_computed_count}",
        f"Runtime: {result.runtime_seconds:.3f} s",
        f"Total CO2: {total_co2_g:.2f} g over {total_distance_m:.1f} m",
        f"Emission intensity: {_intensity_g_per_km(total_co2_g, total_distance_m):.2f} g/km",
    ]
    if result.average_delay_seconds is not None:
        lines.append(f"Average delay: {result.average_delay_seconds:.2f} s")

    for index, interval_result in enumerate(result.interval_results, start=1):
        co2_g = interval_result.total_sample.pollutants_g.get("co2", 0.0)
        lines.append(
            f"- Interval {index}: timestep {interval_result.timestep}, "
            f"{co2_g:.2f} g CO2 over {interval_result.total_sample.distance_m:.1f} m"
        )

    return lines


def _intensity_g_per_km(total_co2_g: float, total_distance_m: float) -> float:
    if total_distance_m <= 0:
        return 0.0

    return total_co2_g / (total_distance_m / 1000.0)
