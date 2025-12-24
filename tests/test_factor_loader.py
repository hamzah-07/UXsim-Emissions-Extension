"""Tests for average-speed factor loading and validation."""

from pathlib import Path
import csv
import sys
import tempfile
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from uxsim_emissions.factors import load_average_speed_factor_table


class AverageSpeedFactorLoaderTestCase(unittest.TestCase):
    def test_loads_valid_factor_table(self) -> None:
        csv_path = self._write_csv(
            fieldnames=[
                "vehicle_type",
                "pollutant",
                "speed_kph",
                "emission_g_per_km",
            ],
            rows=[
                {
                    "vehicle_type": "passenger_car",
                    "pollutant": "co2",
                    "speed_kph": "10",
                    "emission_g_per_km": "320",
                },
                {
                    "vehicle_type": "passenger_car",
                    "pollutant": "co2",
                    "speed_kph": "30",
                    "emission_g_per_km": "190",
                },
                {
                    "vehicle_type": "passenger_car",
                    "pollutant": "co2",
                    "speed_kph": "50",
                    "emission_g_per_km": "160",
                },
            ],
        )

        table = load_average_speed_factor_table(csv_path)

        self.assertEqual(len(table.factors), 3)
        passenger_car_series = table.series_for(vehicle_type="passenger_car")
        self.assertEqual(
            [factor.speed_kph for factor in passenger_car_series],
            [10.0, 30.0, 50.0],
        )
        self.assertEqual(
            [factor.emission_g_per_km for factor in passenger_car_series],
            [320.0, 190.0, 160.0],
        )

    def test_rejects_missing_required_columns(self) -> None:
        csv_path = self._write_csv(
            fieldnames=["vehicle_type", "speed_kph", "emission_g_per_km"],
            rows=[
                {
                    "vehicle_type": "passenger_car",
                    "speed_kph": "30",
                    "emission_g_per_km": "190",
                }
            ],
        )

        with self.assertRaisesRegex(ValueError, "missing required columns"):
            load_average_speed_factor_table(csv_path)

    def test_rejects_negative_values(self) -> None:
        csv_path = self._write_csv(
            fieldnames=[
                "vehicle_type",
                "pollutant",
                "speed_kph",
                "emission_g_per_km",
            ],
            rows=[
                {
                    "vehicle_type": "passenger_car",
                    "pollutant": "co2",
                    "speed_kph": "-1",
                    "emission_g_per_km": "190",
                }
            ],
        )

        with self.assertRaisesRegex(ValueError, "must be non-negative"):
            load_average_speed_factor_table(csv_path)

    def _write_csv(
        self,
        *,
        fieldnames: list[str],
        rows: list[dict[str, str]],
    ) -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        csv_path = Path(temp_dir.name) / "factors.csv"
        with csv_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        return csv_path


if __name__ == "__main__":
    unittest.main()
