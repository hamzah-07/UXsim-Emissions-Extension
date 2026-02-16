"""Checks for the tracked VT-Micro CO2 dataset."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from uxsim_emissions.factors import VTMicroRegime, load_vt_micro_factor_table


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
        self.assertEqual(non_negative_surface.coefficient(speed_power=0, acceleration_power=0), 6.916)
        self.assertEqual(non_negative_surface.coefficient(speed_power=1, acceleration_power=0), -0.02754)

        negative_surface = table.surface_for(
            vehicle_type="passenger_car",
            regime=VTMicroRegime.NEGATIVE_ACCELERATION,
        )
        self.assertEqual(negative_surface.coefficient(speed_power=0, acceleration_power=1), -0.032)
        self.assertEqual(negative_surface.coefficient(speed_power=3, acceleration_power=3), 2.95e-9)


if __name__ == "__main__":
    unittest.main()
