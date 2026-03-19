"""Checks for the Linlithgow analysis table export."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from experiments.linlithgow_analysis_table import (
    build_linlithgow_analysis_csv_lines,
    build_linlithgow_analysis_rows,
)


class LinlithgowAnalysisTableTestCase(unittest.TestCase):
    def test_analysis_rows_cover_both_models_and_variants(self) -> None:
        rows = build_linlithgow_analysis_rows()

        self.assertEqual(len(rows), 4)
        self.assertEqual(rows[0]["scenario_name"], "linlithgow-town-centre-baseline")
        self.assertEqual(rows[0]["variant"], "baseline")
        self.assertEqual(rows[0]["model_kind"], "average_speed")
        self.assertEqual(rows[0]["total_co2_g"], "12210.88")
        self.assertEqual(rows[0]["intensity_g_per_km"], "126.91")
        self.assertEqual(rows[1]["model_kind"], "speed_acceleration")
        self.assertEqual(rows[1]["total_co2_g"], "5458.34")
        self.assertEqual(rows[2]["scenario_name"], "linlithgow-town-centre-peak-demand")
        self.assertEqual(rows[2]["variant"], "peak_demand")
        self.assertEqual(rows[2]["total_co2_g"], "19751.66")
        self.assertEqual(rows[3]["model_kind"], "speed_acceleration")
        self.assertEqual(rows[3]["total_co2_g"], "9521.46")

    def test_analysis_csv_lines_include_header_and_known_rows(self) -> None:
        lines = build_linlithgow_analysis_csv_lines()
        output = "\n".join(lines)

        self.assertIn(
            "scenario_name,variant,model_kind,runtime_seconds,total_co2_g,distance_m,intensity_g_per_km,average_delay_s",
            output,
        )
        self.assertIn(
            "linlithgow-town-centre-baseline,baseline,average_speed,",
            output,
        )
        self.assertIn(
            "linlithgow-town-centre-peak-demand,peak_demand,speed_acceleration,",
            output,
        )


if __name__ == "__main__":
    unittest.main()
