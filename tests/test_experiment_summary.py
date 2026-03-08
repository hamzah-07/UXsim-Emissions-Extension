"""Tests for the plain-text experiment summary helper."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from uxsim_emissions.aggregation import SnapshotIntervalEmissionResult
from uxsim_emissions.experiments import (
    ExperimentRunResult,
    ExperimentRunTotals,
    build_experiment_summary_lines,
)
from uxsim_emissions.integration import WorldObservationSnapshot
from uxsim_emissions.models import EmissionSample


class ExperimentSummaryTestCase(unittest.TestCase):
    def test_summary_lines_cover_counts_and_interval_totals(self) -> None:
        result = ExperimentRunResult(
            scenario_name="baseline-summary",
            snapshots_captured_count=3,
            intervals_computed_count=2,
            runtime_seconds=1.25,
            average_delay_seconds=0.5,
            totals=ExperimentRunTotals(
                total_sample=EmissionSample(
                    pollutants_g={"co2": 1.81},
                    distance_m=10.0,
                )
            ),
            snapshots=[
                WorldObservationSnapshot(timestep=None, time_s=None, vehicle_observations=[], link_observations=[]),
                WorldObservationSnapshot(timestep=2, time_s=2.0, vehicle_observations=[], link_observations=[]),
                WorldObservationSnapshot(timestep=4, time_s=4.0, vehicle_observations=[], link_observations=[]),
            ],
            interval_results=[
                SnapshotIntervalEmissionResult(
                    timestep=2,
                    time_s=2.0,
                    total_sample=EmissionSample(pollutants_g={"co2": 0.0}, distance_m=0.0),
                ),
                SnapshotIntervalEmissionResult(
                    timestep=4,
                    time_s=4.0,
                    total_sample=EmissionSample(pollutants_g={"co2": 1.81}, distance_m=10.0),
                ),
            ],
        )

        lines = build_experiment_summary_lines(result)
        output = "\n".join(lines)

        self.assertIn("Scenario: baseline-summary", output)
        self.assertIn("Snapshots captured: 3", output)
        self.assertIn("Intervals computed: 2", output)
        self.assertIn("Runtime: 1.250 s", output)
        self.assertIn("Total CO2: 1.81 g over 10.0 m", output)
        self.assertIn("Emission intensity: 181.00 g/km", output)
        self.assertIn("Average delay: 0.50 s", output)
        self.assertIn("- Interval 2: timestep 4, 1.81 g CO2 over 10.0 m", output)

    def test_summary_uses_raw_counts_when_per_timestep_outputs_are_not_retained(self) -> None:
        result = ExperimentRunResult(
            scenario_name="retained-light",
            snapshots_captured_count=3,
            intervals_computed_count=2,
            runtime_seconds=1.25,
            totals=ExperimentRunTotals(
                total_sample=EmissionSample(
                    pollutants_g={"co2": 1.81},
                    distance_m=10.0,
                )
            ),
            snapshots=[],
            interval_results=[],
        )

        lines = build_experiment_summary_lines(result)
        output = "\n".join(lines)

        self.assertIn("Snapshots captured: 3", output)
        self.assertIn("Intervals computed: 2", output)


if __name__ == "__main__":
    unittest.main()
