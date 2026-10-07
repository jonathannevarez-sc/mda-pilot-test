"""What the driver's device shows after a reorder."""

import unittest

from dispatch.projection import driver_projection
from dispatch.sequence import accept_revision
from tests.synthetic import porch_load


class ProjectionTest(unittest.TestCase):
    def test_the_projection_names_the_current_stop(self) -> None:
        shown = driver_projection(porch_load())
        self.assertEqual(shown.current_stop.stop_id, "SYN-STOP-1-4")

    def test_the_current_stop_is_unchanged_after_a_reorder(self) -> None:
        before = driver_projection(porch_load())
        revised = accept_revision(porch_load(), ("SYN-STOP-1-8",), "SYN-REV-1")
        self.assertEqual(driver_projection(revised).current_stop, before.current_stop)

    def test_the_remaining_stops_follow_the_accepted_order(self) -> None:
        revised = accept_revision(
            porch_load(), ("SYN-STOP-1-7", "SYN-STOP-1-5"), "SYN-REV-1"
        )
        self.assertEqual(
            [s.stop_id for s in driver_projection(revised).remaining_stops],
            ["SYN-STOP-1-7", "SYN-STOP-1-5", "SYN-STOP-1-6", "SYN-STOP-1-8"],
        )

    def test_the_projection_leaves_out_the_served_stops(self) -> None:
        shown = driver_projection(porch_load())
        self.assertNotIn(
            "SYN-STOP-1-1", [s.stop_id for s in shown.remaining_stops]
        )

    def test_the_projection_carries_the_load_id(self) -> None:
        self.assertEqual(driver_projection(porch_load()).load_id, "SYN-LOAD-1")


if __name__ == "__main__":
    unittest.main()
