"""Acceptance tests for story 1402, one per acceptance line.

Sample day: porch, a drive order the driver has already started. Each test
opens this story's sample file for its own acceptance line; those files hold
the porch shape, the same one `fixtures/synthetic/porch.json` holds.

Each test is named for the Test Case it reports against.
"""

import unittest

from dispatch.projection import driver_projection
from dispatch.sequence import accept_revision, preview_revision
from tests.loader import scenario

REVISION = "SYN-REV-1"


class Story1402AcceptanceTest(unittest.TestCase):
    def test_tc1408_ac1_in_progress_stop_is_still_the_current_stop(self) -> None:
        """AC1: the stop in progress is still the current stop."""
        order = scenario("AC1")
        before = order.current_stop()
        planned = [stop.stop_id for stop in order.planned_stops()]

        revised = accept_revision(order, tuple(reversed(planned)), REVISION)

        self.assertEqual(revised.current_stop(), before)

    def test_tc1409_ac2_planned_stops_follow_the_dispatchers_order(self) -> None:
        """AC2: the planned stops follow the dispatcher's order behind the current stop."""
        order = scenario("AC2")
        submitted = tuple(reversed([stop.stop_id for stop in order.planned_stops()]))

        revised = accept_revision(order, submitted, REVISION)

        stops = [stop.stop_id for stop in revised.stops()]
        current = revised.current_stop().stop_id
        self.assertEqual(stops[stops.index(current) + 1 :], list(submitted))

    def test_tc1410_ac3_served_stops_keep_their_places(self) -> None:
        """AC3: the served stops keep their places and are not reordered."""
        order = scenario("AC3")
        before = order.served_stops()
        planned = [stop.stop_id for stop in order.planned_stops()]

        revised = accept_revision(order, tuple(reversed(planned)), REVISION)

        self.assertEqual(revised.served_stops(), before)
        self.assertEqual(revised.stops()[: len(before)], before)

    def test_tc1411_ac4_moving_the_in_progress_stop_leaves_it_current(self) -> None:
        """AC4: an order that moves the in-progress stop still leaves it current."""
        order = scenario("AC4")
        current = order.current_stop()
        planned = [stop.stop_id for stop in order.planned_stops()]
        # The dispatcher puts the in-progress stop behind the first planned stop.
        submitted = (planned[0], current.stop_id, *planned[1:])

        revised = accept_revision(order, submitted, REVISION)

        self.assertEqual(revised.current_stop(), current)
        self.assertEqual(
            [stop.stop_id for stop in revised.planned_stops()], planned
        )

    def test_tc1412_ac5_device_shows_the_same_current_stop_and_new_order(self) -> None:
        """AC5: the device shows the same current stop and the remaining stops in the new order."""
        order = scenario("AC5")
        before = driver_projection(order)
        submitted = tuple(reversed([stop.stop_id for stop in order.planned_stops()]))

        revised = accept_revision(order, submitted, REVISION)
        after = driver_projection(revised)

        self.assertEqual(after.current_stop, before.current_stop)
        self.assertEqual(
            [stop.stop_id for stop in after.remaining_stops], list(submitted)
        )


class DispatcherPreviewTest(unittest.TestCase):
    """The dispatcher sees the drive order they will get before they accept it."""

    def test_the_preview_matches_what_accepting_produces(self) -> None:
        order = scenario("AC2")
        submitted = tuple(reversed([stop.stop_id for stop in order.planned_stops()]))

        shown = preview_revision(order, submitted)
        accepted = accept_revision(order, submitted, REVISION).stops()

        self.assertEqual(shown, accepted)


if __name__ == "__main__":
    unittest.main()
