"""Job scheduling example."""

from datetime import timedelta

from dotenv import load_dotenv

from jobs.jobs import example_job_1, example_job_2, example_job_3
from miniflow import HOURLY, Job, Queue, Schedule, schedule

if __name__ == "__main__":
    load_dotenv(override=True)
    JOBS = [
        # run job now
        Job(example_job_1),
        # put job in "low" queue and run every 5 minutes
        Job(example_job_2, schedule=Schedule(repeat=timedelta(minutes=5)), queue=Queue.LOW),
        # run job once an hour with args
        Job(example_job_3, schedule=HOURLY, args=("This is a message",)),
    ]
    schedule(JOBS)
