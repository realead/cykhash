cimport numpy as np
import numpy as np

from cykhash.khashsets cimport Int64Set, Int64SetIterator

def unique_int64(np.int64_t[::1] data):
    cdef np.ndarray[dtype=np.int64_t] res
    cdef Int64Set s=Int64Set(len(data))
    cdef Int64SetIterator it
    cdef Py_ssize_t i
    cdef int cnt=0
    for i in range(len(data)):
        s.add(data[i])
    res=np.empty(s.table.size, dtype=np.int64)
    it = s.get_iter()
    for i in range(s.table.size):
        res[cnt]=it.next()
        cnt+=1
    return res



