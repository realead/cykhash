#
#
# Don't edit it, unless this is I_n_t_6_4_S_e_t implementation
#
# run sh all_from_XXX.sh to create it from blueprint - I_n_t_6_4_S_e_t
#
#

include "int32set_impl_core.pxi"

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
        _dealloc_int32(self.table)
        self.table = NULL

    def __contains__(self, int32_t key):
        return self.contains(key)


    cdef bint contains(self, int32_t key) except *:
        return _contains_int32(self.table, key)


    cpdef void add(self, int32_t key) except *:
        _add_int32(self.table, key)

    
    cpdef void discard(self, int32_t key) except *:
        _discard_int32(self.table, key)


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

    def __repr__(self):
        return "{"+','.join(map(str, self))+"}"

    def __le__(self, Int32Set other):
        return issubset_int32(other, self)

    def __lt__(self, Int32Set other):
        return issubset_int32(other, self) and self.size()<other.size()

    def __ge__(self, Int32Set other):
        return issubset_int32(self,  other)

    def __gt__(self, Int32Set other):
        return issubset_int32(self, other) and self.size()>other.size()

    def __eq__(self, Int32Set other):
        return issubset_int32(self, other) and self.size()==other.size()

    def __or__(self, Int32Set other):
        cdef Int32Set res = copy_int32(self)
        update_int32(res, other)
        return res

    def __ior__(self, Int32Set other):
        update_int32(self, other)
        return self

    def __and__(self, Int32Set other):
        return intersect_int32(self, other)

    def __iand__(self, Int32Set other):
        cdef Int32Set res = intersect_int32(self, other)
        swap_int32(self, res)
        return self

    def __sub__(self, Int32Set other):
        return difference_int32(self, other)

    def __isub__(self, Int32Set other):
        cdef Int32Set res = difference_int32(self, other)
        swap_int32(self, res)
        return self

    def __xor__(self, Int32Set other):
        return symmetric_difference_int32(self, other)

    def __ixor__(self, Int32Set other):
        cdef Int32Set res = symmetric_difference_int32(self, other)
        swap_int32(self, res)
        return self

    def copy(self):
        return copy_int32(self)

    def union(self, *others):
        cdef Int32Set res = copy_int32(self)
        for o in others:
            res.update(o)
        return res

    def update(self, other):
        if isinstance(other, Int32Set):
            update_int32(self, other)
            return
        cdef int32_t el
        for el in other:
            self.add(el)

    def intersection(self, *others):
        cdef Int32Set res = copy_int32(self)
        for o in others:
            res.intersection_update(o)
        return res

    def intersection_update(self, other):
        cdef Int32Set res 
        cdef int32_t el
        if isinstance(other, Int32Set):
            res = intersect_int32(self, other)
        else:
            res = Int32Set()
            for el in other:
                if self.contains(el):
                    res.add(el)
        swap_int32(self, res)

    def difference_update(self, other):
        cdef Int32Set res 
        cdef int32_t el
        if isinstance(other, Int32Set):
            res = difference_int32(self, other)
            swap_int32(self, res)
        else:
            for el in other:
                self.discard(el)

    def difference(self, *others):
        cdef Int32Set res = copy_int32(self)
        for o in others:
            res.difference_update(o)
        return res

    def symmetric_difference_update(self, other):
        cdef Int32Set res 
        cdef int32_t el
        if isinstance(other, Int32Set):
            res = symmetric_difference_int32(self, other)
        else:
            res = self.copy()
            for el in other:
                if self.contains(el):
                    res.discard(el)
                else:
                    res.add(el)
        swap_int32(self, res)

    def symmetric_difference(self, *others):
        cdef Int32Set res = copy_int32(self)
        for o in others:
            res.symmetric_difference_update(o)
        return res

    def clear(self):
        cdef Int32Set res = Int32Set()
        swap_int32(self, res)

    def remove(self, key):
        cdef size_t old=self.size()
        self.discard(key)
        if old==self.size():
            raise KeyError(key)

    def pop(self):
        if self.size()== 0:
            raise KeyError("pop from empty set")
        cdef Int32SetIterator it = self.get_iter()
        cdef int32_t el = it.next()
        self.discard(el)
        return el
        



### Utils:

def Int32Set_from(it):
    res=Int32Set()
    for i in it:
        res.add(i)
    return res

include "int32set_impl_cpdef.pxi"
