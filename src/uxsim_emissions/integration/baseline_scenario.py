"""Helpers for building small reusable baseline scenarios in UXsim."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path

from ..config import ScenarioConfig
from .uxsim_adapter import UXsimAdapter, WorldObservationSnapshot

PROJECT_ROOT = Path(__file__).resolve().parents[3]


def _ensure_matplotlib_cache_dir() -> None:
    """Keep UXsim's matplotlib cache inside the repo during local runs."""

    os.environ.setdefault("MPLCONFIGDIR", str(PROJECT_ROOT / ".mplconfig"))


@dataclass(slots=True)
class BaselineScenario:
    """A built UXsim world plus the first snapshot captured from it."""

    config: ScenarioConfig
    world: object
    adapter: UXsimAdapter
    initial_snapshot: WorldObservationSnapshot


def build_baseline_scenario(
    config: ScenarioConfig,
    adapter: UXsimAdapter | None = None,
) -> BaselineScenario:
    """Build a ready-to-run UXsim world from a reusable scenario config."""

    _ensure_matplotlib_cache_dir()

    from uxsim import World

    adapter = adapter or UXsimAdapter()
    world = World(
        name=config.name,
        deltan=config.deltan,
        random_seed=config.random_seed,
        tmax=config.tmax_s,
        print_mode=config.print_mode,
        save_mode=config.save_mode,
        show_mode=config.show_mode,
        show_progress=config.show_progress,
        vehicle_logging_timestep_interval=config.vehicle_logging_timestep_interval,
    )

    for node in config.nodes:
        world.addNode(
            node.name,
            node.x,
            node.y,
            signal=list(node.signal),
            flow_capacity=node.flow_capacity,
        )

    for link in config.links:
        world.addLink(
            link.name,
            link.start_node,
            link.end_node,
            length=link.length_m,
            free_flow_speed=link.free_flow_speed_mps,
            jam_density=link.jam_density,
            number_of_lanes=link.number_of_lanes,
            signal_group=list(link.signal_group),
        )

    vehicle_index = 0
    for demand in config.demands:
        for departure_time_s in demand.departure_times_s:
            world.addVehicle(
                demand.origin,
                demand.destination,
                departure_time_s,
                name=f"{demand.vehicle_type}_{vehicle_index}",
            )
            vehicle_index += 1

    # The first snapshot is taken straight away so every experiment starts from
    # the same observed state before any simulation time has advanced.
    # The generated vehicle name still carries the configured vehicle type so
    # lightweight experiments can recover that metadata without a heavier side
    # channel.
    initial_snapshot = adapter.capture_snapshot(world)

    return BaselineScenario(
        config=config,
        world=world,
        adapter=adapter,
        initial_snapshot=initial_snapshot,
    )
