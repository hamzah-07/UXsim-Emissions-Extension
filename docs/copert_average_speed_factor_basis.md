# COPERT-Derived Average-Speed Factor Basis

This note records the basis for replacing the tracked starter average-speed
CO2 factors with a more credible representative table.

## Intended model scope

The replacement average-speed table is intended to represent:

- `vehicle_type`: `passenger_car`
- pollutant: `co2`
- representative vehicle basis: medium petrol passenger car
- emission standard: Euro 6
- driving condition: Urban Peak

## Source basis

The replacement factors are treated as COPERT-derived representative values.
They are not being presented as a verbatim export of a full official COPERT
dataset.

This wording is deliberate. The repo uses one simplified `passenger_car`
category, so the replacement table is meant to provide a defensible
representative speed curve for that abstraction rather than a full fleet model.

## Speed points

The planned speed points are:

- `10`
- `20`
- `30`
- `40`
- `50`
- `60`

These bins keep the table focused on urban and town-centre conditions rather
than trying to cover the full motorway-speed range.

## Repo impact

The replacement table will continue to use the existing average-speed factor
schema:

- `vehicle_type`
- `pollutant`
- `speed_kph`
- `emission_g_per_km`

That keeps the data-layer change small and avoids unnecessary loader or schema
churn while the factor values are being upgraded.
