"""Tests for the Linlithgow signal-control helpers."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from uxsim_emissions.integration import LinkObservation, WorldObservationSnapshot
from uxsim_emissions.scenarios.town_centre_signals import QueueResponsiveSignalController


class TownCentreSignalsTestCase(unittest.TestCase):
    def test_controller_biases_green_towards_busier_group(self) -> None:
        controller = QueueResponsiveSignalController(
            node_name="3200728316",
            group_0_links=("a", "b"),
            group_1_links=("c",),
        )
        snapshot = WorldObservationSnapshot(
            timestep=10,
            time_s=10.0,
            vehicle_observations=[],
            link_observations=[
                _link("a", 1.0),
                _link("b", 0.0),
                _link("c", 4.0),
            ],
        )

        self.assertEqual(controller.signal_for_snapshot(snapshot), (25.0, 35.0))

    def test_controller_keeps_default_split_when_group_zero_is_busier(self) -> None:
        controller = QueueResponsiveSignalController(
            node_name="3200728316",
            group_0_links=("a", "b"),
            group_1_links=("c",),
        )
        snapshot = WorldObservationSnapshot(
            timestep=10,
            time_s=10.0,
            vehicle_observations=[],
            link_observations=[
                _link("a", 2.0),
                _link("b", 1.0),
                _link("c", 1.0),
            ],
        )

        self.assertEqual(controller.signal_for_snapshot(snapshot), (35.0, 25.0))


def _link(link_id: str, queue: float) -> LinkObservation:
    return LinkObservation(
        link_id=link_id,
        speed_mps=0.0,
        density=0.0,
        flow=0.0,
        num_vehicles=queue,
        num_vehicles_queue=queue,
        length_m=10.0,
        timestep=10,
        time_s=10.0,
    )


if __name__ == "__main__":
    unittest.main()
