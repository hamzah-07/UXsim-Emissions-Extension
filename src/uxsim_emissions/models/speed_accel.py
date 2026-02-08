"""Speed-acceleration emissions models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from uxsim_emissions.factors import SpeedAccelerationFactorTable

from .base import EmissionModel, EmissionSample


@dataclass(slots=True)
class SpeedAccelerationCO2Model(EmissionModel):
    """Placeholder CO2 model using speed-acceleration coefficients."""

    factor_table: SpeedAccelerationFactorTable
    default_vehicle_type: str = "passenger_car"
    pollutant: str = "co2"
    name: str = "speed_acceleration_co2"

    def compute(
        self,
        *,
        speed_mps: float,
        acceleration_mps2: float | None = None,
        distance_m: float = 0.0,
        metadata: Mapping[str, object] | None = None,
    ) -> EmissionSample:
        del speed_mps, acceleration_mps2, distance_m, metadata
        raise NotImplementedError("Speed-acceleration computation is not implemented yet")
