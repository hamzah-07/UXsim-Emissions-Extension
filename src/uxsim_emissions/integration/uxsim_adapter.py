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


@dataclass(slots=True)
class LinkObservation:
    """Normalised per-link traffic state captured from a UXsim timestep."""

    link_id: str
    speed_mps: float
    density: float
    flow: float
    num_vehicles: float
    num_vehicles_queue: float
    length_m: float
    timestep: int | None
    time_s: float | None


@dataclass(slots=True)
class WorldObservationSnapshot:
    """Bundle all normalized observations captured for one world instant."""

    timestep: int | None
    time_s: float | None
    vehicle_observations: list[VehicleObservation]
    link_observations: list[LinkObservation]


class UXsimAdapter:
    """Translate live UXsim world state into normalised observations."""

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

    def iter_link_observations(self, world: Any) -> list[LinkObservation]:
        if not hasattr(world, "LINKS"):
            return []

        observations: list[LinkObservation] = []
        for link in world.LINKS:
            # WIP: keep the raw UXsim aggregate fields visible for now so we can
            # validate units before the first emissions model consumes them.
            observations.append(
                LinkObservation(
                    link_id=link.name,
                    speed_mps=link.speed,
                    density=link.density,
                    flow=link.flow,
                    num_vehicles=link.num_vehicles,
                    num_vehicles_queue=link.num_vehicles_queue,
                    length_m=link.length,
                    timestep=getattr(world, "T", None),
                    time_s=getattr(world, "TIME", None),
                )
            )

        return observations

    def capture_snapshot(self, world: Any) -> WorldObservationSnapshot:
        return WorldObservationSnapshot(
            timestep=getattr(world, "T", None),
            time_s=getattr(world, "TIME", None),
            vehicle_observations=self.iter_vehicle_observations(world),
            link_observations=self.iter_link_observations(world),
        )
