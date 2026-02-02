"""Result shapes shared by small experiment helpers."""

from dataclasses import dataclass, field

from uxsim_emissions.aggregation import SnapshotIntervalEmissionResult
from uxsim_emissions.integration import WorldObservationSnapshot


@dataclass(slots=True)
class ExperimentRunResult:
    """Captured outputs from one baseline experiment run."""

    scenario_name: str
    snapshots: list[WorldObservationSnapshot] = field(default_factory=list)
    interval_results: list[SnapshotIntervalEmissionResult] = field(default_factory=list)
    log_lines: list[str] = field(default_factory=list)
