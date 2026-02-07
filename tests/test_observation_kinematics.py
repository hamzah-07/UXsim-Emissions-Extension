"""Tests for small observation-pair kinematic helpers."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from uxsim_emissions.integration import VehicleObservation, derive_acceleration_mps2


class ObservationKinematicsTestCase(unittest.TestCase):
    def test_helper_derives_positive_acceleration(self) -> None:
        acceleration = derive_acceleration_mps2(
            previous_observation=_build_observation(speed_mps=8.0, time_s=2.0),
            current_observation=_build_observation(speed_mps=12.0, time_s=4.0),
        )

        self.assertEqual(acceleration, 2.0)

    def test_helper_derives_negative_acceleration(self) -> None:
        acceleration = derive_acceleration_mps2(
            previous_observation=_build_observation(speed_mps=10.0, time_s=3.0),
            current_observation=_build_observation(speed_mps=6.0, time_s=5.0),
        )

        self.assertEqual(acceleration, -2.0)

    def test_helper_rejects_invalid_elapsed_time(self) -> None:
        with self.assertRaises(ValueError):
            derive_acceleration_mps2(
                previous_observation=_build_observation(speed_mps=8.0, time_s=4.0),
                current_observation=_build_observation(speed_mps=12.0, time_s=4.0),
            )


def _build_observation(*, speed_mps: float, time_s: float) -> VehicleObservation:
    return VehicleObservation(
        vehicle_id="veh_0",
        state="run",
        link_id="orig_dest",
        position_m=0.0,
        speed_mps=speed_mps,
        acceleration_mps2=None,
        distance_traveled_m=0.0,
        timestep=int(time_s),
        time_s=time_s,
    )


if __name__ == "__main__":
    unittest.main()
