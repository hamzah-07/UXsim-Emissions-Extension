"""Small signal-control helpers for the Linlithgow case study."""

from __future__ import annotations

from dataclasses import dataclass

from uxsim_emissions.integration import WorldObservationSnapshot


@dataclass(frozen=True, slots=True)
class SignalDecision:
    """A small record of which split was chosen and why."""

    signal: tuple[float, float]
    group_0_queue: float
    group_1_queue: float
    group_0_vehicles: float
    group_1_vehicles: float
    reason: str


@dataclass(slots=True)
class QueueResponsiveSignalController:
    """Rebalance a two-phase signal towards the busier approach group."""

    node_name: str
    group_0_links: tuple[str, ...]
    group_1_links: tuple[str, ...]
    group_0_green_s: float = 35.0
    group_1_green_s: float = 25.0
    minimum_queue_advantage: float = 1.0

    def __call__(self, world: object, snapshot: WorldObservationSnapshot) -> None:
        decision = self.decision_for_snapshot(snapshot)
        world.NODES_NAME_DICT[self.node_name].signal = list(decision.signal)

    def signal_for_snapshot(
        self,
        snapshot: WorldObservationSnapshot,
    ) -> tuple[float, float]:
        return self.decision_for_snapshot(snapshot).signal

    def decision_for_snapshot(self, snapshot: WorldObservationSnapshot) -> SignalDecision:
        # Use the observed queued vehicles on each approach group as the
        # smallest traffic-responsive signal input we can justify in the
        # current case study, with total vehicles as a fallback when the
        # queued counts alone are too sparse to separate the approaches.
        queue_by_link = {}
        vehicles_by_link = {}
        for observation in snapshot.link_observations:
            queue_by_link[observation.link_id] = observation.num_vehicles_queue
            vehicles_by_link[observation.link_id] = observation.num_vehicles
        group_0_queue = sum(queue_by_link.get(link_id, 0.0) for link_id in self.group_0_links)
        group_1_queue = sum(queue_by_link.get(link_id, 0.0) for link_id in self.group_1_links)
        group_0_vehicles = sum(
            vehicles_by_link.get(link_id, 0.0) for link_id in self.group_0_links
        )
        group_1_vehicles = sum(
            vehicles_by_link.get(link_id, 0.0) for link_id in self.group_1_links
        )
        if group_1_queue >= group_0_queue + self.minimum_queue_advantage:
            return SignalDecision(
                signal=(self.group_1_green_s, self.group_0_green_s),
                group_0_queue=group_0_queue,
                group_1_queue=group_1_queue,
                group_0_vehicles=group_0_vehicles,
                group_1_vehicles=group_1_vehicles,
                reason="group_1_queue_advantage",
            )
        if group_0_queue >= group_1_queue + self.minimum_queue_advantage:
            return SignalDecision(
                signal=(self.group_0_green_s, self.group_1_green_s),
                group_0_queue=group_0_queue,
                group_1_queue=group_1_queue,
                group_0_vehicles=group_0_vehicles,
                group_1_vehicles=group_1_vehicles,
                reason="group_0_queue_advantage",
            )
        if group_1_vehicles > group_0_vehicles:
            return SignalDecision(
                signal=(self.group_1_green_s, self.group_0_green_s),
                group_0_queue=group_0_queue,
                group_1_queue=group_1_queue,
                group_0_vehicles=group_0_vehicles,
                group_1_vehicles=group_1_vehicles,
                reason="group_1_vehicle_pressure",
            )
        return SignalDecision(
            signal=(self.group_0_green_s, self.group_1_green_s),
            group_0_queue=group_0_queue,
            group_1_queue=group_1_queue,
            group_0_vehicles=group_0_vehicles,
            group_1_vehicles=group_1_vehicles,
            reason="group_0_default",
        )


def build_linlithgow_queue_responsive_controller() -> QueueResponsiveSignalController:
    """Build the tracked responsive controller for the Linlithgow signal test."""

    # Reuse the same junction and link groups as the fixed-time baseline so
    # the intervention changes the control policy rather than the layout.
    return QueueResponsiveSignalController(
        node_name="243662941",
        group_0_links=(
            "tc_863372585_243662941_0",
            "tc_369817321_243662941_0",
        ),
        group_1_links=("tc_410182009_243662941_0",),
    )
