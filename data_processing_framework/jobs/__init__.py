"""Jobs."""

from data_processing_framework.jobs.dummy import hello, hi
from data_processing_framework.jobs.ingest_data import ingest_data

__all__ = ["hello", "hi", "ingest_data"]
