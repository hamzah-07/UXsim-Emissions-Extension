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
    load_speed_acceleration_factor_table,
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
        load_speed_acceleration_factor_table(
            PROJECT_ROOT
            / "data"
            / "emission_factors"
            / "starter_speed_acceleration_co2_factors.csv"
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

    return [
        f"Scenario: {world.name}",
        f"Interval: timestep {current_observation.timestep} at {current_observation.time_s} s",
        f"Average-speed CO2: {float(average_speed_sample.pollutants_g.get('co2', 0.0)):.2f} g",
        f"Speed-acceleration CO2: {float(speed_accel_sample.pollutants_g.get('co2', 0.0)):.2f} g",
        f"Difference: {float(speed_accel_sample.pollutants_g.get('co2', 0.0) - average_speed_sample.pollutants_g.get('co2', 0.0)):.2f} g",
    ]


if __name__ == "__main__":
    print("\n".join(build_model_comparison_summary()))
