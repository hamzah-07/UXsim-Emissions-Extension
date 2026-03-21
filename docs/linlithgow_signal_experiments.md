# Linlithgow Signal Experiment Design

This note records the controlled signal-policy experiments added to the
Linlithgow town-centre case study.

## Purpose

The aim of these runs is to compare how two traffic-management strategies
change CO2 outcomes on the same OSM-backed network:

- a fixed-time signal baseline
- a traffic-responsive signal intervention

These experiments support the proposal requirement to compare baseline and
intervention runs using the extended UXsim framework.

## What Stays Fixed

To keep the comparison controlled, the following parts of the case study stay
the same across the signal-policy runs:

- the processed Linlithgow OSM network
- the baseline demand profile
- the emissions model selection workflow
- the experiment runner and summary metrics

This means the signal policy is the main intended source of behavioural change
between the two runs.

## Fixed-Time Baseline

The fixed-time baseline uses one tracked signal plan at node `3200728316`.

- phase split: `35 s / 25 s`
- group 0 links:
  - `tc_1051498106_3200728316_0`
  - `tc_1051503017_3200728316_0`
- group 1 link:
  - `tc_863303607_3200728316_0`

This provides a simple reproducible baseline control policy without adding a
larger hand-built signal network.

## Responsive Intervention

The responsive intervention uses the same junction and signal groups, but
rebalances the two-phase split based on observed queued vehicles.

- if group 1 has the larger queue, the split becomes `25 s / 35 s`
- otherwise the split stays `35 s / 25 s`

The cycle length remains fixed at `60 s`, so the intervention changes green
allocation rather than total cycle time.

## Evaluation Read-Out

Each signal policy is run with both implemented CO2 models:

- average-speed
- speed-acceleration

The comparison read-out records:

- total CO2
- emission intensity in `g/km`
- average delay
- runtime

## Current Scope Note

This is a deliberately small signal-control experiment rather than a full
network-wide adaptive control system. The goal is to provide a clear and
repeatable intervention comparison for the dissertation, not to claim a
production-grade signal optimisation method.
