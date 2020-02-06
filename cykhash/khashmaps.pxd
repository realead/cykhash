from libc.stdint cimport  uint32_t,  int64_t,  int32_t
from cpython.object cimport PyObject


### Common definitions:
ctypedef double float64_t
ctypedef float  float32_t 
ctypedef PyObject* pyobject_t

include "khash.pxi"
cdef extern from *:
    ctypedef uint32_t khint_t



#utilities for int<->float
include "float_utils.pxi"
include "pyobject_utils.pxi"

# different implementation
include "maps/int64/int64to64map_header.pxi"
include "maps/int32/int32to32map_header.pxi"
include "maps/float64/float64to64map_header.pxi"
include "maps/float32/float32to32map_header.pxi"
include "maps/pyobject/pyobjectmap_header.pxi"

