"""Helpers for loading Linlithgow town-centre case-study artefacts."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import json
from pathlib import Path

import pandas as pd

from uxsim_emissions.config import DemandConfig, LinkConfig, NodeConfig, ScenarioConfig

from .town_centre import (
    TownCentreImportConfig,
    load_town_centre_import_config,
    load_town_centre_signal_plan,
)


@dataclass(slots=True)
class TownCentreDemandProfile:
    """Demand profile used for one town-centre scenario variant."""

    name: str
    tmax_s: float
    demands: list[DemandConfig]


class TownCentreVariant(StrEnum):
    """Supported demand-profile variants for the tracked town-centre case study."""

    BASELINE = "baseline"
    PEAK_DEMAND = "peak_demand"


def load_town_centre_demand_profile(
    profile_path: Path | str,
) -> TownCentreDemandProfile:
    """Load a machine-readable town-centre demand profile."""

    path = Path(profile_path)
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    demands = [
        DemandConfig(
            origin=str(demand["origin"]),
            destination=str(demand["destination"]),
            departure_times_s=tuple(float(value) for value in demand["departure_times_s"]),
            vehicle_type=str(demand.get("vehicle_type", "passenger_car")),
        )
        for demand in payload["demands"]
    ]
    return TownCentreDemandProfile(
        name=str(payload["name"]),
        tmax_s=float(payload["tmax_s"]),
        demands=demands,
    )


def build_town_centre_scenario_config(
    *,
    import_config: TownCentreImportConfig,
    nodes_csv_path: Path | str,
    links_csv_path: Path | str,
    demand_profile_path: Path | str,
    signal_plan_path: Path | str | None = None,
    scenario_name_suffix: str | None = None,
) -> ScenarioConfig:
    """Build a runnable UXsim scenario config from processed town-centre files."""

    # Keep node and link identifiers as strings so OSM-derived ids do not get
    # coerced into numeric values and drift when we rebuild the case study.
    nodes_table = pd.read_csv(nodes_csv_path, dtype={"name": str})
    links_table = pd.read_csv(
        links_csv_path,
        dtype={
            "name": str,
            "start_node": str,
            "end_node": str,
        },
    )
    demand_profile = load_town_centre_demand_profile(demand_profile_path)
    signal_plan = (
        load_town_centre_signal_plan(signal_plan_path)
        if signal_plan_path is not None
        else None
    )
    # Build simple name-to-settings lookups once so the CSV row mapping stays
    # easy to follow when we overlay a tracked signal plan onto the network.
    node_signals = (
        {plan.node_name: plan.signal for plan in signal_plan.node_plans}
        if signal_plan is not None
        else {}
    )
    link_signal_groups = (
        {plan.link_name: plan.signal_group for plan in signal_plan.link_plans}
        if signal_plan is not None
        else {}
    )

    return ScenarioConfig(
        name=_scenario_name(
            study_area=import_config.study_area,
            demand_profile_name=demand_profile.name,
            scenario_name_suffix=scenario_name_suffix,
        ),
        nodes=[
            NodeConfig(
                name=str(row["name"]),
                x=float(row["x"]),
                y=float(row["y"]),
                signal=node_signals.get(str(row["name"]), (0.0,)),
            )
            for _, row in nodes_table.iterrows()
        ],
        links=[
            LinkConfig(
                name=str(row["name"]),
                start_node=str(row["start_node"]),
                end_node=str(row["end_node"]),
                length_m=float(row["length_m"]),
                free_flow_speed_mps=float(row["free_flow_speed_mps"]),
                jam_density=float(row.get("jam_density", 0.2)),
                number_of_lanes=int(row.get("number_of_lanes", 1)),
                signal_group=link_signal_groups.get(str(row["name"]), (0,)),
            )
            for _, row in links_table.iterrows()
        ],
        demands=demand_profile.demands,
        tmax_s=demand_profile.tmax_s,
    )


def build_tracked_town_centre_scenario_config(
    *,
    metadata_path: Path | str,
    variant: TownCentreVariant | str = TownCentreVariant.BASELINE,
    use_fixed_time_signals: bool = False,
    scenario_name_suffix: str | None = None,
) -> ScenarioConfig:
    """Build a tracked town-centre scenario config from committed artefacts."""

    metadata_file = Path(metadata_path)
    import_config = load_town_centre_import_config(metadata_file)
    variant_value = TownCentreVariant(variant)
    case_study_dir = metadata_file.parent
    demand_profile_name = (
        import_config.baseline_demand_profile_json
        if variant_value is TownCentreVariant.BASELINE
        else import_config.intervention_demand_profile_json
    )
    # Signal-policy experiments reuse the same tracked network and demand files;
    # only the optional signal overlay and scenario label change.
    signal_plan_path = (
        case_study_dir / import_config.fixed_time_signal_plan_json
        if use_fixed_time_signals
        else None
    )

    return build_town_centre_scenario_config(
        import_config=import_config,
        nodes_csv_path=case_study_dir / import_config.processed_nodes_csv,
        links_csv_path=case_study_dir / import_config.processed_links_csv,
        demand_profile_path=case_study_dir / demand_profile_name,
        signal_plan_path=signal_plan_path,
        scenario_name_suffix=(
            scenario_name_suffix
            if scenario_name_suffix is not None
            else "fixed-time-signals" if use_fixed_time_signals else None
        ),
    )


def _slugify(value: str) -> str:
    return value.lower().replace(" ", "-")


def _scenario_name(
    *,
    study_area: str,
    demand_profile_name: str,
    scenario_name_suffix: str | None,
) -> str:
    base_name = f"{_slugify(study_area)}-{demand_profile_name}"
    if scenario_name_suffix is None:
        return base_name
    return f"{base_name}-{scenario_name_suffix}"
