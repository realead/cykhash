#
#
# Don't edit it, unless this is I_n_t_6_4_S_e_t implementation
#
# run sh all_from_XXX.sh to create it from blueprint - I_n_t_6_4_S_e_t
#
#

include "int64set_impl_core.pxi"

cdef class Int64Set:

    def __cinit__(self, iterable=None, *, number_of_elements_hint=None):
        """
        iterable - initial elements in the set
        number_of_elements_hint - number of elements without the need of reallocation.
        """
        self.table = kh_init_int64set()
        if number_of_elements_hint is not None:    
            kh_resize_int64set(self.table, element_n_to_bucket_n(number_of_elements_hint))
        cdef int64_t el
        if iterable is not None:
            for el in iterable:
                self.add(el)

    def __len__(self):
        return self.size()
  
    cdef khint_t size(self):
        return self.table.size
        

    def __dealloc__(self):
        _dealloc_int64(self.table)
        self.table = NULL

    def __contains__(self, int64_t key):
        return self.contains(key)


    cdef bint contains(self, int64_t key) except *:
        return _contains_int64(self.table, key)


    cpdef void add(self, int64_t key) except *:
        _add_int64(self.table, key)

    
    cpdef void discard(self, int64_t key) except *:
        _discard_int64(self.table, key)


    cdef Int64SetIterator get_iter(self):
        return Int64SetIterator(self)

    def __iter__(self):
        return self.get_iter()

    def get_state_info(self):
        return {"n_buckets" : self.table.n_buckets, 
                "n_occupied" : self.table.n_occupied, 
                "upper_bound" : self.table.upper_bound}

    ### drop-in for set:
    def isdisjoint(self, other):
        if isinstance(other, Int64Set):
            return aredisjoint_int64(self, other)
        cdef int64_t el
        for el in other:
            if self.contains(el):
                return False
        return True

    def issuperset(self, other):
        if isinstance(other, Int64Set):
            return issubset_int64(self, other)
        cdef int64_t el
        for el in other:
            if not self.contains(el):
                return False
        return True

    def issubset(self, other):
        if isinstance(other, Int64Set):
            return issubset_int64(other, self)
        cdef int64_t el
        cdef Int64Set mem=Int64Set()
        for el in other:
            if self.contains(el):
                mem.add(el)
        return mem.size()==self.size()

    def __le__(self, Int64Set other):
        return issubset_int64(other, self)

    def __lt__(self, Int64Set other):
        return issubset_int64(other, self) and self.size()<other.size()

    def __ge__(self, Int64Set other):
        return issubset_int64(self,  other)

    def __gt__(self, Int64Set other):
        return issubset_int64(self, other) and self.size()>other.size()

    def __eq__(self, Int64Set other):
        return issubset_int64(self, other) and self.size()==other.size()

    def __or__(self, Int64Set other):
        cdef Int64Set res = copy_int64(self)
        update_int64(res, other)
        return res

    def __ior__(self, Int64Set other):
        update_int64(self, other)
        return self

    def union(self, *others):
        cdef Int64Set res = copy_int64(self)
        for o in others:
            res.update(o)
        return res

    def copy(self):
        return copy_int64(self)

    def update(self, other):
        if isinstance(other, Int64Set):
            update_int64(self, other)
            return
        cdef int64_t el
        for el in other:
            self.add(el)



### Utils:

def Int64Set_from(it):
    res=Int64Set()
    for i in it:
        res.add(i)
    return res

include "int64set_impl_cpdef.pxi"
