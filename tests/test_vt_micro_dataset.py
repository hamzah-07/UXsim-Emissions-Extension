"""Checks for the tracked VT-Micro CO2 dataset."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from uxsim_emissions.factors import VTMicroRegime, load_vt_micro_factor_table


EXPECTED_NON_NEGATIVE_COEFFICIENTS = (
    (6.916, 0.217, 2.354e-4, -3.639e-4),
    (-0.02754, -9.68e-3, -1.75e-3, 8.35e-5),
    (-2.070e-4, -1.0138e-4, 1.966e-5, -1.02e-6),
    (9.80e-7, 3.66e-7, -1.08e-7, 8.50e-9),
)
EXPECTED_NEGATIVE_COEFFICIENTS = (
    (6.915, -0.032, 9.17e-3, -2.88e-4),
    (0.0284, 8.53e-3, 1.15e-3, -3.06e-6),
    (-2.26e-4, -6.594e-5, -1.289e-5, -2.68e-7),
    (1.11e-6, 3.20e-7, 7.56e-8, 2.95e-9),
)


class VTMicroDatasetTestCase(unittest.TestCase):
    def test_vt_micro_dataset_loads_and_has_expected_surfaces(self) -> None:
        table = load_vt_micro_factor_table(
            PROJECT_ROOT / "data" / "emission_factors" / "vt_micro_co2_coefficients.csv"
        )

        self.assertEqual(len(table.surfaces), 2)

        non_negative_surface = table.surface_for(
            vehicle_type="passenger_car",
            regime=VTMicroRegime.NON_NEGATIVE_ACCELERATION,
        )
        self._assert_surface_matches(
            non_negative_surface.coefficients,
            EXPECTED_NON_NEGATIVE_COEFFICIENTS,
        )

        negative_surface = table.surface_for(
            vehicle_type="passenger_car",
            regime=VTMicroRegime.NEGATIVE_ACCELERATION,
        )
        self._assert_surface_matches(
            negative_surface.coefficients,
            EXPECTED_NEGATIVE_COEFFICIENTS,
        )

    def _assert_surface_matches(
        self,
        observed: tuple[tuple[float, float, float, float], ...],
        expected: tuple[tuple[float, float, float, float], ...],
    ) -> None:
        for speed_power, expected_row in enumerate(expected):
            for acceleration_power, expected_value in enumerate(expected_row):
                self.assertAlmostEqual(
                    observed[speed_power][acceleration_power],
                    expected_value,
                )


if __name__ == "__main__":
    unittest.main()
