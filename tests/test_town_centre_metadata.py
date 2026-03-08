"""Tests for town-centre case-study metadata scaffolding."""

from pathlib import Path
import json
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]


class TownCentreMetadataTestCase(unittest.TestCase):
    def test_linlithgow_metadata_records_expected_bbox_and_outputs(self) -> None:
        metadata_path = PROJECT_ROOT / "scenarios" / "town_centre" / "linlithgow_metadata.json"

        with metadata_path.open("r", encoding="utf-8") as handle:
            metadata = json.load(handle)

        self.assertEqual(metadata["study_area"], "Linlithgow town centre")
        self.assertEqual(metadata["source"]["bbox_string"], "-3.630,55.965,-3.580,55.985")
        self.assertEqual(metadata["planned_outputs"]["processed_nodes_csv"], "linlithgow_nodes.csv")
        self.assertEqual(metadata["planned_outputs"]["processed_links_csv"], "linlithgow_links.csv")
        self.assertEqual(
            metadata["planned_outputs"]["baseline_demand_profile_json"],
            "linlithgow_baseline_demands.json",
        )


if __name__ == "__main__":
    unittest.main()
