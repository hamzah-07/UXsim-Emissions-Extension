"""Checks for the tracked starter average-speed dataset."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from uxsim_emissions.factors import load_average_speed_factor_table


class StarterFactorDatasetTestCase(unittest.TestCase):
    def test_starter_dataset_loads_and_has_expected_series(self) -> None:
        table = load_average_speed_factor_table(
            PROJECT_ROOT
            / "data"
            / "emission_factors"
            / "starter_average_speed_co2_factors.csv"
        )

        self.assertEqual(len(table.factors), 6)

        passenger_car_series = table.series_for(vehicle_type="passenger_car")
        self.assertEqual(
            [factor.emission_g_per_km for factor in passenger_car_series],
            [320.0, 190.0, 160.0],
        )

        light_van_series = table.series_for(vehicle_type="light_van")
        self.assertEqual(
            [factor.emission_g_per_km for factor in light_van_series],
            [380.0, 240.0, 200.0],
        )


if __name__ == "__main__":
    unittest.main()
