"""Common utilities."""

import sys
from logging import INFO, Formatter, Logger, StreamHandler, getLogger
from os import getenv

from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler
from sqlalchemy import Engine, create_engine

POSTGRES_USER = getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = getenv("POSTGRES_DB", "postgres")
POSTGRES_HOST = getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORT = int(getenv("POSTGRES_PORT", 5432))

REDIS_HOST = getenv("REDIS_HOST", "redis")
REDIS_PORT = int(getenv("REDIS_PORT", 6379))


def get_logger(identifier: str) -> Logger:
    logger = getLogger(identifier)

    handler = StreamHandler(sys.stdout)
    formatter = Formatter("%(asctime)s - %(levelname)s - %(message)s")

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.setLevel(INFO)
    return logger


def get_redis_conn() -> Redis:
    redis_conn = Redis(REDIS_HOST, REDIS_PORT)
    return redis_conn


def get_postgres_conn(database: str) -> Engine:
    postgres_conn_str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{database}"
    return create_engine(postgres_conn_str)


def get_redis_queue() -> Queue:
    redis_conn = get_redis_conn()
    queue = Queue(connection=redis_conn)
    return queue


def get_scheduler() -> Scheduler:
    redis_conn = get_redis_conn()
    scheduler = Scheduler(connection=redis_conn)
    return scheduler
