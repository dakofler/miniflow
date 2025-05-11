# Miniflow

Minimal job scheduling and execution framework based on Python RQ.

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dakofler/miniflow)


## Requirements
- Docker and Docker Compose

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

1. Define your jobs as Python functions (preferrably in `miniflow/jobs`).
```Python
def example_job_1():
    LOGGER.info("Hello from example job 1.")
```

2. Add your jobs to a job list in the `miniflow/__main__.py` file
```Python
JOBS = [
    Job(example_job_1, schedule=Schedule()),  # run job now
    Job(example_job_2, schedule=Schedule(repeat=timedelta(minutes=5))),  # run every 5 minutes
    Job(example_job_3, schedule=HOURLY),  # run once an hour
]
```

3. (Optional) Confige the number of runners via `replicas` in `docker-compose.yml``
```YAML
rq-worker:
    <<: *base
    command: worker
    restart: always
    deploy:
        mode: replicated
        replicas: 1  # set number of worker replicas
        endpoint_mode: vip
```


3. Schedule jobs and start workers using
```bash
docker compose up -d --build
```

This also launches the RQ dashboard at `localhost:9181`.

## Author
Daniel Kofler - [dkofler@outlook.com](mailto:dkofler@outlook.com)