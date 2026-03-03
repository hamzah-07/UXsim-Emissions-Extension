# Town-Centre OSM Case-Study Scope

## Selected Study Area

The final OSM-backed case study will use **Linlithgow town centre, Scotland**.

Chosen bounding box:

- `min_lon = -3.630`
- `min_lat = 55.965`
- `max_lon = -3.580`
- `max_lat = 55.985`

Standard OSM bbox order:

- `-3.630,55.965,-3.580,55.985`

## Why Linlithgow

Linlithgow is a suitable dissertation case-study area because it offers:

- a compact town-centre network rather than an unmanageably large urban area
- multiple junctions and through movements that should make congestion-emissions patterns visible
- a clear geographic boundary for reproducible OSM import
- a network scale that should remain feasible for UXsim preprocessing and repeated experiments

## Intended Role In The Project

This area will provide the realistic network required by Objective 3 in the
proposal. It is intended to support:

- a stable baseline town-centre simulation
- comparison between the average-speed and speed-acceleration CO2 models
- later validation against literature ranges and any usable local reference context

## Initial OSM Preprocessing Assumptions

The first preprocessing path should aim for a credible but manageable UXsim
network rather than a perfect digital twin. Initial assumptions are:

- keep the study area limited to the agreed bounding box
- prioritise roads that form the main town-centre movement network
- simplify geometries into UXsim-compatible nodes and links
- resolve junction structure where OSM detail is too fine-grained for direct simulation
- treat missing speed or lane metadata with explicit documented defaults
- keep demand assumptions simple at first, then refine only if the baseline run is stable

## Expected Step 14 Outputs

Step 14 should leave the repo with:

- a reproducible Linlithgow OSM import path
- a processed UXsim-compatible town-centre network
- one baseline case-study run
- one simple intervention or scenario variation scaffold
