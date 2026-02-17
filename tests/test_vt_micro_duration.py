"""Tests for VT-Micro duration resolution."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from uxsim_emissions.models.vt_micro_duration import resolve_duration_s


class VTMicroDurationTestCase(unittest.TestCase):
    def test_helper_prefers_explicit_duration(self) -> None:
        self.assertEqual(resolve_duration_s(duration_s=4.5, distance_m=100.0, speed_mps=20.0), 4.5)

    def test_helper_can_derive_duration_from_distance_and_speed(self) -> None:
        self.assertEqual(resolve_duration_s(distance_m=50.0, speed_mps=10.0), 5.0)

    def test_helper_returns_zero_when_no_distance_is_travelled(self) -> None:
        self.assertEqual(resolve_duration_s(distance_m=0.0, speed_mps=None), 0.0)

    def test_helper_rejects_negative_explicit_duration(self) -> None:
        with self.assertRaisesRegex(ValueError, "non-negative"):
            resolve_duration_s(duration_s=-1.0)

    def test_helper_rejects_non_positive_speed_for_duration_fallback(self) -> None:
        with self.assertRaisesRegex(ValueError, "must be positive"):
            resolve_duration_s(distance_m=10.0, speed_mps=0.0)


if __name__ == "__main__":
    unittest.main()
