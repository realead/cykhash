
from libc.stdint cimport int64_t,  int32_t
from cpython.object cimport PyObject
ctypedef double float64_t
ctypedef float  float32_t 


cpdef unique_int64(int64_t[:] vals, double size_hint=*)

