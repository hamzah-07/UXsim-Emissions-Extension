"""Small kinematic helpers for observation-pair calculations."""

from .uxsim_adapter import VehicleObservation


def derive_acceleration_mps2(
    *,
    previous_observation: VehicleObservation,
    current_observation: VehicleObservation,
) -> float:
    """Estimate acceleration from two observations of the same vehicle."""

    if previous_observation.vehicle_id != current_observation.vehicle_id:
        raise ValueError("Observation pair must belong to the same vehicle")
    if previous_observation.time_s is None or current_observation.time_s is None:
        raise ValueError("Observation pair must include time_s values")

    delta_time_s = current_observation.time_s - previous_observation.time_s
    if delta_time_s <= 0:
        raise ValueError("Observation pair must have a positive elapsed time")

    # Raw snapshots keep speed directly but not acceleration, so infer the
    # interval acceleration from the change in speed over elapsed time.
    return (current_observation.speed_mps - previous_observation.speed_mps) / delta_time_s
