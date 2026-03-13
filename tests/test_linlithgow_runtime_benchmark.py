"""Checks for the Linlithgow runtime benchmark helper."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from experiments.linlithgow_runtime_benchmark import (
    build_linlithgow_model_overhead_summary,
    run_plain_uxsim_linlithgow_benchmark,
)


class LinlithgowRuntimeBenchmarkTestCase(unittest.TestCase):
    def test_plain_linlithgow_benchmark_returns_runtime(self) -> None:
        result = run_plain_uxsim_linlithgow_benchmark()

        self.assertEqual(result["scenario_name"], "linlithgow-town-centre-baseline")
        self.assertEqual(result["variant"], "baseline")
        self.assertGreaterEqual(result["runtime_seconds"], 0.0)

    def test_linlithgow_overhead_summary_contains_expected_lines(self) -> None:
        lines = build_linlithgow_model_overhead_summary()
        output = "\n".join(lines)

        self.assertIn("Scenario family: linlithgow-town-centre", output)
        self.assertIn("Variant: baseline", output)
        self.assertIn("Plain UXsim runtime:", output)
        self.assertIn("Average-speed runtime:", output)
        self.assertIn("Speed-acceleration runtime:", output)
        self.assertIn("plain UXsim", output)


if __name__ == "__main__":
    unittest.main()
