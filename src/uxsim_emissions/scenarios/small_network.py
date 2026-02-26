"""Small validation-network scenarios used before OSM case-study work."""

from __future__ import annotations

from uxsim_emissions.config import DemandConfig, LinkConfig, NodeConfig, ScenarioConfig


def merge_validation_scenario_config() -> ScenarioConfig:
    """Return a small merge network for pre-case-study validation runs."""

    return ScenarioConfig(
        name="merge-validation-network",
        nodes=[
            NodeConfig(name="west", x=0.0, y=50.0),
            NodeConfig(name="south", x=60.0, y=0.0),
            NodeConfig(name="merge", x=120.0, y=50.0),
            NodeConfig(name="east", x=240.0, y=50.0),
        ],
        links=[
            LinkConfig(
                name="west_merge",
                start_node="west",
                end_node="merge",
                length_m=120.0,
                free_flow_speed_mps=12.0,
            ),
            LinkConfig(
                name="south_merge",
                start_node="south",
                end_node="merge",
                length_m=90.0,
                free_flow_speed_mps=10.0,
            ),
            LinkConfig(
                name="merge_east",
                start_node="merge",
                end_node="east",
                length_m=140.0,
                free_flow_speed_mps=9.0,
            ),
        ],
        demands=[
            DemandConfig(
                origin="west",
                destination="east",
                departure_times_s=(0.0, 4.0, 8.0, 12.0),
            ),
            DemandConfig(
                origin="south",
                destination="east",
                departure_times_s=(2.0, 6.0, 10.0),
            ),
        ],
        tmax_s=90.0,
    )
