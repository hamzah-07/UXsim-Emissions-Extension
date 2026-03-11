"""Checks for the Linlithgow per-link hotspot validation script."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from experiments.linlithgow_link_hotspot_validation import (
    build_linlithgow_link_hotspot_validation_summary,
)


class LinlithgowLinkHotspotValidationTestCase(unittest.TestCase):
    def test_hotspot_validation_summary_contains_expected_lines(self) -> None:
        lines = build_linlithgow_link_hotspot_validation_summary()
        output = "\n".join(lines)

        self.assertIn("Scenario family: linlithgow-town-centre", output)
        self.assertIn(
            "Baseline hotspot 1: tc_322847838_190546646_0 (primary), 908.97 g CO2",
            output,
        )
        self.assertIn(
            "Peak-demand hotspot 1: tc_863278826_324283489_0 (residential), 2791.11 g CO2",
            output,
        )
        self.assertIn("through-movement links", output)
        self.assertIn("residential gateway connectors", output)
        self.assertIn("rises from 908.97 g to 2791.11 g", output)


if __name__ == "__main__":
    unittest.main()
