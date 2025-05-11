"""Miniflow entrypoint."""

from datetime import timedelta

from miniflow.common import get_logger
from miniflow.job import HOURLY, Job, Schedule, schedule_jobs
from miniflow.jobs.job_1 import example_job_1
from miniflow.jobs.job_2 import example_job_2
from miniflow.jobs.job_3 import example_job_3

LOGGER = get_logger(__file__)
JOBS = [
    Job(example_job_1, schedule=Schedule()),  # run job now
    Job(example_job_2, schedule=Schedule(repeat=timedelta(minutes=5))),  # run every 5 minutes
    Job(example_job_3, schedule=HOURLY),  # run once an hour
]

if __name__ == "__main__":
    schedule_jobs(JOBS)
