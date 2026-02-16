"""Tests for VT-Micro polynomial evaluation."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from uxsim_emissions.factors import VTMicroCoefficientSurface, VTMicroRegime
from uxsim_emissions.models.vt_micro_polynomial import evaluate_vt_micro_log_rate


class VTMicroPolynomialTestCase(unittest.TestCase):
    def test_evaluator_keeps_constant_only_surfaces_simple(self) -> None:
        self.assertEqual(
            evaluate_vt_micro_log_rate(
                surface=_surface(((2.5, 0.0, 0.0, 0.0),) + ((0.0, 0.0, 0.0, 0.0),) * 3),
                speed_kph=36.0,
                acceleration_kph_per_s=3.6,
            ),
            2.5,
        )

    def test_evaluator_uses_speed_and_acceleration_powers_in_the_right_slots(self) -> None:
        result = evaluate_vt_micro_log_rate(
            surface=_surface(
                (
                    (1.0, 2.0, 0.0, 0.0),
                    (3.0, 4.0, 0.0, 0.0),
                    (0.0, 5.0, 0.0, 0.0),
                    (0.0, 0.0, 0.0, 0.0),
                )
            ),
            speed_kph=2.0,
            acceleration_kph_per_s=3.0,
        )

        self.assertEqual(result, 97.0)

    def test_evaluator_rejects_negative_speed(self) -> None:
        with self.assertRaisesRegex(ValueError, "non-negative"):
            evaluate_vt_micro_log_rate(
                surface=_surface(((1.0, 0.0, 0.0, 0.0),) + ((0.0, 0.0, 0.0, 0.0),) * 3),
                speed_kph=-1.0,
                acceleration_kph_per_s=0.0,
            )


def _surface(
    coefficients: tuple[tuple[float, float, float, float], ...],
) -> VTMicroCoefficientSurface:
    return VTMicroCoefficientSurface(
        vehicle_type="passenger_car",
        pollutant="co2",
        regime=VTMicroRegime.NON_NEGATIVE_ACCELERATION,
        coefficients=coefficients,
    )


if __name__ == "__main__":
    unittest.main()
