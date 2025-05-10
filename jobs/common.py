"""Job scheduling utils."""

from os import getenv

from redis import Redis
from rq import Queue

REDIS_HOST = getenv("REDIS_HOST", "redis")
REDIS_PORT = int(getenv("REDIS_PORT", 6379))


def get_redis_queue() -> None:
    redis_conn = Redis(REDIS_HOST, REDIS_PORT)
    queue = Queue(connection=redis_conn)
    return queue
