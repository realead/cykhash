#
#
# Don't edit it, unless this is I_n_t_6_4_S_e_t implementation
#
# run sh all_from_XXX.sh to create it from blueprint - I_n_t_6_4_S_e_t
#
#

cdef class Int32Set:

    def __cinit__(self, iterable=None, *, number_of_elements_hint=None):
        """
        iterable - initial elements in the set
        number_of_elements_hint - number of elements without the need of reallocation.
        """
        self.table = kh_init_int32set()
        if number_of_elements_hint is not None:    
            kh_resize_int32set(self.table, element_n_to_bucket_n(number_of_elements_hint))
        cdef int32_t el
        if iterable is not None:
            for el in iterable:
                self.add(el)

    def __len__(self):
        return self.size()
  
    cdef khint_t size(self):
        return self.table.size
        

    def __dealloc__(self):
        if self.table is not NULL:
            kh_destroy_int32set(self.table)
            self.table = NULL

    def __contains__(self, int32_t key):
        return self.contains(key)


    cdef bint contains(self, int32_t key) except *:
        cdef khint_t k
        k = kh_get_int32set(self.table, key)
        return k != self.table.n_buckets


    cpdef void add(self, int32_t key) except *:
        cdef:
            khint_t k
            int ret = 0

        k = kh_put_int32set(self.table, key, &ret)
        self.table.keys[k] = key

    
    cpdef void discard(self, int32_t key) except *:
        cdef khint_t k
        k = kh_get_int32set(self.table, key)
        if k != self.table.n_buckets:
            kh_del_int32set(self.table, k)


    cdef Int32SetIterator get_iter(self):
        return Int32SetIterator(self)

    def __iter__(self):
        return self.get_iter()

    def get_state_info(self):
        return {"n_buckets" : self.table.n_buckets, 
                "n_occupied" : self.table.n_occupied, 
                "upper_bound" : self.table.upper_bound}

    ### drop-in for set:
    def isdisjoint(self, other):
        if isinstance(other, Int32Set):
            return aredisjoint_int32(self, other)
        cdef int32_t el
        for el in other:
            if self.contains(el):
                return False
        return True

    def issuperset(self, other):
        if isinstance(other, Int32Set):
            return issubset_int32(self, other)
        cdef int32_t el
        for el in other:
            if not self.contains(el):
                return False
        return True

    def issubset(self, other):
        if isinstance(other, Int32Set):
            return issubset_int32(other, self)
        cdef int32_t el
        cdef Int32Set mem=Int32Set()
        for el in other:
            if self.contains(el):
                mem.add(el)
        return mem.size()==self.size()

    def __le__(self, Int32Set other):
        return issubset_int32(other, self)

    def __lt__(self, Int32Set other):
        return issubset_int32(other, self) and self.size()<other.size()

    def __ge__(self, Int32Set other):
        return issubset_int32(self,  other)

    def __gt__(self, Int32Set other):
        return issubset_int32(self, other) and self.size()>other.size()



### Iterator:
cdef class Int32SetIterator:

    cdef void __move(self) except *:
        while self.it<self.size and not kh_exist_int32set(self.parent.table, self.it):
              self.it+=1       

    cdef bint has_next(self) except *:
        return self.it != self.parent.table.n_buckets
        
    cdef int32_t next(self) except *:
        cdef int32_t result = self.parent.table.keys[self.it]
        self.it+=1#ensure at least one move!
        self.__move()
        return result


    def __cinit__(self, Int32Set parent):
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

def Int32Set_from(it):
    res=Int32Set()
    for i in it:
        res.add(i)
    return res

include "int32set_impl_cpdef.pxi"
