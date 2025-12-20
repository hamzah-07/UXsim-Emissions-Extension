"""Shared configuration objects for experiments and logging."""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class LoggingConfig:
    """Controls which emission outputs are recorded during a run."""

    per_timestep: bool = True
    per_vehicle: bool = True
    per_link: bool = True
    output_dir: Path = Path("outputs")


@dataclass(slots=True)
class ProjectConfig:
    """Top-level project settings used across experiments."""

    random_seed: int = 42
    timestep_seconds: float = 1.0
    logging: LoggingConfig = field(default_factory=LoggingConfig)

