from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Callable, Optional

from data_processing_framework.common import get_redis_queue


@dataclass
class Schedule:
    every: timedelta

    def __call__(self) -> datetime:
        return datetime.now() + self.every


HOURLY = Schedule(timedelta(hours=1))
DAILY = Schedule(timedelta(days=1))
WEEKLY = Schedule(timedelta(days=7))
MONTHLY = Schedule(timedelta(weeks=4))


def job(schedule: Optional[Schedule] = None) -> Callable[[Any], Any]:
    def decorator(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Callable[[Any], Any]:
            # reschedule periodic job
            if schedule is not None:
                queue = get_redis_queue()
                queue.enqueue_at(schedule(), wrapper)

            result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator
