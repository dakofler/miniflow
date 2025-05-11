"""Common utilities."""

import sys
from logging import INFO, Formatter, Logger, StreamHandler, getLogger
from os import getenv

from redis import Redis
from rq import Queue

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


def get_redis_queue() -> Queue:
    redis_conn = Redis(REDIS_HOST, REDIS_PORT)
    queue = Queue(connection=redis_conn)
    return queue
