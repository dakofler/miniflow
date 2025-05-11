"""Job scheduling."""

from abc import ABC
from datetime import datetime, timedelta
from typing import Any, Callable, Optional

from data_processing_framework.common import get_redis_queue


class Schedule:
    def __init__(
        self, every: Optional[timedelta] = None, delay: Optional[timedelta] = None
    ) -> None:
        self.every = every
        self.delay = delay

    @property
    def first_exec(self) -> datetime:
        if self.every > timedelta(days=1):
            # tomorrow midnight
            dt = datetime.now() + timedelta(days=1)
            dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            dt = datetime.now()
        if self.delay:
            return dt + self.delay
        return dt

    def next_exec(self) -> datetime:
        return datetime.now() + self.every

    def __str__(self):
        return f"Schedule({self.every})"


HOURLY = Schedule(every=timedelta(hours=1))
DAILY = Schedule(every=timedelta(days=1))
WEEKLY = Schedule(every=timedelta(weeks=1))
MONTHLY = Schedule(every=timedelta(weeks=4))


class Job(ABC):
    def __init__(
        self,
        func: Callable,
        schedule: Optional[Schedule] = None,
        args: Optional[tuple[Any, ...]] = None,
        kwargs: Optional[dict[str, Any]] = None,
    ) -> None:
        self.func = func
        self.description = func.__name__
        self.args = args or ()
        self.kwargs = kwargs or {}
        self.schedule = schedule

    def __call__(self) -> Any:
        if self.schedule:
            queue = get_redis_queue()
            next_exec = self.schedule.next_exec()
            queue.enqueue_at(
                next_exec,
                self,
                description=self.description,
                meta={
                    "args": str(self.args),
                    "kwargs": str(self.kwargs),
                    "schedule": str(self.schedule),
                },
            )
        return self.func(*self.args, **self.kwargs)

    def __str__(self):
        return f"Job({self.description})"
