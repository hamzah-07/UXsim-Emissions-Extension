# VT-Micro Validation Note

This note records the current validation read-out for the VT-Micro
speed-acceleration CO2 model used by the repo.

The purpose of this note is to gather the present evidence for the VT-Micro
path in one place. It is intended to support dissertation discussion of model
behaviour, traceability, and comparison against the average-speed baseline.

## Model basis

The tracked VT-Micro implementation uses the standard passenger-car CO2
surface form with separate coefficient grids for:

- `non_negative_acceleration`
- `negative_acceleration`

The coefficient file used by the repo is:

- `data/emission_factors/vt_micro_co2_coefficients.csv`

The model form follows:

- Rakha, H., Ahn, K. and Trani, A. (2004). *Development of VT-Micro model for
  estimating hot stabilised light duty vehicle and truck emissions*.
  Transportation Research Part D: Transport and Environment, 9(1), pp.49-74.
  doi:10.1016/S1361-9209(03)00054-3

The numerical coefficient values were cross-checked against a later academic
reproduction of the passenger-car CO2 tables:

- Mao, F., Li, Z. and Zhang, K. (2021). *A Comparison of Carbon Dioxide
  Emissions between Battery Electric Buses and Conventional Diesel Buses*.
  Sustainability, 13(9), 5170. doi:10.3390/su13095170

## Implementation path

The current repo implementation applies the VT-Micro surfaces to successive
UXsim observation pairs.

In practical terms, the model path:

- converts speed from `m/s` into `km/h`
- converts acceleration from `m/s^2` into `km/h/s`
- evaluates the relevant VT-Micro surface as a log-rate
- converts the resulting rate into emitted mass over the observed interval

This allows the repo to use the VT-Micro structure within the mesoscopic
observation path already captured by the UXsim adapter layer.

## Linlithgow baseline results

For the Linlithgow town-centre baseline, the VT-Micro path produced:

- total CO2: `5458.34 g`
- distance: `96218.3 m`
- intensity: `56.73 g/km`
- average delay: `0.58 s`

For comparison, the current COPERT-derived average-speed path on the same
baseline produced:

- total CO2: `12210.88 g`
- distance: `96218.3 m`
- intensity: `126.91 g/km`
- average delay: `0.58 s`

Because the travelled distance and traffic state were the same in both runs,
the difference is attributable to the emissions model rather than to a
scenario change.

## Linlithgow peak-demand results

For the Linlithgow `peak_demand` variant, the VT-Micro path produced:

- total CO2: `9521.46 g`
- distance: `155341.8 m`
- intensity: `61.29 g/km`
- average delay: `0.64 s`

For comparison, the current COPERT-derived average-speed path on the same
peak-demand variant produced:

- total CO2: `19751.66 g`
- distance: `155341.8 m`
- intensity: `127.15 g/km`
- average delay: `0.64 s`

## Behaviour under higher demand

The VT-Micro Linlithgow results show a clear increase between the tracked
baseline and `peak_demand` variants:

- total CO2: `5458.34 g -> 9521.46 g`
- intensity: `56.73 g/km -> 61.29 g/km`
- average delay: `0.58 s -> 0.64 s`

This shows that the VT-Micro path responds in a plausible direction when the
network is placed under heavier demand.

## Benchmark context

The broad external benchmark context used elsewhere in the repo remains useful
here as well:

- European Environment Agency average emissions from newly registered passenger
  cars in Europe in 2022: `108.2 g/km`
- US EPA typical passenger vehicle reference: about `248.5 g/km`

These figures are not direct Linlithgow ground truth and are not a like-for-
like validation target for VT-Micro. They are used here as broad context for
the order of magnitude of the current outputs.

## Current interpretation

Within the current repo workflow, the VT-Micro path is:

- structurally traceable to the original VT-Micro model family
- numerically consistent with the tracked coefficient dataset
- responsive to higher demand in the expected direction
- lower in absolute magnitude than the current COPERT-derived average-speed
  comparison path on the Linlithgow case study

This makes the VT-Micro results useful for model comparison and congestion-
sensitivity analysis within the dissertation, while keeping the interpretation
anchored to the current Linlithgow case-study evidence.
