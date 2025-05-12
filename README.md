# Miniflow

Minimal, ready-to-use job scheduling and execution built on [Python RQ](https://python-rq.org/).

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dakofler/miniflow)


## Requirements
- Docker and Docker Compose to run Redis, workers and the dashboard.

## Installation

Using UV (recommended)
```bash
uv sync
```

Using pip
```bash
pip3 install .
```

## Usage

1. Define your jobs as Python functions  in `./jobs`.
```Python
# ./jobs/jobs.py

def example_job_1():
    print("Hello from example job 1.")
```

2. (Optional) Confige the number of runners via `replicas`.
```YAML
# ./docker-compose.yml

deploy:
    mode: replicated
    replicas: 1  # set number of worker replicas
    endpoint_mode: vip
```

3. Start workers and the dashboard (available at `localhost:9181`).
```bash
docker compose up -d --build
```

3. Configure your jobs and schedule them to run.
```Python
# ./run.py

from datetime import timedelta
from jobs.jobs import example_job_1, example_job_2, example_job_3
from miniflow import HOURLY, Job, Queue, Schedule, schedule

JOBS = [
    # run job now
    Job(example_job_1),
    # put job in "low" queue and run every 5 minutes
    Job(example_job_2, schedule=Schedule(repeat=timedelta(minutes=5)), queue=Queue.LOW),
    # run job once an hour with args
    Job(example_job_3, schedule=HOURLY, args=("This is a message",)),
]
schedule(JOBS)
```

```bash
uv run run.py
```

Done!



## Author
Daniel Kofler - [dkofler@outlook.com](mailto:dkofler@outlook.com)