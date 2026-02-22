"""Checks for the small synthetic baseline experiment script."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from experiments.baseline_synthetic_experiment import build_baseline_experiment_summary


class BaselineSyntheticExperimentTestCase(unittest.TestCase):
    def test_script_summary_contains_expected_headings(self) -> None:
        lines = build_baseline_experiment_summary()
        output = "\n".join(lines)

        self.assertIn("Model: average_speed_co2", output)
        self.assertIn("Scenario: baseline-two-link", output)
        self.assertIn("Snapshots captured:", output)
        self.assertIn("Intervals computed:", output)
        self.assertIn("Total CO2:", output)
        self.assertIn("Average delay: 0.50 s", output)
        self.assertIn("- Interval", output)

    def test_script_can_run_speed_acceleration_path(self) -> None:
        lines = build_baseline_experiment_summary(model_kind="speed_acceleration")
        output = "\n".join(lines)

        self.assertIn("Model: speed_acceleration_co2", output)
        self.assertIn("Scenario: baseline-two-link", output)
        self.assertIn("Total CO2:", output)


if __name__ == "__main__":
    unittest.main()
