from libc.stdint cimport  uint32_t,  int64_t,  int32_t
from cpython.object cimport PyObject

from .floatdef cimport float64_t, float32_t

### Common definitions:
 
ctypedef PyObject* pyobject_t

include "khash.pxi"
cdef extern from *:
    ctypedef uint32_t khint_t


#utilities for int<->float
include "float_utils.pxi"
include "pyobject_utils.pxi"

# different implementation
include "sets/int64/int64set_header.pxi"
include "sets/int32/int32set_header.pxi"
include "sets/float64/float64set_header.pxi"
include "sets/float32/float32set_header.pxi"
include "sets/pyobject/pyobjectset_header.pxi"

