"""CSV loaders for early emission factor datasets."""

from __future__ import annotations

import csv
from pathlib import Path

from .schema import (
    AverageSpeedFactor,
    AverageSpeedFactorTable,
    SpeedAccelerationFactor,
    SpeedAccelerationFactorTable,
)

REQUIRED_AVERAGE_SPEED_COLUMNS = {
    "vehicle_type",
    "pollutant",
    "speed_kph",
    "emission_g_per_km",
}
REQUIRED_SPEED_ACCELERATION_COLUMNS = {
    "vehicle_type",
    "pollutant",
    "coeff_constant",
    "coeff_speed",
    "coeff_acceleration",
}


def load_average_speed_factor_table(path: str | Path) -> AverageSpeedFactorTable:
    """Load a validated average-speed factor table from CSV."""

    csv_path = Path(path)
    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fieldnames = set(reader.fieldnames or [])
        missing_columns = REQUIRED_AVERAGE_SPEED_COLUMNS - fieldnames
        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            raise ValueError(
                f"Average-speed factor table is missing required columns: {missing}"
            )

        factors: list[AverageSpeedFactor] = []
        for row_number, row in enumerate(reader, start=2):
            vehicle_type = row["vehicle_type"].strip()
            pollutant = row["pollutant"].strip().lower()
            speed_kph = _parse_non_negative_float(
                row["speed_kph"], row_number=row_number, column="speed_kph"
            )
            emission_g_per_km = _parse_non_negative_float(
                row["emission_g_per_km"],
                row_number=row_number,
                column="emission_g_per_km",
            )
            if not vehicle_type:
                raise ValueError(f"Row {row_number}: vehicle_type must not be empty")
            if not pollutant:
                raise ValueError(f"Row {row_number}: pollutant must not be empty")

            factors.append(
                AverageSpeedFactor(
                    vehicle_type=vehicle_type,
                    pollutant=pollutant,
                    speed_kph=speed_kph,
                    emission_g_per_km=emission_g_per_km,
                )
            )

    factors.sort(key=lambda factor: (factor.vehicle_type, factor.pollutant, factor.speed_kph))
    return AverageSpeedFactorTable(factors=factors)


def load_speed_acceleration_factor_table(
    path: str | Path,
) -> SpeedAccelerationFactorTable:
    """Load a validated speed-acceleration coefficient table from CSV."""

    csv_path = Path(path)
    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fieldnames = set(reader.fieldnames or [])
        missing_columns = REQUIRED_SPEED_ACCELERATION_COLUMNS - fieldnames
        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            raise ValueError(
                f"Speed-acceleration factor table is missing required columns: {missing}"
            )

        factors: list[SpeedAccelerationFactor] = []
        for row_number, row in enumerate(reader, start=2):
            factors.append(
                SpeedAccelerationFactor(
                    vehicle_type=row["vehicle_type"].strip(),
                    pollutant=row["pollutant"].strip().lower(),
                    coeff_constant=_parse_float(
                        row["coeff_constant"], row_number=row_number, column="coeff_constant"
                    ),
                    coeff_speed=_parse_float(
                        row["coeff_speed"], row_number=row_number, column="coeff_speed"
                    ),
                    coeff_acceleration=_parse_float(
                        row["coeff_acceleration"],
                        row_number=row_number,
                        column="coeff_acceleration",
                    ),
                )
            )

    factors.sort(key=lambda factor: (factor.vehicle_type, factor.pollutant))
    return SpeedAccelerationFactorTable(factors=factors)


def _parse_non_negative_float(value: str, *, row_number: int, column: str) -> float:
    parsed = _parse_float(value, row_number=row_number, column=column)
    if parsed < 0:
        raise ValueError(f"Row {row_number}: {column} must be non-negative")

    return parsed


def _parse_float(value: str, *, row_number: int, column: str) -> float:
    try:
        return float(value)
    except ValueError as exc:
        raise ValueError(
            f"Row {row_number}: {column} must be a numeric value"
        ) from exc
