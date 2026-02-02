"""Small baseline experiment built on the reusable scenario harness."""

from __future__ import annotations

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from uxsim_emissions import DemandConfig, LinkConfig, NodeConfig, ScenarioConfig
from uxsim_emissions.experiments import ExperimentRunner, build_experiment_summary_lines
from uxsim_emissions.factors import load_average_speed_factor_table
from uxsim_emissions.integration import build_baseline_scenario
from uxsim_emissions.models import AverageSpeedCO2Model


def build_baseline_experiment_summary() -> list[str]:
    """Run the small synthetic baseline example and return summary lines."""

    factor_table = load_average_speed_factor_table(
        PROJECT_ROOT / "data" / "emission_factors" / "starter_average_speed_co2_factors.csv"
    )
    model = AverageSpeedCO2Model(factor_table=factor_table)
    runner = ExperimentRunner(interval_steps=2, max_intervals=3)
    scenario = build_baseline_scenario(_scenario_config())
    result = runner.run(baseline_scenario=scenario, model=model)
    return build_experiment_summary_lines(result)


def _scenario_config() -> ScenarioConfig:
    return ScenarioConfig(
        name="baseline-two-link",
        nodes=[
            NodeConfig(name="orig", x=0.0, y=0.0),
            NodeConfig(name="mid", x=100.0, y=0.0, signal=(20.0, 20.0)),
            NodeConfig(name="dest", x=200.0, y=0.0),
        ],
        links=[
            LinkConfig(
                name="orig_mid",
                start_node="orig",
                end_node="mid",
                length_m=100.0,
                free_flow_speed_mps=10.0,
            ),
            LinkConfig(
                name="mid_dest",
                start_node="mid",
                end_node="dest",
                length_m=100.0,
                free_flow_speed_mps=8.0,
            ),
        ],
        demands=[
            DemandConfig(
                origin="orig",
                destination="dest",
                departure_times_s=(0.0, 2.0, 4.0),
            )
        ],
        tmax_s=60.0,
    )


if __name__ == "__main__":
    print("\n".join(build_baseline_experiment_summary()))
