# Data Layout

This directory is reserved for tracked project data and reference inputs.

Suggested structure:

- `emission_factors/` for source CSV or JSON factor tables
- `fleet_profiles/` for vehicle mix assumptions
- `osm/` for curated OSM extracts and preprocessing outputs

The current `starter_average_speed_co2_factors.csv` file is only a small tracked
starter table for loader and model integration work. It should be replaced or expanded
with literature-backed factors before final experiments and evaluation.

Generated experiment outputs should go to `outputs/`, which is ignored by Git.
