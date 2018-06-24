from libc.stdint cimport  uint32_t,  int64_t,  int32_t



### Common definitions:
ctypedef double float64_t
ctypedef float  float32_t 

include "khash.pxi"
cdef extern from *:
    ctypedef uint32_t khint_t


# different implementation
include "int64set_header.pxi"
include "int32set_header.pxi"
include "float64set_header.pxi"
