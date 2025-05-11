"""Job scheduling."""

from datetime import timedelta
from functools import wraps
from typing import Any, Callable, Optional

from data_processing_framework.common import get_redis_queue

HOURLY = timedelta(hours=1)
DAILY = timedelta(days=1)
WEEKLY = timedelta(days=7)
MONTHLY = timedelta(weeks=4)


def job(schedule: Optional[timedelta] = None) -> Callable[[Any], Any]:
    def decorator(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Callable[[Any], Any]:
            # reschedule periodic job
            if schedule is not None:
                queue = get_redis_queue()
                queue.enqueue_in(schedule, wrapper)

            result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator
