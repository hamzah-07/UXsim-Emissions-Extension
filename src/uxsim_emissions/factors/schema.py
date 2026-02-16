"""Data shapes for emission factor tables."""

from dataclasses import dataclass
from enum import StrEnum


class VTMicroRegime(StrEnum):
    """Acceleration regime used to select a VT-Micro coefficient surface."""

    NON_NEGATIVE_ACCELERATION = "non_negative_acceleration"
    NEGATIVE_ACCELERATION = "negative_acceleration"

    @classmethod
    def for_acceleration(cls, acceleration_mps2: float) -> "VTMicroRegime":
        if acceleration_mps2 < 0:
            return cls.NEGATIVE_ACCELERATION
        return cls.NON_NEGATIVE_ACCELERATION


@dataclass(slots=True, frozen=True)
class AverageSpeedFactor:
    """One average-speed emission factor entry."""

    vehicle_type: str
    pollutant: str
    speed_kph: float
    emission_g_per_km: float


@dataclass(slots=True)
class AverageSpeedFactorTable:
    """Collection of validated average-speed factors."""

    factors: list[AverageSpeedFactor]

    def series_for(
        self,
        *,
        vehicle_type: str,
        pollutant: str = "co2",
    ) -> list[AverageSpeedFactor]:
        return [
            factor
            for factor in self.factors
            if factor.vehicle_type == vehicle_type and factor.pollutant == pollutant
        ]


@dataclass(slots=True, frozen=True)
class SpeedAccelerationFactor:
    """One speed-acceleration coefficient set for a vehicle type."""

    vehicle_type: str
    pollutant: str
    coeff_constant: float
    coeff_speed: float
    coeff_acceleration: float
    coeff_speed_squared: float = 0.0
    coeff_acceleration_squared: float = 0.0
    coeff_speed_acceleration: float = 0.0


@dataclass(slots=True)
class SpeedAccelerationFactorTable:
    """Collection of validated speed-acceleration coefficient sets."""

    factors: list[SpeedAccelerationFactor]

    def factors_for(
        self,
        *,
        vehicle_type: str,
        pollutant: str = "co2",
    ) -> list[SpeedAccelerationFactor]:
        return [
            factor
            for factor in self.factors
            if factor.vehicle_type == vehicle_type and factor.pollutant == pollutant
        ]
