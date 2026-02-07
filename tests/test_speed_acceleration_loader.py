"""Tests for speed-acceleration factor loading and validation."""

from pathlib import Path
import csv
import sys
import tempfile
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from uxsim_emissions.factors import load_speed_acceleration_factor_table


class SpeedAccelerationFactorLoaderTestCase(unittest.TestCase):
    def test_loads_valid_coefficient_table(self) -> None:
        csv_path = self._write_csv(
            fieldnames=[
                "vehicle_type",
                "pollutant",
                "coeff_constant",
                "coeff_speed",
                "coeff_acceleration",
            ],
            rows=[{"vehicle_type": "car", "pollutant": "co2", "coeff_constant": "1.0", "coeff_speed": "0.1", "coeff_acceleration": "0.2"}],
        )

        table = load_speed_acceleration_factor_table(csv_path)

        self.assertEqual(len(table.factors), 1)
        factor = table.factors_for(vehicle_type="car")[0]
        self.assertEqual(factor.coeff_constant, 1.0)
        self.assertEqual(factor.coeff_speed, 0.1)
        self.assertEqual(factor.coeff_acceleration, 0.2)

    def test_allows_negative_numeric_coefficients(self) -> None:
        csv_path = self._write_csv(
            fieldnames=[
                "vehicle_type",
                "pollutant",
                "coeff_constant",
                "coeff_speed",
                "coeff_acceleration",
            ],
            rows=[{"vehicle_type": "car", "pollutant": "co2", "coeff_constant": "1.0", "coeff_speed": "-0.1", "coeff_acceleration": "0.2"}],
        )

        table = load_speed_acceleration_factor_table(csv_path)

        self.assertEqual(table.factors_for(vehicle_type="car")[0].coeff_speed, -0.1)

    def test_rejects_missing_required_columns(self) -> None:
        csv_path = self._write_csv(
            fieldnames=["vehicle_type", "pollutant", "coeff_constant", "coeff_speed"],
            rows=[{"vehicle_type": "car", "pollutant": "co2", "coeff_constant": "1.0", "coeff_speed": "0.1"}],
        )

        with self.assertRaisesRegex(ValueError, "missing required columns"):
            load_speed_acceleration_factor_table(csv_path)

    def _write_csv(self, *, fieldnames: list[str], rows: list[dict[str, str]]) -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        csv_path = Path(temp_dir.name) / "speed_accel_factors.csv"
        with csv_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        return csv_path


if __name__ == "__main__":
    unittest.main()
