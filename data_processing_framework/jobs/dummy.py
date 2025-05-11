"""Dummy jobs."""

from data_processing_framework.common import get_logger

LOGGER = get_logger(__file__)


def test_5_min():
    LOGGER.info("5min")


def test_15_min():
    LOGGER.info("15min")
