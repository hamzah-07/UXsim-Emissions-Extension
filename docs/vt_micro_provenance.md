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
- The source citation for the intended VT-Micro dataset has been identified.
- A full coefficient-by-coefficient check against the original 2004 source has
  not yet been recorded in the repo.

## Verification checklist

- [x] Record the intended source paper for the tracked coefficients.
- [x] Record that the CSV layout is an internal repo format.
- [x] Record the present scope of the tracked file.
- [ ] Confirm each coefficient value against the original Rakha et al. source.
- [ ] Record any transcription assumptions or unit interpretation notes found
  during that check.
- [ ] Mark the dataset as dissertation-ready only after the manual source check
  is complete.
