#
#
# Don't edit it, unless this is I_n_t_6_4_S_e_t implementation
#
# run sh all_from_XXX.sh to create it from blueprint - I_n_t_6_4_S_e_t
#
#

cdef void _dealloc_int64(kh_int64set_t *table) nogil:
    if table is not NULL:
        kh_destroy_int64set(table)

cdef bint _contains_int64(kh_int64set_t *table, int64_t key) nogil:
    cdef khint_t k
    k = kh_get_int64set(table, key)
    return k != table.n_buckets

cdef void _add_int64(kh_int64set_t *table, int64_t key) nogil:
    cdef:
        khint_t k
        int ret = 0

    k = kh_put_int64set(table, key, &ret)
    table.keys[k] = key

cdef void _discard_int64(kh_int64set_t *table, int64_t key) nogil:
    cdef khint_t k
    k = kh_get_int64set(table, key)
    if k != table.n_buckets:
        kh_del_int64set(table, k)


### Iterator:
cdef class Int64SetIterator:

    cdef void __move(self) except *:
        while self.it<self.size and not kh_exist_int64set(self.parent.table, self.it):
              self.it+=1       

    cdef bint has_next(self) except *:
        return self.it < self.parent.table.n_buckets
        
    cdef int64_t next(self) except *:
        cdef int64_t result = self.parent.table.keys[self.it]
        self.it+=1#ensure at least one move!
        self.__move()
        return result


    def __cinit__(self, Int64Set parent):
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

