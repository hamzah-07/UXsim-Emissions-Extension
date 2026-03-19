# VT-Micro CO2 Provenance Note

This note records the provenance and current verification status of the tracked
VT-Micro CO2 coefficient file used by the repo.

## Tracked file

- `data/emission_factors/vt_micro_co2_coefficients.csv`

## Source target

The current tracked coefficients are intended to represent the VT-Micro CO2
surfaces described in:

Rakha, H., Ahn, K. and Trani, A. (2004). Development of VT-Micro model for
estimating hot stabilised light duty vehicle and truck emissions.
Transportation Research Part D: Transport and Environment, 9(1), pp.49-74.
doi:10.1016/S1361-9209(03)00054-3

## Repo storage note

The CSV uses the repo's own internal storage layout rather than the paper's
published table layout. Each row stores one 4x4 coefficient surface with:

- `vehicle_type`
- `pollutant`
- `regime`
- `c00` to `c33`

This is a loader-friendly representation for source control and internal model
evaluation. It should not be treated as a claim that the original paper was
published in this exact tabular form.

## Current status

- The implementation path is complete and uses this file successfully.
- The tracked file currently contains two CO2 surfaces for `passenger_car`.
- The two regimes are `non_negative_acceleration` and
  `negative_acceleration`.
- A manual source review was carried out on 8 April 2026.

## Cross-check result

- Rakha et al. (2004) confirms the VT-Micro model form used by the repo:
  separate 4x4 coefficient surfaces for non-negative and negative
  acceleration, with speed in km/h, acceleration in km/h/s, and emission rate
  in mg/s.
- The accessible paper text includes a sample coefficient table for HC
  emissions for one LDT category, which is consistent with the loader's 4x4
  storage shape.
- The current CSV values were compared against an open-access later
  reproduction of the CO2 `L_i,j` and `M_i,j` tables in Mao, Li and Zhang
  (2021), and the tracked values matched that reproduction entry by entry.

## Direct original source search

The strongest direct original archival source identified so far is the Virginia
Tech dissertation by Kyoungho Ahn, which predates the 2004 journal paper and
documents the VT-Micro model development:

Ahn, K. (2002). *Modeling Light Duty Vehicle Emissions Based on Instantaneous
Speed and Acceleration Levels*. PhD thesis, Virginia Polytechnic Institute and
State University.

VTechWorks item page:

- https://vtechworks.lib.vt.edu/items/5c838801-e5bc-49b3-9bcb-4eef85661155

Direct dissertation content URL cited by a later review article:

- https://vtechworks.lib.vt.edu/server/api/core/bitstreams/5301ce13-7275-4871-953b-d1d60b7a6f18/content

## Secondary numerical corroboration

Open-access reproduction used for the numerical cross-check:

Mao, F., Li, Z. and Zhang, K. (2021). A Comparison of Carbon Dioxide
Emissions between Battery Electric Buses and Conventional Diesel Buses.
Sustainability, 13(9), 5170. doi:10.3390/su13095170

## Implementation assumption review

The current implementation assumptions were checked again against the published
VT-Micro structure and against the repo code path:

- speed is converted from UXsim `m/s` into VT-Micro `km/h`
- acceleration is converted from UXsim `m/s^2` into VT-Micro `km/h/s`
- the coefficient surfaces are evaluated as log-rates and then exponentiated
- the resulting emission rate is treated as `mg/s` and converted into repo
  output units of `g/s`
- emitted mass is then resolved over the actual interval duration when an
  observation pair provides one
- the regime split is driven by the sign of the derived acceleration, with the
  negative-acceleration surface applied directly when `a < 0`

## Verification checklist

- [x] Record the intended source paper for the tracked coefficients.
- [x] Record that the CSV layout is an internal repo format.
- [x] Record the present scope of the tracked file.
- [x] Confirm the VT-Micro model structure and unit conventions against Rakha
  et al. (2004).
- [x] Cross-check the tracked CO2 coefficient values against a later open-access
  numerical reproduction.
- [x] Identify a direct original archival source candidate for the coefficient
  tables.
