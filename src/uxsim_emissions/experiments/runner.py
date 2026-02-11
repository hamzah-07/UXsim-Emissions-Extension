"""Small orchestration helpers for repeatable baseline runs."""

from dataclasses import dataclass

from uxsim_emissions.aggregation import EmissionCollector, SnapshotIntervalEmissionResult
from uxsim_emissions.integration import BaselineScenario, WorldObservationSnapshot
from uxsim_emissions.models import (
    AverageSpeedCO2Model,
    EmissionSample,
    SpeedAccelerationCO2Model,
)

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
        model: AverageSpeedCO2Model | SpeedAccelerationCO2Model,
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
            interval_results.append(
                _run_snapshot_interval(
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


def _run_snapshot_interval(
    *,
    model: AverageSpeedCO2Model | SpeedAccelerationCO2Model,
    previous_snapshot: WorldObservationSnapshot,
    current_snapshot: WorldObservationSnapshot,
) -> SnapshotIntervalEmissionResult:
    previous_by_vehicle_id = {
        observation.vehicle_id: observation
        for observation in previous_snapshot.vehicle_observations
    }
    vehicle_samples: dict[str, EmissionSample] = {}
    collector = EmissionCollector()

    for current_observation in current_snapshot.vehicle_observations:
        previous_observation = previous_by_vehicle_id.get(current_observation.vehicle_id)
        if previous_observation is None:
            continue

        sample = model.compute_from_observation_pair(
            previous_observation=previous_observation,
            current_observation=current_observation,
        )
        vehicle_samples[current_observation.vehicle_id] = sample
        collector.add(sample)

    return SnapshotIntervalEmissionResult(
        timestep=current_snapshot.timestep,
        time_s=current_snapshot.time_s,
        vehicle_samples=vehicle_samples,
        total_sample=EmissionSample(
            pollutants_g=dict(collector.total_pollutants_g),
            distance_m=sum(sample.distance_m for sample in vehicle_samples.values()),
        ),
    )
