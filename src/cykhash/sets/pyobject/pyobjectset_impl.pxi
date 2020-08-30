#
#
# Don't edit it, unless this is I_n_t_6_4_S_e_t implementation
#
# run sh all_from_XXX.sh to create it from blueprint - I_n_t_6_4_S_e_t
#
#

include "pyobjectset_impl_core.pxi"

cdef class PyObjectSet:

    def __cinit__(self, iterable=None, *, number_of_elements_hint=None):
        """
        iterable - initial elements in the set
        number_of_elements_hint - number of elements without the need of reallocation.
        """
        self.table = kh_init_pyobjectset()
        if number_of_elements_hint is not None:    
            kh_resize_pyobjectset(self.table, element_n_to_bucket_n(number_of_elements_hint))
        cdef object el
        if iterable is not None:
            for el in iterable:
                self.add(el)

    def __len__(self):
        return self.size()
  
    cdef khint_t size(self):
        return self.table.size
        

    def __dealloc__(self):
        _dealloc_pyobject(self.table)
        self.table = NULL

    def __contains__(self, object key):
        return self.contains(key)


    cdef bint contains(self, object key) except *:
        return _contains_pyobject(self.table, key)


    cpdef void add(self, object key) except *:
        _add_pyobject(self.table, key)

    
    cpdef void discard(self, object key) except *:
        _discard_pyobject(self.table, key)


    cdef PyObjectSetIterator get_iter(self):
        return PyObjectSetIterator(self)

    def __iter__(self):
        return self.get_iter()

    def get_state_info(self):
        return {"n_buckets" : self.table.n_buckets, 
                "n_occupied" : self.table.n_occupied, 
                "upper_bound" : self.table.upper_bound}

    ### drop-in for set:
    def isdisjoint(self, other):
        if isinstance(other, PyObjectSet):
            return aredisjoint_pyobject(self, other)
        cdef object el
        for el in other:
            if self.contains(el):
                return False
        return True

    def issuperset(self, other):
        if isinstance(other, PyObjectSet):
            return issubset_pyobject(self, other)
        cdef object el
        for el in other:
            if not self.contains(el):
                return False
        return True

    def issubset(self, other):
        if isinstance(other, PyObjectSet):
            return issubset_pyobject(other, self)
        cdef object el
        cdef PyObjectSet mem=PyObjectSet()
        for el in other:
            if self.contains(el):
                mem.add(el)
        return mem.size()==self.size()

    def __repr__(self):
        return "{"+','.join(map(str, self))+"}"

    def __le__(self, PyObjectSet other):
        return issubset_pyobject(other, self)

    def __lt__(self, PyObjectSet other):
        return issubset_pyobject(other, self) and self.size()<other.size()

    def __ge__(self, PyObjectSet other):
        return issubset_pyobject(self,  other)

    def __gt__(self, PyObjectSet other):
        return issubset_pyobject(self, other) and self.size()>other.size()

    def __eq__(self, PyObjectSet other):
        return issubset_pyobject(self, other) and self.size()==other.size()

    def __or__(self, PyObjectSet other):
        cdef PyObjectSet res = copy_pyobject(self)
        update_pyobject(res, other)
        return res

    def __ior__(self, PyObjectSet other):
        update_pyobject(self, other)
        return self

    def __and__(self, PyObjectSet other):
        return intersect_pyobject(self, other)

    def __iand__(self, PyObjectSet other):
        cdef PyObjectSet res = intersect_pyobject(self, other)
        swap_pyobject(self, res)
        return self

    def __sub__(self, PyObjectSet other):
        return difference_pyobject(self, other)

    def __isub__(self, PyObjectSet other):
        cdef PyObjectSet res = difference_pyobject(self, other)
        swap_pyobject(self, res)
        return self

    def __xor__(self, PyObjectSet other):
        return symmetric_difference_pyobject(self, other)

    def __ixor__(self, PyObjectSet other):
        cdef PyObjectSet res = symmetric_difference_pyobject(self, other)
        swap_pyobject(self, res)
        return self

    def copy(self):
        return copy_pyobject(self)

    def union(self, *others):
        cdef PyObjectSet res = copy_pyobject(self)
        for o in others:
            res.update(o)
        return res

    def update(self, other):
        if isinstance(other, PyObjectSet):
            update_pyobject(self, other)
            return
        cdef object el
        for el in other:
            self.add(el)

    def intersection(self, *others):
        cdef PyObjectSet res = copy_pyobject(self)
        for o in others:
            res.intersection_update(o)
        return res

    def intersection_update(self, other):
        cdef PyObjectSet res 
        cdef object el
        if isinstance(other, PyObjectSet):
            res = intersect_pyobject(self, other)
        else:
            res = PyObjectSet()
            for el in other:
                if self.contains(el):
                    res.add(el)
        swap_pyobject(self, res)

    def difference_update(self, other):
        cdef PyObjectSet res 
        cdef object el
        if isinstance(other, PyObjectSet):
            res = difference_pyobject(self, other)
            swap_pyobject(self, res)
        else:
            for el in other:
                self.discard(el)

    def difference(self, *others):
        cdef PyObjectSet res = copy_pyobject(self)
        for o in others:
            res.difference_update(o)
        return res

    def symmetric_difference_update(self, other):
        cdef PyObjectSet res 
        cdef object el
        if isinstance(other, PyObjectSet):
            res = symmetric_difference_pyobject(self, other)
        else:
            res = self.copy()
            for el in other:
                if self.contains(el):
                    res.discard(el)
                else:
                    res.add(el)
        swap_pyobject(self, res)

    def symmetric_difference(self, *others):
        cdef PyObjectSet res = copy_pyobject(self)
        for o in others:
            res.symmetric_difference_update(o)
        return res
        



### Utils:

def PyObjectSet_from(it):
    res=PyObjectSet()
    for i in it:
        res.add(i)
    return res

include "pyobjectset_impl_cpdef.pxi"
