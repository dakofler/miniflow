"""Example job 1."""

from miniflow.common import get_logger

LOGGER = get_logger(__file__)


def example_job_1():
    LOGGER.info("Hello from example job 1.")
