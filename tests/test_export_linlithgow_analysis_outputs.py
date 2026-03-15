"""Checks for generated Linlithgow analysis output exports."""

from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from experiments.export_linlithgow_analysis_outputs import (
    export_linlithgow_analysis_outputs,
)


class ExportLinlithgowAnalysisOutputsTestCase(unittest.TestCase):
    def test_export_writes_csv_svg_and_markdown_outputs(self) -> None:
        with TemporaryDirectory() as temp_dir:
            exported = export_linlithgow_analysis_outputs(temp_dir)

            self.assertEqual(
                set(exported),
                {
                    "run_summary_csv",
                    "link_hotspots_csv",
                    "intensity_chart_svg",
                    "analysis_summary_md",
                },
            )
            for path in exported.values():
                self.assertTrue(path.exists())

            run_summary = exported["run_summary_csv"].read_text(encoding="utf-8")
            self.assertIn(
                "scenario_name,variant,model_kind,runtime_seconds,total_co2_g,distance_m,intensity_g_per_km,average_delay_s",
                run_summary,
            )
            self.assertIn(
                "linlithgow-town-centre-baseline,baseline,average_speed,",
                run_summary,
            )

            hotspot_summary = exported["link_hotspots_csv"].read_text(encoding="utf-8")
            self.assertIn("variant,rank,link_id,highway,co2_g", hotspot_summary)
            self.assertIn(
                "baseline,1,tc_322847838_190546646_0,primary,908.97",
                hotspot_summary,
            )

            figure = exported["intensity_chart_svg"].read_text(encoding="utf-8")
            self.assertIn("<svg", figure)
            self.assertIn("Linlithgow Emission Intensity", figure)
            self.assertIn("168.84", figure)

            summary = exported["analysis_summary_md"].read_text(encoding="utf-8")
            self.assertIn("# Linlithgow Analysis Summary", summary)
            self.assertIn("| Variant | Model | Runtime (s) | Total CO2 (g) |", summary)
            self.assertIn("## Top Link Hotspots", summary)
            self.assertIn("Peak demand increases total CO2", summary)


if __name__ == "__main__":
    unittest.main()
