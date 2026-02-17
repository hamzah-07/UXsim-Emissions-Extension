"""Tests for VT-Micro factor loading and validation."""

from pathlib import Path
import csv
import sys
import tempfile
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from uxsim_emissions.factors import VTMicroRegime, load_vt_micro_factor_table


class VTMicroFactorLoaderTestCase(unittest.TestCase):
    def test_loads_valid_vt_micro_surface_table(self) -> None:
        csv_path = self._write_csv(
            fieldnames=["vehicle_type", "pollutant", "regime"] + self._coefficient_fields(),
            rows=[{"vehicle_type": "car", "pollutant": "co2", "regime": "negative_acceleration", **self._coefficient_values()}],
        )

        table = load_vt_micro_factor_table(csv_path)

        self.assertEqual(len(table.surfaces), 1)
        surface = table.surface_for(
            vehicle_type="car",
            regime=VTMicroRegime.NEGATIVE_ACCELERATION,
        )
        self.assertEqual(surface.coefficient(speed_power=2, acceleration_power=1), 21.0)

    def test_rejects_missing_required_columns(self) -> None:
        csv_path = self._write_csv(
            fieldnames=["vehicle_type", "pollutant", "regime", "c00"],
            rows=[{"vehicle_type": "car", "pollutant": "co2", "regime": "negative_acceleration", "c00": "1.0"}],
        )

        with self.assertRaisesRegex(ValueError, "missing required columns"):
            load_vt_micro_factor_table(csv_path)

    def test_rejects_invalid_regime_values(self) -> None:
        csv_path = self._write_csv(
            fieldnames=["vehicle_type", "pollutant", "regime"] + self._coefficient_fields(),
            rows=[{"vehicle_type": "car", "pollutant": "co2", "regime": "sideways", **self._coefficient_values()}],
        )

        with self.assertRaisesRegex(ValueError, "valid VT-Micro regime"):
            load_vt_micro_factor_table(csv_path)

    def _coefficient_fields(self) -> list[str]:
        return [f"c{speed_power}{acceleration_power}" for speed_power in range(4) for acceleration_power in range(4)]

    def _coefficient_values(self) -> dict[str, str]:
        return {
            f"c{speed_power}{acceleration_power}": f"{speed_power}{acceleration_power}.0"
            for speed_power in range(4)
            for acceleration_power in range(4)
        }

    def _write_csv(self, *, fieldnames: list[str], rows: list[dict[str, str]]) -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        csv_path = Path(temp_dir.name) / "vt_micro_factors.csv"
        with csv_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        return csv_path


if __name__ == "__main__":
    unittest.main()
