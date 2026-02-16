"""Helpers for evaluating the VT-Micro polynomial surfaces."""

from uxsim_emissions.factors import VTMicroCoefficientSurface


def evaluate_vt_micro_log_rate(
    *,
    surface: VTMicroCoefficientSurface,
    speed_kph: float,
    acceleration_kph_per_s: float,
) -> float:
    """Evaluate the VT-Micro log-rate polynomial for one speed/acceleration pair."""

    if speed_kph < 0:
        raise ValueError("speed_kph must be non-negative")

    # The coefficient grid follows the paper's i/j notation:
    # rows are speed powers and columns are acceleration powers.
    return sum(
        surface.coefficient(speed_power=i, acceleration_power=j)
        * speed_kph**i
        * acceleration_kph_per_s**j
        for i in range(4)
        for j in range(4)
    )
