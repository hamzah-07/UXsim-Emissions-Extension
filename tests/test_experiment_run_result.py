"""Tests for the small experiment result container."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from uxsim_emissions.experiments import ExperimentRunResult


class ExperimentRunResultTestCase(unittest.TestCase):
    def test_result_starts_with_empty_collections(self) -> None:
        result = ExperimentRunResult(scenario_name="baseline-check")

        self.assertEqual(result.scenario_name, "baseline-check")
        self.assertEqual(result.runtime_seconds, 0.0)
        self.assertEqual(result.snapshots, [])
        self.assertEqual(result.interval_results, [])
        self.assertEqual(result.log_lines, [])


if __name__ == "__main__":
    unittest.main()
