#
#
# Don't edit it, unless this is I_n_t_6_4_to_6_4_m_a_p implementation
#
# run sh all_from_XXX.sh to create it from blueprint - I_n_t_6_4_to_6_4_m_a_p
#
#

cdef class Int64to64Map:

    def __cinit__(self, size_hint=1):
        self.table = kh_init_int64to64map()
        if size_hint is not None:
            kh_resize_int64to64map(self.table, size_hint)

    def __len__(self):
        return self.size()
  
    cdef khint_t size(self):
        return self.table.size
        

    def __dealloc__(self):
        if self.table is not NULL:
            kh_destroy_int64to64map(self.table)
            self.table = NULL

    def __contains__(self, int64_t key):
        return self.contains(key)


    cdef bint contains(self, int64_t key) except *:
        cdef khint_t k
        k = kh_get_int64to64map(self.table, key)
        return k != self.table.n_buckets


    cpdef void put_int64(self, int64_t key) except *:
        cdef:
            khint_t k
            int ret = 0

        k = kh_put_int64to64map(self.table, key, &ret)
        self.table.keys[k] = key

    
    cpdef void discard(self, int64_t key) except *:
        cdef khint_t k
        k = kh_get_int64to64map(self.table, key)
        if k != self.table.n_buckets:
            kh_del_int64to64map(self.table, k)


    cdef int64to64mapIterator get_iter(self):
        return int64to64mapIterator(self)

    def __iter__(self):
        return self.get_iter()


### Iterator:
cdef class int64to64mapIterator:

    cdef void __move(self) except *:
        while self.it<self.size and not kh_exist_int64to64map(self.parent.table, self.it):
              self.it+=1       

    cdef bint has_next(self) except *:
        return self.it != self.parent.table.n_buckets
        
    cdef int64_t next(self) except *:
        cdef int64_t result = self.parent.table.keys[self.it]
        self.it+=1#ensure at least one move!
        self.__move()
        return result


    def __cinit__(self, int64to64map parent):
        self.parent = parent
        self.size = parent.table.n_buckets
        #search the start:
        self.it = 0
        self.__move()

    def __next__(self):
        if self.has_next():
            return self.next()
        else:
            raise StopIteration

### Utils:

def int64to64map_from(it):
    res=int64to64map()
    for i in it:
        res.add(i)
    return res

def int64to64map_from_buffer(int64_t[:] buf, double size_hint = 1.25):
    cdef Py_ssize_t n = len(buf)
    cdef Py_ssize_t start_size = <Py_ssize_t>(len(buf)*size_hint)+1
    res=int64to64map(start_size)
    cdef Py_ssize_t i
    for i in range(n):
        res.add(buf[i])
    return res
    


from libc.stdint cimport  uint8_t

def isin_int64(int64_t[:] query, int64to64map db, uint8_t[:] result):
    cdef size_t i
    cdef size_t n=len(query)
    for i in range(n):
        result[i]=db.contains(query[i])


