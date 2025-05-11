"""Job scheduling."""

from datetime import datetime, timedelta
from typing import Any, Callable, Optional

from miniflow.common import get_logger, get_redis_queue

__all__ = ["DAILY", "HOURLY", "MONTHLY", "WEEKLY", "Job", "Schedule", "schedule_jobs"]

LOGGER = get_logger(__file__)


class Schedule:
    """Defines when to run a job."""

    def __init__(self, at: Optional[datetime] = None, repeat: Optional[timedelta] = None) -> None:
        self.at = at or datetime.now()
        self.repeat = repeat

    def __str__(self):
        return f"Schedule(at={self.at}, repeat={self.repeat})"

    def first_exec(self) -> datetime:
        return self.at

    def next_exec(self) -> datetime:
        if not self.repeat:
            raise AttributeError("Schedule not set to repeat.")
        return datetime.now() + self.repeat


HOURLY = Schedule(repeat=timedelta(hours=1))
DAILY = Schedule(repeat=timedelta(days=1))
WEEKLY = Schedule(repeat=timedelta(weeks=1))
MONTHLY = Schedule(repeat=timedelta(weeks=4))


class Job:
    """Job to run on a schedule."""

    def __init__(
        self,
        func: Callable[[Any], Any],
        schedule: Schedule,
        args: Optional[tuple[Any, ...]] = None,
        kwargs: Optional[dict[str, Any]] = None,
    ) -> None:
        self._func = func
        self.description = func.__name__
        self.args = args or ()
        self.kwargs = kwargs or {}
        self.schedule = schedule

    def __str__(self):
        return f"Job({self.description})"

    def __call__(self) -> Any:
        if self.schedule.repeat is not None:
            queue = get_redis_queue()
            next_exec = self.schedule.next_exec()
            queue.enqueue_at(
                datetime=next_exec,
                f=self,
                description=self.description,
                meta=self.meta(),
            )
        return self._func(*self.args, **self.kwargs)

    def meta(self) -> dict[str, str]:
        return {"args": str(self.args), "kwargs": str(self.kwargs), "schedule": str(self.schedule)}


def schedule_jobs(jobs: list[Job]) -> None:
    """Enqueues a list of jobs to the Redis Queue."""

    queue = get_redis_queue()

    # cancel scheduled jobs
    for job in queue.jobs:
        job.cancel()

    # schedule jobs
    for job in jobs:
        _ = queue.enqueue_at(
            datetime=job.schedule.first_exec(), f=job, description=job.description, meta=job.meta()
        )
        LOGGER.info(f"Scheduled job {job}.")
