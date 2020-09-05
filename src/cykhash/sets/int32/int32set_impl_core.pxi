#
#
# Don't edit it, unless this is I_n_t_6_4_S_e_t implementation
#
# run sh all_from_XXX.sh to create it from blueprint - I_n_t_6_4_S_e_t
#
#

cdef void _dealloc_int32(kh_int32set_t *table) nogil:
    if table is not NULL:
        kh_destroy_int32set(table)

cdef bint _contains_int32(kh_int32set_t *table, int32_t key) nogil:
    cdef khint_t k
    k = kh_get_int32set(table, key)
    return k != table.n_buckets

cdef void _add_int32(kh_int32set_t *table, int32_t key) nogil:
    cdef:
        khint_t k
        int ret = 0

    k = kh_put_int32set(table, key, &ret)
    table.keys[k] = key

cdef void _discard_int32(kh_int32set_t *table, int32_t key) nogil:
    cdef khint_t k
    k = kh_get_int32set(table, key)
    if k != table.n_buckets:
        kh_del_int32set(table, k)


### Iterator:
cdef class Int32SetIterator:

    cdef void __move(self) except *:
        while self.it<self.parent.table.n_buckets and not kh_exist_int32set(self.parent.table, self.it):
              self.it+=1       

    cdef bint has_next(self) except *:
        self.__move()
        return self.it < self.parent.table.n_buckets
      
    # doesn't work if there was change between last has_next() and next()  
    cdef int32_t next(self) except *:
        cdef int32_t result = self.parent.table.keys[self.it]
        self.it+=1#ensure at least one move!
        return result


    def __cinit__(self, Int32Set parent):
        self.parent = parent
        #search the start:
        self.it = 0
        self.__move()

    def __next__(self):
        if self.has_next():
            return self.next()
        else:
            raise StopIteration

