"""Reordering the planned stops of a drive order that is already underway.

The dispatcher submits an order. Served stops and the stop in progress hold
their places whatever that order says; only the planned stops move. The result
is appended as a sequence revision, so the loaded snapshot is left as it was.
"""

from __future__ import annotations

from dispatch.drive_order import DriveOrder, SequenceRevision, Stop, StopProgress


def resulting_planned_order(
    drive_order: DriveOrder, submitted_order: tuple[str, ...]
) -> tuple[str, ...]:
    """The planned stop ids as they would stand after this submitted order.

    Ids that name a served stop or the stop in progress are dropped: those stops
    are not the dispatcher's to move. A planned stop the dispatcher did not name
    keeps its place relative to the other unnamed stops, behind the named ones.
    """
    planned_ids = [stop.stop_id for stop in drive_order.planned_stops()]
    named: list[str] = []
    for stop_id in submitted_order:
        stop = drive_order.stop(stop_id)
        if stop.progress is not StopProgress.PLANNED:
            # A served or in-progress stop cannot be sequenced; AC3 and AC4 both
            # turn on the submitted order being read without it.
            continue
        if stop_id in named:
            raise ValueError(f"{stop_id} appears twice in the submitted order")
        named.append(stop_id)
    unnamed = [stop_id for stop_id in planned_ids if stop_id not in named]
    return tuple(named + unnamed)


def preview_revision(
    drive_order: DriveOrder, submitted_order: tuple[str, ...]
) -> tuple[Stop, ...]:
    """The whole drive order the dispatcher would get, without accepting it.

    Nothing is appended, so a dispatcher can read the result before deciding.
    """
    planned = {stop.stop_id: stop for stop in drive_order.planned_stops()}
    current = drive_order.current_stop()
    head = drive_order.served_stops() + ((current,) if current is not None else ())
    order = resulting_planned_order(drive_order, submitted_order)
    return head + tuple(planned[stop_id] for stop_id in order)


def accept_revision(
    drive_order: DriveOrder, submitted_order: tuple[str, ...], revision_id: str
) -> DriveOrder:
    """Append the dispatcher's order to the drive order as a sequence revision."""
    order = resulting_planned_order(drive_order, submitted_order)
    return drive_order.with_revision(
        SequenceRevision(revision_id=revision_id, planned_order=order)
    )
