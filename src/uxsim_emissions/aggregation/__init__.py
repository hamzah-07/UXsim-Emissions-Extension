"""Aggregation helpers for turning samples into useful totals."""

from .collector import EmissionCollector
from .results import SnapshotIntervalEmissionResult
from .snapshot_runner import run_average_speed_snapshot_interval

__all__ = [
    "EmissionCollector",
    "SnapshotIntervalEmissionResult",
    "run_average_speed_snapshot_interval",
]

