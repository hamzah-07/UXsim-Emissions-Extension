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
    def test_capture_snapshot_before_simulation_starts(self) -> None:
        world, _, _ = build_smoke_world()

        snapshot = UXsimAdapter().capture_snapshot(world)

        self.assertIsNone(snapshot.timestep)
        self.assertIsNone(snapshot.time_s)
        self.assertEqual(snapshot.vehicle_observations, [])
        self.assertEqual(len(snapshot.link_observations), 1)
        self.assertEqual(snapshot.link_observations[0].link_id, "orig_dest")

    def test_adapter_extracts_link_state_before_simulation_starts(self) -> None:
        world, _, _ = build_smoke_world()

        observations = UXsimAdapter().iter_link_observations(world)

        self.assertEqual(len(observations), 1)
        observation = observations[0]
        self.assertEqual(observation.link_id, "orig_dest")
        self.assertEqual(observation.speed_mps, 10)
        self.assertEqual(observation.density, 0.0)
        self.assertEqual(observation.flow, 0.0)
        self.assertEqual(observation.num_vehicles, 0)
        self.assertEqual(observation.num_vehicles_queue, 0)
        self.assertEqual(observation.length_m, 100)
        self.assertIsNone(observation.timestep)
        self.assertIsNone(observation.time_s)

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

    def test_adapter_extracts_link_state_mid_simulation(self) -> None:
        world, _, _ = build_smoke_world()
        world.exec_simulation(duration_t2=5)

        observations = UXsimAdapter().iter_link_observations(world)

        self.assertEqual(len(observations), 1)
        observation = observations[0]
        self.assertEqual(observation.link_id, "orig_dest")
        self.assertEqual(observation.speed_mps, 10.0)
        self.assertEqual(observation.density, 0.01)
        self.assertEqual(observation.flow, 0.1)
        self.assertEqual(observation.num_vehicles, 1)
        self.assertEqual(observation.num_vehicles_queue, 0)
        self.assertEqual(observation.length_m, 100)
        self.assertEqual(observation.timestep, 5)
        self.assertEqual(observation.time_s, 5)

    def test_capture_snapshot_mid_simulation(self) -> None:
        world, _, _ = build_smoke_world()
        world.exec_simulation(duration_t2=5)

        snapshot = UXsimAdapter().capture_snapshot(world)

        self.assertEqual(snapshot.timestep, 5)
        self.assertEqual(snapshot.time_s, 5)
        self.assertEqual(len(snapshot.vehicle_observations), 1)
        self.assertEqual(len(snapshot.link_observations), 1)
        self.assertEqual(snapshot.vehicle_observations[0].vehicle_id, "veh_0")
        self.assertEqual(snapshot.link_observations[0].link_id, "orig_dest")

    def test_adapter_returns_no_observations_after_trip_completion(self) -> None:
        world, _, _ = build_smoke_world()
        world.exec_simulation()

        observations = UXsimAdapter().iter_vehicle_observations(world)

        self.assertEqual(observations, [])

    def test_adapter_extracts_link_state_after_trip_completion(self) -> None:
        world, _, _ = build_smoke_world()
        world.exec_simulation()

        observations = UXsimAdapter().iter_link_observations(world)

        self.assertEqual(len(observations), 1)
        observation = observations[0]
        self.assertEqual(observation.link_id, "orig_dest")
        self.assertEqual(observation.num_vehicles, 0)
        self.assertEqual(observation.num_vehicles_queue, 0)
        self.assertEqual(observation.timestep, 60)
        self.assertEqual(observation.time_s, 60)

    def test_capture_snapshot_after_trip_completion(self) -> None:
        world, _, _ = build_smoke_world()
        world.exec_simulation()

        snapshot = UXsimAdapter().capture_snapshot(world)

        self.assertEqual(snapshot.timestep, 60)
        self.assertEqual(snapshot.time_s, 60)
        self.assertEqual(snapshot.vehicle_observations, [])
        self.assertEqual(len(snapshot.link_observations), 1)
        self.assertEqual(snapshot.link_observations[0].num_vehicles, 0)


if __name__ == "__main__":
    unittest.main()
