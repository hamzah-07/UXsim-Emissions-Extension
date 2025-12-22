"""Integration boundary between UXsim and the emissions extension."""

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class VehicleObservation:
    """Normalised vehicle state captured from a UXsim timestep."""

    vehicle_id: str
    state: str
    link_id: str | None
    position_m: float
    speed_mps: float
    acceleration_mps2: float | None
    distance_traveled_m: float
    timestep: int
    time_s: float | None


class UXsimAdapter:
    """Translate live UXsim world state into normalised vehicle observations."""

    def iter_vehicle_observations(self, world: Any) -> list[VehicleObservation]:
        if not hasattr(world, "VEHICLES_RUNNING"):
            return []

        observations: list[VehicleObservation] = []
        for vehicle in world.VEHICLES_RUNNING.values():
            # WIP: leave acceleration unset until we decide whether to derive it
            # from successive snapshots or vehicle logs.
            observations.append(
                VehicleObservation(
                    vehicle_id=vehicle.name,
                    state=vehicle.state,
                    link_id=getattr(vehicle.link, "name", None),
                    position_m=vehicle.x,
                    speed_mps=vehicle.v,
                    acceleration_mps2=None,
                    distance_traveled_m=vehicle.distance_traveled,
                    timestep=getattr(world, "T", 0),
                    time_s=getattr(world, "TIME", None),
                )
            )

        return observations
