from libc.stdint cimport  uint64_t, uint32_t,  int64_t,  int32_t
from .floatdef cimport float64_t, float32_t

include "common.pxi"
include "memory.pxi"

def get_cykhash_trace_domain():
    """
    yield domain number of the cykhash trace domain (as specified by trace malloc),
    using this trace domain it is possible to trace memory allocations done by cykhash
    """
    return CYKHASH_TRACE_DOMAIN


include "hash_functions.pxi"

cdef extern from *:
    """
    // from hash_functions.pxi
    """
    uint32_t cykh_float32_hash_func(float val)
    uint32_t cykh_float64_hash_func(double val)
    uint32_t cykh_int32_hash_func(uint32_t val)
    uint32_t cykh_int64_hash_func(uint64_t val)
    uint32_t cykh_pyobject_hash_func(object ob)
    bint pyobject_cmp(object a, object b) 



# some utils useful for investigations
def objects_are_equal(a, b):
    """
    returns true if both objects are considered equal for khash-set/map
    """
    return pyobject_cmp(a, b)


def float64_hash(double val):
    """
    returns hash used for float64-values by cykhash sets/maps

    >>> from cykhash.utils import float64_hash
    >>> float64_hash(0.0)
    0
    >>> float64_hash(-0.0)
    0

    """
    return cykh_float64_hash_func(val)


def float32_hash(float val):
    """
    returns hash used for float32-values by cykhash sets/maps

    >>> from cykhash.utils import float32_hash
    >>> float32_hash(0.0)
    0
    >>> float32_hash(-0.0)
    0

    """
    return cykh_float32_hash_func(val)


def object_hash(val):
    """
    returns hash used for objects by cykhash sets/maps
    """
    return cykh_pyobject_hash_func(val)


def int64_hash(int64_t val):
    """
    returns hash used for int64-values by cykhash sets/maps
    """
    return cykh_int64_hash_func(val)


def int32_hash(int32_t val):
    """
    returns hash used for int32-values by cykhash sets/maps

    """
    return cykh_int32_hash_func(val)
