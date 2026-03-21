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
- the emissions model selection workflow
- the experiment runner and summary metrics

Within each signal-policy comparison, the demand profile also stays fixed. This
means the signal policy is the main intended source of behavioural change
between the two runs.

## How The Controlled Junction Was Chosen

The first trial junction produced no meaningful policy difference because the
controlled approaches were not carrying traffic under the tracked Linlithgow
OD demand. The junction choice was therefore revised by inspecting which
incoming links were active in the current case-study flows and selecting a node
that sat on those routes.

The final controlled node is `243662941`, because it lies on active Linlithgow
traffic movements and provides a small two-phase control problem that can be
tested without turning the case study into a full network-wide signal project.

During the refinement pass, one additional incoming link,
`tc_369817321_243662941_0`, was added to the controlled group after it became
clear that the initial two-link grouping did not cover the full set of inbound
approaches at the chosen junction.

## Fixed-Time Baseline

The fixed-time baseline uses one tracked signal plan at node `243662941`.

- phase split: `35 s / 25 s`
- group 0 links:
  - `tc_863372585_243662941_0`
  - `tc_369817321_243662941_0`
- group 1 link:
  - `tc_410182009_243662941_0`

This provides a simple reproducible baseline control policy without adding a
larger hand-built signal network.

## Responsive Intervention

The responsive intervention uses the same junction and signal groups, but
rebalances the two-phase split using the `SignalDecision` record built from the
current snapshot of the controlled approaches.

The decision order is:

- if group 1 has at least one more queued vehicle than group 0, the split
  becomes `25 s / 35 s`
- if group 0 has at least one more queued vehicle than group 1, the split
  stays `35 s / 25 s`
- if the queued counts are tied, the controller falls back to total vehicles on
  each approach group
- if neither queue nor vehicle pressure favours group 1, the default remains
  `35 s / 25 s`

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

## Baseline And Heavier-Demand Comparison

The signal-policy comparison is now run under two tracked Linlithgow demand
profiles:

- `baseline`
- `peak_demand`

This keeps the network and signal layout fixed while allowing the same control
logic to be tested under a busier demand pattern.

For the `baseline` demand profile, the responsive controller reduced average
delay relative to the fixed-time plan:

- average-speed: `3.59 s` to `1.83 s`
- speed-acceleration: `3.59 s` to `1.83 s`

It also reduced total CO2 in both model paths:

- average-speed: `13016.73 g` to `12579.79 g`
- speed-acceleration: `5558.90 g` to `5416.10 g`

For the `peak_demand` profile, the responsive controller again reduced delay:

- average-speed: `7.32 s` to `4.91 s`
- speed-acceleration: `7.32 s` to `4.91 s`

The CO2 response under heavier demand is more mixed but remains comparable:

- average-speed: `19926.64 g` to `20001.00 g`
- speed-acceleration: `9788.88 g` to `9703.26 g`

This gives the dissertation two useful controlled signal experiments on the
same network:

- a baseline-demand comparison
- a heavier-demand stress comparison

## Current Scope Note

This is a deliberately small signal-control experiment rather than a full
network-wide adaptive control system. The goal is to provide a clear and
repeatable intervention comparison for the dissertation, not to claim a
production-grade signal optimisation method.
