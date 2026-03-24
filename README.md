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

## Commit Messages

We follow Conventional Commits:(https://www.conventionalcommits.org/) - basically giving each commit a header such as `feat:`, `fix:`, `chore:`, `docs:`, etc.

This makes the git history much easier to read.
