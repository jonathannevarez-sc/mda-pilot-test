"""A drive order: the stops of one load, and the revisions made to their order.

The loaded snapshot is the stop order captured at load-commit. A later reorder
is a sequence revision appended to `revisions`; the snapshot itself is never
rewritten, so the order the driver was given at load-commit stays readable.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import StrEnum


class StopProgress(StrEnum):
    """Where a stop stands on its load. A stop is in exactly one of these."""

    SERVED = "served"
    IN_PROGRESS = "in-progress"
    PLANNED = "planned"


@dataclass(frozen=True)
class Stop:
    stop_id: str
    progress: StopProgress = StopProgress.PLANNED


@dataclass(frozen=True)
class SequenceRevision:
    """An accepted order for the planned stops, appended to a drive order."""

    revision_id: str
    planned_order: tuple[str, ...]


@dataclass(frozen=True)
class DriveOrder:
    load_id: str
    loaded_snapshot: tuple[Stop, ...]
    revisions: tuple[SequenceRevision, ...] = ()

    def stop(self, stop_id: str) -> Stop:
        """The stop with this id, or KeyError when the load has no such stop."""
        for stop in self.loaded_snapshot:
            if stop.stop_id == stop_id:
                return stop
        raise KeyError(f"{self.load_id} has no stop {stop_id}")

    def served_stops(self) -> tuple[Stop, ...]:
        """The stops already served, in the order of the loaded snapshot.

        A revision never names these, so the snapshot is the only order they have.
        """
        return tuple(
            stop
            for stop in self.loaded_snapshot
            if stop.progress is StopProgress.SERVED
        )

    def current_stop(self) -> Stop | None:
        """The stop the driver is serving now, or None when none is in progress."""
        for stop in self.loaded_snapshot:
            if stop.progress is StopProgress.IN_PROGRESS:
                return stop
        return None

    def last_accepted_order(self) -> SequenceRevision | None:
        """The revision the dispatcher accepted most recently."""
        return self.revisions[-1] if self.revisions else None

    def planned_stops(self) -> tuple[Stop, ...]:
        """The stops still to be served, in the order that stands now.

        That is the last accepted revision when there is one, and otherwise the
        order captured in the loaded snapshot.
        """
        snapshot_order = tuple(
            stop
            for stop in self.loaded_snapshot
            if stop.progress is StopProgress.PLANNED
        )
        accepted = self.last_accepted_order()
        if accepted is None:
            return snapshot_order
        by_id = {stop.stop_id: stop for stop in snapshot_order}
        return tuple(by_id[stop_id] for stop_id in accepted.planned_order)

    def stops(self) -> tuple[Stop, ...]:
        """The whole drive order as it stands: served, then current, then planned."""
        current = self.current_stop()
        head = self.served_stops() + ((current,) if current is not None else ())
        return head + self.planned_stops()

    def with_revision(self, revision: SequenceRevision) -> DriveOrder:
        """This drive order with one more revision appended."""
        return replace(self, revisions=self.revisions + (revision,))
