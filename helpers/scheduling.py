"""Scheduling helpers."""

from rq import Queue
from rq_scheduler import Scheduler

from helpers.db import get_redis_conn


def get_redis_queue() -> Queue:
    redis_conn = get_redis_conn()
    queue = Queue(connection=redis_conn)
    return queue


def get_scheduler() -> Scheduler:
    queue = get_redis_queue()
    scheduler = Scheduler(queue=queue, connection=queue.connection)
    return scheduler
