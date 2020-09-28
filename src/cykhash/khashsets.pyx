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

cdef extern from *:
    """
    //others
    """
    khint_t kh_int64_hash_func(int64_t val)
    khint_t kh_int_hash_func(int32_t val)

# different implementations:
include "sets/int64/int64set_impl.pxi"
include "sets/int32/int32set_impl.pxi"
include "sets/float64/float64set_impl.pxi"
include "sets/float32/float32set_impl.pxi"
include "sets/pyobject/pyobjectset_impl.pxi"



# some utils useful for investigations
def float64_hash(double val):
    return kh_float64_hash_func(val)

def float32_hash(float val):
    return kh_float32_hash_func(val)

def int64_hash(int64_t val):
    return kh_int64_hash_func(val)

def int32_hash(int32_t val):
    return kh_int_hash_func(val)


