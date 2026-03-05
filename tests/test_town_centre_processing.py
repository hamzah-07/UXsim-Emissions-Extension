"""Tests for OSM town-centre conversion helpers."""

from pathlib import Path
import sys
import unittest

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from uxsim_emissions.scenarios import (
    build_processed_town_centre_tables_from_frames,
    linlithgow_preprocessing_rules,
)


class TownCentreProcessingTestCase(unittest.TestCase):
    def test_builds_processed_tables_from_osm_like_frames(self) -> None:
        nodes_frame = pd.DataFrame(
            [
                {"osmid": 1, "x": -3.62, "y": 55.97},
                {"osmid": 2, "x": -3.61, "y": 55.971},
                {"osmid": 3, "x": -3.60, "y": 55.972},
            ]
        )
        edges_frame = pd.DataFrame(
            [
                {
                    "u": 1,
                    "v": 2,
                    "key": 0,
                    "highway": "primary",
                    "maxspeed": "30 mph",
                    "length": 120.0,
                    "lanes": "2",
                    "oneway": True,
                },
                {
                    "u": 2,
                    "v": 3,
                    "key": 0,
                    "highway": "footway",
                    "length": 80.0,
                    "oneway": False,
                },
            ]
        )

        nodes_table, links_table = build_processed_town_centre_tables_from_frames(
            nodes_frame=nodes_frame,
            edges_frame=edges_frame,
            rules=linlithgow_preprocessing_rules(),
        )

        self.assertEqual(list(nodes_table["name"]), ["1", "2"])
        self.assertEqual(len(links_table), 1)
        self.assertEqual(links_table.loc[0, "name"], "tc_1_2_0")
        self.assertAlmostEqual(links_table.loc[0, "free_flow_speed_mps"], 13.4112)
        self.assertEqual(links_table.loc[0, "number_of_lanes"], 2)


if __name__ == "__main__":
    unittest.main()
