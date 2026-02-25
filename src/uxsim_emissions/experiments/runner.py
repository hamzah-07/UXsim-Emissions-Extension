"""Small orchestration helpers for repeatable baseline runs."""

from dataclasses import dataclass, field
from time import perf_counter

from uxsim_emissions.aggregation import EmissionCollector, SnapshotIntervalEmissionResult
from uxsim_emissions.config import LoggingConfig
from uxsim_emissions.integration import BaselineScenario, WorldObservationSnapshot
from uxsim_emissions.models import (
    AverageSpeedCO2Model,
    EmissionSample,
    SpeedAccelerationCO2Model,
)

from .results import ExperimentRunResult, ExperimentRunTotals


@dataclass(slots=True)
class ExperimentRunner:
    """Prepare the initial state for a baseline experiment run."""

    interval_steps: int = 1
    max_intervals: int | None = 2
    logging_config: LoggingConfig = field(default_factory=LoggingConfig)

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
        previous_snapshot = baseline_scenario.initial_snapshot
        snapshots = [previous_snapshot] if self.logging_config.per_timestep else []
        interval_results = []
        raw_interval_results = []
        log_lines = [f"Scenario: {baseline_scenario.config.name}"]
        intervals_run = 0

        while True:
            if not world.check_simulation_ongoing():
                break
            # `None` means "keep going until UXsim says the run is finished",
            # which we now need for full-run metrics such as average delay.
            if self.max_intervals is not None and intervals_run >= self.max_intervals:
                break

            world.exec_simulation(duration_t2=self.interval_steps)
            current_snapshot = adapter.capture_snapshot(world)
            raw_interval_result = _run_snapshot_interval(
                model=model,
                previous_snapshot=previous_snapshot,
                current_snapshot=current_snapshot,
            )
            raw_interval_results.append(raw_interval_result)
            if self.logging_config.per_timestep:
                snapshots.append(current_snapshot)
                interval_results.append(
                    _filter_interval_result(
                        raw_interval_result=raw_interval_result,
                        logging_config=self.logging_config,
                    )
                )
            log_lines.append(f"Advanced to timestep {current_snapshot.timestep}")
            intervals_run += 1
            previous_snapshot = current_snapshot

        return ExperimentRunResult(
            scenario_name=baseline_scenario.config.name,
            runtime_seconds=perf_counter() - start_time,
            completed=not world.check_simulation_ongoing(),
            average_delay_seconds=_average_delay_seconds(world),
            totals=_build_run_totals(
                raw_interval_results,
                include_link_samples=self.logging_config.per_link,
            ),
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
    link_samples: dict[str, EmissionSample] = {}
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
        if current_observation.link_id is not None:
            _add_sample_to_mapping(
                samples_by_key=link_samples,
                key=current_observation.link_id,
                sample=sample,
            )

    return SnapshotIntervalEmissionResult(
        timestep=current_snapshot.timestep,
        time_s=current_snapshot.time_s,
        vehicle_samples=vehicle_samples,
        link_samples=link_samples,
        total_sample=EmissionSample(
            pollutants_g=dict(collector.total_pollutants_g),
            distance_m=sum(sample.distance_m for sample in vehicle_samples.values()),
        ),
    )


def _average_delay_seconds(world: object) -> float | None:
    analyzer = getattr(world, "analyzer", None)
    average_delay = getattr(analyzer, "average_delay", None)
    # UXsim uses `-1` when no completed trips exist yet, so treat that as
    # unavailable rather than quietly pretending the delay was zero.
    if average_delay is None or average_delay == -1:
        return None

    return float(average_delay)


def _build_run_totals(
    interval_results: list[SnapshotIntervalEmissionResult],
    *,
    include_link_samples: bool,
) -> ExperimentRunTotals:
    collector = EmissionCollector()
    total_distance_m = 0.0
    link_samples: dict[str, EmissionSample] = {}

    for interval_result in interval_results:
        collector.add(interval_result.total_sample)
        total_distance_m += interval_result.total_sample.distance_m
        if include_link_samples:
            for link_id, sample in interval_result.link_samples.items():
                _add_sample_to_mapping(
                    samples_by_key=link_samples,
                    key=link_id,
                    sample=sample,
                )

    return ExperimentRunTotals(
        total_sample=EmissionSample(
            pollutants_g=dict(collector.total_pollutants_g),
            distance_m=total_distance_m,
        ),
        link_samples=link_samples,
    )


def _filter_interval_result(
    *,
    raw_interval_result: SnapshotIntervalEmissionResult,
    logging_config: LoggingConfig,
) -> SnapshotIntervalEmissionResult:
    return SnapshotIntervalEmissionResult(
        timestep=raw_interval_result.timestep,
        time_s=raw_interval_result.time_s,
        vehicle_samples=(
            raw_interval_result.vehicle_samples if logging_config.per_vehicle else {}
        ),
        link_samples=raw_interval_result.link_samples if logging_config.per_link else {},
        total_sample=raw_interval_result.total_sample,
    )


def _add_sample_to_mapping(
    *,
    samples_by_key: dict[str, EmissionSample],
    key: str,
    sample: EmissionSample,
) -> None:
    existing = samples_by_key.get(key)
    if existing is None:
        samples_by_key[key] = EmissionSample(
            pollutants_g=dict(sample.pollutants_g),
            distance_m=sample.distance_m,
            fuel_ml=sample.fuel_ml,
        )
        return

    for pollutant, value in sample.pollutants_g.items():
        existing.pollutants_g[pollutant] = existing.pollutants_g.get(pollutant, 0.0) + value
    existing.distance_m += sample.distance_m
    existing.fuel_ml += sample.fuel_ml
