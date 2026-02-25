"""Tests for snapshot interval result data shapes."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from uxsim_emissions.aggregation import SnapshotIntervalEmissionResult


class SnapshotIntervalEmissionResultTestCase(unittest.TestCase):
    def test_result_defaults_to_empty_samples(self) -> None:
        result = SnapshotIntervalEmissionResult(timestep=5, time_s=5.0)

        self.assertEqual(result.timestep, 5)
        self.assertEqual(result.time_s, 5.0)
        self.assertEqual(result.vehicle_samples, {})
        self.assertEqual(result.link_samples, {})
        self.assertEqual(result.total_sample.pollutants_g, {})
        self.assertEqual(result.total_sample.distance_m, 0.0)


if __name__ == "__main__":
    unittest.main()
