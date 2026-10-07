"""The Dispatch stop order: the planned stop order for a day, the moment a
truck is loaded, and what the driver sees on the device.

Modules are added one story at a time. Standard library only; a new package
needs an ADR.
"""

from dispatch.drive_order import DriveOrder, SequenceRevision, Stop, StopProgress
from dispatch.projection import DriverProjection, driver_projection
from dispatch.sequence import accept_revision, preview_revision, resulting_planned_order

__all__: list[str] = [
    "DriveOrder",
    "DriverProjection",
    "SequenceRevision",
    "Stop",
    "StopProgress",
    "accept_revision",
    "driver_projection",
    "preview_revision",
    "resulting_planned_order",
]
