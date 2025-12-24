"""Helpers for loading and validating emission factor datasets."""

from .loader import load_average_speed_factor_table
from .schema import AverageSpeedFactor, AverageSpeedFactorTable

__all__ = [
    "AverageSpeedFactor",
    "AverageSpeedFactorTable",
    "load_average_speed_factor_table",
]

