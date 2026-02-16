"""Emission model interfaces and implementations."""

from .average_speed import AverageSpeedCO2Model
from .base import EmissionModel, EmissionSample
from .speed_accel import SpeedAccelerationCO2Model
from .vt_micro_units import (
    acceleration_mps2_to_kph_per_s,
    emission_rate_mg_per_s_to_g_per_s,
    speed_mps_to_kph,
)

__all__ = [
    "EmissionModel",
    "EmissionSample",
    "AverageSpeedCO2Model",
    "SpeedAccelerationCO2Model",
    "speed_mps_to_kph",
    "acceleration_mps2_to_kph_per_s",
    "emission_rate_mg_per_s_to_g_per_s",
]
