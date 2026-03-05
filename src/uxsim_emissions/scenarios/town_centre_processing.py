"""Conversion helpers for turning OSM town-centre data into UXsim artefacts."""

from __future__ import annotations

from pathlib import Path
import re

import pandas as pd

from .town_centre import OSMPreprocessingRules, TownCentreImportConfig


def fetch_town_centre_drive_graph(import_config: TownCentreImportConfig) -> object:
    """Download the drive network for the configured town-centre area."""

    import osmnx as ox

    return ox.graph_from_bbox(import_config.bbox.as_tuple(), network_type="drive")


def build_processed_town_centre_tables_from_graph(
    graph: object,
    rules: OSMPreprocessingRules,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Build processed node and link tables from an OSMnx graph."""

    import osmnx as ox

    nodes_frame, edges_frame = ox.graph_to_gdfs(graph)
    return build_processed_town_centre_tables_from_frames(
        nodes_frame=nodes_frame,
        edges_frame=edges_frame,
        rules=rules,
    )


def build_processed_town_centre_tables_from_frames(
    *,
    nodes_frame: pd.DataFrame,
    edges_frame: pd.DataFrame,
    rules: OSMPreprocessingRules,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Build processed UXsim-ready node and link tables from OSM frames."""

    processed_links: list[dict[str, object]] = []

    for edge_index, edge in edges_frame.reset_index().iterrows():
        highway = _normalise_highway(edge.get("highway"))
        if highway not in rules.kept_highway_types:
            continue

        length_m = float(edge.get("length", 0.0))
        if length_m < rules.minimum_link_length_m:
            continue

        start_node = str(edge["u"])
        end_node = str(edge["v"])
        key = int(edge.get("key", edge_index))
        processed_links.append(
            {
                "name": f"tc_{start_node}_{end_node}_{key}",
                "start_node": start_node,
                "end_node": end_node,
                "length_m": length_m,
                "free_flow_speed_mps": _speed_mps_for_edge(
                    raw_maxspeed=edge.get("maxspeed"),
                    highway=highway,
                    rules=rules,
                ),
                "jam_density": 0.2,
                "number_of_lanes": _lane_count_for_edge(
                    raw_lanes=edge.get("lanes"),
                    highway=highway,
                    rules=rules,
                ),
                "highway": highway,
                "oneway": bool(edge.get("oneway", False)) if rules.use_oneway_tags else False,
            }
        )

    links_table = pd.DataFrame(processed_links).sort_values(
        by=["start_node", "end_node", "name"]
    )
    used_node_names = set(links_table["start_node"]) | set(links_table["end_node"])

    processed_nodes = (
        nodes_frame.reset_index()
        .assign(name=lambda frame: frame["osmid"].astype(str))
        .loc[lambda frame: frame["name"].isin(used_node_names), ["name", "x", "y"]]
        .sort_values(by="name")
        .reset_index(drop=True)
    )

    return processed_nodes.reset_index(drop=True), links_table.reset_index(drop=True)


def write_processed_town_centre_tables(
    *,
    import_config: TownCentreImportConfig,
    nodes_table: pd.DataFrame,
    links_table: pd.DataFrame,
    output_dir: Path | str,
) -> tuple[Path, Path]:
    """Write processed town-centre node and link tables to tracked CSV files."""

    base_path = Path(output_dir)
    nodes_path = base_path / import_config.processed_nodes_csv
    links_path = base_path / import_config.processed_links_csv
    nodes_table.to_csv(nodes_path, index=False)
    links_table.to_csv(links_path, index=False)
    return nodes_path, links_path


def _normalise_highway(raw_highway: object) -> str | None:
    value = _first_scalar(raw_highway)
    if value is None:
        return None
    return str(value)


def _speed_mps_for_edge(
    *,
    raw_maxspeed: object,
    highway: str | None,
    rules: OSMPreprocessingRules,
) -> float:
    raw_value = _first_scalar(raw_maxspeed)
    if raw_value is not None:
        text = str(raw_value).lower()
        match = re.search(r"(\d+(?:\.\d+)?)", text)
        if match is not None:
            speed_value = float(match.group(1))
            speed_kph = speed_value * 1.609344 if "mph" in text else speed_value
            return speed_kph / 3.6

    default_kph = rules.default_speed_kph_by_highway.get(
        str(highway), rules.default_speed_kph_by_highway["residential"]
    )
    return default_kph / 3.6


def _lane_count_for_edge(
    *,
    raw_lanes: object,
    highway: str | None,
    rules: OSMPreprocessingRules,
) -> int:
    raw_value = _first_scalar(raw_lanes)
    if raw_value is not None:
        match = re.search(r"(\d+)", str(raw_value))
        if match is not None:
            return max(1, int(match.group(1)))

    return rules.default_lanes_by_highway.get(str(highway), 1)


def _first_scalar(raw_value: object) -> object | None:
    if isinstance(raw_value, list):
        return None if not raw_value else raw_value[0]
    return raw_value
