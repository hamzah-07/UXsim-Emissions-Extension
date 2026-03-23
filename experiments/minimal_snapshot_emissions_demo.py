"""Tiny end-to-end demo for one snapshot-interval emissions calculation."""

from __future__ import annotations

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from experiments.minimal_uxsim_smoke import build_smoke_world
from uxsim_emissions.aggregation import run_average_speed_snapshot_interval
from uxsim_emissions.factors import load_average_speed_factor_table
from uxsim_emissions.integration import UXsimAdapter
from uxsim_emissions.models import AverageSpeedCO2Model


def build_demo_summary() -> list[str]:
    world, _, _ = build_smoke_world()
    adapter = UXsimAdapter()
    factor_table = load_average_speed_factor_table(
        PROJECT_ROOT / "data" / "emission_factors" / "copert_average_speed_co2_factors.csv"
    )
    model = AverageSpeedCO2Model(factor_table)

    world.exec_simulation(duration_t2=4)
    previous_snapshot = adapter.capture_snapshot(world)
    world.exec_simulation(duration_t2=1)
    current_snapshot = adapter.capture_snapshot(world)

    result = run_average_speed_snapshot_interval(
        model=model,
        previous_snapshot=previous_snapshot,
        current_snapshot=current_snapshot,
    )

    lines = [
        f"Scenario: {world.name}",
        f"Interval: timestep {result.timestep} at {result.time_s} s",
        f"Vehicles with emissions this interval: {len(result.vehicle_samples)}",
        f"Total CO2: {float(result.total_sample.pollutants_g.get('co2', 0.0)):.2f} g over {float(result.total_sample.distance_m):.1f} m",
    ]

    for vehicle_id, sample in result.vehicle_samples.items():
        lines.append(
            f"- {vehicle_id}: {float(sample.pollutants_g.get('co2', 0.0)):.2f} g CO2 over {float(sample.distance_m):.1f} m"
        )

    return lines


if __name__ == "__main__":
    print("\n".join(build_demo_summary()))
