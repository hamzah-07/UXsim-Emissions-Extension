"""Tests for the speed-acceleration model skeleton."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from uxsim_emissions.factors import SpeedAccelerationFactor, SpeedAccelerationFactorTable
from uxsim_emissions.models import SpeedAccelerationCO2Model


class SpeedAccelerationModelTestCase(unittest.TestCase):
    def test_model_keeps_expected_defaults(self) -> None:
        model = SpeedAccelerationCO2Model(factor_table=_build_table())

        self.assertEqual(model.default_vehicle_type, "passenger_car")
        self.assertEqual(model.pollutant, "co2")
        self.assertEqual(model.name, "speed_acceleration_co2")

    def test_model_compute_is_not_implemented_yet(self) -> None:
        model = SpeedAccelerationCO2Model(factor_table=_build_table())

        with self.assertRaises(NotImplementedError):
            model.compute(speed_mps=10.0, acceleration_mps2=1.0, distance_m=5.0)


def _build_table() -> SpeedAccelerationFactorTable:
    return SpeedAccelerationFactorTable(
        factors=[SpeedAccelerationFactor("passenger_car", "co2", 1.0, 0.1, 0.2)]
    )


if __name__ == "__main__":
    unittest.main()
