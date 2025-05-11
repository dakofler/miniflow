"""Jobs."""

from typing import Any, Callable, TypedDict

from data_processing_framework.jobs.dummy import test_5_min, test_15_min


class Job(TypedDict):
    func: Callable[[Any], Any]
    args: tuple[Any, ...]
    kwargs: dict[str, Any]


JOBS: list[Job] = [
    {"func": test_5_min, "args": (), "kwargs": {}},
    {"func": test_15_min, "args": (), "kwargs": {}},
]
