"""Tests for the initial average-speed CO2 model."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from uxsim_emissions.factors import load_average_speed_factor_table
from uxsim_emissions.models import AverageSpeedCO2Model


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


if __name__ == "__main__":
    unittest.main()
