"""Integration boundary between UXsim and the emissions extension."""

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class VehicleObservation:
    """Normalised vehicle state captured from a UXsim timestep."""

    vehicle_id: str
    link_id: str | None
    speed_mps: float
    acceleration_mps2: float | None
    distance_m: float
    timestep: int


class UXsimAdapter:
    """Placeholder adapter for translating UXsim state into observations."""

    def iter_vehicle_observations(self, world: Any) -> list[VehicleObservation]:
        raise NotImplementedError(
            "UXsim state mapping will be implemented after runtime reconnaissance."
        )

