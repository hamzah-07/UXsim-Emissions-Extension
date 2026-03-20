"""Tests for typed town-centre signal-plan loading."""

from pathlib import Path
import json
import sys
from tempfile import TemporaryDirectory
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from uxsim_emissions.scenarios import load_town_centre_signal_plan


class TownCentreSignalPlanTestCase(unittest.TestCase):
    def test_loads_fixed_time_signal_plan(self) -> None:
        with TemporaryDirectory() as temp_dir:
            signal_plan_path = Path(temp_dir) / "signals.json"
            signal_plan_path.write_text(
                json.dumps(
                    {
                        "name": "fixed_time",
                        "node_plans": [
                            {"node_name": "node_a", "signal": [35.0, 25.0]},
                        ],
                        "link_plans": [
                            {"link_name": "link_1", "signal_group": [0]},
                            {"link_name": "link_2", "signal_group": [1]},
                        ],
                    }
                ),
                encoding="utf-8",
            )

            plan = load_town_centre_signal_plan(signal_plan_path)

        self.assertEqual(plan.name, "fixed_time")
        self.assertEqual(plan.node_plans[0].node_name, "node_a")
        self.assertEqual(plan.node_plans[0].signal, (35.0, 25.0))
        self.assertEqual(plan.node_plans[0].signal_offset_s, 0.0)
        self.assertEqual(plan.link_plans[0].link_name, "link_1")
        self.assertEqual(plan.link_plans[0].signal_group, (0,))


if __name__ == "__main__":
    unittest.main()
