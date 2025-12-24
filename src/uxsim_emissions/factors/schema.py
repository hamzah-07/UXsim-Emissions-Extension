"""Data shapes for emission factor tables."""

from dataclasses import dataclass


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

