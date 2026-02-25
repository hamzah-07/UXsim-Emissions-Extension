"""Result shapes shared by small experiment helpers."""

from dataclasses import dataclass, field

from uxsim_emissions.aggregation import SnapshotIntervalEmissionResult
from uxsim_emissions.integration import WorldObservationSnapshot
from uxsim_emissions.models import EmissionSample


@dataclass(slots=True)
class ExperimentRunTotals:
    """Structured headline totals for one experiment run."""

    total_sample: EmissionSample = field(default_factory=EmissionSample)
    link_samples: dict[str, EmissionSample] = field(default_factory=dict)


@dataclass(slots=True)
class ExperimentRunResult:
    """Captured outputs from one baseline experiment run."""

    scenario_name: str
    runtime_seconds: float = 0.0
    completed: bool = False
    average_delay_seconds: float | None = None
    totals: ExperimentRunTotals = field(default_factory=ExperimentRunTotals)
    snapshots: list[WorldObservationSnapshot] = field(default_factory=list)
    interval_results: list[SnapshotIntervalEmissionResult] = field(default_factory=list)
    log_lines: list[str] = field(default_factory=list)
