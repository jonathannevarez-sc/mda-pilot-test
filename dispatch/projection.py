"""The driver projection: what the device shows for a drive order.

It is derived from the last accepted revision. The driver reads the stop they
are serving and the stops still ahead of them, and nothing about what moved.
"""

from __future__ import annotations

from dataclasses import dataclass

from dispatch.drive_order import DriveOrder, Stop


@dataclass(frozen=True)
class DriverProjection:
    load_id: str
    current_stop: Stop | None
    remaining_stops: tuple[Stop, ...]


def driver_projection(drive_order: DriveOrder) -> DriverProjection:
    """What the driver's device shows for this drive order as it stands."""
    return DriverProjection(
        load_id=drive_order.load_id,
        current_stop=drive_order.current_stop(),
        remaining_stops=drive_order.planned_stops(),
    )
