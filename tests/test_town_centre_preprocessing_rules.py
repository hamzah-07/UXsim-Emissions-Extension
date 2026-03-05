"""Tests for Linlithgow town-centre preprocessing defaults."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from uxsim_emissions.scenarios import linlithgow_preprocessing_rules


class TownCentrePreprocessingRulesTestCase(unittest.TestCase):
    def test_linlithgow_rules_cover_core_urban_road_defaults(self) -> None:
        rules = linlithgow_preprocessing_rules()

        self.assertIn("primary", rules.kept_highway_types)
        self.assertIn("residential", rules.kept_highway_types)
        self.assertEqual(rules.default_speed_kph_by_highway["residential"], 32.0)
        self.assertEqual(rules.default_lanes_by_highway["service"], 1)
        self.assertTrue(rules.use_oneway_tags)
        self.assertTrue(rules.simplify_junctions)


if __name__ == "__main__":
    unittest.main()
