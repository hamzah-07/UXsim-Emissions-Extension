"""Focused tests for the first UXsim adapter increment."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from experiments.minimal_uxsim_smoke import build_smoke_world
from uxsim_emissions.integration import UXsimAdapter


class UXsimAdapterTestCase(unittest.TestCase):
    def test_adapter_returns_no_observations_before_simulation_starts(self) -> None:
        world, _, _ = build_smoke_world()

        observations = UXsimAdapter().iter_vehicle_observations(world)

        self.assertEqual(observations, [])

    def test_adapter_extracts_running_vehicle_state_mid_simulation(self) -> None:
        world, _, _ = build_smoke_world()
        world.exec_simulation(duration_t2=5)

        observations = UXsimAdapter().iter_vehicle_observations(world)

        self.assertEqual(len(observations), 1)
        observation = observations[0]
        self.assertEqual(observation.vehicle_id, "veh_0")
        self.assertEqual(observation.state, "run")
        self.assertEqual(observation.link_id, "orig_dest")
        self.assertEqual(observation.position_m, 40)
        self.assertEqual(observation.speed_mps, 10.0)
        self.assertIsNone(observation.acceleration_mps2)
        self.assertEqual(observation.timestep, 5)
        self.assertEqual(observation.time_s, 5)

    def test_adapter_returns_no_observations_after_trip_completion(self) -> None:
        world, _, _ = build_smoke_world()
        world.exec_simulation()

        observations = UXsimAdapter().iter_vehicle_observations(world)

        self.assertEqual(observations, [])


if __name__ == "__main__":
    unittest.main()
