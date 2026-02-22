"""Small orchestration helpers for repeatable baseline runs."""

from dataclasses import dataclass
from time import perf_counter

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
    max_intervals: int | None = 2

    def run(
        self,
        *,
        baseline_scenario: BaselineScenario,
        model: AverageSpeedCO2Model | SpeedAccelerationCO2Model,
    ) -> ExperimentRunResult:
        if self.interval_steps <= 0:
            raise ValueError("interval_steps must be positive")
        if self.max_intervals is not None and self.max_intervals < 0:
            raise ValueError("max_intervals must be non-negative when provided")

        start_time = perf_counter()
        world = baseline_scenario.world
        adapter = baseline_scenario.adapter
        snapshots = [baseline_scenario.initial_snapshot]
        interval_results = []
        log_lines = [f"Scenario: {baseline_scenario.config.name}"]
        intervals_run = 0

        while True:
            if not world.check_simulation_ongoing():
                break
            if self.max_intervals is not None and intervals_run >= self.max_intervals:
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
            intervals_run += 1

        return ExperimentRunResult(
            scenario_name=baseline_scenario.config.name,
            runtime_seconds=perf_counter() - start_time,
            completed=not world.check_simulation_ongoing(),
            average_delay_seconds=_average_delay_seconds(world),
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


def _average_delay_seconds(world: object) -> float | None:
    analyzer = getattr(world, "analyzer", None)
    average_delay = getattr(analyzer, "average_delay", None)
    if average_delay is None or average_delay == -1:
        return None

    return float(average_delay)
