

cdef class Int64Set:

    def __cinit__(self, size_hint=1):
        self.table = kh_init_int64set()
        if size_hint is not None:
            kh_resize_int64set(self.table, size_hint)

    def __len__(self):
        return self.table.size

    def __dealloc__(self):
        if self.table is not NULL:
            kh_destroy_int64set(self.table)
            self.table = NULL

    def __contains__(self, int64_t key):
        return self.contains(key)

    def sizeof(self, deep=False):
        """ return the size of my table in bytes """
        return self.table.n_buckets * (sizeof(int64_t) + # keys
                                       sizeof(size_t) +  # vals
                                       sizeof(uint32_t)) # flags

    cdef contains(self, int64_t key):
        cdef khint_t k
        k = kh_get_int64set(self.table, key)
        return k != self.table.n_buckets


    cpdef add(self, int64_t key):
        cdef:
            khint_t k
            int ret = 0

        k = kh_put_int64set(self.table, key, &ret)
        self.table.keys[k] = key


### Utils:

def Int64Set_from(it):
    res=Int64Set()
    for i in it:
        res.add(i)
    return res
    


from libc.stdint cimport  uint8_t

def isin(int64_t[:] query, Int64Set db, uint8_t[:] result):
    cdef size_t i
    cdef size_t n=len(query)
    for i in range(n):
        if db.contains(query[i]):
            result[i]=1
        else:   
            result[i]=0

