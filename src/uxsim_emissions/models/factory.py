"""Helpers for building configured emissions model instances."""

from __future__ import annotations

from pathlib import Path

from uxsim_emissions.config import EmissionModelConfig, EmissionModelKind
from uxsim_emissions.factors import (
    load_average_speed_factor_table,
    load_vt_micro_factor_table,
)

from .average_speed import AverageSpeedCO2Model
from .base import EmissionModel
from .speed_accel import SpeedAccelerationCO2Model

PROJECT_ROOT = Path(__file__).resolve().parents[3]
# These defaults intentionally point at the tracked datasets already used by
# the repo so config-driven runs keep the same baseline behaviour as the
# existing scripts unless a caller opts into a different table explicitly.
DEFAULT_AVERAGE_SPEED_FACTOR_TABLE_PATH = (
    PROJECT_ROOT / "data" / "emission_factors" / "copert_average_speed_co2_factors.csv"
)
DEFAULT_SPEED_ACCELERATION_FACTOR_TABLE_PATH = (
    PROJECT_ROOT / "data" / "emission_factors" / "vt_micro_co2_coefficients.csv"
)


def build_emission_model(config: EmissionModelConfig) -> EmissionModel:
    """Build an emissions model from shared project configuration."""

    factor_table_path = (
        config.factor_table_path
        if config.factor_table_path is not None
        else _default_factor_table_path(config.kind)
    )
    # Keep model selection centralised here so scripts can switch model family
    # through config without each one rebuilding the same branching logic.
    if config.kind == EmissionModelKind.AVERAGE_SPEED:
        return AverageSpeedCO2Model(
            factor_table=load_average_speed_factor_table(factor_table_path)
        )
    if config.kind == EmissionModelKind.SPEED_ACCELERATION:
        return SpeedAccelerationCO2Model(
            factor_table=load_vt_micro_factor_table(factor_table_path)
        )

    raise ValueError(f"Unsupported emissions model kind: {config.kind}")


def _default_factor_table_path(kind: EmissionModelKind) -> Path:
    if kind == EmissionModelKind.AVERAGE_SPEED:
        return DEFAULT_AVERAGE_SPEED_FACTOR_TABLE_PATH
    if kind == EmissionModelKind.SPEED_ACCELERATION:
        return DEFAULT_SPEED_ACCELERATION_FACTOR_TABLE_PATH

    raise ValueError(f"Unsupported emissions model kind: {kind}")
