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
class VTMicroCoefficientSurface:
    """One VT-Micro coefficient surface for a vehicle, pollutant and regime."""

    vehicle_type: str
    pollutant: str
    regime: VTMicroRegime
    coefficients: tuple[tuple[float, float, float, float], ...]
    speed_unit: str = "kph"
    acceleration_unit: str = "mps2"
    emission_rate_unit: str = "g_per_s"

    def __post_init__(self) -> None:
        if len(self.coefficients) != 4 or any(
            len(row) != 4 for row in self.coefficients
        ):
            raise ValueError("VT-Micro coefficient surfaces must be 4x4")

    def coefficient(self, *, speed_power: int, acceleration_power: int) -> float:
        return self.coefficients[speed_power][acceleration_power]


@dataclass(slots=True)
class VTMicroFactorTable:
    """Collection of VT-Micro coefficient surfaces keyed by regime."""

    surfaces: list[VTMicroCoefficientSurface]

    def surface_for(
        self,
        *,
        vehicle_type: str,
        pollutant: str = "co2",
        regime: VTMicroRegime,
    ) -> VTMicroCoefficientSurface:
        matching_surfaces = [
            surface
            for surface in self.surfaces
            if surface.vehicle_type == vehicle_type
            and surface.pollutant == pollutant
            and surface.regime == regime
        ]
        if not matching_surfaces:
            raise ValueError(
                "No VT-Micro coefficient surface found for "
                f"vehicle_type={vehicle_type!r}, pollutant={pollutant!r}, regime={regime.value!r}"
            )
        if len(matching_surfaces) > 1:
            raise ValueError(
                "Expected one VT-Micro coefficient surface for "
                f"vehicle_type={vehicle_type!r}, pollutant={pollutant!r}, regime={regime.value!r}"
            )
        return matching_surfaces[0]


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
