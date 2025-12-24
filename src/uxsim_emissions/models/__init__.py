"""Emission model interfaces and implementations."""

from .average_speed import AverageSpeedCO2Model
from .base import EmissionModel, EmissionSample

__all__ = ["EmissionModel", "EmissionSample", "AverageSpeedCO2Model"]

