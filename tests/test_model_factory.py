"""Tests for config-driven emissions model construction."""

from pathlib import Path
import sys
import tempfile
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from uxsim_emissions import EmissionModelConfig, EmissionModelKind
from uxsim_emissions.factors import AverageSpeedFactorTable, VTMicroFactorTable
from uxsim_emissions.models import (
    AverageSpeedCO2Model,
    SpeedAccelerationCO2Model,
    build_emission_model,
)


class EmissionModelFactoryTestCase(unittest.TestCase):
    def test_builds_average_speed_model_from_default_config(self) -> None:
        model = build_emission_model(EmissionModelConfig())

        self.assertIsInstance(model, AverageSpeedCO2Model)
        self.assertIsInstance(model.factor_table, AverageSpeedFactorTable)

    def test_builds_speed_acceleration_model_from_config(self) -> None:
        model = build_emission_model(
            EmissionModelConfig(kind=EmissionModelKind.SPEED_ACCELERATION)
        )

        self.assertIsInstance(model, SpeedAccelerationCO2Model)
        self.assertIsInstance(model.factor_table, VTMicroFactorTable)

    def test_uses_custom_average_speed_factor_table_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_path = Path(temp_dir) / "average_speed.csv"
            csv_path.write_text(
                (
                    "vehicle_type,pollutant,speed_kph,emission_g_per_km\n"
                    "car,co2,50,123.4\n"
                ),
                encoding="utf-8",
            )

            model = build_emission_model(
                EmissionModelConfig(
                    kind=EmissionModelKind.AVERAGE_SPEED,
                    factor_table_path=csv_path,
                )
            )

        self.assertEqual(len(model.factor_table.factors), 1)
        self.assertEqual(model.factor_table.factors[0].vehicle_type, "car")


if __name__ == "__main__":
    unittest.main()
