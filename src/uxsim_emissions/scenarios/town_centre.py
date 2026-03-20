"""Helpers for loading town-centre OSM case-study metadata."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path


@dataclass(slots=True)
class OSMBoundingBox:
    """Simple bounding-box definition for an OSM area extract."""

    min_lon: float
    min_lat: float
    max_lon: float
    max_lat: float

    def as_tuple(self) -> tuple[float, float, float, float]:
        """Return the bbox in standard OSM left,bottom,right,top order."""

        return (self.min_lon, self.min_lat, self.max_lon, self.max_lat)


@dataclass(slots=True)
class TownCentreImportConfig:
    """Structured import configuration derived from town-centre metadata."""

    study_area: str
    country: str
    bbox: OSMBoundingBox
    bbox_string: str
    raw_osm_basename: str
    processed_nodes_csv: str
    processed_links_csv: str
    fixed_time_signal_plan_json: str
    baseline_demand_notes: str
    baseline_demand_profile_json: str
    intervention_demand_profile_json: str


@dataclass(slots=True)
class OSMPreprocessingRules:
    """Initial OSM filtering and default assumptions for UXsim conversion."""

    kept_highway_types: tuple[str, ...]
    default_speed_kph_by_highway: dict[str, float]
    default_lanes_by_highway: dict[str, int]
    minimum_link_length_m: float = 5.0
    use_oneway_tags: bool = True
    simplify_junctions: bool = True


@dataclass(slots=True)
class SignalNodePlan:
    """Fixed-time signal timings for one named town-centre node."""

    node_name: str
    signal: tuple[float, ...]
    signal_offset_s: float = 0.0


@dataclass(slots=True)
class LinkSignalGroupPlan:
    """Signal-group assignment for one named incoming link."""

    link_name: str
    signal_group: tuple[int, ...]


@dataclass(slots=True)
class TownCentreSignalPlan:
    """Structured signal-plan overlay for a town-centre scenario."""

    name: str
    node_plans: list[SignalNodePlan]
    link_plans: list[LinkSignalGroupPlan]


def load_town_centre_import_config(
    metadata_path: Path | str,
) -> TownCentreImportConfig:
    """Load a town-centre OSM import configuration from tracked metadata."""

    path = Path(metadata_path)
    with path.open("r", encoding="utf-8") as handle:
        metadata = json.load(handle)

    # Keep the external JSON shape simple so the chosen case-study area and
    # planned artefact names remain editable without changing Python code.
    source = metadata["source"]
    planned_inputs = metadata["planned_inputs"]
    planned_outputs = metadata["planned_outputs"]
    bbox = source["bbox"]

    return TownCentreImportConfig(
        study_area=metadata["study_area"],
        country=metadata["country"],
        bbox=OSMBoundingBox(
            min_lon=float(bbox["min_lon"]),
            min_lat=float(bbox["min_lat"]),
            max_lon=float(bbox["max_lon"]),
            max_lat=float(bbox["max_lat"]),
        ),
        bbox_string=str(source["bbox_string"]),
        raw_osm_basename=str(planned_inputs["raw_osm_basename"]),
        processed_nodes_csv=str(planned_outputs["processed_nodes_csv"]),
        processed_links_csv=str(planned_outputs["processed_links_csv"]),
        fixed_time_signal_plan_json=str(planned_outputs["fixed_time_signal_plan_json"]),
        baseline_demand_notes=str(planned_outputs["baseline_demand_notes"]),
        baseline_demand_profile_json=str(planned_outputs["baseline_demand_profile_json"]),
        intervention_demand_profile_json=str(
            planned_outputs["intervention_demand_profile_json"]
        ),
    )


def load_town_centre_signal_plan(path: Path | str) -> TownCentreSignalPlan:
    """Load a machine-readable fixed-time signal plan."""

    with Path(path).open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    return TownCentreSignalPlan(
        name=str(payload["name"]),
        node_plans=[
            SignalNodePlan(
                node_name=str(node_plan["node_name"]),
                signal=tuple(float(value) for value in node_plan["signal"]),
                signal_offset_s=float(node_plan.get("signal_offset_s", 0.0)),
            )
            for node_plan in payload["node_plans"]
        ],
        link_plans=[
            LinkSignalGroupPlan(
                link_name=str(link_plan["link_name"]),
                signal_group=tuple(int(value) for value in link_plan["signal_group"]),
            )
            for link_plan in payload["link_plans"]
        ],
    )


def linlithgow_preprocessing_rules() -> OSMPreprocessingRules:
    """Return the first-pass OSM preprocessing rules for Linlithgow."""

    # Start with a conservative urban road set so the first town-centre network
    # is manageable to validate before adding lower-priority edges.
    return OSMPreprocessingRules(
        kept_highway_types=(
            "motorway",
            "trunk",
            "primary",
            "secondary",
            "tertiary",
            "unclassified",
            "residential",
            "living_street",
            "service",
        ),
        default_speed_kph_by_highway={
            "primary": 48.0,
            "secondary": 48.0,
            "tertiary": 40.0,
            "unclassified": 32.0,
            "residential": 32.0,
            "living_street": 16.0,
            "service": 16.0,
        },
        default_lanes_by_highway={
            "primary": 2,
            "secondary": 2,
            "tertiary": 2,
            "unclassified": 1,
            "residential": 1,
            "living_street": 1,
            "service": 1,
        },
    )
