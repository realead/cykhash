
from libc.stdint cimport int64_t,  int32_t
from .floatdef cimport float64_t, float32_t

cpdef unique_int64(int64_t[:] vals, double size_hint=*)
cpdef unique_int32(int32_t[:] vals, double size_hint=*)
cpdef unique_float64(float64_t[:] vals, double size_hint=*)
cpdef unique_float32(float32_t[:] vals, double size_hint=*)

cpdef unique_stable_int64(int64_t[:] vals, double size_hint=*)
cpdef unique_stable_int32(int32_t[:] vals, double size_hint=*)
cpdef unique_stable_float64(float64_t[:] vals, double size_hint=*)
cpdef unique_stable_float32(float32_t[:] vals, double size_hint=*)

