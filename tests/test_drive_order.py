"""The drive order partitions a load and reads the order that stands now."""

import unittest

from dispatch.drive_order import DriveOrder, SequenceRevision, StopProgress
from tests.synthetic import porch_load, stop


class PartitionTest(unittest.TestCase):
    def test_served_stops_come_from_the_snapshot(self) -> None:
        order = porch_load()
        self.assertEqual(
            [s.stop_id for s in order.served_stops()],
            ["SYN-STOP-1-1", "SYN-STOP-1-2", "SYN-STOP-1-3"],
        )

    def test_current_stop_is_the_one_in_progress(self) -> None:
        self.assertEqual(porch_load().current_stop().stop_id, "SYN-STOP-1-4")

    def test_current_stop_is_none_when_no_stop_is_in_progress(self) -> None:
        order = porch_load()
        snapshot = tuple(
            stop(4) if s.progress is StopProgress.IN_PROGRESS else s
            for s in order.loaded_snapshot
        )
        self.assertIsNone(DriveOrder(order.load_id, snapshot).current_stop())

    def test_planned_stops_follow_the_snapshot_without_a_revision(self) -> None:
        self.assertEqual(
            [s.stop_id for s in porch_load().planned_stops()],
            ["SYN-STOP-1-5", "SYN-STOP-1-6", "SYN-STOP-1-7", "SYN-STOP-1-8"],
        )

    def test_planned_stops_follow_the_last_accepted_revision(self) -> None:
        order = porch_load().with_revision(
            SequenceRevision("SYN-REV-1", ("SYN-STOP-1-8", "SYN-STOP-1-5"))
        ).with_revision(
            SequenceRevision("SYN-REV-2", ("SYN-STOP-1-6", "SYN-STOP-1-7"))
        )
        self.assertEqual(
            [s.stop_id for s in order.planned_stops()],
            ["SYN-STOP-1-6", "SYN-STOP-1-7"],
        )

    def test_stops_reads_served_then_current_then_planned(self) -> None:
        self.assertEqual(
            [s.stop_id for s in porch_load().stops()],
            [f"SYN-STOP-1-{n}" for n in range(1, 9)],
        )

    def test_unknown_stop_id_is_refused(self) -> None:
        with self.assertRaises(KeyError):
            porch_load().stop("SYN-STOP-1-99")


class AppendTest(unittest.TestCase):
    def test_a_revision_is_appended_and_the_snapshot_is_left_alone(self) -> None:
        order = porch_load()
        revised = order.with_revision(
            SequenceRevision("SYN-REV-1", ("SYN-STOP-1-8",))
        )
        self.assertEqual(order.revisions, ())
        self.assertEqual(len(revised.revisions), 1)
        self.assertEqual(revised.loaded_snapshot, order.loaded_snapshot)


if __name__ == "__main__":
    unittest.main()
