# Architecture Notes

The extension is being built as a standalone Python package around UXsim rather than
as a fork of UXsim itself.

Planned responsibilities:

- `integration/`: convert UXsim simulation state into normalised observations
- `models/`: host the shared `EmissionModel` interface and concrete model classes
- `aggregation/`: roll per-step emissions into per-vehicle, per-link, and network totals
- `factors/`: load external CSV or JSON factor tables and fleet assumptions
- `validation/`: benchmark outputs against literature and record runtime overhead

This scaffold intentionally stops short of runtime UXsim integration. The next stage is
to verify the dependency set, run a minimal UXsim example, and inspect which vehicle
and link variables are exposed at each timestep.

