"""Tests for VT-Micro unit conversions."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from uxsim_emissions.models import (
    acceleration_mps2_to_kph_per_s,
    emission_rate_mg_per_s_to_g_per_s,
    speed_mps_to_kph,
)


class VTMicroUnitsTestCase(unittest.TestCase):
    def test_speed_conversion_matches_vt_micro_units(self) -> None:
        self.assertEqual(speed_mps_to_kph(10.0), 36.0)

    def test_acceleration_conversion_matches_vt_micro_units(self) -> None:
        self.assertEqual(acceleration_mps2_to_kph_per_s(1.5), 5.4)

    def test_emission_rate_conversion_normalises_repo_output_units(self) -> None:
        self.assertEqual(emission_rate_mg_per_s_to_g_per_s(2500.0), 2.5)

    def test_speed_conversion_rejects_negative_values(self) -> None:
        with self.assertRaisesRegex(ValueError, "non-negative"):
            speed_mps_to_kph(-0.1)


if __name__ == "__main__":
    unittest.main()
