#
#This is special functionality and isn't created from Int64Set-blueprint
#
#


from cpython.ref cimport Py_INCREF,Py_DECREF

cdef void _dealloc_pyobject(kh_pyobjectset_t *table) except *:
    cdef khint_t i = 0
    if table is not NULL:
        for i in range(table.size):
            if kh_exist_pyobjectset(table, i):
                Py_DECREF(<object>table.keys[i])
        kh_destroy_pyobjectset(table)

cdef bint _contains_pyobject(kh_pyobjectset_t *table, object key) nogil:
        cdef khint_t k
        k = kh_get_pyobjectset(table, <pyobject_t>key)
        return k != table.n_buckets

cdef void _add_pyobject(kh_pyobjectset_t *table, object key) except *:
        cdef:
            khint_t k
            int ret = 0
            pyobject_t key_ptr = <pyobject_t> key
        k = kh_put_pyobjectset(table, key_ptr, &ret)
        if ret: 
            #element was really added, so we need to increase reference
            Py_INCREF(key)

cdef void _discard_pyobject(kh_pyobjectset_t *table, object key) except *:
    cdef khint_t k
    cdef pyobject_t key_ptr = <pyobject_t> key
    k = kh_get_pyobjectset(table, key_ptr)
    if k != table.n_buckets:
        Py_DECREF(<object>table.keys[k])
        kh_del_pyobjectset(table, k)


### Iterator:
cdef class PyObjectSetIterator:

    cdef void __move(self) except *:
        while self.it<self.parent.table.n_buckets and not kh_exist_pyobjectset(self.parent.table, self.it):
              self.it+=1       

    cdef bint has_next(self) except *:
        self.__move()
        return self.it < self.parent.table.n_buckets
        

    # doesn't work if there was change between last has_next() and next() 
    cdef object next(self):
        cdef pyobject_t result = self.parent.table.keys[self.it]
        self.it+=1#ensure at least one move!
        return <object>result


    def __cinit__(self, PyObjectSet parent):
        self.parent = parent
        #search the start:
        self.it = 0
        self.__move()

    def __next__(self):
        if self.has_next():
            return self.next()
        else:
            raise StopIteration

