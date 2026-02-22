# Data Layout

This directory is reserved for tracked project data and reference inputs.

Suggested structure:

- `emission_factors/` for source CSV or JSON factor tables
- `fleet_profiles/` for vehicle mix assumptions
- `osm/` for curated OSM extracts and preprocessing outputs

The current `starter_average_speed_co2_factors.csv` file is only a small tracked
starter table for loader and model integration work. It should be replaced or expanded
with literature-backed factors before final experiments and evaluation.

The current `vt_micro_co2_coefficients.csv` file stores VT-Micro surfaces in the
repo's own CSV layout so they are easy to load and diff. That layout is our
implementation choice, not the original table format from the VT-Micro papers.
The 2004 Rakha et al. paper confirms the VT-Micro structure and unit
conventions used here, while the tracked CO2 values have been checked against a
later open-access numerical reproduction. Direct original numerical provenance
for the full passenger-car CO2 tables is still worth archiving before we treat
the dataset as dissertation-ready.
See `docs/vt_micro_provenance.md` for the current provenance note and
verification checklist tied to the tracked file.

Generated experiment outputs should go to `outputs/`, which is ignored by Git.
