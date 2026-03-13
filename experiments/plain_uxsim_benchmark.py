"""Plain UXsim timing helpers used as the benchmark baseline."""

from __future__ import annotations

from pathlib import Path
import sys
from time import perf_counter

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from uxsim_emissions.integration import build_baseline_scenario
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


if __name__ == "__main__":
    benchmark = run_plain_uxsim_small_network_benchmark()
    print(
        f"{benchmark['scenario_name']}: plain UXsim runtime "
        f"{benchmark['runtime_seconds']:.6f} s"
    )
