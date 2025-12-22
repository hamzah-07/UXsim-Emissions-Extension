"""Minimal UXsim smoke run used for early integration reconnaissance."""

from __future__ import annotations

import json
import os
from pathlib import Path

# WIP: keep matplotlib's cache inside the repo while we are still doing
# local integration experiments in a constrained environment.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(PROJECT_ROOT / ".mplconfig"))

from uxsim import World


def _vehicle_snapshot(vehicle) -> dict[str, object]:
    return {
        "name": vehicle.name,
        "state": vehicle.state,
        "link": getattr(vehicle.link, "name", None),
        "x": vehicle.x,
        "speed_mps": vehicle.v,
        "distance_traveled_m": vehicle.distance_traveled,
        "travel_time_s": vehicle.travel_time,
        "log_lengths": {
            "t": len(vehicle.log_t),
            "state": len(vehicle.log_state),
            "link": len(vehicle.log_link),
            "x": len(vehicle.log_x),
            "v": len(vehicle.log_v),
        },
    }


def _link_snapshot(link) -> dict[str, object]:
    return {
        "name": link.name,
        "speed_mps": link.speed,
        "density": link.density,
        "flow": link.flow,
        "num_vehicles": link.num_vehicles,
        "num_vehicles_queue": link.num_vehicles_queue,
        "length_m": link.length,
    }


def _world_snapshot(world) -> dict[str, object]:
    vehicles_living = getattr(world, "VEHICLES_LIVING", {})
    vehicles_running = getattr(world, "VEHICLES_RUNNING", {})
    return {
        "timestep": getattr(world, "T", None),
        "time_s": getattr(world, "TIME", None),
        "num_nodes": len(world.NODES),
        "num_links": len(world.LINKS),
        "num_vehicles_defined": len(world.VEHICLES),
        "num_vehicles_living": len(vehicles_living),
        "num_vehicles_running": len(vehicles_running),
    }


def build_smoke_world() -> tuple[World, object, object]:
    world = World(
        name="minimal-smoke",
        deltan=1,
        random_seed=42,
        tmax=60,
        print_mode=0,
        save_mode=0,
        show_mode=0,
        show_progress=0,
        vehicle_logging_timestep_interval=1,
    )
    world.addNode("orig", 0, 0)
    world.addNode("dest", 100, 0)
    link = world.addLink(
        "orig_dest",
        "orig",
        "dest",
        length=100,
        free_flow_speed=10,
        jam_density=0.2,
    )
    vehicle = world.addVehicle("orig", "dest", 0, name="veh_0")
    return world, link, vehicle


def run_smoke() -> dict[str, object]:
    world, link, vehicle = build_smoke_world()

    # WIP: this uses a partial run on purpose so we can compare mid-run and
    # completed states before writing the real adapter layer.
    initial = {
        "world": _world_snapshot(world),
        "link": _link_snapshot(link),
        "vehicle": _vehicle_snapshot(vehicle),
    }

    world.exec_simulation(duration_t2=5)
    mid_run = {
        "world": _world_snapshot(world),
        "link": _link_snapshot(link),
        "vehicle": _vehicle_snapshot(vehicle),
    }

    world.exec_simulation()
    completed = {
        "world": _world_snapshot(world),
        "link": _link_snapshot(link),
        "vehicle": _vehicle_snapshot(vehicle),
    }

    return {
        "uxsim_world_name": world.name,
        "deltat_s": world.DELTAT,
        "initial": initial,
        "mid_run": mid_run,
        "completed": completed,
    }


if __name__ == "__main__":
    print(json.dumps(run_smoke(), indent=2, default=str))
