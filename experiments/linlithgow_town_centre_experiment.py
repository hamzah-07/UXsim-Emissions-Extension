"""Run the Linlithgow town-centre case study through the experiment harness."""

from __future__ import annotations

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from uxsim_emissions import EmissionModelConfig, EmissionModelKind, LoggingConfig
from uxsim_emissions.experiments import ExperimentRunner, build_experiment_summary_lines
from uxsim_emissions.integration import build_baseline_scenario
from uxsim_emissions.models import build_emission_model
from uxsim_emissions.scenarios import (
    TownCentreVariant,
    build_tracked_town_centre_scenario_config,
)

LINLITHGOW_METADATA_PATH = (
    PROJECT_ROOT / "scenarios" / "town_centre" / "linlithgow_metadata.json"
)


def build_linlithgow_town_centre_summary(
    *,
    model_kind: EmissionModelKind | str = EmissionModelKind.AVERAGE_SPEED,
    variant: TownCentreVariant | str = TownCentreVariant.BASELINE,
    interval_steps: int = 10,
    max_intervals: int | None = None,
) -> list[str]:
    """Run the tracked Linlithgow town-centre scenario and return summary lines."""

    model = build_emission_model(EmissionModelConfig(kind=model_kind))
    runner = ExperimentRunner(
        interval_steps=interval_steps,
        max_intervals=max_intervals,
        # Keep the first town-centre summary path light on retained detail so
        # the case-study runs stay focused on headline metrics.
        logging_config=LoggingConfig(
            per_timestep=False,
            per_vehicle=False,
            per_link=False,
        ),
    )
    scenario = build_tracked_town_centre_scenario_config(
        metadata_path=LINLITHGOW_METADATA_PATH,
        variant=variant,
    )
    result = runner.run(
        baseline_scenario=build_baseline_scenario(scenario),
        model=model,
    )
    return [
        f"Model: {model.name}",
        f"Variant: {TownCentreVariant(variant).value}",
        *build_experiment_summary_lines(result),
    ]


if __name__ == "__main__":
    print("\n".join(build_linlithgow_town_centre_summary()))
