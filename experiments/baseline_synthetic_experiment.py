"""Small baseline experiment built on the reusable scenario harness."""

from __future__ import annotations

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from uxsim_emissions import EmissionModelConfig, EmissionModelKind
from uxsim_emissions.experiments import ExperimentRunner, build_experiment_summary_lines
from uxsim_emissions.integration import build_baseline_scenario
from uxsim_emissions.models import build_emission_model
from uxsim_emissions.scenarios import ScenarioKind, build_scenario_config


def build_baseline_experiment_summary(
    model_kind: EmissionModelKind | str = EmissionModelKind.AVERAGE_SPEED,
    scenario_kind: ScenarioKind | str = ScenarioKind.SYNTHETIC_BASELINE,
) -> list[str]:
    """Run the small synthetic baseline example and return summary lines."""

    model = build_emission_model(EmissionModelConfig(kind=model_kind))
    # The baseline summary is now meant to reflect dissertation-style headline
    # metrics, so let the run finish rather than truncating after a few early
    # intervals.
    runner = ExperimentRunner(interval_steps=2, max_intervals=None)
    scenario = build_baseline_scenario(build_scenario_config(scenario_kind))
    result = runner.run(baseline_scenario=scenario, model=model)
    return [f"Model: {model.name}", *build_experiment_summary_lines(result)]


if __name__ == "__main__":
    print("\n".join(build_baseline_experiment_summary()))
