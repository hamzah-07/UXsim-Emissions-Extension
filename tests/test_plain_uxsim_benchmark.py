"""Checks for the plain UXsim benchmark helper."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from experiments.plain_uxsim_benchmark import run_plain_uxsim_small_network_benchmark


class PlainUXsimBenchmarkTestCase(unittest.TestCase):
    def test_small_network_benchmark_returns_runtime(self) -> None:
        result = run_plain_uxsim_small_network_benchmark()

        self.assertEqual(result["scenario_name"], "merge-validation-network")
        self.assertGreaterEqual(result["runtime_seconds"], 0.0)


if __name__ == "__main__":
    unittest.main()
