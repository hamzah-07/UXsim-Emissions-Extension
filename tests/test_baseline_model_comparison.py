"""Checks for the richer baseline comparison script."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from experiments.baseline_model_comparison import build_baseline_model_comparison_summary


class BaselineModelComparisonTestCase(unittest.TestCase):
    def test_comparison_summary_contains_expected_lines(self) -> None:
        lines = build_baseline_model_comparison_summary()
        output = "\n".join(lines)

        self.assertIn("Scenario: baseline-two-link", output)
        self.assertIn("Average-speed CO2: 76.24 g", output)
        self.assertIn("Average-speed intensity: 142.77 g/km", output)
        self.assertIn("Speed-acceleration CO2: 29.10 g", output)
        self.assertIn("Speed-acceleration intensity: 54.49 g/km", output)
        self.assertIn("Difference: -47.14 g", output)
        self.assertIn("gap as provisional", output)


if __name__ == "__main__":
    unittest.main()
