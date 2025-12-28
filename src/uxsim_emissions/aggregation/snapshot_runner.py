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
    # TODO: this is fine for one interval at a time, but we will probably want
    # a small higher-level helper that walks a whole run and yields these
    # results in sequence.
    return _run_snapshot_interval(
        model=model,
        previous_snapshot=previous_snapshot,
        current_snapshot=current_snapshot,
        metadata_for_vehicle=lambda _vehicle_id: None,
    )


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

    return SnapshotIntervalEmissionResult(
        timestep=current_snapshot.timestep,
        time_s=current_snapshot.time_s,
        vehicle_samples=vehicle_samples,
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
    # TODO: once link-level rollups arrive, this total builder will probably
    # want to return a bit more than just pollutant totals and distance.
    return EmissionSample(
        pollutants_g=dict(collector.total_pollutants_g),
        distance_m=sum(sample.distance_m for sample in vehicle_samples.values()),
    )
