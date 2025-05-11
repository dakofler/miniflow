"""DPF entrypoint."""

from datetime import timedelta

from data_processing_framework.common import get_logger, get_redis_queue
from data_processing_framework.job import HOURLY, Job, Schedule
from data_processing_framework.jobs import ingest_data, test_5_min, test_15_min

LOGGER = get_logger(__file__)
JOBS = [
    Job(test_5_min, schedule=Schedule(every=timedelta(minutes=5))),
    Job(test_15_min, schedule=Schedule(every=timedelta(minutes=15))),
    Job(ingest_data, schedule=HOURLY),
]


def main() -> None:
    queue = get_redis_queue()

    # cancel scheduled jobs
    for job in queue.jobs:
        job.cancel()

    # schedule jobs
    for job in JOBS:
        _ = queue.enqueue_at(
            job.schedule.first_exec,
            job,
            description=job.description,
            meta={"args": str(job.args), "kwargs": str(job.kwargs), "schedule": str(job.schedule)},
        )
        LOGGER.info(f"Scheduled job {job}.")


if __name__ == "__main__":
    main()
