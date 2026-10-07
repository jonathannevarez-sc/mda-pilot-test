"""Read a synthetic Dispatch load file into a drive order.

The sample files hold the stop ids of one load and which of them are completed
or in progress. Everything else on the load is a planned stop. The rows stay in
the file; nothing here rewrites them.
"""

from __future__ import annotations

import json
from pathlib import Path

from dispatch.drive_order import DriveOrder, Stop, StopProgress

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures" / "synthetic"


def drive_order_from_load(load: dict) -> DriveOrder:
    """The drive order a sample load describes, in its snapshot order."""
    progress: dict[str, StopProgress] = {
        stop_id: StopProgress.SERVED for stop_id in load["completed"]
    }
    in_progress = load.get("in_progress")
    if in_progress:
        progress[in_progress] = StopProgress.IN_PROGRESS
    return DriveOrder(
        load_id=load["id"],
        loaded_snapshot=tuple(
            Stop(stop_id, progress.get(stop_id, StopProgress.PLANNED))
            for stop_id in load["stops"]
        ),
    )


def scenario(ac: str) -> DriveOrder:
    """The drive order in this story's sample file for one acceptance line."""
    document = json.loads(
        (FIXTURES / "1402" / f"{ac.lower()}.json").read_text(encoding="utf-8")
    )
    return drive_order_from_load(document["data"]["load"][0])


def sample_day(day: str) -> DriveOrder:
    """The drive order in a sample day file, such as porch."""
    load = json.loads((FIXTURES / f"{day}.json").read_text(encoding="utf-8"))
    return drive_order_from_load(load)
