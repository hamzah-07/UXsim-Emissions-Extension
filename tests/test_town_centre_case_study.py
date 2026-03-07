"""Tests for town-centre case-study scenario loading."""

from pathlib import Path
import sys
import tempfile
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from uxsim_emissions.scenarios import (
    TownCentreVariant,
    build_tracked_town_centre_scenario_config,
    build_town_centre_scenario_config,
    load_town_centre_demand_profile,
    load_town_centre_import_config,
)


class TownCentreCaseStudyTestCase(unittest.TestCase):
    def test_loads_town_centre_demand_profile(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            demand_path = Path(temp_dir) / "demand.json"
            demand_path.write_text(
                """
{
  "name": "baseline",
  "tmax_s": 300.0,
  "demands": [
    {
      "origin": "1",
      "destination": "2",
      "departure_times_s": [0.0, 30.0]
    }
  ]
}
                """.strip(),
                encoding="utf-8",
            )

            profile = load_town_centre_demand_profile(demand_path)

        self.assertEqual(profile.name, "baseline")
        self.assertEqual(profile.tmax_s, 300.0)
        self.assertEqual(profile.demands[0].origin, "1")
        self.assertEqual(profile.demands[0].departure_times_s, (0.0, 30.0))

    def test_builds_scenario_config_from_processed_files(self) -> None:
        import_config = load_town_centre_import_config(
            PROJECT_ROOT / "scenarios" / "town_centre" / "linlithgow_metadata.json"
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            nodes_path = temp_path / "nodes.csv"
            links_path = temp_path / "links.csv"
            demands_path = temp_path / "demands.json"
            nodes_path.write_text("name,x,y\n1,-3.62,55.97\n2,-3.61,55.971\n", encoding="utf-8")
            links_path.write_text(
                "name,start_node,end_node,length_m,free_flow_speed_mps,jam_density,number_of_lanes\n"
                "tc_1_2_0,1,2,120.0,10.0,0.2,1\n",
                encoding="utf-8",
            )
            demands_path.write_text(
                """
{
  "name": "baseline",
  "tmax_s": 300.0,
  "demands": [
    {
      "origin": "1",
      "destination": "2",
      "departure_times_s": [0.0, 30.0]
    }
  ]
}
                """.strip(),
                encoding="utf-8",
            )

            scenario = build_town_centre_scenario_config(
                import_config=import_config,
                nodes_csv_path=nodes_path,
                links_csv_path=links_path,
                demand_profile_path=demands_path,
            )

        self.assertEqual(scenario.name, "linlithgow-town-centre-baseline")
        self.assertEqual(len(scenario.nodes), 2)
        self.assertEqual(len(scenario.links), 1)
        self.assertEqual(len(scenario.demands), 1)

    def test_builds_tracked_linlithgow_baseline_and_intervention_configs(self) -> None:
        metadata_path = PROJECT_ROOT / "scenarios" / "town_centre" / "linlithgow_metadata.json"

        baseline = build_tracked_town_centre_scenario_config(metadata_path=metadata_path)
        peak_demand = build_tracked_town_centre_scenario_config(
            metadata_path=metadata_path,
            variant=TownCentreVariant.PEAK_DEMAND,
        )

        self.assertEqual(baseline.name, "linlithgow-town-centre-baseline")
        self.assertEqual(peak_demand.name, "linlithgow-town-centre-peak-demand")
        self.assertGreater(len(baseline.nodes), 100)
        self.assertGreater(len(baseline.links), 100)
        self.assertEqual(sum(len(demand.departure_times_s) for demand in baseline.demands), 20)
        self.assertEqual(sum(len(demand.departure_times_s) for demand in peak_demand.demands), 32)


if __name__ == "__main__":
    unittest.main()
