"""Helpers for loading Linlithgow town-centre case-study artefacts."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import json
from pathlib import Path

import pandas as pd

from uxsim_emissions.config import DemandConfig, LinkConfig, NodeConfig, ScenarioConfig

from .town_centre import TownCentreImportConfig, load_town_centre_import_config


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
) -> ScenarioConfig:
    """Build a runnable UXsim scenario config from processed town-centre files."""

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

    return ScenarioConfig(
        name=f"{_slugify(import_config.study_area)}-{demand_profile.name}",
        nodes=[
            NodeConfig(
                name=str(row["name"]),
                x=float(row["x"]),
                y=float(row["y"]),
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

    return build_town_centre_scenario_config(
        import_config=import_config,
        nodes_csv_path=case_study_dir / import_config.processed_nodes_csv,
        links_csv_path=case_study_dir / import_config.processed_links_csv,
        demand_profile_path=case_study_dir / demand_profile_name,
    )


def _slugify(value: str) -> str:
    return value.lower().replace(" ", "-")
