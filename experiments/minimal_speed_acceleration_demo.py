"""Tiny end-to-end demo for one speed-acceleration interval calculation."""

from __future__ import annotations

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from experiments.minimal_uxsim_smoke import build_smoke_world
from uxsim_emissions.factors import load_vt_micro_factor_table
from uxsim_emissions.integration import UXsimAdapter, derive_acceleration_mps2
from uxsim_emissions.models import SpeedAccelerationCO2Model


def build_speed_acceleration_demo_summary() -> list[str]:
    world, _, _ = build_smoke_world()
    adapter = UXsimAdapter()
    # This now uses the tracked VT-Micro table documented in the provenance
    # note so the demo follows the same coefficient path as the main model.
    factor_table = load_vt_micro_factor_table(
        PROJECT_ROOT
        / "data"
        / "emission_factors"
        / "vt_micro_co2_coefficients.csv"
    )
    model = SpeedAccelerationCO2Model(factor_table=factor_table)

    world.exec_simulation(duration_t2=4)
    previous_observation = adapter.capture_snapshot(world).vehicle_observations[0]
    world.exec_simulation(duration_t2=1)
    current_observation = adapter.capture_snapshot(world).vehicle_observations[0]

    acceleration_mps2 = derive_acceleration_mps2(
        previous_observation=previous_observation,
        current_observation=current_observation,
    )
    sample = model.compute_from_observation_pair(
        previous_observation=previous_observation,
        current_observation=current_observation,
    )

    return [
        f"Scenario: {world.name}",
        f"Interval: timestep {current_observation.timestep} at {current_observation.time_s} s",
        f"Derived acceleration: {acceleration_mps2:.2f} m/s^2",
        f"Total CO2: {float(sample.pollutants_g.get('co2', 0.0)):.2f} g over {float(sample.distance_m):.1f} m",
        f"- {current_observation.vehicle_id}: {float(sample.pollutants_g.get('co2', 0.0)):.2f} g CO2 over {float(sample.distance_m):.1f} m",
    ]


if __name__ == "__main__":
    print("\n".join(build_speed_acceleration_demo_summary()))
