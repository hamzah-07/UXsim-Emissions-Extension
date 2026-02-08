"""Speed-acceleration emissions models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from uxsim_emissions.factors import SpeedAccelerationFactorTable
from uxsim_emissions.integration import derive_acceleration_mps2
from uxsim_emissions.integration.uxsim_adapter import VehicleObservation

from .base import EmissionModel, EmissionSample


@dataclass(slots=True)
class SpeedAccelerationCO2Model(EmissionModel):
    """Compute CO2 emissions from speed-acceleration coefficients."""

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
        if speed_mps < 0:
            raise ValueError("speed_mps must be non-negative")
        if distance_m < 0:
            raise ValueError("distance_m must be non-negative")

        vehicle_type = self.default_vehicle_type
        if metadata is not None and metadata.get("vehicle_type") is not None:
            vehicle_type = str(metadata["vehicle_type"])

        factor = self._factor_for_vehicle_type(vehicle_type=vehicle_type)
        acceleration_mps2 = 0.0 if acceleration_mps2 is None else acceleration_mps2
        emission_rate_g_per_km = max(
            0.0,
            factor.coeff_constant
            + factor.coeff_speed * speed_mps
            + factor.coeff_acceleration * acceleration_mps2
            + factor.coeff_speed_squared * speed_mps**2
            + factor.coeff_acceleration_squared * acceleration_mps2**2
            + factor.coeff_speed_acceleration * speed_mps * acceleration_mps2,
        )
        return EmissionSample(
            pollutants_g={self.pollutant: emission_rate_g_per_km * (distance_m / 1000.0)},
            distance_m=distance_m,
        )

    def compute_from_observation_pair(
        self,
        *,
        previous_observation: VehicleObservation,
        current_observation: VehicleObservation,
        metadata: Mapping[str, object] | None = None,
    ) -> EmissionSample:
        if previous_observation.time_s is None or current_observation.time_s is None:
            raise ValueError("Observation pair must include time_s values")

        delta_time_s = current_observation.time_s - previous_observation.time_s
        if delta_time_s <= 0:
            raise ValueError("Observation pair must have a positive elapsed time")

        acceleration_mps2 = derive_acceleration_mps2(
            previous_observation=previous_observation,
            current_observation=current_observation,
        )
        distance_m = _distance_from_observation_pair(
            previous_observation=previous_observation,
            current_observation=current_observation,
            delta_time_s=delta_time_s,
        )
        return self.compute(
            speed_mps=current_observation.speed_mps,
            acceleration_mps2=acceleration_mps2,
            distance_m=distance_m,
            metadata=metadata,
        )

    def _factor_for_vehicle_type(self, *, vehicle_type: str):
        factors = self.factor_table.factors_for(
            vehicle_type=vehicle_type,
            pollutant=self.pollutant,
        )
        if not factors:
            raise ValueError(
                f"No {self.pollutant} speed-acceleration factors found for vehicle_type={vehicle_type!r}"
            )
        if len(factors) > 1:
            raise ValueError(
                f"Expected one {self.pollutant} speed-acceleration factor for vehicle_type={vehicle_type!r}"
            )
        return factors[0]


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
