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


### Utils:

def PyObjectSet_from(it):
    res=PyObjectSet()
    for i in it:
        res.add(i)
    return res

include "pyobjectset_impl_cpdef.pxi"
