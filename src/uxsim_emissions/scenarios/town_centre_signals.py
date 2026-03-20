"""Small signal-control helpers for the Linlithgow case study."""

from __future__ import annotations

from dataclasses import dataclass

from uxsim_emissions.integration import WorldObservationSnapshot


@dataclass(slots=True)
class QueueResponsiveSignalController:
    """Rebalance a two-phase signal towards the busier approach group."""

    node_name: str
    group_0_links: tuple[str, ...]
    group_1_links: tuple[str, ...]
    group_0_green_s: float = 35.0
    group_1_green_s: float = 25.0

    def __call__(self, world: object, snapshot: WorldObservationSnapshot) -> None:
        signal = self.signal_for_snapshot(snapshot)
        world.NODES_NAME_DICT[self.node_name].signal = list(signal)

    def signal_for_snapshot(
        self,
        snapshot: WorldObservationSnapshot,
    ) -> tuple[float, float]:
        queue_by_link = {
            observation.link_id: observation.num_vehicles_queue
            for observation in snapshot.link_observations
        }
        group_0_queue = sum(queue_by_link.get(link_id, 0.0) for link_id in self.group_0_links)
        group_1_queue = sum(queue_by_link.get(link_id, 0.0) for link_id in self.group_1_links)
        if group_1_queue > group_0_queue:
            return (self.group_1_green_s, self.group_0_green_s)
        return (self.group_0_green_s, self.group_1_green_s)


def build_linlithgow_queue_responsive_controller() -> QueueResponsiveSignalController:
    """Build the tracked responsive controller for the Linlithgow signal test."""

    return QueueResponsiveSignalController(
        node_name="3200728316",
        group_0_links=(
            "tc_1051498106_3200728316_0",
            "tc_1051503017_3200728316_0",
        ),
        group_1_links=("tc_863303607_3200728316_0",),
    )
