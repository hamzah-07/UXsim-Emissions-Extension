"""Small orchestration helpers for repeatable baseline runs."""

from dataclasses import dataclass

from uxsim_emissions.aggregation import run_average_speed_snapshot_interval
from uxsim_emissions.integration import BaselineScenario
from uxsim_emissions.models import AverageSpeedCO2Model

from .results import ExperimentRunResult


@dataclass(slots=True)
class ExperimentRunner:
    """Prepare the initial state for a baseline experiment run."""

    interval_steps: int = 1
    max_intervals: int = 2

    def run(
        self,
        *,
        baseline_scenario: BaselineScenario,
        model: AverageSpeedCO2Model,
    ) -> ExperimentRunResult:
        if self.interval_steps <= 0:
            raise ValueError("interval_steps must be positive")

        world = baseline_scenario.world
        adapter = baseline_scenario.adapter
        snapshots = [baseline_scenario.initial_snapshot]
        interval_results = []
        log_lines = [f"Scenario: {baseline_scenario.config.name}"]

        for _ in range(self.max_intervals):
            if not world.check_simulation_ongoing():
                break

            world.exec_simulation(duration_t2=self.interval_steps)
            current_snapshot = adapter.capture_snapshot(world)
            snapshots.append(current_snapshot)
            # The first interval can still be empty if vehicles only appear
            # once the simulation has started, which is fine at this stage.
            interval_results.append(
                run_average_speed_snapshot_interval(
                    model=model,
                    previous_snapshot=snapshots[-2],
                    current_snapshot=snapshots[-1],
                )
            )
            log_lines.append(f"Advanced to timestep {current_snapshot.timestep}")

        return ExperimentRunResult(
            scenario_name=baseline_scenario.config.name,
            snapshots=snapshots,
            interval_results=interval_results,
            log_lines=log_lines,
        )
