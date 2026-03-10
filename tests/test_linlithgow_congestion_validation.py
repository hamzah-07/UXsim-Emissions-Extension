"""Checks for the Linlithgow congestion-sensitivity validation script."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from experiments.linlithgow_congestion_validation import (
    build_linlithgow_congestion_validation_summary,
)


class LinlithgowCongestionValidationTestCase(unittest.TestCase):
    def test_validation_summary_contains_expected_trends(self) -> None:
        lines = build_linlithgow_congestion_validation_summary()
        output = "\n".join(lines)

        self.assertIn("Scenario family: linlithgow-town-centre", output)
        self.assertIn("Average-speed baseline -> peak-demand:", output)
        self.assertIn("16245.12 g -> 26270.96 g", output)
        self.assertIn("168.84 -> 169.12 g/km", output)
        self.assertIn("delay 0.58 -> 0.64 s", output)
        self.assertIn("Speed-acceleration baseline -> peak-demand:", output)
        self.assertIn("5458.34 g -> 9521.46 g", output)
        self.assertIn("56.73 -> 61.29 g/km", output)
        self.assertIn("higher total CO2 and higher delay", output)
        self.assertIn("modest rise in g/km", output)


if __name__ == "__main__":
    unittest.main()
