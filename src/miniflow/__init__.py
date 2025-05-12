"""
# Miniflow

Minimal job scheduling and execution framework based on Python RQ.

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dakofler/miniflow)
"""

from importlib.metadata import version

from miniflow.jobs import *

__version__ = version("miniflow")
