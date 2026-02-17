"""Tests for VT-Micro coefficient surface data shapes."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from uxsim_emissions.factors import VTMicroCoefficientSurface, VTMicroRegime


class VTMicroCoefficientSurfaceTestCase(unittest.TestCase):
    def test_surface_keeps_a_4x4_grid_of_coefficients(self) -> None:
        surface = VTMicroCoefficientSurface(
            vehicle_type="passenger_car",
            pollutant="co2",
            regime=VTMicroRegime.NON_NEGATIVE_ACCELERATION,
            coefficients=((1.0, 2.0, 3.0, 4.0), (5.0, 6.0, 7.0, 8.0), (9.0, 10.0, 11.0, 12.0), (13.0, 14.0, 15.0, 16.0)),
        )

        self.assertEqual(surface.coefficient(speed_power=2, acceleration_power=1), 10.0)
        self.assertEqual(surface.acceleration_unit, "kph_per_s")
        self.assertEqual(surface.emission_rate_unit, "mg_per_s")

    def test_surface_rejects_non_4x4_coefficients(self) -> None:
        with self.assertRaisesRegex(ValueError, "must be 4x4"):
            VTMicroCoefficientSurface(
                vehicle_type="passenger_car",
                pollutant="co2",
                regime=VTMicroRegime.NON_NEGATIVE_ACCELERATION,
                coefficients=((1.0, 2.0), (3.0, 4.0)),
            )


if __name__ == "__main__":
    unittest.main()
