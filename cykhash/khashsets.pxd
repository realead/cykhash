from libc.stdint cimport  uint32_t,  int64_t,  int32_t
from cpython.object cimport PyObject


### Common definitions:
ctypedef double float64_t
ctypedef float  float32_t 
ctypedef PyObject* pyobject_t

include "khash.pxi"
cdef extern from *:
    ctypedef uint32_t khint_t


# different implementation
include "sets/int64/int64set_header.pxi"
include "sets/int32/int32set_header.pxi"
include "sets/float64/float64set_header.pxi"
include "sets/float32/float32set_header.pxi"
include "sets/pyobject/pyobjectset_header.pxi"

