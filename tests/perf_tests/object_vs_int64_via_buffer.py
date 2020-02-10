import perfplot
import numpy as np

from cykhash import isin_int64, Int64Set_from, Int64Set_from_buffer, Int64Set
from cykhash import isin_int32, Int32Set_from, Int32Set_from_buffer
from cykhash import isin_float64, Float64Set_from, Float64Set_from_buffer
from cykhash import isin_float32, Float32Set_from, Float32Set_from_buffer
from cykhash import isin_pyobject,  PyObjectSet_from, PyObjectSet_from_buffer, PyObjectSet


def pyobjectset_from_buffer(bufs):
    PyObjectSet_from_buffer(bufs[0])

def pyobjectset_from_iter(bufs):
    PyObjectSet_from(bufs[0])

def pyobjectset_add_preallocated(bufs):
    n = len(bufs[1])
    p = PyObjectSet(int(1.3*n))   
    for i in range(n):
        p.add(i)

def int64set_add_preallocated(bufs):
    n = len(bufs[1])
    p = Int64Set(int(1.3*n))   
    for i in range(n):
        p.add(i)

def int64set_from_buffer(bufs):
    Int64Set_from_buffer(bufs[1])

def int32set_from_buffer(bufs):
    Int32Set_from_buffer(bufs[2])


if True:  
    perfplot.show(
        setup = lambda n : (np.arange(n, dtype = np.object), np.arange(n, dtype=np.int64), np.arange(n, dtype=np.int32)),
        n_range=[2**k for k in range(18)],
        kernels=[
            pyobjectset_from_buffer,
            pyobjectset_from_iter,
            pyobjectset_add_preallocated,
            int64set_add_preallocated,
            int64set_from_buffer,
            int32set_from_buffer,
            ],
        logx=False,
        logy=False,
        xlabel='number of operations',
        title = "pyobject_set vs set",
        equality_check = None,
        )
