"""DPF entrypoint."""

from data_processing_framework.common import get_logger, get_redis_queue
from data_processing_framework.jobs import JOBS

LOGGER = get_logger(__file__)


def main() -> None:
    queue = get_redis_queue()

    # cancel scheduled jobs
    for job in queue.jobs:
        job.delete()

    # schedule jobs
    for job in JOBS:
        scheduled_job = queue.enqueue(job)
        LOGGER.info(f"Scheduled job {scheduled_job.description}.")


if __name__ == "__main__":
    main()
