"""Checks for the tiny snapshot emissions demo script."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from experiments.minimal_snapshot_emissions_demo import build_demo_summary


class MinimalSnapshotEmissionsDemoTestCase(unittest.TestCase):
    def test_demo_summary_contains_expected_lines(self) -> None:
        lines = build_demo_summary()
        output = "\n".join(lines)

        self.assertIn("Scenario: minimal-smoke", output)
        self.assertIn("Interval: timestep 5 at 5 s", output)
        self.assertIn("Total CO2: 1.36 g over 10.0 m", output)
        self.assertIn("- veh_0: 1.36 g CO2 over 10.0 m", output)


if __name__ == "__main__":
    unittest.main()
