# Linlithgow Baseline Validation Note

This note records the first validation read-out for the Linlithgow
town-centre baseline.

The purpose of this step is not to claim ground-truth validation of CO2, but
to document whether the current outputs look broadly credible, internally
consistent, and traceable against published reference points.

## Baseline comparison

The baseline Linlithgow case study was run through both implemented CO2 models
using the same processed OSM network and the same demand profile.

Current baseline results:

- Average-speed model: `12210.88 g CO2` over `96218.3 m`, `126.91 g/km`
- Speed-acceleration model: `5458.34 g CO2` over `96218.3 m`, `56.73 g/km`
- Average delay in both runs: `0.58 s`

Because the travelled distance and traffic state were the same in both runs,
the gap is attributable to the emissions model rather than a scenario change.
The average-speed path now uses a COPERT-derived representative factor curve
for a medium petrol passenger car (Euro 6, Urban Peak) rather than the earlier
placeholder table.

## Published reference context

The broad benchmark context used for this first plausibility check is:

- The European Environment Agency reported average CO2 emissions of newly
  registered passenger cars in Europe in 2022 at `108.2 g/km`.
- The US EPA states that a typical passenger vehicle emits about `400 g CO2`
  per mile, which is approximately `248.5 g/km`.

These are not Linlithgow-specific and do not provide direct ground truth for
the case study. They are used here only as broad external reference points.

## Local context

The strongest local validation context currently available is the West Lothian
Council / Ricardo detailed air-quality assessment for Linlithgow. That study
used traffic survey data collected in Linlithgow in 2017 and local pollutant
monitoring data to assess roadside conditions in the town centre.

This is not direct CO2 validation, but it does provide useful evidence that:

- Linlithgow is a legitimate traffic and air-quality case-study location
- the town-centre network has already been studied using local traffic data
- local conditions are not consistent with an extreme chronic hotspot in the
  baseline year considered by that report

## Sources

- European Environment Agency news note on average emissions from new cars and
  vans, used here as a broad certified new-car benchmark reference:
  https://www.eea.europa.eu/en/newsroom/news/average-emissions-from-new-cars-and-vans/
- US EPA note on greenhouse gas emissions from a typical passenger vehicle,
  used here as a broad in-use passenger-vehicle reference point:
  https://www.epa.gov/greenvehicles/greenhouse-gas-emissions-typical-passenger-vehicle?source=ddd
- West Lothian Council / Ricardo detailed Linlithgow air-quality assessment,
  used here as the strongest local traffic and roadside environmental context:
  https://www.westlothian.gov.uk/media/55358/2022-Linlithgow-Detailed-Assessment-of-Air-Quality/pdf/2022_Linlithgow_Detailed_Assessment_of_Air_Quality.pdf

## Interpretation

The current average-speed baseline result of `126.91 g/km` appears broadly
plausible as an in-use urban passenger-car estimate. It sits above the EEA
new-car benchmark and below the EPA typical passenger-vehicle figure, which is
reasonable for a town-centre simulation that reflects mixed urban driving
rather than certified laboratory conditions.

The current speed-acceleration result of `56.73 g/km` appears low by
comparison and is discussed further below.

## Likely explanation for the VT-Micro gap

Several factors could explain why the current VT-Micro path is substantially
lower than the average-speed result:

- VT-Micro was originally developed for much more microscopic trajectory data
  than the mesoscopic snapshot pairs available from the current UXsim path.
- The current implementation infers acceleration from successive observations,
  which may smooth out short-lived aggressive driving behaviour.
- The tracked VT-Micro coefficient file follows the documented VT-Micro model
  form and the repo's current coefficient set for `passenger_car`.

## Congestion sensitivity

The Linlithgow case study was also compared between the tracked `baseline` and
`peak-demand` variants for both current models.

Observed changes under higher demand:

- Average-speed model:
  `12210.88 g -> 19751.66 g`,
  `126.91 -> 127.15 g/km`,
  delay `0.58 -> 0.64 s`
- Speed-acceleration model:
  `5458.34 g -> 9521.46 g`,
  `56.73 -> 61.29 g/km`,
  delay `0.58 -> 0.64 s`

This is a plausible congestion-sensitivity pattern. Both models produce higher
total CO2 and higher delay under heavier demand, and both also show a modest
rise in g/km rather than an implausible flat or falling intensity.

## Link hotspot plausibility

Per-link aggregation was enabled for the Linlithgow baseline and peak-demand
variants using the average-speed model to check whether the highest-emission
links align with plausible town-centre corridors.

Baseline top hotspot:

- `tc_322847838_190546646_0` (`primary`), `680.34 g CO2`

Peak-demand top hotspot:

- `tc_863278826_324283489_0` (`residential`), `2090.20 g CO2`

Across the top hotspot set, baseline emissions are concentrated on `primary`,
`secondary`, `tertiary`, and similar through-movement links rather than on
low-priority `service` edges. Under peak demand, emissions strengthen on major
corridors and residential gateway connectors, which is plausible for a
boundary-to-boundary town-centre demand pattern.

## Validation Process

- [x] Compare both current models on the Linlithgow baseline.
- [x] Record total CO2 and g/km for the same scenario.
- [x] Check the outputs against broad published benchmarks.
- [x] Record the strongest currently available local reference context.
- [x] Compare baseline and higher-demand Linlithgow variants for congestion
  sensitivity.
- [x] Inspect per-link outputs to check whether hotspots align with plausible
  town-centre corridors.
- [x] Expand the validation note once those checks are complete.
