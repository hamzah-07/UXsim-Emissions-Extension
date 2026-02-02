"""Tests for the reusable baseline scenario builder."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from uxsim_emissions import DemandConfig, LinkConfig, NodeConfig, ScenarioConfig
from uxsim_emissions.integration import BaselineScenario, build_baseline_scenario


class BaselineScenarioTestCase(unittest.TestCase):
    def test_builder_creates_world_and_initial_snapshot(self) -> None:
        scenario_config = ScenarioConfig(
            name="two-link-baseline",
            nodes=[
                NodeConfig(name="orig", x=0.0, y=0.0),
                NodeConfig(name="mid", x=100.0, y=0.0, signal=(20.0, 20.0)),
                NodeConfig(name="dest", x=200.0, y=0.0),
            ],
            links=[
                LinkConfig(
                    name="orig_mid",
                    start_node="orig",
                    end_node="mid",
                    length_m=100.0,
                    free_flow_speed_mps=10.0,
                ),
                LinkConfig(
                    name="mid_dest",
                    start_node="mid",
                    end_node="dest",
                    length_m=100.0,
                    free_flow_speed_mps=8.0,
                    signal_group=(0, 1),
                ),
            ],
            demands=[
                DemandConfig(
                    origin="orig",
                    destination="dest",
                    departure_times_s=(0.0, 5.0, 10.0),
                )
            ],
            tmax_s=180.0,
        )

        baseline = build_baseline_scenario(scenario_config)

        self.assertIsInstance(baseline, BaselineScenario)
        self.assertEqual(baseline.world.name, "two-link-baseline")
        self.assertEqual(len(baseline.world.NODES), 3)
        self.assertEqual(len(baseline.world.LINKS), 2)
        self.assertEqual(len(baseline.world.VEHICLES), 3)
        self.assertEqual(len(baseline.initial_snapshot.link_observations), 2)
        self.assertEqual(baseline.initial_snapshot.vehicle_observations, [])
        self.assertIsNone(baseline.initial_snapshot.timestep)
        self.assertIsNone(baseline.initial_snapshot.time_s)

    def test_builder_uses_vehicle_type_in_generated_vehicle_names(self) -> None:
        scenario_config = ScenarioConfig(
            name="fleet-check",
            nodes=[
                NodeConfig(name="orig", x=0.0, y=0.0),
                NodeConfig(name="dest", x=100.0, y=0.0),
            ],
            links=[
                LinkConfig(
                    name="orig_dest",
                    start_node="orig",
                    end_node="dest",
                    length_m=100.0,
                )
            ],
            demands=[
                DemandConfig(
                    origin="orig",
                    destination="dest",
                    departure_times_s=(0.0, 10.0),
                    vehicle_type="bus",
                )
            ],
        )

        baseline = build_baseline_scenario(scenario_config)
        vehicle_names = sorted(vehicle.name for vehicle in baseline.world.VEHICLES.values())

        self.assertEqual(vehicle_names, ["bus_0", "bus_1"])


if __name__ == "__main__":
    unittest.main()
