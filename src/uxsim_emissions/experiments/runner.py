"""Small orchestration helpers for repeatable baseline runs."""

from dataclasses import dataclass

from uxsim_emissions.integration import BaselineScenario
from uxsim_emissions.models import AverageSpeedCO2Model

from .results import ExperimentRunResult


@dataclass(slots=True)
class ExperimentRunner:
    """Prepare the initial state for a baseline experiment run."""

    interval_steps: int = 1

    def run(
        self,
        *,
        baseline_scenario: BaselineScenario,
        model: AverageSpeedCO2Model,
    ) -> ExperimentRunResult:
        del model

        if self.interval_steps <= 0:
            raise ValueError("interval_steps must be positive")

        return ExperimentRunResult(
            scenario_name=baseline_scenario.config.name,
            snapshots=[baseline_scenario.initial_snapshot],
            log_lines=[f"Scenario: {baseline_scenario.config.name}"],
        )
