"""Helpers for applying per-vehicle metadata during snapshot interval runs."""

from __future__ import annotations

from typing import Mapping

from uxsim_emissions.integration import WorldObservationSnapshot
from uxsim_emissions.models import AverageSpeedCO2Model, EmissionSample

from .collector import EmissionCollector
from .results import SnapshotIntervalEmissionResult


def run_average_speed_snapshot_interval_with_metadata(
    *,
    model: AverageSpeedCO2Model,
    previous_snapshot: WorldObservationSnapshot,
    current_snapshot: WorldObservationSnapshot,
    vehicle_metadata: Mapping[str, Mapping[str, object]] | None = None,
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

        metadata = None
        if vehicle_metadata is not None:
            metadata = vehicle_metadata.get(current_observation.vehicle_id)

        sample = model.compute_from_observation_pair(
            previous_observation=previous_observation,
            current_observation=current_observation,
            metadata=metadata,
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

