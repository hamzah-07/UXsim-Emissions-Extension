"""Tests for typed town-centre import configuration loading."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from uxsim_emissions.scenarios import load_town_centre_import_config


class TownCentreImportConfigTestCase(unittest.TestCase):
    def test_loads_linlithgow_metadata_into_typed_config(self) -> None:
        config = load_town_centre_import_config(
            PROJECT_ROOT / "scenarios" / "town_centre" / "linlithgow_metadata.json"
        )

        self.assertEqual(config.study_area, "Linlithgow town centre")
        self.assertEqual(config.country, "Scotland")
        self.assertEqual(config.bbox.as_tuple(), (-3.63, 55.965, -3.58, 55.985))
        self.assertEqual(config.raw_osm_basename, "linlithgow_bbox")
        self.assertEqual(config.processed_nodes_csv, "linlithgow_nodes.csv")
        self.assertEqual(config.processed_links_csv, "linlithgow_links.csv")
        self.assertEqual(
            config.fixed_time_signal_plan_json,
            "linlithgow_fixed_time_signals.json",
        )
        self.assertEqual(
            config.baseline_demand_profile_json,
            "linlithgow_baseline_demands.json",
        )


if __name__ == "__main__":
    unittest.main()
