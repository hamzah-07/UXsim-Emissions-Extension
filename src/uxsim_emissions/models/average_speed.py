"""Average-speed emissions models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from uxsim_emissions.factors.schema import AverageSpeedFactorTable
from uxsim_emissions.integration.uxsim_adapter import VehicleObservation

from .base import EmissionModel, EmissionSample


@dataclass(slots=True)
class AverageSpeedCO2Model(EmissionModel):
    """Compute CO2 emissions from an average-speed factor table."""

    factor_table: AverageSpeedFactorTable
    default_vehicle_type: str = "passenger_car"
    pollutant: str = "co2"
    name: str = "average_speed_co2"

    def compute(
        self,
        *,
        speed_mps: float,
        acceleration_mps2: float | None = None,
        distance_m: float = 0.0,
        metadata: Mapping[str, object] | None = None,
    ) -> EmissionSample:
        del acceleration_mps2

        if speed_mps < 0:
            raise ValueError("speed_mps must be non-negative")
        if distance_m < 0:
            raise ValueError("distance_m must be non-negative")

        vehicle_type = self.default_vehicle_type
        if metadata is not None and metadata.get("vehicle_type") is not None:
            vehicle_type = str(metadata["vehicle_type"])

        factor_g_per_km = self._factor_for_speed_kph(
            speed_kph=speed_mps * 3.6,
            vehicle_type=vehicle_type,
        )
        emission_g = factor_g_per_km * (distance_m / 1000.0)
        return EmissionSample(
            pollutants_g={self.pollutant: emission_g},
            distance_m=distance_m,
        )

    def _factor_for_speed_kph(self, *, speed_kph: float, vehicle_type: str) -> float:
        series = self.factor_table.series_for(
            vehicle_type=vehicle_type,
            pollutant=self.pollutant,
        )
        if not series:
            raise ValueError(
                f"No {self.pollutant} average-speed factors found for vehicle_type={vehicle_type!r}"
            )
        if len(series) == 1:
            return series[0].emission_g_per_km

        if speed_kph <= series[0].speed_kph:
            # Early-model choice: clamp outside the known range until we adopt a
            # final literature-backed extrapolation policy.
            return series[0].emission_g_per_km
        if speed_kph >= series[-1].speed_kph:
            return series[-1].emission_g_per_km

        for lower, upper in zip(series, series[1:]):
            if lower.speed_kph <= speed_kph <= upper.speed_kph:
                return _interpolate(
                    x=speed_kph,
                    x0=lower.speed_kph,
                    y0=lower.emission_g_per_km,
                    x1=upper.speed_kph,
                    y1=upper.emission_g_per_km,
                )

        raise RuntimeError("Failed to resolve average-speed emission factor")

    def compute_from_observation_pair(
        self,
        *,
        previous_observation: VehicleObservation,
        current_observation: VehicleObservation,
        metadata: Mapping[str, object] | None = None,
    ) -> EmissionSample:
        if previous_observation.vehicle_id != current_observation.vehicle_id:
            raise ValueError("Observation pair must belong to the same vehicle")
        if previous_observation.time_s is None or current_observation.time_s is None:
            raise ValueError("Observation pair must include time_s values")

        delta_time_s = current_observation.time_s - previous_observation.time_s
        if delta_time_s <= 0:
            raise ValueError("Observation pair must have a positive elapsed time")

        distance_m = _distance_from_observation_pair(
            previous_observation=previous_observation,
            current_observation=current_observation,
            delta_time_s=delta_time_s,
        )
        if distance_m <= 0:
            return EmissionSample(
                pollutants_g={self.pollutant: 0.0},
                distance_m=0.0,
            )

        average_speed_mps = distance_m / delta_time_s
        return self.compute(
            speed_mps=average_speed_mps,
            distance_m=distance_m,
            metadata=metadata,
        )


def _interpolate(*, x: float, x0: float, y0: float, x1: float, y1: float) -> float:
    if x1 == x0:
        return y0
    return y0 + (x - x0) * (y1 - y0) / (x1 - x0)


def _distance_from_observation_pair(
    *,
    previous_observation: VehicleObservation,
    current_observation: VehicleObservation,
    delta_time_s: float,
) -> float:
    distance_delta_m = (
        current_observation.distance_traveled_m - previous_observation.distance_traveled_m
    )
    if distance_delta_m > 0:
        return distance_delta_m

    if (
        previous_observation.link_id is not None
        and previous_observation.link_id == current_observation.link_id
        and current_observation.position_m >= previous_observation.position_m
    ):
        position_delta_m = current_observation.position_m - previous_observation.position_m
        if position_delta_m > 0:
            return position_delta_m

    average_speed_mps = (
        previous_observation.speed_mps + current_observation.speed_mps
    ) / 2.0
    return max(0.0, average_speed_mps * delta_time_s)
