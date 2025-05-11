"""Dummy jobs."""

from data_processing_framework.common import get_logger

LOGGER = get_logger(__file__)


def hi():
    print("Hi")
    LOGGER.info("Said Hi")


def hello():
    print("Hello")
    LOGGER.info("Said Hello")
