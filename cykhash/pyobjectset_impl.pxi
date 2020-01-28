#
#
# Don't edit it, unless this is I_n_t_6_4_S_e_t implementation
#
# run sh all_from_XXX.sh to create it from bluepring - I_n_t_6_4_S_e_t
#
#
from cpython.ref cimport Py_INCREF,Py_DECREF

cdef class PyObjectSet:

    def __cinit__(self, size_hint=1):
        self.table = kh_init_pyobjectset()
        if size_hint is not None:
            kh_resize_pyobjectset(self.table, size_hint)

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
    


from libc.stdint cimport  uint8_t

def isin_pyobject(object[:] query, PyObjectSet db, uint8_t[:] result):
    cdef size_t i
    cdef size_t n=len(query)
    for i in range(n):
        result[i]=db.contains(query[i])


