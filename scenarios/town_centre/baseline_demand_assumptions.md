# Linlithgow Baseline Demand Assumptions

The first Linlithgow town-centre baseline uses a deliberately simple gateway
approach so the OSM case study is stable before later refinement.

## Gateway Nodes

- west gateway: `863395379`
- east gateway: `1598385340`
- south gateway: `343450940`
- north gateway: `75632172`

These nodes sit close to the bounding-box edges and were checked against the
downloaded drive network to confirm that paths exist between all four gateways.

## Baseline Demand Profile

The baseline scenario uses four directional flows:

- west to east
- east to west
- south to north
- north to south

Each flow uses a small set of staggered departures for `passenger_car`
vehicles. This keeps the first town-centre run computationally manageable while
still producing crossing movements through the central network.

## Intervention Scaffold

The first intervention scaffold is a `peak-demand` variant. It keeps the same
gateway pairs but reduces the spacing between departures to create a simple
heavier-demand comparison case.
