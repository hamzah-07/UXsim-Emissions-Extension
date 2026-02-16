"""Tests for VT-Micro coefficient table lookup."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from uxsim_emissions.factors import (
    VTMicroCoefficientSurface,
    VTMicroFactorTable,
    VTMicroRegime,
)


class VTMicroFactorTableTestCase(unittest.TestCase):
    def test_surface_for_returns_the_matching_surface(self) -> None:
        table = VTMicroFactorTable(
            surfaces=[
                self._surface(regime=VTMicroRegime.NON_NEGATIVE_ACCELERATION),
                self._surface(regime=VTMicroRegime.NEGATIVE_ACCELERATION),
            ]
        )

        surface = table.surface_for(
            vehicle_type="passenger_car",
            regime=VTMicroRegime.NEGATIVE_ACCELERATION,
        )

        self.assertEqual(surface.regime, VTMicroRegime.NEGATIVE_ACCELERATION)

    def test_surface_for_rejects_duplicate_matches(self) -> None:
        table = VTMicroFactorTable(
            surfaces=[
                self._surface(regime=VTMicroRegime.NON_NEGATIVE_ACCELERATION),
                self._surface(regime=VTMicroRegime.NON_NEGATIVE_ACCELERATION),
            ]
        )

        with self.assertRaisesRegex(ValueError, "Expected one VT-Micro"):
            table.surface_for(
                vehicle_type="passenger_car",
                regime=VTMicroRegime.NON_NEGATIVE_ACCELERATION,
            )

    def _surface(self, *, regime: VTMicroRegime) -> VTMicroCoefficientSurface:
        return VTMicroCoefficientSurface(
            vehicle_type="passenger_car",
            pollutant="co2",
            regime=regime,
            coefficients=((1.0, 0.0, 0.0, 0.0),) * 4,
        )


if __name__ == "__main__":
    unittest.main()
