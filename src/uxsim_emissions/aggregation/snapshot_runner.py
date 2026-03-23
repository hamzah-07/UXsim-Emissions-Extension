"""Helpers for running emissions models across snapshot intervals."""

from collections.abc import Callable

from uxsim_emissions.integration import WorldObservationSnapshot
from uxsim_emissions.models import AverageSpeedCO2Model, EmissionSample

from .collector import EmissionCollector
from .results import SnapshotIntervalEmissionResult


def run_average_speed_snapshot_interval(
    *,
    model: AverageSpeedCO2Model,
    previous_snapshot: WorldObservationSnapshot,
    current_snapshot: WorldObservationSnapshot,
) -> SnapshotIntervalEmissionResult:
    return _run_snapshot_interval(
        model=model,
        previous_snapshot=previous_snapshot,
        current_snapshot=current_snapshot,
        metadata_for_vehicle=lambda _vehicle_id: None,
    )


def run_average_speed_snapshot_sequence(
    *,
    model: AverageSpeedCO2Model,
    snapshots: list[WorldObservationSnapshot],
) -> list[SnapshotIntervalEmissionResult]:
    # Keep this simple for now: walk the snapshots in order and reuse the
    # existing single-interval path for each neighbouring pair.
    if len(snapshots) < 2:
        return []

    results: list[SnapshotIntervalEmissionResult] = []
    for previous_snapshot, current_snapshot in zip(snapshots, snapshots[1:]):
        results.append(
            run_average_speed_snapshot_interval(
                model=model,
                previous_snapshot=previous_snapshot,
                current_snapshot=current_snapshot,
            )
        )

    return results


def _run_snapshot_interval(
    *,
    model: AverageSpeedCO2Model,
    previous_snapshot: WorldObservationSnapshot,
    current_snapshot: WorldObservationSnapshot,
    metadata_for_vehicle: Callable[[str], dict[str, object] | None],
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
            # A vehicle can appear part-way through the run, so only compute an
            # interval when we have both ends of the pair.
            continue

        sample = model.compute_from_observation_pair(
            previous_observation=previous_observation,
            current_observation=current_observation,
            metadata=metadata_for_vehicle(current_observation.vehicle_id),
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
        total_sample=_build_total_sample(
            collector=collector,
            vehicle_samples=vehicle_samples,
        ),
    )


def _build_total_sample(
    *,
    collector: EmissionCollector,
    vehicle_samples: dict[str, EmissionSample],
) -> EmissionSample:
    # Keep the run total compact here. Link-level roll-ups are already carried
    # separately in the interval result when callers need them.
    return EmissionSample(
        pollutants_g=dict(collector.total_pollutants_g),
        distance_m=sum(sample.distance_m for sample in vehicle_samples.values()),
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
