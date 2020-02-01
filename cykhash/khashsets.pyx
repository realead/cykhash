from cpython cimport array


# different implementations:
include "sets/int64/int64set_impl.pxi"
include "sets/int32/int32set_impl.pxi"
include "sets/float64/float64set_impl.pxi"
include "sets/float32/float32set_impl.pxi"
include "sets/pyobject/pyobjectset_impl.pxi"
