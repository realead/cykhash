from cpython cimport array


cdef extern from *:
    """
    // from float_utils.pxi
    """  
    int64_t   f64_to_i64(float64_t val)
    float64_t i64_to_f64(int64_t   val)
    int32_t   f32_to_i32(float32_t val)
    float32_t i32_to_f32(int32_t   val)
    khint_t kh_float64_hash_func(double val)
    khint_t kh_float32_hash_func(float val)
    khint_t murmur2_32to32(int32_t val)
    khint_t murmur2_64to32(int64_t val)

cdef extern from *:
    """
    //others
    """
    khint_t kh_int64_hash_func(int64_t val)
    khint_t kh_int_hash_func(int32_t val)

# different implementations:
include "sets/set_impl.pxi"



# some utils useful for investigations
def float64_hash(double val):
    """
    returns hash used for float64-values by cykhash sets/maps

    >>> from cykhash.khashsets import float64_hash
    >>> float64_hash(0.0)
    0
    >>> float64_hash(-0.0)
    0

    """
    return kh_float64_hash_func(val)

def float32_hash(float val):
    """
    returns hash used for float32-values by cykhash sets/maps

    >>> from cykhash.khashsets import float32_hash
    >>> float32_hash(0.0)
    0
    >>> float32_hash(-0.0)
    0

    """
    return kh_float32_hash_func(val)

def int64_hash(int64_t val):
    return murmur2_64to32(val)

def int32_hash(int32_t val):
    return murmur2_32to32(val)


