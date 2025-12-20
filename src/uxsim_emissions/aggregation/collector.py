"""Helpers for aggregating per-step emissions into reportable totals."""

from dataclasses import dataclass, field

from uxsim_emissions.models.base import EmissionSample


@dataclass(slots=True)
class EmissionCollector:
    """In-memory accumulator for pollutant totals."""

    total_pollutants_g: dict[str, float] = field(default_factory=dict)

    def add(self, sample: EmissionSample) -> None:
        for pollutant, value in sample.pollutants_g.items():
            self.total_pollutants_g[pollutant] = (
                self.total_pollutants_g.get(pollutant, 0.0) + value
            )

    def reset(self) -> None:
        self.total_pollutants_g.clear()

