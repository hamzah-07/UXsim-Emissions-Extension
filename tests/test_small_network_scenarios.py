"""Tests for reusable small validation-network scenarios."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from uxsim_emissions.integration import build_baseline_scenario
from uxsim_emissions.scenarios import merge_validation_scenario_config


class SmallNetworkScenarioTestCase(unittest.TestCase):
    def test_merge_validation_scenario_builds_cleanly(self) -> None:
        baseline = build_baseline_scenario(merge_validation_scenario_config())

        self.assertEqual(baseline.world.name, "merge-validation-network")
        self.assertEqual(len(baseline.world.NODES), 4)
        self.assertEqual(len(baseline.world.LINKS), 3)
        self.assertEqual(len(baseline.world.VEHICLES), 7)


if __name__ == "__main__":
    unittest.main()
