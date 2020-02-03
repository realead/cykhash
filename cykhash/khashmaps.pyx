from cpython cimport array

cdef extern from *:
    """
    // from float_utils.pxi
    """  
    int64_t   f64_to_i64(float64_t val)
    float64_t i64_to_f64(int64_t   val)
    int32_t   f32_to_i32(float32_t val)
    float32_t i32_to_f32(int32_t   val)

# different implementations:
include "maps/int64/int64to64map_impl.pxi"
#include "sets/int32/int32set_impl.pxi"
#include "sets/float64/float64set_impl.pxi"
#include "sets/float32/float32set_impl.pxi"
#include "sets/pyobject/pyobjectset_impl.pxi"
