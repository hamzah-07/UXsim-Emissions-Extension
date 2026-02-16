"""Unit conversions for feeding UXsim observations into VT-Micro."""


def speed_mps_to_kph(speed_mps: float) -> float:
    """Convert UXsim speed from metres per second to kilometres per hour."""

    if speed_mps < 0:
        raise ValueError("speed_mps must be non-negative")
    return speed_mps * 3.6


def acceleration_mps2_to_kph_per_s(acceleration_mps2: float) -> float:
    """Convert UXsim acceleration from m/s^2 to the km/h/s used by VT-Micro."""

    return acceleration_mps2 * 3.6


def emission_rate_mg_per_s_to_g_per_s(emission_rate_mg_per_s: float) -> float:
    """Convert a VT-Micro pollutant rate from mg/s into g/s for repo outputs."""

    # UXsim gives us SI motion units, while the published VT-Micro equations
    # use road-traffic units for speed and acceleration and a mass-per-time
    # emission rate. Keeping the conversions here makes that boundary obvious.
    return emission_rate_mg_per_s / 1000.0
