"""Runtime benchmark helpers for the Linlithgow town-centre case study."""

from __future__ import annotations

from pathlib import Path
import sys
from time import perf_counter

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from uxsim_emissions import EmissionModelConfig, EmissionModelKind, LoggingConfig
from uxsim_emissions.experiments import ExperimentRunner
from uxsim_emissions.integration import build_baseline_scenario
from uxsim_emissions.models import build_emission_model
from uxsim_emissions.scenarios import (
    TownCentreVariant,
    build_tracked_town_centre_scenario_config,
)

LINLITHGOW_METADATA_PATH = (
    PROJECT_ROOT / "scenarios" / "town_centre" / "linlithgow_metadata.json"
)


def run_plain_uxsim_linlithgow_benchmark(
    *,
    variant: TownCentreVariant | str = TownCentreVariant.BASELINE,
) -> dict[str, float | str]:
    """Run the tracked Linlithgow case study in plain UXsim and time it."""

    scenario = build_tracked_town_centre_scenario_config(
        metadata_path=LINLITHGOW_METADATA_PATH,
        variant=variant,
    )
    baseline = build_baseline_scenario(scenario)
    start_time = perf_counter()
    baseline.world.exec_simulation()
    runtime_seconds = perf_counter() - start_time

    return {
        "scenario_name": scenario.name,
        "variant": TownCentreVariant(variant).value,
        "runtime_seconds": runtime_seconds,
    }


def build_linlithgow_model_overhead_summary(
    *,
    variant: TownCentreVariant | str = TownCentreVariant.BASELINE,
) -> list[str]:
    """Compare Linlithgow runtime overhead across the current model choices."""

    variant_value = TownCentreVariant(variant)
    plain_runtime = run_plain_uxsim_linlithgow_benchmark(
        variant=variant_value
    )["runtime_seconds"]
    average_speed_runtime = _run_emissions_linlithgow_benchmark(
        EmissionModelKind.AVERAGE_SPEED,
        variant=variant_value,
    )
    speed_acceleration_runtime = _run_emissions_linlithgow_benchmark(
        EmissionModelKind.SPEED_ACCELERATION,
        variant=variant_value,
    )

    return [
        "Scenario family: linlithgow-town-centre",
        f"Variant: {variant_value.value}",
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


def _run_emissions_linlithgow_benchmark(
    model_kind: EmissionModelKind,
    *,
    variant: TownCentreVariant,
) -> float:
    scenario = build_tracked_town_centre_scenario_config(
        metadata_path=LINLITHGOW_METADATA_PATH,
        variant=variant,
    )
    runner = ExperimentRunner(
        interval_steps=10,
        max_intervals=None,
        # Match the case-study summary path so we measure model overhead rather
        # than paying extra for retained high-frequency logging.
        logging_config=LoggingConfig(
            per_timestep=False,
            per_vehicle=False,
            per_link=False,
        ),
    )
    model = build_emission_model(EmissionModelConfig(kind=model_kind))
    result = runner.run(
        baseline_scenario=build_baseline_scenario(scenario),
        model=model,
    )
    return result.runtime_seconds


def _overhead_ratio(runtime_seconds: float, plain_runtime_seconds: float) -> float:
    if plain_runtime_seconds <= 0:
        return 0.0
    return runtime_seconds / plain_runtime_seconds


if __name__ == "__main__":
    print("\n".join(build_linlithgow_model_overhead_summary()))
