"""Aggregation helpers for turning samples into useful totals."""

from .collector import EmissionCollector
from .results import SnapshotIntervalEmissionResult
from .snapshot_runner import run_average_speed_snapshot_interval
from .snapshot_runner_metadata import run_average_speed_snapshot_interval_with_metadata

__all__ = [
    "EmissionCollector",
    "SnapshotIntervalEmissionResult",
    "run_average_speed_snapshot_interval",
    "run_average_speed_snapshot_interval_with_metadata",
]
