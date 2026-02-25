"""Result data shapes for snapshot-interval emissions."""

from dataclasses import dataclass, field

from uxsim_emissions.models import EmissionSample


@dataclass(slots=True)
class SnapshotIntervalEmissionResult:
    """Emission outputs computed for one snapshot-to-snapshot interval."""

    timestep: int | None
    time_s: float | None
    vehicle_samples: dict[str, EmissionSample] = field(default_factory=dict)
    link_samples: dict[str, EmissionSample] = field(default_factory=dict)
    total_sample: EmissionSample = field(default_factory=EmissionSample)
