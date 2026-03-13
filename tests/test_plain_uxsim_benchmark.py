"""Checks for the plain UXsim benchmark helper."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from experiments.plain_uxsim_benchmark import (
    build_small_network_model_overhead_summary,
    run_plain_uxsim_small_network_benchmark,
)


class PlainUXsimBenchmarkTestCase(unittest.TestCase):
    def test_small_network_benchmark_returns_runtime(self) -> None:
        result = run_plain_uxsim_small_network_benchmark()

        self.assertEqual(result["scenario_name"], "merge-validation-network")
        self.assertGreaterEqual(result["runtime_seconds"], 0.0)

    def test_small_network_overhead_summary_contains_expected_lines(self) -> None:
        lines = build_small_network_model_overhead_summary()
        output = "\n".join(lines)

        self.assertIn("Scenario: merge-validation-network", output)
        self.assertIn("Plain UXsim runtime:", output)
        self.assertIn("Average-speed runtime:", output)
        self.assertIn("Speed-acceleration runtime:", output)
        self.assertIn("plain UXsim", output)


if __name__ == "__main__":
    unittest.main()
