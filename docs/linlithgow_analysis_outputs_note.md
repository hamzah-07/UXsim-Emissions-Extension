# Linlithgow Analysis Outputs Note

This note records the first figure-ready analysis outputs produced for the
Linlithgow town-centre case study.

The goal of this step is to turn the validation and benchmark results into
reusable analysis artefacts that can support dissertation tables, charts, and
discussion without relying only on plain-text run summaries.

## Current analysis artefacts

The current Linlithgow analysis output layer includes:

- a run-level comparison table covering both current models and both tracked
  town-centre variants
- a link-level hotspot table covering the top-emitting links for the baseline
  and peak-demand variants

These are produced by:

- `experiments/linlithgow_analysis_table.py`
- `experiments/linlithgow_link_hotspot_table.py`

## Run-level comparison read-out

The run-level table currently records:

- scenario name
- scenario variant
- model kind
- runtime
- total CO2
- total distance
- emission intensity in `g/km`
- average delay

The current Linlithgow rows show that:

- the `peak_demand` variant increases total CO2 and average delay for both
  models
- the average-speed model remains consistently higher than the current
  speed-acceleration path in both variants
- the two-model gap is large enough to be analytically meaningful and should
  be discussed explicitly in the dissertation rather than hidden inside prose

## Link-level hotspot read-out

The hotspot table currently records:

- scenario variant
- hotspot rank
- link identifier
- OSM highway class
- total CO2 on that link

The current hotspot rows show that:

- baseline emissions concentrate on plausible through-movement links such as
  `primary`, `secondary`, and `tertiary` corridors
- under `peak_demand`, the top hotspot intensifies sharply and emissions also
  strengthen on residential gateway connectors
- this gives us a useful bridge between network-wide totals and spatially
  differentiated interpretation

## Immediate analysis value

Together, these two artefacts are enough to support at least three useful
dissertation outputs:

- a compact table comparing Linlithgow baseline and peak-demand runs across
  both current models
- a hotspot table or ranked bar chart for the top-emitting links
- a short discussion of how network stress changes both aggregate emissions
  and where those emissions are concentrated

## Current limitation

These outputs are currently generated as CSV-style lines printed to stdout by
their scripts. That is enough for a first analysis layer, but later Step 17
work should make it easier to save them as files and turn them into plots or
dissertation-ready tables automatically.
