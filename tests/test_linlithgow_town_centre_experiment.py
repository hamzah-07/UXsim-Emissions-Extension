"""Smoke checks for the Linlithgow town-centre experiment entry point."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from experiments.linlithgow_town_centre_experiment import (
    build_linlithgow_town_centre_summary,
)
from uxsim_emissions.scenarios import TownCentreVariant


class LinlithgowTownCentreExperimentTestCase(unittest.TestCase):
    def test_summary_runs_for_baseline_case_study_smoke_path(self) -> None:
        lines = build_linlithgow_town_centre_summary(max_intervals=1)
        output = "\n".join(lines)

        self.assertIn("Variant: baseline", output)
        self.assertIn("Scenario: linlithgow-town-centre-baseline", output)
        self.assertIn("Total CO2:", output)

    def test_summary_runs_for_peak_demand_smoke_path(self) -> None:
        lines = build_linlithgow_town_centre_summary(
            variant=TownCentreVariant.PEAK_DEMAND,
            max_intervals=1,
        )
        output = "\n".join(lines)

        self.assertIn("Variant: peak_demand", output)
        self.assertIn("Scenario: linlithgow-town-centre-peak-demand", output)
        self.assertIn("Total CO2:", output)

    def test_summary_runs_for_fixed_time_signal_smoke_path(self) -> None:
        lines = build_linlithgow_town_centre_summary(
            use_fixed_time_signals=True,
            max_intervals=1,
        )
        output = "\n".join(lines)

        self.assertIn("Signals: fixed_time", output)
        self.assertIn(
            "Scenario: linlithgow-town-centre-baseline-fixed-time-signals",
            output,
        )
        self.assertIn("Total CO2:", output)

    def test_summary_runs_for_responsive_signal_smoke_path(self) -> None:
        lines = build_linlithgow_town_centre_summary(
            use_responsive_signals=True,
            max_intervals=1,
        )
        output = "\n".join(lines)

        self.assertIn("Signals: responsive", output)
        self.assertIn(
            "Scenario: linlithgow-town-centre-baseline-responsive-signals",
            output,
        )
        self.assertIn("Total CO2:", output)


if __name__ == "__main__":
    unittest.main()
