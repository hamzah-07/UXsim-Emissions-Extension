"""Tiny side-by-side demo comparing the two current emissions models."""

from __future__ import annotations

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from experiments.minimal_uxsim_smoke import build_smoke_world
from uxsim_emissions.factors import (
    load_average_speed_factor_table,
    load_vt_micro_factor_table,
)
from uxsim_emissions.integration import UXsimAdapter
from uxsim_emissions.models import AverageSpeedCO2Model, SpeedAccelerationCO2Model


def build_model_comparison_summary() -> list[str]:
    world, _, _ = build_smoke_world()
    adapter = UXsimAdapter()
    # The point here is not which number is "right" yet, only that both model
    # paths can read the same interval and give us something comparable.
    average_speed_model = AverageSpeedCO2Model(
        load_average_speed_factor_table(
            PROJECT_ROOT / "data" / "emission_factors" / "starter_average_speed_co2_factors.csv"
        )
    )
    speed_accel_model = SpeedAccelerationCO2Model(
        load_vt_micro_factor_table(
            PROJECT_ROOT
            / "data"
            / "emission_factors"
            / "vt_micro_co2_coefficients.csv"
        )
    )

    world.exec_simulation(duration_t2=4)
    previous_observation = adapter.capture_snapshot(world).vehicle_observations[0]
    world.exec_simulation(duration_t2=1)
    current_observation = adapter.capture_snapshot(world).vehicle_observations[0]

    average_speed_sample = average_speed_model.compute_from_observation_pair(
        previous_observation=previous_observation,
        current_observation=current_observation,
    )
    speed_accel_sample = speed_accel_model.compute_from_observation_pair(
        previous_observation=previous_observation,
        current_observation=current_observation,
    )
    average_speed_co2 = float(average_speed_sample.pollutants_g.get("co2", 0.0))
    speed_accel_co2 = float(speed_accel_sample.pollutants_g.get("co2", 0.0))

    return [
        f"Scenario: {world.name}",
        f"Interval: timestep {current_observation.timestep} at {current_observation.time_s} s",
        f"Average-speed CO2: {average_speed_co2:.2f} g",
        f"Average-speed intensity: {_intensity_g_per_km(average_speed_co2, average_speed_sample.distance_m):.2f} g/km",
        f"Speed-acceleration CO2: {speed_accel_co2:.2f} g",
        f"Speed-acceleration intensity: {_intensity_g_per_km(speed_accel_co2, speed_accel_sample.distance_m):.2f} g/km",
        f"Difference: {speed_accel_co2 - average_speed_co2:.2f} g",
        "Note: average-speed now uses COPERT-derived representative factors, so this gap is still provisional.",
    ]


def _intensity_g_per_km(co2_g: float, distance_m: float) -> float:
    if distance_m <= 0:
        return 0.0
    return co2_g / (distance_m / 1000.0)


if __name__ == "__main__":
    print("\n".join(build_model_comparison_summary()))
