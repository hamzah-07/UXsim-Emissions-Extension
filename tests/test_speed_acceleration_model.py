"""Tests for the speed-acceleration model skeleton."""

from math import log
from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from uxsim_emissions.factors import (
    SpeedAccelerationFactor,
    SpeedAccelerationFactorTable,
    VTMicroCoefficientSurface,
    VTMicroFactorTable,
    VTMicroRegime,
)
from uxsim_emissions.integration import VehicleObservation
from uxsim_emissions.models import SpeedAccelerationCO2Model


class SpeedAccelerationModelTestCase(unittest.TestCase):
    def test_model_keeps_expected_defaults(self) -> None:
        model = SpeedAccelerationCO2Model(factor_table=_build_vt_micro_table())

        self.assertEqual(model.default_vehicle_type, "passenger_car")
        self.assertEqual(model.pollutant, "co2")
        self.assertEqual(model.name, "speed_acceleration_co2")

    def test_model_computes_emissions_for_direct_inputs(self) -> None:
        model = SpeedAccelerationCO2Model(factor_table=_build_vt_micro_table())

        sample = model.compute(
            speed_mps=10.0,
            acceleration_mps2=1.0,
            distance_m=50.0,
            duration_s=5.0,
        )

        self.assertAlmostEqual(sample.pollutants_g["co2"], 10.0)
        self.assertEqual(sample.distance_m, 50.0)

    def test_model_uses_vehicle_type_override_from_metadata(self) -> None:
        model = SpeedAccelerationCO2Model(factor_table=_build_vt_micro_table())

        sample = model.compute(
            speed_mps=10.0,
            acceleration_mps2=1.0,
            distance_m=50.0,
            duration_s=5.0,
            metadata={"vehicle_type": "light_van"},
        )

        self.assertAlmostEqual(sample.pollutants_g["co2"], 5.0)

    def test_model_treats_missing_acceleration_as_zero(self) -> None:
        model = SpeedAccelerationCO2Model(factor_table=_build_vt_micro_table())

        sample = model.compute(
            speed_mps=10.0,
            acceleration_mps2=None,
            distance_m=50.0,
            duration_s=5.0,
        )

        self.assertAlmostEqual(sample.pollutants_g["co2"], 10.0)

    def test_model_uses_negative_acceleration_surface_for_direct_inputs(self) -> None:
        model = SpeedAccelerationCO2Model(factor_table=_build_vt_micro_table())

        sample = model.compute(
            speed_mps=10.0,
            acceleration_mps2=-1.0,
            distance_m=50.0,
            duration_s=5.0,
        )

        self.assertAlmostEqual(sample.pollutants_g["co2"], 2.5)

    def test_model_computes_from_observation_pair(self) -> None:
        model = SpeedAccelerationCO2Model(factor_table=_build_vt_micro_table())

        sample = model.compute_from_observation_pair(
            previous_observation=_build_observation(speed_mps=8.0, time_s=2.0, distance_m=10.0),
            current_observation=_build_observation(speed_mps=12.0, time_s=4.0, distance_m=30.0),
        )

        self.assertAlmostEqual(sample.pollutants_g["co2"], 4.0)
        self.assertEqual(sample.distance_m, 20.0)

    def test_model_uses_negative_acceleration_surface_from_observation_pair(self) -> None:
        model = SpeedAccelerationCO2Model(factor_table=_build_vt_micro_table())

        sample = model.compute_from_observation_pair(
            previous_observation=_build_observation(speed_mps=12.0, time_s=2.0, distance_m=10.0),
            current_observation=_build_observation(speed_mps=8.0, time_s=4.0, distance_m=30.0),
        )

        self.assertAlmostEqual(sample.pollutants_g["co2"], 1.0)


def _build_table() -> SpeedAccelerationFactorTable:
    return SpeedAccelerationFactorTable(
        factors=[
            SpeedAccelerationFactor("passenger_car", "co2", 1.0, 0.1, 0.2),
            SpeedAccelerationFactor("light_van", "co2", 2.0, 0.2, 0.3),
        ]
    )


def _build_vt_micro_table() -> VTMicroFactorTable:
    return VTMicroFactorTable(
        surfaces=[
            _surface(
                vehicle_type="passenger_car",
                regime=VTMicroRegime.NON_NEGATIVE_ACCELERATION,
                rate_mg_per_s=2000.0,
            ),
            _surface(
                vehicle_type="passenger_car",
                regime=VTMicroRegime.NEGATIVE_ACCELERATION,
                rate_mg_per_s=500.0,
            ),
            _surface(
                vehicle_type="light_van",
                regime=VTMicroRegime.NON_NEGATIVE_ACCELERATION,
                rate_mg_per_s=1000.0,
            ),
            _surface(
                vehicle_type="light_van",
                regime=VTMicroRegime.NEGATIVE_ACCELERATION,
                rate_mg_per_s=400.0,
            ),
        ]
    )


def _surface(
    *,
    vehicle_type: str,
    regime: VTMicroRegime,
    rate_mg_per_s: float,
) -> VTMicroCoefficientSurface:
    return VTMicroCoefficientSurface(
        vehicle_type=vehicle_type,
        pollutant="co2",
        regime=regime,
        coefficients=((log(rate_mg_per_s), 0.0, 0.0, 0.0),) + ((0.0, 0.0, 0.0, 0.0),) * 3,
    )


def _build_observation(
    *,
    speed_mps: float,
    time_s: float,
    distance_m: float,
) -> VehicleObservation:
    return VehicleObservation(
        vehicle_id="veh_0",
        state="run",
        link_id="orig_dest",
        position_m=distance_m,
        speed_mps=speed_mps,
        acceleration_mps2=None,
        distance_traveled_m=distance_m,
        timestep=int(time_s),
        time_s=time_s,
    )


if __name__ == "__main__":
    unittest.main()
