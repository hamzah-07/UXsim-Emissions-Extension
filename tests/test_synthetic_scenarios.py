"""Tests for reusable synthetic scenario definitions."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from uxsim_emissions.scenarios import baseline_two_link_scenario_config


class SyntheticScenarioTestCase(unittest.TestCase):
    def test_baseline_two_link_scenario_matches_expected_shape(self) -> None:
        scenario = baseline_two_link_scenario_config()

        self.assertEqual(scenario.name, "baseline-two-link")
        self.assertEqual(len(scenario.nodes), 3)
        self.assertEqual(len(scenario.links), 2)
        self.assertEqual(len(scenario.demands), 1)
        self.assertEqual(scenario.demands[0].departure_times_s, (0.0, 2.0, 4.0))
        self.assertEqual(scenario.tmax_s, 60.0)


if __name__ == "__main__":
    unittest.main()
