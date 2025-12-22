"""Smoke checks for the minimal UXsim integration runner."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from experiments.minimal_uxsim_smoke import run_smoke


class MinimalUXsimSmokeTestCase(unittest.TestCase):
    def test_smoke_run_reports_expected_state_transitions(self) -> None:
        result = run_smoke()

        self.assertEqual(result["deltat_s"], 1)
        self.assertEqual(result["initial"]["vehicle"]["state"], "home")
        self.assertEqual(result["mid_run"]["vehicle"]["state"], "run")
        self.assertEqual(result["completed"]["vehicle"]["state"], "end")
        self.assertEqual(result["completed"]["vehicle"]["travel_time_s"], 10)
        self.assertEqual(result["completed"]["vehicle"]["distance_traveled_m"], 100)
        self.assertEqual(result["completed"]["world"]["num_vehicles_running"], 0)


if __name__ == "__main__":
    unittest.main()
