"""Tests for speed-acceleration factor schema types."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from uxsim_emissions.factors import SpeedAccelerationFactor, SpeedAccelerationFactorTable


class SpeedAccelerationSchemaTestCase(unittest.TestCase):
    def test_table_filters_by_vehicle_type_and_pollutant(self) -> None:
        table = SpeedAccelerationFactorTable(
            factors=[
                SpeedAccelerationFactor("car", "co2", 1.0, 0.1, 0.2),
                SpeedAccelerationFactor("car", "nox", 2.0, 0.2, 0.3),
                SpeedAccelerationFactor("bus", "co2", 3.0, 0.3, 0.4),
            ]
        )

        series = table.factors_for(vehicle_type="car")

        self.assertEqual(len(series), 1)
        self.assertEqual(series[0].pollutant, "co2")
        self.assertEqual(series[0].coeff_constant, 1.0)

    def test_factor_defaults_keep_optional_terms_zeroed(self) -> None:
        factor = SpeedAccelerationFactor("car", "co2", 1.0, 0.1, 0.2)

        self.assertEqual(factor.coeff_speed_squared, 0.0)
        self.assertEqual(factor.coeff_acceleration_squared, 0.0)
        self.assertEqual(factor.coeff_speed_acceleration, 0.0)


if __name__ == "__main__":
    unittest.main()
