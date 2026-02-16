"""Tests for VT-Micro acceleration regime selection."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from uxsim_emissions.factors import VTMicroRegime


class VTMicroRegimeTestCase(unittest.TestCase):
    def test_non_negative_acceleration_uses_non_negative_regime(self) -> None:
        self.assertEqual(
            VTMicroRegime.for_acceleration(0.0),
            VTMicroRegime.NON_NEGATIVE_ACCELERATION,
        )
        self.assertEqual(
            VTMicroRegime.for_acceleration(1.2),
            VTMicroRegime.NON_NEGATIVE_ACCELERATION,
        )

    def test_negative_acceleration_uses_negative_regime(self) -> None:
        self.assertEqual(
            VTMicroRegime.for_acceleration(-0.01),
            VTMicroRegime.NEGATIVE_ACCELERATION,
        )


if __name__ == "__main__":
    unittest.main()
