#
#
# Don't edit it, unless this is I_n_t_6_4_S_e_t implementation
#
# run sh all_from_XXX.sh to create it from bluepring - I_n_t_6_4_S_e_t
#
#

cdef class Float64Set:

    def __cinit__(self, size_hint=1):
        self.table = kh_init_float64set()
        if size_hint is not None:
            kh_resize_float64set(self.table, size_hint)

    def __len__(self):
        return self.size()
  
    cdef khint_t size(self):
        return self.table.size
        

    def __dealloc__(self):
        if self.table is not NULL:
            kh_destroy_float64set(self.table)
            self.table = NULL

    def __contains__(self, float64_t key):
        return self.contains(key)


    cdef bint contains(self, float64_t key) except *:
        cdef khint_t k
        k = kh_get_float64set(self.table, key)
        return k != self.table.n_buckets


    cpdef void add(self, float64_t key) except *:
        cdef:
            khint_t k
            int ret = 0

        k = kh_put_float64set(self.table, key, &ret)
        self.table.keys[k] = key

    
    cpdef void discard(self, float64_t key) except *:
        cdef khint_t k
        k = kh_get_float64set(self.table, key)
        if k != self.table.n_buckets:
            kh_del_float64set(self.table, k)


    cdef Float64SetIterator get_iter(self):
        return Float64SetIterator(self)

    def __iter__(self):
        return self.get_iter()


### Iterator:
cdef class Float64SetIterator:

    cdef void __move(self) except *:
        while self.it<self.size and not kh_exist_float64set(self.parent.table, self.it):
              self.it+=1       

    cdef bint has_next(self) except *:
        return self.it != self.parent.table.n_buckets
        
    cdef float64_t next(self) except *:
        cdef float64_t result = self.parent.table.keys[self.it]
        self.it+=1#ensure at least one move!
        self.__move()
        return result


    def __cinit__(self, Float64Set parent):
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

def Float64Set_from(it):
    res=Float64Set()
    for i in it:
        res.add(i)
    return res
    


from libc.stdint cimport  uint8_t

def isin_float64(float64_t[:] query, Float64Set db, uint8_t[:] result):
    cdef size_t i
    cdef size_t n=len(query)
    for i in range(n):
        result[i]=db.contains(query[i])


