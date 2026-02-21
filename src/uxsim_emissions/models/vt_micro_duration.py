"""Helpers for resolving VT-Micro interval durations."""


def resolve_duration_s(
    *,
    duration_s: float | None = None,
    distance_m: float = 0.0,
    speed_mps: float | None = None,
) -> float:
    """Resolve an interval duration for turning VT-Micro rates into emitted mass."""

    if duration_s is not None:
        if duration_s < 0:
            raise ValueError("duration_s must be non-negative")
        return duration_s

    if distance_m < 0:
        raise ValueError("distance_m must be non-negative")
    if distance_m == 0:
        return 0.0
    if speed_mps is None or speed_mps <= 0:
        raise ValueError("speed_mps must be positive when deriving duration_s")

    # This fallback is only for direct inputs. Observation pairs should
    # usually hand us a real elapsed interval instead.
    return distance_m / speed_mps
