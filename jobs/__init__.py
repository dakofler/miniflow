"""Jobs."""

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any, Callable, Optional

from helpers.scheduling import get_scheduler
from jobs.dummy import hello, hi
from jobs.ingest_data import ingest_data

__all__ = ["ingest_data", "schedule"]


@dataclass
class JobSpec:
    func: Callable[[Any], Any]
    interval: int
    initial_offset: int
    args: Optional[tuple[Any, ...]] = None
    kwargs: Optional[dict[str, Any]] = None


JOBS = (
    JobSpec(func=hi, interval=10, initial_offset=0),
    JobSpec(func=hello, interval=30, initial_offset=5),
)


def schedule() -> None:
    scheduler = get_scheduler()
    now = datetime.now(UTC)

    for job in JOBS:
        offset = now + timedelta(seconds=job.initial_offset)
        scheduler.schedule(
            scheduled_time=offset,
            func=job.func,
            args=job.args,
            kwargs=job.kwargs,
            interval=job.interval,
        )
