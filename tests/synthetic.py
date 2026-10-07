"""Synthetic drive orders for the unit tests.

Identifiers follow the SYN- tokens. The sample-day files belong to the
acceptance tests; these are small loads built in code for the unit tests.
"""

from dispatch.drive_order import DriveOrder, Stop, StopProgress

LOAD = "SYN-LOAD-1"


def stop(number: int, progress: StopProgress = StopProgress.PLANNED) -> Stop:
    return Stop(stop_id=f"SYN-STOP-1-{number}", progress=progress)


def porch_load() -> DriveOrder:
    """Three stops served, one in progress, four planned."""
    return DriveOrder(
        load_id=LOAD,
        loaded_snapshot=(
            stop(1, StopProgress.SERVED),
            stop(2, StopProgress.SERVED),
            stop(3, StopProgress.SERVED),
            stop(4, StopProgress.IN_PROGRESS),
            stop(5),
            stop(6),
            stop(7),
            stop(8),
        ),
    )
