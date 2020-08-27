#
#
# Don't edit it, unless this is I_n_t_6_4_S_e_t implementation
#
# run sh all_from_XXX.sh to create it from blueprint - I_n_t_6_4_S_e_t
#
#

include "float32set_impl_core.pxi"

cdef class Float32Set:

    def __cinit__(self, iterable=None, *, number_of_elements_hint=None):
        """
        iterable - initial elements in the set
        number_of_elements_hint - number of elements without the need of reallocation.
        """
        self.table = kh_init_float32set()
        if number_of_elements_hint is not None:    
            kh_resize_float32set(self.table, element_n_to_bucket_n(number_of_elements_hint))
        cdef float32_t el
        if iterable is not None:
            for el in iterable:
                self.add(el)

    def __len__(self):
        return self.size()
  
    cdef khint_t size(self):
        return self.table.size
        

    def __dealloc__(self):
        _dealloc_float32(self.table)
        self.table = NULL

    def __contains__(self, float32_t key):
        return self.contains(key)


    cdef bint contains(self, float32_t key) except *:
        return _contains_float32(self.table, key)


    cpdef void add(self, float32_t key) except *:
        _add_float32(self.table, key)

    
    cpdef void discard(self, float32_t key) except *:
        _discard_float32(self.table, key)


    cdef Float32SetIterator get_iter(self):
        return Float32SetIterator(self)

    def __iter__(self):
        return self.get_iter()

    def get_state_info(self):
        return {"n_buckets" : self.table.n_buckets, 
                "n_occupied" : self.table.n_occupied, 
                "upper_bound" : self.table.upper_bound}

    ### drop-in for set:
    def isdisjoint(self, other):
        if isinstance(other, Float32Set):
            return aredisjoint_float32(self, other)
        cdef float32_t el
        for el in other:
            if self.contains(el):
                return False
        return True

    def issuperset(self, other):
        if isinstance(other, Float32Set):
            return issubset_float32(self, other)
        cdef float32_t el
        for el in other:
            if not self.contains(el):
                return False
        return True

    def issubset(self, other):
        if isinstance(other, Float32Set):
            return issubset_float32(other, self)
        cdef float32_t el
        cdef Float32Set mem=Float32Set()
        for el in other:
            if self.contains(el):
                mem.add(el)
        return mem.size()==self.size()

    def __le__(self, Float32Set other):
        return issubset_float32(other, self)

    def __lt__(self, Float32Set other):
        return issubset_float32(other, self) and self.size()<other.size()

    def __ge__(self, Float32Set other):
        return issubset_float32(self,  other)

    def __gt__(self, Float32Set other):
        return issubset_float32(self, other) and self.size()>other.size()

    def __eq__(self, Float32Set other):
        return issubset_float32(self, other) and self.size()==other.size()


### Utils:

def Float32Set_from(it):
    res=Float32Set()
    for i in it:
        res.add(i)
    return res

include "float32set_impl_cpdef.pxi"
