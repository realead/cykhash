from contextlib import contextmanager
import tracemalloc

import numpy as np
import pytest

from cykhash.utils import get_cykhash_trace_domain


@contextmanager
def activated_tracemalloc():
    tracemalloc.start()
    try:
        yield
    finally:
        tracemalloc.stop()


def get_allocated_cykhash_memory():
    snapshot = tracemalloc.take_snapshot()
    snapshot = snapshot.filter_traces(
        (tracemalloc.DomainFilter(True, get_cykhash_trace_domain()),)
    )
    return sum(map(lambda x: x.size, snapshot.traces))


def test_trace_domain():
    assert 414141 == get_cykhash_trace_domain()
