"""Checks for the tiny side-by-side model comparison demo."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from experiments.minimal_model_comparison_demo import build_model_comparison_summary


class MinimalModelComparisonDemoTestCase(unittest.TestCase):
    def test_demo_summary_contains_expected_lines(self) -> None:
        lines = build_model_comparison_summary()
        output = "\n".join(lines)

        self.assertIn("Scenario: minimal-smoke", output)
        self.assertIn("Interval: timestep 5 at 5 s", output)
        self.assertIn("Average-speed CO2: 1.81 g", output)
        self.assertIn("Speed-acceleration CO2: 0.30 g", output)
        self.assertIn("Difference: -1.51 g", output)


if __name__ == "__main__":
    unittest.main()
