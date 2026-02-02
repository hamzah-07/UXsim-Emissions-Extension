"""Tests for the first experiment runner slice."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from uxsim_emissions import DemandConfig, LinkConfig, NodeConfig, ScenarioConfig
from uxsim_emissions.experiments import ExperimentRunResult, ExperimentRunner
from uxsim_emissions.factors import load_average_speed_factor_table
from uxsim_emissions.integration import build_baseline_scenario
from uxsim_emissions.models import AverageSpeedCO2Model

FACTOR_TABLE_PATH = (
    PROJECT_ROOT / "data" / "emission_factors" / "starter_average_speed_co2_factors.csv"
)
SCENARIO_CONFIG = ScenarioConfig(
    name="runner-skeleton",
    nodes=[
        NodeConfig(name="orig", x=0.0, y=0.0),
        NodeConfig(name="dest", x=100.0, y=0.0),
    ],
    links=[
        LinkConfig(
            name="orig_dest",
            start_node="orig",
            end_node="dest",
            length_m=100.0,
        )
    ],
    demands=[
        DemandConfig(
            origin="orig",
            destination="dest",
            departure_times_s=(0.0,),
        )
    ],
)


class ExperimentRunnerTestCase(unittest.TestCase):
    def test_runner_advances_twice_and_collects_second_interval(self) -> None:
        runner = ExperimentRunner(interval_steps=2)

        result = runner.run(
            baseline_scenario=build_baseline_scenario(SCENARIO_CONFIG),
            model=_build_model(),
        )

        self.assertIsInstance(result, ExperimentRunResult)
        self.assertEqual(result.scenario_name, "runner-skeleton")
        self.assertEqual(len(result.snapshots), 3)
        self.assertIsNone(result.snapshots[0].timestep)
        self.assertEqual(result.snapshots[1].timestep, 2)
        self.assertEqual(result.snapshots[2].timestep, 4)
        self.assertEqual(len(result.interval_results), 2)
        self.assertEqual(result.interval_results[0].timestep, 2)
        self.assertEqual(result.interval_results[1].timestep, 4)
        self.assertGreater(
            result.interval_results[1].total_sample.pollutants_g.get("co2", 0.0),
            0.0,
        )
        self.assertEqual(
            result.log_lines,
            [
                "Scenario: runner-skeleton",
                "Advanced to timestep 2",
                "Advanced to timestep 4",
            ],
        )

    def test_runner_rejects_non_positive_interval_steps(self) -> None:
        runner = ExperimentRunner(interval_steps=0)

        with self.assertRaises(ValueError):
            runner.run(
                baseline_scenario=build_baseline_scenario(SCENARIO_CONFIG),
                model=_build_model(),
            )


def _build_model() -> AverageSpeedCO2Model:
    factor_table = load_average_speed_factor_table(FACTOR_TABLE_PATH)
    return AverageSpeedCO2Model(factor_table=factor_table)


if __name__ == "__main__":
    unittest.main()
