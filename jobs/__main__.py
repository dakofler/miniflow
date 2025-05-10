"""Job scheduler."""

from logging import getLogger

from jobs.common import get_redis_queue
from jobs.say_hi_job import say_hi

LOGGER = getLogger(__file__)


def main():
    queue = get_redis_queue()
    job = queue.enqueue(say_hi)
    LOGGER.info(f"Enqueued job {job}")


if __name__ == "__main__":
    main()
