#
#
# Don't edit it, unless this is I_n_t_6_4_S_e_t implementation
#
# run sh all_from_XXX.sh to create it from blueprint - I_n_t_6_4_S_e_t
#
#

include "float64set_impl_core.pxi"

cdef class Float64Set:

    def __cinit__(self, iterable=None, *, number_of_elements_hint=None):
        """
        iterable - initial elements in the set
        number_of_elements_hint - number of elements without the need of reallocation.
        """
        self.table = kh_init_float64set()
        if number_of_elements_hint is not None:    
            kh_resize_float64set(self.table, element_n_to_bucket_n(number_of_elements_hint))
        cdef float64_t el
        if iterable is not None:
            for el in iterable:
                self.add(el)

    def __len__(self):
        return self.size()
  
    cdef khint_t size(self):
        return self.table.size
        

    def __dealloc__(self):
        _dealloc_float64(self.table)
        self.table = NULL

    def __contains__(self, float64_t key):
        return self.contains(key)


    cdef bint contains(self, float64_t key) except *:
        return _contains_float64(self.table, key)


    cpdef void add(self, float64_t key) except *:
        _add_float64(self.table, key)

    
    cpdef void discard(self, float64_t key) except *:
        _discard_float64(self.table, key)


    cdef Float64SetIterator get_iter(self):
        return Float64SetIterator(self)

    def __iter__(self):
        return self.get_iter()

    def get_state_info(self):
        return {"n_buckets" : self.table.n_buckets, 
                "n_occupied" : self.table.n_occupied, 
                "upper_bound" : self.table.upper_bound}

    ### drop-in for set:
    def isdisjoint(self, other):
        if isinstance(other, Float64Set):
            return aredisjoint_float64(self, other)
        cdef float64_t el
        for el in other:
            if self.contains(el):
                return False
        return True

    def issuperset(self, other):
        if isinstance(other, Float64Set):
            return issubset_float64(self, other)
        cdef float64_t el
        for el in other:
            if not self.contains(el):
                return False
        return True

    def issubset(self, other):
        if isinstance(other, Float64Set):
            return issubset_float64(other, self)
        cdef float64_t el
        cdef Float64Set mem=Float64Set()
        for el in other:
            if self.contains(el):
                mem.add(el)
        return mem.size()==self.size()

    def __repr__(self):
        return "{"+','.join(map(str, self))+"}"

    def __le__(self, Float64Set other):
        return issubset_float64(other, self)

    def __lt__(self, Float64Set other):
        return issubset_float64(other, self) and self.size()<other.size()

    def __ge__(self, Float64Set other):
        return issubset_float64(self,  other)

    def __gt__(self, Float64Set other):
        return issubset_float64(self, other) and self.size()>other.size()

    def __eq__(self, Float64Set other):
        return issubset_float64(self, other) and self.size()==other.size()

    def __or__(self, Float64Set other):
        cdef Float64Set res = copy_float64(self)
        update_float64(res, other)
        return res

    def __ior__(self, Float64Set other):
        update_float64(self, other)
        return self

    def __and__(self, Float64Set other):
        return intersect_float64(self, other)

    def __iand__(self, Float64Set other):
        cdef Float64Set res = intersect_float64(self, other)
        swap_float64(self, res)
        return self

    def __sub__(self, Float64Set other):
        return difference_float64(self, other)

    def __isub__(self, Float64Set other):
        cdef Float64Set res = difference_float64(self, other)
        swap_float64(self, res)
        return self

    def __xor__(self, Float64Set other):
        return symmetric_difference_float64(self, other)

    def __ixor__(self, Float64Set other):
        cdef Float64Set res = symmetric_difference_float64(self, other)
        swap_float64(self, res)
        return self

    def copy(self):
        return copy_float64(self)

    def union(self, *others):
        cdef Float64Set res = copy_float64(self)
        for o in others:
            res.update(o)
        return res

    def update(self, other):
        if isinstance(other, Float64Set):
            update_float64(self, other)
            return
        cdef float64_t el
        for el in other:
            self.add(el)

    def intersection(self, *others):
        cdef Float64Set res = copy_float64(self)
        for o in others:
            res.intersection_update(o)
        return res

    def intersection_update(self, other):
        cdef Float64Set res 
        cdef float64_t el
        if isinstance(other, Float64Set):
            res = intersect_float64(self, other)
        else:
            res = Float64Set()
            for el in other:
                if self.contains(el):
                    res.add(el)
        swap_float64(self, res)

    def difference_update(self, other):
        cdef Float64Set res 
        cdef float64_t el
        if isinstance(other, Float64Set):
            res = difference_float64(self, other)
            swap_float64(self, res)
        else:
            for el in other:
                self.discard(el)

    def difference(self, *others):
        cdef Float64Set res = copy_float64(self)
        for o in others:
            res.difference_update(o)
        return res

    def symmetric_difference_update(self, other):
        cdef Float64Set res 
        cdef float64_t el
        if isinstance(other, Float64Set):
            res = symmetric_difference_float64(self, other)
        else:
            res = self.copy()
            for el in other:
                if self.contains(el):
                    res.discard(el)
                else:
                    res.add(el)
        swap_float64(self, res)

    def symmetric_difference(self, *others):
        cdef Float64Set res = copy_float64(self)
        for o in others:
            res.symmetric_difference_update(o)
        return res

    def clear(self):
        cdef Float64Set res = Float64Set()
        swap_float64(self, res)

    def remove(self, key):
        cdef size_t old=self.size()
        self.discard(key)
        if old==self.size():
            raise KeyError(key)
        



### Utils:

def Float64Set_from(it):
    res=Float64Set()
    for i in it:
        res.add(i)
    return res

include "float64set_impl_cpdef.pxi"
