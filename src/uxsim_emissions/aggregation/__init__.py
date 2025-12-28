"""Aggregation helpers for turning samples into useful totals."""

from .collector import EmissionCollector
from .results import SnapshotIntervalEmissionResult

__all__ = ["EmissionCollector", "SnapshotIntervalEmissionResult"]

