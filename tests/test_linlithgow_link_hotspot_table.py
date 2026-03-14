"""Checks for the Linlithgow link hotspot table export."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from experiments.linlithgow_link_hotspot_table import (
    build_linlithgow_link_hotspot_csv_lines,
)
from experiments.linlithgow_link_hotspot_validation import (
    build_linlithgow_link_hotspot_rows,
)


class LinlithgowLinkHotspotTableTestCase(unittest.TestCase):
    def test_hotspot_rows_cover_both_variants(self) -> None:
        rows = build_linlithgow_link_hotspot_rows()

        self.assertEqual(len(rows), 10)
        self.assertEqual(rows[0]["variant"], "baseline")
        self.assertEqual(rows[0]["rank"], 1)
        self.assertEqual(rows[0]["link_id"], "tc_322847838_190546646_0")
        self.assertEqual(rows[0]["highway"], "primary")
        self.assertAlmostEqual(float(rows[0]["co2_g"]), 908.97, places=2)
        self.assertEqual(rows[5]["variant"], "peak_demand")
        self.assertEqual(rows[5]["rank"], 1)
        self.assertEqual(rows[5]["link_id"], "tc_863278826_324283489_0")
        self.assertEqual(rows[5]["highway"], "residential")
        self.assertAlmostEqual(float(rows[5]["co2_g"]), 2791.11, places=2)

    def test_hotspot_csv_lines_include_header_and_known_rows(self) -> None:
        lines = build_linlithgow_link_hotspot_csv_lines()
        output = "\n".join(lines)

        self.assertIn("variant,rank,link_id,highway,co2_g", output)
        self.assertIn(
            "baseline,1,tc_322847838_190546646_0,primary,908.97",
            output,
        )
        self.assertIn(
            "peak_demand,1,tc_863278826_324283489_0,residential,2791.11",
            output,
        )


if __name__ == "__main__":
    unittest.main()
