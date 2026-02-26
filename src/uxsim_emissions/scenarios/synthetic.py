"""Synthetic scenario definitions used for early validation runs."""

from __future__ import annotations

from uxsim_emissions.config import DemandConfig, LinkConfig, NodeConfig, ScenarioConfig


def baseline_two_link_scenario_config() -> ScenarioConfig:
    """Return the tiny two-link baseline used across smoke and harness checks."""

    return ScenarioConfig(
        name="baseline-two-link",
        nodes=[
            NodeConfig(name="orig", x=0.0, y=0.0),
            NodeConfig(name="mid", x=100.0, y=0.0, signal=(20.0, 20.0)),
            NodeConfig(name="dest", x=200.0, y=0.0),
        ],
        links=[
            LinkConfig(
                name="orig_mid",
                start_node="orig",
                end_node="mid",
                length_m=100.0,
                free_flow_speed_mps=10.0,
            ),
            LinkConfig(
                name="mid_dest",
                start_node="mid",
                end_node="dest",
                length_m=100.0,
                free_flow_speed_mps=8.0,
            ),
        ],
        demands=[
            DemandConfig(
                origin="orig",
                destination="dest",
                departure_times_s=(0.0, 2.0, 4.0),
            )
        ],
        tmax_s=60.0,
    )
