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
    )
