"""Dummy jobs."""

from datetime import timedelta

from data_processing_framework.common import get_logger
from data_processing_framework.schedule import job

LOGGER = get_logger(__file__)


@job(schedule=timedelta(minutes=5))
def test_5_min():
    LOGGER.info("5min")


@job(schedule=timedelta(minutes=15))
def test_15_min():
    LOGGER.info("15min")
