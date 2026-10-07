"""Reordering the planned stops while a stop is in progress."""

import unittest

from dispatch.sequence import accept_revision, preview_revision, resulting_planned_order
from tests.synthetic import porch_load


class ResultingOrderTest(unittest.TestCase):
    def test_named_planned_stops_take_the_submitted_order(self) -> None:
        order = resulting_planned_order(
            porch_load(),
            ("SYN-STOP-1-7", "SYN-STOP-1-5", "SYN-STOP-1-8", "SYN-STOP-1-6"),
        )
        self.assertEqual(
            order,
            ("SYN-STOP-1-7", "SYN-STOP-1-5", "SYN-STOP-1-8", "SYN-STOP-1-6"),
        )

    def test_unnamed_planned_stops_keep_their_relative_place_behind(self) -> None:
        order = resulting_planned_order(porch_load(), ("SYN-STOP-1-8",))
        self.assertEqual(
            order,
            ("SYN-STOP-1-8", "SYN-STOP-1-5", "SYN-STOP-1-6", "SYN-STOP-1-7"),
        )

    def test_the_in_progress_stop_is_dropped_from_the_submitted_order(self) -> None:
        order = resulting_planned_order(
            porch_load(), ("SYN-STOP-1-5", "SYN-STOP-1-4", "SYN-STOP-1-6")
        )
        self.assertNotIn("SYN-STOP-1-4", order)
        self.assertEqual(order[:2], ("SYN-STOP-1-5", "SYN-STOP-1-6"))

    def test_a_served_stop_is_dropped_from_the_submitted_order(self) -> None:
        order = resulting_planned_order(
            porch_load(), ("SYN-STOP-1-1", "SYN-STOP-1-6")
        )
        self.assertNotIn("SYN-STOP-1-1", order)
        self.assertEqual(order[0], "SYN-STOP-1-6")

    def test_a_repeated_stop_is_refused(self) -> None:
        with self.assertRaises(ValueError):
            resulting_planned_order(
                porch_load(), ("SYN-STOP-1-5", "SYN-STOP-1-5")
            )

    def test_an_unknown_stop_is_refused(self) -> None:
        with self.assertRaises(KeyError):
            resulting_planned_order(porch_load(), ("SYN-STOP-1-99",))


class PreviewTest(unittest.TestCase):
    def test_preview_shows_the_resulting_drive_order(self) -> None:
        shown = preview_revision(porch_load(), ("SYN-STOP-1-8",))
        self.assertEqual(
            [s.stop_id for s in shown],
            [
                "SYN-STOP-1-1",
                "SYN-STOP-1-2",
                "SYN-STOP-1-3",
                "SYN-STOP-1-4",
                "SYN-STOP-1-8",
                "SYN-STOP-1-5",
                "SYN-STOP-1-6",
                "SYN-STOP-1-7",
            ],
        )

    def test_preview_appends_nothing(self) -> None:
        order = porch_load()
        preview_revision(order, ("SYN-STOP-1-8",))
        self.assertEqual(order.revisions, ())


class AcceptTest(unittest.TestCase):
    def test_accept_appends_one_revision_with_the_resulting_order(self) -> None:
        revised = accept_revision(porch_load(), ("SYN-STOP-1-8",), "SYN-REV-1")
        self.assertEqual(len(revised.revisions), 1)
        self.assertEqual(revised.revisions[0].revision_id, "SYN-REV-1")
        self.assertEqual(
            revised.revisions[0].planned_order,
            ("SYN-STOP-1-8", "SYN-STOP-1-5", "SYN-STOP-1-6", "SYN-STOP-1-7"),
        )

    def test_accept_leaves_the_current_stop_current(self) -> None:
        revised = accept_revision(
            porch_load(), ("SYN-STOP-1-7", "SYN-STOP-1-4"), "SYN-REV-1"
        )
        self.assertEqual(revised.current_stop().stop_id, "SYN-STOP-1-4")

    def test_accept_leaves_the_served_stops_where_they_were(self) -> None:
        order = porch_load()
        revised = accept_revision(order, ("SYN-STOP-1-8",), "SYN-REV-1")
        self.assertEqual(revised.served_stops(), order.served_stops())

    def test_accepting_twice_keeps_both_revisions(self) -> None:
        revised = accept_revision(porch_load(), ("SYN-STOP-1-8",), "SYN-REV-1")
        revised = accept_revision(revised, ("SYN-STOP-1-6",), "SYN-REV-2")
        self.assertEqual(
            [r.revision_id for r in revised.revisions], ["SYN-REV-1", "SYN-REV-2"]
        )
        self.assertEqual(revised.planned_stops()[0].stop_id, "SYN-STOP-1-6")


if __name__ == "__main__":
    unittest.main()
