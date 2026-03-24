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

## Commit Messages

We follow Conventional Commits:(https://www.conventionalcommits.org/) - basically giving each commit a header such as `feat:`, `fix:`, `chore:`, `docs:`, etc.

This makes the git history much easier to read.
