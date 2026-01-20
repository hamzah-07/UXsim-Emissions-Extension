"""Tests for the core snapshot interval emissions runner."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from experiments.minimal_uxsim_smoke import build_smoke_world
from uxsim_emissions.aggregation import (
    run_average_speed_snapshot_interval,
    run_average_speed_snapshot_sequence,
)
from uxsim_emissions.factors import load_average_speed_factor_table
from uxsim_emissions.integration import UXsimAdapter
from uxsim_emissions.models import AverageSpeedCO2Model


class SnapshotRunnerTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        factor_table = load_average_speed_factor_table(
            PROJECT_ROOT
            / "data"
            / "emission_factors"
            / "starter_average_speed_co2_factors.csv"
        )
        cls.model = AverageSpeedCO2Model(factor_table)

    def test_runs_interval_for_matched_vehicle_observations(self) -> None:
        world, _, _ = build_smoke_world()
        adapter = UXsimAdapter()

        world.exec_simulation(duration_t2=4)
        previous_snapshot = adapter.capture_snapshot(world)
        world.exec_simulation(duration_t2=1)
        current_snapshot = adapter.capture_snapshot(world)

        result = run_average_speed_snapshot_interval(
            model=self.model,
            previous_snapshot=previous_snapshot,
            current_snapshot=current_snapshot,
        )

        self.assertEqual(result.timestep, 5)
        self.assertEqual(result.time_s, 5)
        self.assertEqual(list(result.vehicle_samples), ["veh_0"])
        self.assertAlmostEqual(
            result.vehicle_samples["veh_0"].pollutants_g["co2"], 1.81, places=6
        )
        self.assertAlmostEqual(result.total_sample.pollutants_g["co2"], 1.81, places=6)
        self.assertEqual(result.total_sample.distance_m, 10.0)

    def test_skips_vehicle_without_previous_snapshot_match(self) -> None:
        world, _, _ = build_smoke_world()
        adapter = UXsimAdapter()

        previous_snapshot = adapter.capture_snapshot(world)
        world.exec_simulation(duration_t2=1)
        current_snapshot = adapter.capture_snapshot(world)

        result = run_average_speed_snapshot_interval(
            model=self.model,
            previous_snapshot=previous_snapshot,
            current_snapshot=current_snapshot,
        )

        self.assertEqual(result.vehicle_samples, {})
        self.assertEqual(result.total_sample.pollutants_g, {})
        self.assertEqual(result.total_sample.distance_m, 0)

    def test_runs_multiple_consecutive_snapshot_intervals(self) -> None:
        world, _, _ = build_smoke_world()
        adapter = UXsimAdapter()

        snapshots = []
        world.exec_simulation(duration_t2=4)
        snapshots.append(adapter.capture_snapshot(world))
        world.exec_simulation(duration_t2=1)
        snapshots.append(adapter.capture_snapshot(world))
        world.exec_simulation(duration_t2=1)
        snapshots.append(adapter.capture_snapshot(world))

        results = run_average_speed_snapshot_sequence(
            model=self.model,
            snapshots=snapshots,
        )

        self.assertEqual(len(results), 2)
        self.assertEqual([result.timestep for result in results], [5, 6])
        self.assertAlmostEqual(results[0].total_sample.pollutants_g["co2"], 1.81, places=6)
        self.assertAlmostEqual(results[1].total_sample.pollutants_g["co2"], 1.81, places=6)
        self.assertEqual(results[0].total_sample.distance_m, 10.0)
        self.assertEqual(results[1].total_sample.distance_m, 10.0)

    def test_returns_empty_sequence_when_there_are_not_enough_snapshots(self) -> None:
        world, _, _ = build_smoke_world()
        adapter = UXsimAdapter()

        world.exec_simulation(duration_t2=4)
        snapshots = [adapter.capture_snapshot(world)]

        results = run_average_speed_snapshot_sequence(
            model=self.model,
            snapshots=snapshots,
        )

        self.assertEqual(results, [])


if __name__ == "__main__":
    unittest.main()
