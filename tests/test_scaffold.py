"""Basic smoke tests for the initial project scaffold."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from uxsim_emissions import ProjectConfig
from uxsim_emissions.aggregation import EmissionCollector
from uxsim_emissions.models import EmissionSample


class ScaffoldTestCase(unittest.TestCase):
    def test_project_config_defaults(self) -> None:
        config = ProjectConfig()

        self.assertEqual(config.random_seed, 42)
        self.assertTrue(config.logging.per_timestep)
        self.assertEqual(config.logging.output_dir, Path("outputs"))

    def test_collector_accumulates_pollutants(self) -> None:
        collector = EmissionCollector()

        collector.add(EmissionSample(pollutants_g={"co2": 1.25}))
        collector.add(EmissionSample(pollutants_g={"co2": 0.75, "nox": 0.1}))

        self.assertEqual(collector.total_pollutants_g["co2"], 2.0)
        self.assertEqual(collector.total_pollutants_g["nox"], 0.1)


if __name__ == "__main__":
    unittest.main()

