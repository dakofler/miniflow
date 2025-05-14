"""Job scheduling."""

from datetime import datetime, timedelta
from enum import StrEnum
from os import getenv
from typing import Any, Callable, Optional

from redis import Redis
from rq import Queue as _Queue

__all__ = ["DAILY", "HOURLY", "MONTHLY", "WEEKLY", "Job", "Queue", "Schedule", "schedule"]

REDIS_HOST = getenv("REDIS_HOST", "localhost")


class Queue(StrEnum):
    HIGH = "high"
    DEFAULT = "default"
    LOW = "low"


def get_redis_queue(name: Queue) -> _Queue:
    redis_conn = Redis(REDIS_HOST)
    queue = _Queue(name=name, connection=redis_conn)
    return queue


class Schedule:
    """Defines when to run a job."""

    def __init__(self, at: Optional[datetime] = None, repeat: Optional[timedelta] = None) -> None:
        self.at = at or datetime.now()
        self.repeat = repeat

    def __repr__(self) -> str:
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
        schedule: Optional[Schedule] = None,
        queue: Queue = Queue.DEFAULT,
        args: Optional[tuple[Any, ...]] = None,
        kwargs: Optional[dict[str, Any]] = None,
    ) -> None:
        self._func = func
        self.schedule = schedule or Schedule()
        self.queue = queue
        self.args = args or ()
        self.kwargs = kwargs or {}

        self.description = func.__name__

    def __repr__(self) -> str:
        return f"Job({self.description})"

    def __call__(self) -> Any:
        if self.schedule.repeat is not None:
            queue = get_redis_queue(self.queue)
            next_exec = self.schedule.next_exec()
            queue.enqueue_at(
                datetime=next_exec, f=self, description=self.description, meta=self.meta()
            )
        return self._func(*self.args, **self.kwargs)

    def meta(self) -> dict[str, str]:
        return {"args": str(self.args), "kwargs": str(self.kwargs), "schedule": repr(self.schedule)}


def schedule(jobs: list[Job]) -> None:
    """Enqueues a list of jobs to the Redis Queue."""

    for job in jobs:
        queue = get_redis_queue(job.queue)
        _ = queue.enqueue_at(
            datetime=job.schedule.first_exec(), f=job, description=job.description, meta=job.meta()
        )
