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

- Average-speed model: `16245.12 g CO2` over `96218.3 m`, `168.84 g/km`
- Speed-acceleration model: `5458.34 g CO2` over `96218.3 m`, `56.73 g/km`
- Average delay in both runs: `0.58 s`

Because the travelled distance and traffic state were the same in both runs,
the gap is attributable to the emissions model rather than a scenario change.

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

The current average-speed baseline result of `168.84 g/km` appears broadly
plausible as an in-use urban passenger-car estimate. It sits above the EEA
new-car benchmark and below the EPA typical passenger-vehicle figure, which is
reasonable for a town-centre simulation that reflects mixed urban driving
rather than certified laboratory conditions.

The current speed-acceleration result of `56.73 g/km` appears low by
comparison. At present, that should be treated as a provisional implementation
result rather than a final dissertation-grade estimate.

## Likely explanation for the VT-Micro gap

Several factors could explain why the current VT-Micro path is substantially
lower than the average-speed result:

- VT-Micro was originally developed for much more microscopic trajectory data
  than the mesoscopic snapshot pairs available from the current UXsim path.
- The current implementation infers acceleration from successive observations,
  which may smooth out short-lived aggressive driving behaviour.
- The tracked VT-Micro coefficient file is still treated as provisional rather
  than final dissertation-ready calibration data.

## Validation Process

- [x] Compare both current models on the Linlithgow baseline.
- [x] Record total CO2 and g/km for the same scenario.
- [x] Check the outputs against broad published benchmarks.
- [x] Record the strongest currently available local reference context.
- [ ] Compare baseline and higher-demand Linlithgow variants for congestion
  sensitivity.
- [ ] Inspect per-link outputs to check whether hotspots align with plausible
  town-centre corridors.
- [ ] Expand the validation note once those checks are complete.
