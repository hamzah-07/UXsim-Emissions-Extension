"""Checks for the Linlithgow town-centre baseline model comparison script."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from experiments.linlithgow_model_comparison import (
    build_linlithgow_model_comparison_summary,
)


class LinlithgowModelComparisonTestCase(unittest.TestCase):
    def test_comparison_summary_contains_expected_lines(self) -> None:
        lines = build_linlithgow_model_comparison_summary()
        output = "\n".join(lines)

        self.assertIn("Scenario: linlithgow-town-centre-baseline", output)
        self.assertIn("Average-speed CO2: 12210.88 g", output)
        self.assertIn("Average-speed intensity: 126.91 g/km", output)
        self.assertIn("Speed-acceleration CO2: 5458.34 g", output)
        self.assertIn("Speed-acceleration intensity: 56.73 g/km", output)
        self.assertIn("Difference: -6752.54 g", output)
        self.assertIn("Intensity gap: -70.18 g/km", output)
        self.assertIn("validation plumbing", output)


if __name__ == "__main__":
    unittest.main()
