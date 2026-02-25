"""Shared configuration objects for experiments and logging."""

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path


class EmissionModelKind(StrEnum):
    """Supported emissions model selections for configurable runs."""

    AVERAGE_SPEED = "average_speed"
    SPEED_ACCELERATION = "speed_acceleration"


@dataclass(slots=True)
class EmissionModelConfig:
    """Select which emissions model family a run should use."""

    kind: EmissionModelKind | str = EmissionModelKind.AVERAGE_SPEED
    factor_table_path: Path | str | None = None

    def __post_init__(self) -> None:
        # Coerce loose config-file or script inputs into the stricter runtime
        # types the rest of the package expects.
        self.kind = EmissionModelKind(self.kind)
        if self.factor_table_path is not None:
            self.factor_table_path = Path(self.factor_table_path)


@dataclass(slots=True)
class LoggingConfig:
    """Controls which emission outputs are recorded during a run."""

    per_timestep: bool = True
    per_vehicle: bool = True
    per_link: bool = True
    output_dir: Path = Path("outputs")


@dataclass(slots=True)
class NodeConfig:
    """Minimal node definition for a reusable scenario."""

    name: str
    x: float
    y: float
    signal: tuple[float, ...] = (0.0,)
    flow_capacity: float | None = None


@dataclass(slots=True)
class LinkConfig:
    """Minimal link definition for a reusable scenario."""

    name: str
    start_node: str
    end_node: str
    length_m: float
    free_flow_speed_mps: float = 20.0
    jam_density: float = 0.2
    number_of_lanes: int = 1
    signal_group: tuple[int, ...] = (0,)


@dataclass(slots=True)
class DemandConfig:
    """Simple origin-destination demand definition."""

    origin: str
    destination: str
    departure_times_s: tuple[float, ...]
    vehicle_type: str = "passenger_car"


@dataclass(slots=True)
class ScenarioConfig:
    """Configuration for a reusable UXsim scenario."""

    name: str
    nodes: list[NodeConfig]
    links: list[LinkConfig]
    demands: list[DemandConfig]
    tmax_s: float = 300.0
    deltan: int = 1
    random_seed: int = 42
    print_mode: int = 0
    save_mode: int = 0
    show_mode: int = 0
    show_progress: int = 0
    vehicle_logging_timestep_interval: int = 1


@dataclass(slots=True)
class ProjectConfig:
    """Top-level project settings used across experiments."""

    random_seed: int = 42
    timestep_seconds: float = 1.0
    model: EmissionModelConfig = field(default_factory=EmissionModelConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
