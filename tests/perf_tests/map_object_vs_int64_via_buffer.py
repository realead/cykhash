import perfplot
import numpy as np

from cykhash import Int64to64Map, Int64to64MapIterator, Int64to64Map_from_int64_buffer, Int64to64Map_from_float64_buffer 
from cykhash import Int32to32Map, Int32to32MapIterator, Int32to32Map_from_int32_buffer, Int32to32Map_from_float32_buffer 
from cykhash import Float64to64Map, Float64to64MapIterator, Float64to64Map_from_int64_buffer, Float64to64Map_from_float64_buffer 
from cykhash import Float32to32Map, Float32to32MapIterator, Float32to32Map_from_int32_buffer, Float32to32Map_from_float32_buffer 
from cykhash import PyObjectMap, PyObjectMapIterator, PyObjectMap_from_object_buffer

def pyobjectset_from_buffer(bufs):
    PyObjectMap_from_object_buffer(bufs[0], bufs[0])

def pyobjectset_add_preallocated(bufs):
    n = len(bufs[0])
    p = PyObjectMap(int(1.3*n))   
    for i in range(n):
        p[i] = i

def int64_add_preallocated(bufs):
    n = len(bufs[1])
    p = Int64to64Map(int(1.3*n))   
    for i in range(n):
        p[i] = i

def int64set_from_buffer(bufs):
    Int64to64Map_from_int64_buffer(bufs[1], bufs[1])

def int32set_from_buffer(bufs):
    Int32to32Map_from_int32_buffer(bufs[2], bufs[2])


if True:  
    perfplot.show(
        setup = lambda n : (np.arange(n, dtype = np.object), np.arange(n, dtype=np.int64), np.arange(n, dtype=np.int32)),
        n_range=[2**k for k in range(18)],
        kernels=[
            pyobjectset_from_buffer,
            pyobjectset_add_preallocated,
            int64_add_preallocated,
            int64set_from_buffer,
            int32set_from_buffer,
            ],
        logx=False,
        logy=False,
        xlabel='number of operations',
        title = "pyobject_map vs dict",
        equality_check = None,
        )
