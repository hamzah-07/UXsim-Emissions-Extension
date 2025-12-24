"""Tests for the initial average-speed CO2 model."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from uxsim_emissions.factors import load_average_speed_factor_table
from uxsim_emissions.integration import UXsimAdapter
from uxsim_emissions.integration.uxsim_adapter import VehicleObservation
from uxsim_emissions.models import AverageSpeedCO2Model
from experiments.minimal_uxsim_smoke import build_smoke_world


class AverageSpeedCO2ModelTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.factor_table = load_average_speed_factor_table(
            PROJECT_ROOT
            / "data"
            / "emission_factors"
            / "starter_average_speed_co2_factors.csv"
        )

    def test_computes_emission_at_exact_speed_band(self) -> None:
        model = AverageSpeedCO2Model(self.factor_table, default_vehicle_type="passenger_car")

        sample = model.compute(speed_mps=30 / 3.6, distance_m=1000)

        self.assertEqual(sample.pollutants_g["co2"], 190.0)
        self.assertEqual(sample.distance_m, 1000)

    def test_interpolates_between_speed_bands(self) -> None:
        model = AverageSpeedCO2Model(self.factor_table, default_vehicle_type="passenger_car")

        sample = model.compute(speed_mps=20 / 3.6, distance_m=1000)

        self.assertEqual(sample.pollutants_g["co2"], 255.0)

    def test_clamps_below_known_speed_range(self) -> None:
        model = AverageSpeedCO2Model(self.factor_table, default_vehicle_type="passenger_car")

        sample = model.compute(speed_mps=5 / 3.6, distance_m=1000)

        self.assertEqual(sample.pollutants_g["co2"], 320.0)

    def test_uses_metadata_vehicle_type_override(self) -> None:
        model = AverageSpeedCO2Model(self.factor_table, default_vehicle_type="passenger_car")

        sample = model.compute(
            speed_mps=30 / 3.6,
            distance_m=500,
            metadata={"vehicle_type": "light_van"},
        )

        self.assertEqual(sample.pollutants_g["co2"], 120.0)

    def test_rejects_negative_speed(self) -> None:
        model = AverageSpeedCO2Model(self.factor_table)

        with self.assertRaisesRegex(ValueError, "speed_mps must be non-negative"):
            model.compute(speed_mps=-1, distance_m=100)

    def test_rejects_unknown_vehicle_type(self) -> None:
        model = AverageSpeedCO2Model(self.factor_table)

        with self.assertRaisesRegex(ValueError, "No co2 average-speed factors found"):
            model.compute(
                speed_mps=10 / 3.6,
                distance_m=100,
                metadata={"vehicle_type": "heavy_truck"},
            )

    def test_compute_from_observation_pair_uses_snapshot_time_delta(self) -> None:
        world, _, _ = build_smoke_world()
        adapter = UXsimAdapter()
        model = AverageSpeedCO2Model(self.factor_table, default_vehicle_type="passenger_car")

        world.exec_simulation(duration_t2=4)
        previous_observation = adapter.capture_snapshot(world).vehicle_observations[0]
        world.exec_simulation(duration_t2=1)
        current_observation = adapter.capture_snapshot(world).vehicle_observations[0]

        sample = model.compute_from_observation_pair(
            previous_observation=previous_observation,
            current_observation=current_observation,
        )

        self.assertAlmostEqual(sample.pollutants_g["co2"], 1.81, places=6)
        self.assertEqual(sample.distance_m, 10.0)

    def test_compute_from_observation_pair_rejects_mismatched_vehicles(self) -> None:
        model = AverageSpeedCO2Model(self.factor_table)

        previous_observation = VehicleObservation(
            vehicle_id="veh_0",
            state="run",
            link_id="orig_dest",
            position_m=10.0,
            speed_mps=10.0,
            acceleration_mps2=None,
            distance_traveled_m=0.0,
            timestep=1,
            time_s=1.0,
        )
        current_observation = VehicleObservation(
            vehicle_id="veh_1",
            state="run",
            link_id="orig_dest",
            position_m=20.0,
            speed_mps=10.0,
            acceleration_mps2=None,
            distance_traveled_m=0.0,
            timestep=2,
            time_s=2.0,
        )

        with self.assertRaisesRegex(ValueError, "same vehicle"):
            model.compute_from_observation_pair(
                previous_observation=previous_observation,
                current_observation=current_observation,
            )

    def test_compute_from_observation_pair_returns_zero_when_vehicle_not_running(self) -> None:
        model = AverageSpeedCO2Model(self.factor_table)

        previous_observation = VehicleObservation(
            vehicle_id="veh_0",
            state="run",
            link_id="orig_dest",
            position_m=90.0,
            speed_mps=10.0,
            acceleration_mps2=None,
            distance_traveled_m=90.0,
            timestep=9,
            time_s=9.0,
        )
        current_observation = VehicleObservation(
            vehicle_id="veh_0",
            state="end",
            link_id=None,
            position_m=0.0,
            speed_mps=10.0,
            acceleration_mps2=None,
            distance_traveled_m=100.0,
            timestep=10,
            time_s=10.0,
        )

        sample = model.compute_from_observation_pair(
            previous_observation=previous_observation,
            current_observation=current_observation,
        )

        self.assertAlmostEqual(sample.pollutants_g["co2"], 1.81, places=6)
        self.assertEqual(sample.distance_m, 10.0)

    def test_compute_from_observation_pair_falls_back_to_average_speed_when_needed(self) -> None:
        model = AverageSpeedCO2Model(self.factor_table)

        previous_observation = VehicleObservation(
            vehicle_id="veh_0",
            state="run",
            link_id="link_a",
            position_m=95.0,
            speed_mps=8.0,
            acceleration_mps2=None,
            distance_traveled_m=0.0,
            timestep=10,
            time_s=10.0,
        )
        current_observation = VehicleObservation(
            vehicle_id="veh_0",
            state="run",
            link_id="link_b",
            position_m=3.0,
            speed_mps=12.0,
            acceleration_mps2=None,
            distance_traveled_m=0.0,
            timestep=11,
            time_s=11.0,
        )

        sample = model.compute_from_observation_pair(
            previous_observation=previous_observation,
            current_observation=current_observation,
        )

        self.assertEqual(sample.distance_m, 10.0)
        self.assertAlmostEqual(sample.pollutants_g["co2"], 1.81, places=6)


if __name__ == "__main__":
    unittest.main()
