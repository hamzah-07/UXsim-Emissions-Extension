# Data Layout

This directory is reserved for tracked project data and reference inputs.

Suggested structure:

- `emission_factors/` for source CSV or JSON factor tables
- `fleet_profiles/` for vehicle mix assumptions
- `osm/` for curated OSM extracts and preprocessing outputs

The tracked `copert_average_speed_co2_factors.csv` file stores a small
COPERT-derived representative CO2 table for the repo's simplified
`passenger_car` average-speed model.

The current table represents:

- a medium petrol passenger car
- Euro 6
- Urban Peak driving conditions
- speed bins from `10` to `60` `km/h`

This is still a simplified representative curve rather than a full fleet model,
so the dataset may be expanded later if the project needs more vehicle classes
or a richer factor basis.

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
