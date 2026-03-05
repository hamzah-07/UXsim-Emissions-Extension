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
        baseline_demand_notes=str(planned_outputs["baseline_demand_notes"]),
        baseline_demand_profile_json=str(planned_outputs["baseline_demand_profile_json"]),
        intervention_demand_profile_json=str(
            planned_outputs["intervention_demand_profile_json"]
        ),
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
