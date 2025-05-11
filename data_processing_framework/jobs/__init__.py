"""Jobs."""

from data_processing_framework.jobs.dummy import test_5_min, test_15_min
from data_processing_framework.jobs.ingest_data import ingest_data

__all__ = ["ingest_data", "test_5_min", "test_15_min"]
