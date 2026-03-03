"""Helpers for selecting reusable scenario definitions by name."""

from __future__ import annotations

from enum import StrEnum

from uxsim_emissions.config import ScenarioConfig
from uxsim_emissions.scenarios.small_network import merge_validation_scenario_config
from uxsim_emissions.scenarios.synthetic import baseline_two_link_scenario_config


class ScenarioKind(StrEnum):
    """Supported staged scenario selections for experiment scripts."""

    SYNTHETIC_BASELINE = "synthetic_baseline"
    SMALL_VALIDATION = "small_validation"


def build_scenario_config(kind: ScenarioKind | str) -> ScenarioConfig:
    """Return a reusable scenario configuration for the requested stage."""

    # Centralise the early staged scenarios here so experiment scripts can
    # switch between them without each growing local branching logic.
    scenario_kind = ScenarioKind(kind)
    if scenario_kind is ScenarioKind.SYNTHETIC_BASELINE:
        return baseline_two_link_scenario_config()
    return merge_validation_scenario_config()
