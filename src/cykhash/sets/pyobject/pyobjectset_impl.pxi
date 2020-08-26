#
#
# Don't edit it, unless this is I_n_t_6_4_S_e_t implementation
#
# run sh all_from_XXX.sh to create it from bluepring - I_n_t_6_4_S_e_t
#
#
from cpython.ref cimport Py_INCREF,Py_DECREF

cdef class PyObjectSet:

    def __cinit__(self, iterable=None,  *, number_of_elements_hint=None):
        """
        iterable - initial elements in the set
        number_of_elements_hint - number of elements without the need of reallocation.
        """
        self.table = kh_init_pyobjectset()
        if number_of_elements_hint is not None:
            kh_resize_pyobjectset(self.table, element_n_to_bucket_n(number_of_elements_hint))
        if iterable is not None:
            for el in iterable:
                self.add(el)

    def __len__(self):
        return self.size()
  
    cdef khint_t size(self):
        return self.table.size
        

    def __dealloc__(self):
        cdef khint_t i = 0
        if self.table is not NULL:
            for i in range(self.table.size):
                if kh_exist_pyobjectset(self.table, i):
                    Py_DECREF(<object>self.table.keys[i])
            kh_destroy_pyobjectset(self.table)
            self.table = NULL

    def __contains__(self, object key):
        return self.contains(key)


    cdef bint contains(self, object key) except *:
        cdef khint_t k
        k = kh_get_pyobjectset(self.table, <pyobject_t>key)
        return k != self.table.n_buckets


    cpdef void add(self, object key) except *:
        cdef:
            khint_t k
            int ret = 0
            pyobject_t key_ptr = <pyobject_t> key
        k = kh_put_pyobjectset(self.table, key_ptr, &ret)
        if ret: 
            #element was really added, so we need to increase reference
            Py_INCREF(key)

    
    cpdef void discard(self, object key) except *:
        cdef khint_t k
        cdef pyobject_t key_ptr = <pyobject_t> key
        k = kh_get_pyobjectset(self.table, key_ptr)
        if k != self.table.n_buckets:
            Py_DECREF(<object>self.table.keys[k])
            kh_del_pyobjectset(self.table, k)


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
        if isinstance(other, Int64Set):
            return aredisjoint_pyobject(self, other)
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


### Iterator:
cdef class PyObjectSetIterator:

    cdef void __move(self) except *:
        while self.it<self.size and not kh_exist_pyobjectset(self.parent.table, self.it):
              self.it+=1       

    cdef bint has_next(self) except *:
        return self.it != self.parent.table.n_buckets
        
    cdef object next(self):
        cdef pyobject_t result = self.parent.table.keys[self.it]
        self.it+=1#ensure at least one move!
        self.__move()
        return <object>result


    def __cinit__(self, PyObjectSet parent):
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

def PyObjectSet_from(it):
    res=PyObjectSet()
    for i in it:
        res.add(i)
    return res
    

include "pyobjectset_impl_cpdef.pxi"
