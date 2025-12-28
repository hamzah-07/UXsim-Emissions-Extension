"""Tests for snapshot runner metadata overrides."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from experiments.minimal_uxsim_smoke import build_smoke_world
from uxsim_emissions.aggregation import run_average_speed_snapshot_interval_with_metadata
from uxsim_emissions.factors import load_average_speed_factor_table
from uxsim_emissions.integration import UXsimAdapter
from uxsim_emissions.models import AverageSpeedCO2Model


class SnapshotRunnerMetadataTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        factor_table = load_average_speed_factor_table(
            PROJECT_ROOT
            / "data"
            / "emission_factors"
            / "starter_average_speed_co2_factors.csv"
        )
        cls.model = AverageSpeedCO2Model(factor_table)

    def test_applies_vehicle_metadata_override_per_vehicle(self) -> None:
        world, _, _ = build_smoke_world()
        adapter = UXsimAdapter()

        world.exec_simulation(duration_t2=4)
        previous_snapshot = adapter.capture_snapshot(world)
        world.exec_simulation(duration_t2=1)
        current_snapshot = adapter.capture_snapshot(world)

        result = run_average_speed_snapshot_interval_with_metadata(
            model=self.model,
            previous_snapshot=previous_snapshot,
            current_snapshot=current_snapshot,
            vehicle_metadata={"veh_0": {"vehicle_type": "light_van"}},
        )

        self.assertAlmostEqual(
            result.vehicle_samples["veh_0"].pollutants_g["co2"], 2.28, places=6
        )
        self.assertAlmostEqual(result.total_sample.pollutants_g["co2"], 2.28, places=6)


if __name__ == "__main__":
    unittest.main()
