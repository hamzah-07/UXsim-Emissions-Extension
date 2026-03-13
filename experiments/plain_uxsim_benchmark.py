"""Plain UXsim timing helpers used as the benchmark baseline."""

from __future__ import annotations

from pathlib import Path
import sys
from time import perf_counter

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from uxsim_emissions.integration import build_baseline_scenario
from uxsim_emissions.models import build_emission_model
from uxsim_emissions import EmissionModelConfig, EmissionModelKind, LoggingConfig
from uxsim_emissions.experiments import ExperimentRunner
from uxsim_emissions.scenarios import merge_validation_scenario_config


def run_plain_uxsim_small_network_benchmark() -> dict[str, float | str]:
    """Run the small validation network in plain UXsim and time it."""

    baseline = build_baseline_scenario(merge_validation_scenario_config())
    start_time = perf_counter()
    baseline.world.exec_simulation()
    runtime_seconds = perf_counter() - start_time

    return {
        "scenario_name": baseline.config.name,
        "runtime_seconds": runtime_seconds,
    }


def build_small_network_model_overhead_summary() -> list[str]:
    """Compare small-network runtime overhead across the current model choices."""

    plain_runtime = run_plain_uxsim_small_network_benchmark()["runtime_seconds"]
    average_speed_runtime = _run_emissions_small_network_benchmark(
        EmissionModelKind.AVERAGE_SPEED
    )
    speed_acceleration_runtime = _run_emissions_small_network_benchmark(
        EmissionModelKind.SPEED_ACCELERATION
    )

    return [
        "Scenario: merge-validation-network",
        f"Plain UXsim runtime: {plain_runtime:.6f} s",
        (
            "Average-speed runtime: "
            f"{average_speed_runtime:.6f} s "
            f"({_overhead_ratio(average_speed_runtime, plain_runtime):.2f}x plain UXsim)"
        ),
        (
            "Speed-acceleration runtime: "
            f"{speed_acceleration_runtime:.6f} s "
            f"({_overhead_ratio(speed_acceleration_runtime, plain_runtime):.2f}x plain UXsim)"
        ),
    ]


def _run_emissions_small_network_benchmark(
    model_kind: EmissionModelKind,
) -> float:
    baseline = build_baseline_scenario(merge_validation_scenario_config())
    runner = ExperimentRunner(
        interval_steps=1,
        max_intervals=None,
        logging_config=LoggingConfig(
            per_timestep=False,
            per_vehicle=False,
            per_link=False,
        ),
    )
    model = build_emission_model(EmissionModelConfig(kind=model_kind))
    result = runner.run(baseline_scenario=baseline, model=model)
    return result.runtime_seconds


def _overhead_ratio(runtime_seconds: float, plain_runtime_seconds: float) -> float:
    if plain_runtime_seconds <= 0:
        return 0.0
    return runtime_seconds / plain_runtime_seconds


if __name__ == "__main__":
    print("\n".join(build_small_network_model_overhead_summary()))
