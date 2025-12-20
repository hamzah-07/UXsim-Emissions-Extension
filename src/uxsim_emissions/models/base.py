"""Abstract building blocks shared by all emission models."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Mapping


@dataclass(slots=True)
class EmissionSample:
    """Normalised output for a single vehicle observation."""

    pollutants_g: dict[str, float] = field(default_factory=dict)
    distance_m: float = 0.0
    fuel_ml: float = 0.0


class EmissionModel(ABC):
    """Defines the minimal API every emission model must implement."""

    name: str

    @abstractmethod
    def compute(
        self,
        *,
        speed_mps: float,
        acceleration_mps2: float | None = None,
        distance_m: float = 0.0,
        metadata: Mapping[str, object] | None = None,
    ) -> EmissionSample:
        """Return emissions for a single timestep observation."""

