# Architecture Notes

The extension is implemented as a standalone Python package around UXsim rather
than as a fork of UXsim itself.

Current responsibilities:

- `integration/`: build reusable UXsim worlds, capture simulation snapshots,
  and derive observation-pair kinematics
- `models/`: host the shared `EmissionModel` interface plus the current
  average-speed and VT-Micro-style speed-acceleration CO2 models
- `aggregation/`: roll interval outputs into per-run and per-link totals
- `factors/`: load external CSV factor tables and coefficient datasets
- `scenarios/`: define synthetic, small-network, and Linlithgow town-centre
  case-study inputs, including signal-control overlays
- `experiments/`: run repeatable baseline, validation, benchmark, and
  intervention experiments and build summary outputs
- `validation/`: hold validation-facing helpers and supporting notes

The integration pattern stays external to UXsim core. UXsim remains the traffic
engine, while this repo handles emissions models, factor management,
aggregation, scenario preparation, validation, benchmarking, and analysis
exports around it.

The current system supports:

- configurable switching between average-speed and speed-acceleration CO2
  models
- staged scenario progression from synthetic tests to the Linlithgow OSM case
  study
- baseline, demand-variant, and signal-policy comparison experiments
- generated CSV, SVG, and Markdown outputs for validation and dissertation use
