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
- A manual source review was carried out on 6 April 2026.

## Cross-check result

- Rakha et al. (2004) confirms the VT-Micro model form used by the repo:
  separate 4x4 coefficient surfaces for non-negative and negative
  acceleration, with speed in km/h, acceleration in km/h/s, and emission rate
  in mg/s.
- The accessible paper text includes a sample coefficient table for HC
  emissions for one LDT category, which is consistent with the loader's 4x4
  storage shape.
- The accessible paper text does not provide the full `passenger_car` CO2
  `L_i,j` and `M_i,j` tables used by
  `data/emission_factors/vt_micro_co2_coefficients.csv`.
- Because of that, the 2004 paper is enough to confirm the model structure and
  unit conventions, but not enough on its own for a direct coefficient-by-
  coefficient verification of the tracked CO2 file.
- The current CSV values were compared against an open-access later
  reproduction of the CO2 `L_i,j` and `M_i,j` tables in Mao, Li and Zhang
  (2021), and the tracked values matched that reproduction entry by entry.

## Secondary numerical corroboration

Open-access reproduction used for the numerical cross-check:

Mao, F., Li, Z. and Zhang, K. (2021). A Comparison of Carbon Dioxide
Emissions between Battery Electric Buses and Conventional Diesel Buses.
Sustainability, 13(9), 5170. doi:10.3390/su13095170

## Verification checklist

- [x] Record the intended source paper for the tracked coefficients.
- [x] Record that the CSV layout is an internal repo format.
- [x] Record the present scope of the tracked file.
- [x] Confirm the VT-Micro model structure and unit conventions against Rakha
  et al. (2004).
- [x] Cross-check the tracked CO2 coefficient values against a later open-access
  numerical reproduction.
- [ ] Obtain a direct original numerical source for the `passenger_car` CO2
  `L_i,j` and `M_i,j` tables before treating the dataset as dissertation-ready.
- [ ] Archive that direct numerical provenance in the repo notes.
