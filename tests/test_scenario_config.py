"""Tests for scenario configuration dataclasses."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from uxsim_emissions import DemandConfig, LinkConfig, NodeConfig, ScenarioConfig


class ScenarioConfigTestCase(unittest.TestCase):
    def test_scenario_config_keeps_network_and_demand_shapes(self) -> None:
        scenario = ScenarioConfig(
            name="small-baseline",
            nodes=[
                NodeConfig(name="n1", x=0.0, y=0.0),
                NodeConfig(name="n2", x=100.0, y=0.0, signal=(30.0, 30.0)),
            ],
            links=[
                LinkConfig(
                    name="l1",
                    start_node="n1",
                    end_node="n2",
                    length_m=100.0,
                    free_flow_speed_mps=10.0,
                )
            ],
            demands=[
                DemandConfig(
                    origin="n1",
                    destination="n2",
                    departure_times_s=(0.0, 5.0, 10.0),
                )
            ],
            tmax_s=120.0,
        )

        self.assertEqual(scenario.name, "small-baseline")
        self.assertEqual(len(scenario.nodes), 2)
        self.assertEqual(len(scenario.links), 1)
        self.assertEqual(len(scenario.demands), 1)
        self.assertEqual(scenario.nodes[1].signal, (30.0, 30.0))
        self.assertEqual(scenario.demands[0].departure_times_s, (0.0, 5.0, 10.0))
        self.assertEqual(scenario.tmax_s, 120.0)

    def test_scenario_config_defaults_match_current_small_run_style(self) -> None:
        scenario = ScenarioConfig(
            name="defaults-check",
            nodes=[],
            links=[],
            demands=[],
        )

        self.assertEqual(scenario.deltan, 1)
        self.assertEqual(scenario.random_seed, 42)
        self.assertEqual(scenario.print_mode, 0)
        self.assertEqual(scenario.save_mode, 0)
        self.assertEqual(scenario.show_mode, 0)
        self.assertEqual(scenario.show_progress, 0)
        self.assertEqual(scenario.vehicle_logging_timestep_interval, 1)


if __name__ == "__main__":
    unittest.main()
