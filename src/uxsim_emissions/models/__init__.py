"""Emission model interfaces and implementations."""

from .average_speed import AverageSpeedCO2Model
from .base import EmissionModel, EmissionSample
from .speed_accel import SpeedAccelerationCO2Model

__all__ = [
    "EmissionModel",
    "EmissionSample",
    "AverageSpeedCO2Model",
    "SpeedAccelerationCO2Model",
]
