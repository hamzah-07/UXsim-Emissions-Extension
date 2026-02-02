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

        world = baseline_scenario.world
        adapter = baseline_scenario.adapter
        snapshots = [baseline_scenario.initial_snapshot]
        log_lines = [f"Scenario: {baseline_scenario.config.name}"]

        if world.check_simulation_ongoing():
            world.exec_simulation(duration_t2=self.interval_steps)
            snapshots.append(adapter.capture_snapshot(world))
            log_lines.append(f"Advanced by {self.interval_steps} timestep(s)")

        return ExperimentRunResult(
            scenario_name=baseline_scenario.config.name,
            snapshots=snapshots,
            log_lines=log_lines,
        )
