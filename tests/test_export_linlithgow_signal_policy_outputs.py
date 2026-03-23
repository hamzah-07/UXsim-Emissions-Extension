"""Checks for generated Linlithgow signal-policy export outputs."""

from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from experiments.export_linlithgow_signal_policy_outputs import (
    export_linlithgow_signal_policy_outputs,
)


class ExportLinlithgowSignalPolicyOutputsTestCase(unittest.TestCase):
    def test_export_writes_signal_policy_tables_figure_and_summary(self) -> None:
        with TemporaryDirectory() as temp_dir:
            exported = export_linlithgow_signal_policy_outputs(temp_dir)

            self.assertEqual(
                set(exported),
                {
                    "signal_policy_summary_csv",
                    "signal_policy_deltas_csv",
                    "signal_policy_co2_chart_svg",
                    "signal_policy_summary_md",
                },
            )
            for path in exported.values():
                self.assertTrue(path.exists())

            summary_csv = exported["signal_policy_summary_csv"].read_text(
                encoding="utf-8"
            )
            self.assertIn(
                "variant,signal_policy,model_kind,runtime_seconds,total_co2_g,distance_m,intensity_g_per_km,average_delay_s",
                summary_csv,
            )
            self.assertIn(
                "baseline,fixed_time,average_speed,",
                summary_csv,
            )
            self.assertIn(
                "peak_demand,responsive,speed_acceleration,",
                summary_csv,
            )

            delta_csv = exported["signal_policy_deltas_csv"].read_text(
                encoding="utf-8"
            )
            self.assertIn(
                "variant,model_kind,fixed_time_total_co2_g,responsive_total_co2_g,delta_total_co2_g",
                delta_csv,
            )
            self.assertIn(
                "baseline,average_speed,13016.73,12579.79,-436.94",
                delta_csv,
            )

            figure = exported["signal_policy_co2_chart_svg"].read_text(
                encoding="utf-8"
            )
            self.assertIn("<svg", figure)
            self.assertIn("Linlithgow Signal Policy CO2 Comparison", figure)
            self.assertIn("13017", figure)

            summary_md = exported["signal_policy_summary_md"].read_text(
                encoding="utf-8"
            )
            self.assertIn("# Linlithgow Signal Policy Summary", summary_md)
            self.assertIn("## Responsive Minus Fixed-Time Deltas", summary_md)
            self.assertIn("| baseline | average_speed | -436.94 |", summary_md)


if __name__ == "__main__":
    unittest.main()
