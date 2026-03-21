"""Checks for the Linlithgow signal-policy comparison helper."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from experiments.linlithgow_signal_policy_comparison import (
    build_linlithgow_signal_policy_comparison_summary,
)
from uxsim_emissions.scenarios import TownCentreVariant


class LinlithgowSignalPolicyComparisonTestCase(unittest.TestCase):
    def test_summary_contains_both_signal_policies_and_models(self) -> None:
        lines = build_linlithgow_signal_policy_comparison_summary()
        output = "\n".join(lines)

        self.assertIn("Scenario family: linlithgow-town-centre-signal-policies", output)
        self.assertIn("fixed_time / average_speed:", output)
        self.assertIn("fixed_time / speed_acceleration:", output)
        self.assertIn("responsive / average_speed:", output)
        self.assertIn("responsive / speed_acceleration:", output)
        self.assertIn("g/km", output)
        self.assertIn("delay", output)
        self.assertIn("runtime", output)

    def test_summary_can_run_peak_demand_variant(self) -> None:
        lines = build_linlithgow_signal_policy_comparison_summary(
            variant=TownCentreVariant.PEAK_DEMAND,
        )
        output = "\n".join(lines)

        self.assertIn("Demand variant: peak_demand", output)
        self.assertIn("responsive / average_speed:", output)


if __name__ == "__main__":
    unittest.main()
