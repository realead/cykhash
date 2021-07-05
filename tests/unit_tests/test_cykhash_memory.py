from contextlib import contextmanager

import numpy as np
import pytest

import cykhash as cyk
from cykhash.utils import get_cykhash_trace_domain

import sys
at_least_python36 = pytest.mark.skipif(sys.version_info < (3, 6),
                                  reason="requires Python3.6+")

from cykhash.compat import PYPY
not_on_pypy = pytest.mark.skipif(PYPY, reason="pypy doesn't support tracemalloc")
if not PYPY:
    import tracemalloc


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


@not_on_pypy
@at_least_python36
@pytest.mark.parametrize(
    "set_type, dtype",
    [
        (cyk.Int64Set, np.int64),
        (cyk.Int32Set, np.int32),
        (cyk.Float64Set, np.float64),
        (cyk.Float32Set, np.float32),
        (cyk.PyObjectSet, np.object),
    ],
)
def test_tracemalloc_works_sets(set_type, dtype):
    N = 2**10
    keys = np.arange(N).astype(dtype)
    with activated_tracemalloc():
        myset = set_type(keys)
        used = get_allocated_cykhash_memory()
        lower_bound = np.dtype(dtype).itemsize * (N*2)
        upper_bound = lower_bound * 1.1
        assert used > lower_bound
        assert used < upper_bound
        del myset
        assert get_allocated_cykhash_memory() == 0

@not_on_pypy
@at_least_python36
@pytest.mark.parametrize(
    "map_type, dtype",
    [
        (cyk.Int64toInt64Map, np.int64),
        (cyk.Int32toInt32Map, np.int32),
        (cyk.Float64toFloat64Map, np.float64),
        (cyk.Float32toFloat32Map, np.float32),
        (cyk.PyObjectMap, np.object),
    ],
)
def test_tracemalloc_works_maps(map_type, dtype):
    N = 2**10
    keys = np.arange(N).astype(dtype)
    with activated_tracemalloc():
        mymap = map_type(zip(keys, keys))
        used = get_allocated_cykhash_memory()
        lower_bound = np.dtype(dtype).itemsize * (N*2*2)
        upper_bound = lower_bound * 1.05
        assert used > lower_bound
        assert used < upper_bound
        del mymap
        assert get_allocated_cykhash_memory() == 0

@not_on_pypy
@at_least_python36
@pytest.mark.parametrize(
    "unique_version, dtype",
    [
        (cyk.unique_int64, np.int64),
        (cyk.unique_int32, np.int32),
        (cyk.unique_float64, np.float64),
        (cyk.unique_float32, np.float32),
    ],
)
def test_unique_memory_consumption(unique_version, dtype):
    N = 2**10
    keys = np.arange(N).astype(dtype)
    with activated_tracemalloc():
        result_buffer = unique_version(keys)
        assert get_allocated_cykhash_memory() == np.dtype(dtype).itemsize * N
        del result_buffer
        assert get_allocated_cykhash_memory() == 0

@not_on_pypy
@at_least_python36
@pytest.mark.parametrize(
    "unique_stable_version, dtype",
    [
        (cyk.unique_stable_int64, np.int64),
        (cyk.unique_stable_int32, np.int32),
        (cyk.unique_stable_float64, np.float64),
        (cyk.unique_stable_float32, np.float32),
    ],
)
def test_unique_memory_consumption(unique_stable_version, dtype):
    N = 2**10
    keys = np.arange(N).astype(dtype)
    with activated_tracemalloc():
        result_buffer = unique_stable_version(keys)
        assert get_allocated_cykhash_memory() == np.dtype(dtype).itemsize * N
        del result_buffer
        assert get_allocated_cykhash_memory() == 0
