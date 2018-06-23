from libc.stdint cimport  uint32_t,  int64_t



### Common definitions:

include "khash.pxi"
cdef extern from *:
    ctypedef uint32_t khint_t

# different implementation
include "int64set_header.pxi"
