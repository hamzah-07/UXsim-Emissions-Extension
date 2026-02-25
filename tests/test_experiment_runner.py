"""Tests for the first experiment runner slice."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from uxsim_emissions import DemandConfig, LinkConfig, NodeConfig, ScenarioConfig
from uxsim_emissions.config import LoggingConfig
from uxsim_emissions.experiments import ExperimentRunResult, ExperimentRunner
from uxsim_emissions.factors import (
    load_average_speed_factor_table,
    load_speed_acceleration_factor_table,
)
from uxsim_emissions.integration import build_baseline_scenario
from uxsim_emissions.models import AverageSpeedCO2Model, SpeedAccelerationCO2Model

FACTOR_TABLE_PATH = (
    PROJECT_ROOT / "data" / "emission_factors" / "starter_average_speed_co2_factors.csv"
)
SPEED_ACCEL_FACTOR_TABLE_PATH = (
    PROJECT_ROOT
    / "data"
    / "emission_factors"
    / "starter_speed_acceleration_co2_factors.csv"
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
        self.assertGreaterEqual(result.runtime_seconds, 0.0)
        self.assertFalse(result.completed)
        self.assertIsNone(result.average_delay_seconds)
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
        self.assertEqual(list(result.interval_results[1].link_samples), ["orig_dest"])
        self.assertGreater(
            result.interval_results[1].link_samples["orig_dest"].pollutants_g.get("co2", 0.0),
            0.0,
        )
        self.assertGreater(result.totals.total_sample.pollutants_g.get("co2", 0.0), 0.0)
        self.assertGreater(result.totals.total_sample.distance_m, 0.0)
        self.assertEqual(list(result.totals.link_samples), ["orig_dest"])
        self.assertGreater(result.totals.link_samples["orig_dest"].distance_m, 0.0)
        self.assertEqual(
            result.log_lines,
            [
                "Scenario: runner-skeleton",
                "Advanced to timestep 2",
                "Advanced to timestep 4",
            ],
        )

    def test_runner_respects_max_intervals_cap(self) -> None:
        runner = ExperimentRunner(interval_steps=2, max_intervals=1)

        result = runner.run(
            baseline_scenario=build_baseline_scenario(SCENARIO_CONFIG),
            model=_build_model(),
        )

        self.assertGreaterEqual(result.runtime_seconds, 0.0)
        self.assertFalse(result.completed)
        self.assertIsNone(result.average_delay_seconds)
        self.assertEqual(len(result.snapshots), 2)
        self.assertEqual(len(result.interval_results), 1)
        self.assertEqual(result.interval_results[0].timestep, 2)
        self.assertEqual(result.interval_results[0].link_samples, {})
        self.assertEqual(result.totals.total_sample.pollutants_g.get("co2", 0.0), 0.0)
        self.assertEqual(result.totals.total_sample.distance_m, 0.0)
        self.assertEqual(result.totals.link_samples, {})
        self.assertEqual(
            result.log_lines,
            ["Scenario: runner-skeleton", "Advanced to timestep 2"],
        )

    def test_runner_supports_speed_acceleration_model(self) -> None:
        runner = ExperimentRunner(interval_steps=2)

        result = runner.run(
            baseline_scenario=build_baseline_scenario(SCENARIO_CONFIG),
            model=_build_speed_accel_model(),
        )

        self.assertGreaterEqual(result.runtime_seconds, 0.0)
        self.assertFalse(result.completed)
        self.assertIsNone(result.average_delay_seconds)
        self.assertEqual(len(result.snapshots), 3)
        self.assertEqual(len(result.interval_results), 2)
        self.assertGreater(
            result.interval_results[1].total_sample.pollutants_g.get("co2", 0.0),
            0.0,
        )
        self.assertEqual(list(result.interval_results[1].link_samples), ["orig_dest"])
        self.assertGreater(result.totals.total_sample.pollutants_g.get("co2", 0.0), 0.0)
        self.assertGreater(result.totals.total_sample.distance_m, 0.0)
        self.assertEqual(list(result.totals.link_samples), ["orig_dest"])

    def test_runner_can_continue_until_simulation_end_when_uncapped(self) -> None:
        scenario_config = ScenarioConfig(
            name="runner-complete",
            nodes=SCENARIO_CONFIG.nodes,
            links=SCENARIO_CONFIG.links,
            demands=SCENARIO_CONFIG.demands,
            tmax_s=4.0,
        )
        runner = ExperimentRunner(interval_steps=2, max_intervals=None)

        result = runner.run(
            baseline_scenario=build_baseline_scenario(scenario_config),
            model=_build_model(),
        )

        self.assertTrue(result.completed)
        self.assertIsNone(result.average_delay_seconds)
        self.assertEqual(len(result.interval_results), 2)
        self.assertEqual(result.interval_results[-1].timestep, 4)
        self.assertGreater(result.totals.total_sample.pollutants_g.get("co2", 0.0), 0.0)
        self.assertGreater(result.totals.total_sample.distance_m, 0.0)
        self.assertEqual(list(result.totals.link_samples), ["orig_dest"])

    def test_runner_rejects_non_positive_interval_steps(self) -> None:
        runner = ExperimentRunner(interval_steps=0)

        with self.assertRaises(ValueError):
            runner.run(
                baseline_scenario=build_baseline_scenario(SCENARIO_CONFIG),
                model=_build_model(),
            )

    def test_runner_rejects_negative_max_intervals(self) -> None:
        runner = ExperimentRunner(interval_steps=1, max_intervals=-1)

        with self.assertRaises(ValueError):
            runner.run(
                baseline_scenario=build_baseline_scenario(SCENARIO_CONFIG),
                model=_build_model(),
            )

    def test_runner_can_suppress_vehicle_and_link_details(self) -> None:
        runner = ExperimentRunner(
            interval_steps=2,
            logging_config=LoggingConfig(per_vehicle=False, per_link=False),
        )

        result = runner.run(
            baseline_scenario=build_baseline_scenario(SCENARIO_CONFIG),
            model=_build_model(),
        )

        self.assertEqual(len(result.interval_results), 2)
        self.assertEqual(result.interval_results[1].vehicle_samples, {})
        self.assertEqual(result.interval_results[1].link_samples, {})
        self.assertGreater(result.interval_results[1].total_sample.pollutants_g["co2"], 0.0)
        self.assertEqual(result.totals.link_samples, {})
        self.assertGreater(result.totals.total_sample.distance_m, 0.0)

    def test_runner_can_disable_per_timestep_outputs_but_keep_totals(self) -> None:
        runner = ExperimentRunner(
            interval_steps=2,
            logging_config=LoggingConfig(per_timestep=False),
        )

        result = runner.run(
            baseline_scenario=build_baseline_scenario(SCENARIO_CONFIG),
            model=_build_model(),
        )

        self.assertEqual(result.snapshots, [])
        self.assertEqual(result.interval_results, [])
        self.assertGreater(result.totals.total_sample.pollutants_g.get("co2", 0.0), 0.0)
        self.assertEqual(list(result.totals.link_samples), ["orig_dest"])


def _build_model() -> AverageSpeedCO2Model:
    factor_table = load_average_speed_factor_table(FACTOR_TABLE_PATH)
    return AverageSpeedCO2Model(factor_table=factor_table)


def _build_speed_accel_model() -> SpeedAccelerationCO2Model:
    factor_table = load_speed_acceleration_factor_table(SPEED_ACCEL_FACTOR_TABLE_PATH)
    return SpeedAccelerationCO2Model(factor_table=factor_table)


if __name__ == "__main__":
    unittest.main()
