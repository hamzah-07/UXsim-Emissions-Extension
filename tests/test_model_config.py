"""Tests for emissions model selection config."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from uxsim_emissions import EmissionModelConfig, EmissionModelKind, ProjectConfig


class EmissionModelConfigTestCase(unittest.TestCase):
    def test_project_config_defaults_to_average_speed_model(self) -> None:
        config = ProjectConfig()

        self.assertEqual(config.model.kind, EmissionModelKind.AVERAGE_SPEED)

    def test_model_config_accepts_valid_string_values(self) -> None:
        config = EmissionModelConfig(kind="speed_acceleration")

        self.assertEqual(config.kind, EmissionModelKind.SPEED_ACCELERATION)

    def test_model_config_rejects_unknown_model_kinds(self) -> None:
        with self.assertRaises(ValueError):
            EmissionModelConfig(kind="fuel_based")


if __name__ == "__main__":
    unittest.main()
