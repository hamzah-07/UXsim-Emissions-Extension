"""Helpers for applying per-vehicle metadata during snapshot interval runs."""

from __future__ import annotations

from typing import Mapping

from uxsim_emissions.integration import WorldObservationSnapshot
from uxsim_emissions.models import AverageSpeedCO2Model

from .results import SnapshotIntervalEmissionResult
from .snapshot_runner import _run_snapshot_interval


def run_average_speed_snapshot_interval_with_metadata(
    *,
    model: AverageSpeedCO2Model,
    previous_snapshot: WorldObservationSnapshot,
    current_snapshot: WorldObservationSnapshot,
    vehicle_metadata: Mapping[str, Mapping[str, object]] | None = None,
) -> SnapshotIntervalEmissionResult:
    # Keep this as a thin wrapper so the plain path stays simple, but metadata
    # overrides can still plug in cleanly when we need them.
    return _run_snapshot_interval(
        model=model,
        previous_snapshot=previous_snapshot,
        current_snapshot=current_snapshot,
        metadata_for_vehicle=lambda vehicle_id: (
            None if vehicle_metadata is None else vehicle_metadata.get(vehicle_id)
        ),
    )
