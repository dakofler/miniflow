"""Job scheduler."""

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any, Callable, Optional

from data_processing_framework.common import get_logger, get_scheduler
from data_processing_framework.jobs import hello, hi

LOGGER = get_logger(__file__)


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


def schedule_jobs() -> None:
    scheduler = get_scheduler()

    # cancel existing jobs
    existing_jobs = scheduler.get_jobs()
    for job in existing_jobs:
        scheduler.cancel(job)

    # schedule jobs
    for job in JOBS:
        scheduled_job = scheduler.schedule(
            scheduled_time=datetime.now(UTC) + timedelta(seconds=job.initial_offset),
            func=job.func,
            interval=job.interval,
            repeat=None,
            args=job.args,
            kwargs=job.kwargs,
        )
        LOGGER.info(f"Scheduled job {scheduled_job.description} to run every {job.interval}s.")
