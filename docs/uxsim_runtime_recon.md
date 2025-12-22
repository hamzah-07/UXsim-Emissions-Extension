# UXsim Runtime Recon

This note records what the current UXsim dependency exposes during a minimal run.
It is intentionally lightweight and will evolve into a more formal integration note
once the adapter layer is implemented.

## Verified Environment

- UXsim `1.13.0`
- Python `3.12.3`

## Smoke Run Entry Point

```bash
source .venv/bin/activate
python experiments/minimal_uxsim_smoke.py
```

## Confirmed World API

The installed `World` class supports the core scenario methods we need:

- `addNode`
- `addLink`
- `addVehicle`
- `exec_simulation`
- `finalize_scenario`

## Confirmed Runtime State

Vehicle objects expose state that is immediately useful for an emissions adapter:

- `state`
- `link`
- `x`
- `v`
- `distance_traveled`
- `travel_time`
- per-step logs such as `log_t`, `log_state`, `log_link`, `log_x`, and `log_v`

Link objects expose aggregate traffic state that is useful for per-link emissions:

- `speed`
- `density`
- `flow`
- `num_vehicles`
- `num_vehicles_queue`
- `length`

World objects expose high-level simulation progress and entity collections:

- `T`
- `TIME`
- `NODES`
- `LINKS`
- `VEHICLES`
- `VEHICLES_LIVING`
- `VEHICLES_RUNNING`

## Early Observations

- `World.T` and `World.TIME` are not initialized before the scenario is finalized or
  the simulation begins, so the adapter must treat pre-run snapshots separately.
- `Vehicle.distance_traveled` is reliable at trip completion in the smoke run, but it
  does not appear to update continuously in the same way as `x` during the mid-run
  snapshot. Early per-timestep work should therefore prefer `x`, `v`, and the vehicle
  logs while we verify the exact lifecycle of `distance_traveled`.
- Vehicle logging works cleanly with `vehicle_logging_timestep_interval=1`, which is
  promising for early validation and debugging.

## Why This Matters

This confirms the extension can likely start with a thin adapter layer that reads:

- per-vehicle speed and distance for timestep emissions
- per-link speed, density, flow, and queue counts for aggregate outputs
- vehicle logs for later validation and comparison work

The next implementation step should build a small adapter that converts these UXsim
objects into the normalised observation shape already scaffolded in
`src/uxsim_emissions/integration/uxsim_adapter.py`.

Keeping a couple of WIP/debug comments in the early integration scripts is worthwhile
here because UXsim's runtime state has a few lifecycle-specific quirks that are easier
to understand when the intent is written down close to the code.
