# UXsim-Emissions-Extension

This repository contains a standalone emissions-modelling extension built
around the open-source traffic simulator UXsim.

The project keeps UXsim as the traffic engine and adds emissions logic around
it rather than modifying UXsim core directly. The extension captures reusable
traffic observations from UXsim, applies configurable emissions models, and
builds validation, benchmark, and analysis outputs for dissertation use.

## Current Scope

The current repo includes:

- an average-speed CO2 model using COPERT-derived representative factors
- a speed-acceleration CO2 model using a VT-Micro-style implementation
- reusable synthetic and small-network validation scenarios
- an OSM-derived Linlithgow town-centre case study
- fixed-time and responsive signal-policy experiments on the Linlithgow network
- analysis exports for model comparison, hotspot inspection, runtime
  benchmarking, and signal-policy comparison

## Setup

Create a virtual environment and install the project in editable mode:

```bash
python3 -m venv .venv
source .venv/bin/activate
.venv/bin/python -m pip install -e .[dev,osm,viz]
```

The same full development setup is also available through the convenience file:

```bash
.venv/bin/python -m pip install -r requirements-dev.txt
```

The project metadata currently supports Python `>=3.10`. The development work
for this repo has been carried out on Python `3.12`.

## Tests

Run the full test suite with:

```bash
.venv/bin/python -m unittest discover -s tests
```

## Usage

Run the tracked Linlithgow town-centre experiment:

```bash
.venv/bin/python experiments/linlithgow_town_centre_experiment.py
```

Export the Linlithgow analysis outputs:

```bash
.venv/bin/python experiments/export_linlithgow_analysis_outputs.py
```

Export the Linlithgow signal-policy comparison outputs:

```bash
.venv/bin/python experiments/export_linlithgow_signal_policy_outputs.py
```

## Data and Scope Notes

- The average-speed model uses a COPERT-derived representative CO2 curve for a
  simplified `passenger_car` category.
- The speed-acceleration model uses the tracked VT-Micro passenger-car CO2
  coefficient dataset.
- The Linlithgow baseline and peak-demand demand files are hand-built scenario
  assumptions rather than calibrated observed OD matrices.
- The fuel-based model discussed in the dissertation proposal was deferred and
  is not part of the current implementation.
- Generated analysis artefacts are written to `outputs/`, which is ignored by
  Git.

## Dataset Locations

- `data/emission_factors/copert_average_speed_co2_factors.csv`: COPERT-derived
  representative average-speed CO2 factors used by the average-speed model.
- `data/emission_factors/vt_micro_co2_coefficients.csv`: tracked VT-Micro CO2
  coefficient surfaces used by the speed-acceleration model.
- `scenarios/town_centre/linlithgow_nodes.csv`: node definitions for the
  Linlithgow town-centre network.
- `scenarios/town_centre/linlithgow_links.csv`: link definitions for the
  Linlithgow town-centre network.
- `scenarios/town_centre/linlithgow_baseline_demands.json`: baseline synthetic
  demand profile for the Linlithgow case study.
- `scenarios/town_centre/linlithgow_peak_demand_demands.json`: heavier-demand
  variant used for congestion and model-comparison experiments.
- `scenarios/town_centre/linlithgow_fixed_time_signals.json`: fixed-time signal
  plan used in the signal-policy comparison.
- `scenarios/town_centre/linlithgow_metadata.json`: supporting metadata for the
  Linlithgow case study configuration.
- `scenarios/town_centre/baseline_demand_assumptions.md`: short note describing
  the assumptions behind the baseline demand file.

## Project Management

The project was managed through a lightweight iterative workflow rather than a formal agile process such as Scrum. Development followed the semester work plan set out in the D1 proposal, with features implemented in small, focused, and testable increments. All changes were tracked using Git version control on GitHub, with every commit written according to the Conventional Commits specification: (https://www.conventionalcommits.org/)
basically giving each commit a header such as `feat:`, `fix:`, `chore:`, `docs:`, etc. This makes the git history much easier to read.

Progress was monitored through the commit history, a comprehensive automated test suite (run after every significant change), milestone deliverables, and regular updates to the dissertation document. This approach ensured the project remained structured, transparent, and traceable without requiring a separate task-management platform.
