"""Dummy jobs."""

from datetime import timedelta

from data_processing_framework.common import get_logger
from data_processing_framework.schedule import HOURLY, Schedule, job

LOGGER = get_logger(__file__)


@job(schedule=Schedule(timedelta(minutes=5)))
def test_5_min():
    LOGGER.info("5min")


@job(schedule=Schedule(timedelta(minutes=15)))
def test_15_min():
    LOGGER.info("15min")


@job(schedule=HOURLY)
def test_1_hour():
    LOGGER.info("1h")
