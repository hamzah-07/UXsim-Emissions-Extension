"""Checks for the tracked starter speed-acceleration dataset."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from uxsim_emissions.factors import load_speed_acceleration_factor_table


class StarterSpeedAccelerationDatasetTestCase(unittest.TestCase):
    def test_starter_dataset_loads_and_has_expected_coefficients(self) -> None:
        table = load_speed_acceleration_factor_table(
            PROJECT_ROOT
            / "data"
            / "emission_factors"
            / "starter_speed_acceleration_co2_factors.csv"
        )

        self.assertEqual(len(table.factors), 2)

        passenger_car = table.factors_for(vehicle_type="passenger_car")[0]
        self.assertEqual(passenger_car.coeff_constant, 1.2)
        self.assertEqual(passenger_car.coeff_speed, 0.08)
        self.assertEqual(passenger_car.coeff_acceleration, 0.15)

        light_van = table.factors_for(vehicle_type="light_van")[0]
        self.assertEqual(light_van.coeff_constant, 1.6)
        self.assertEqual(light_van.coeff_speed, 0.11)
        self.assertEqual(light_van.coeff_acceleration, 0.19)


if __name__ == "__main__":
    unittest.main()
