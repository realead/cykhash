from libc.stdint cimport  uint64_t, uint32_t,  int64_t,  int32_t
from .floatdef cimport float64_t, float32_t


include "memory.pxi"

def get_cykhash_trace_domain():
    """
    yield domain number of the cykhash trace domain (as specified by trace malloc),
    using this trace domain it is possible to trace memory allocations done by cykhash
    """
    return CYKHASH_TRACE_DOMAIN


include "murmurhash.pxi"
include "float_utils.pxi"

cdef extern from *:
    """
    // from float_utils.pxi
    """  
    uint32_t kh_float64_hash_func(double val)
    uint32_t kh_float32_hash_func(float val)
    uint32_t murmur2_32to32(uint32_t val)
    uint32_t murmur2_64to32(uint64_t val)



# some utils useful for investigations
def float64_hash(double val):
    """
    returns hash used for float64-values by cykhash sets/maps

    >>> from cykhash.utils import float64_hash
    >>> float64_hash(0.0)
    0
    >>> float64_hash(-0.0)
    0

    """
    return kh_float64_hash_func(val)


def float32_hash(float val):
    """
    returns hash used for float32-values by cykhash sets/maps

    >>> from cykhash.utils import float32_hash
    >>> float32_hash(0.0)
    0
    >>> float32_hash(-0.0)
    0

    """
    return kh_float32_hash_func(val)


def int64_hash(int64_t val):
    """
    returns hash used for int64-values by cykhash sets/maps
    """
    return murmur2_64to32(val)


def int32_hash(int32_t val):
    """
    returns hash used for int32-values by cykhash sets/maps

    """
    return murmur2_32to32(val)

