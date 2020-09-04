from cpython.ref cimport Py_INCREF,Py_DECREF

cdef class PyObjectMap:

    def __cinit__(self, iterable=None, *, number_of_elements_hint=None):
        """
        number_of_elements_hint - number of elements without the need of reallocation.
        """
        self.table = kh_init_pyobjectmap()
        if number_of_elements_hint is not None:
            kh_resize_pyobjectmap(self.table, element_n_to_bucket_n(number_of_elements_hint))
        if iterable is not None:
            for key, val in iterable:
                    self.put_object(key, val)

    def __len__(self):
        return self.size()
  
    cdef khint_t size(self):
        return self.table.size
        

    def __dealloc__(self):
        cdef Py_ssize_t i
        if self.table is not NULL:
            for i in range(self.table.size):
                if kh_exist_pyobjectmap(self.table, i):
                    Py_DECREF(<object>(self.table.keys[i]))
                    Py_DECREF(<object>(self.table.vals[i]))
            kh_destroy_pyobjectmap(self.table)
            self.table = NULL

    def __contains__(self, object key):
        return self.contains(key)


    cdef bint contains(self, object key) except *:
        cdef khint_t k
        k = kh_get_pyobjectmap(self.table, <pyobject_t>key)
        return k != self.table.n_buckets


    cpdef void put_object(self, object key, object val) except *:
        cdef:
            khint_t k
            int ret = 0
        k = kh_put_pyobjectmap(self.table, <pyobject_t>key, &ret)
        if not ret:
            Py_DECREF(<object>(self.table.vals[k]))
        else:
            Py_INCREF(key)
        Py_INCREF(val)
        self.table.vals[k] = <pyobject_t> val

    
    def __setitem__(self, key, val):
        self.put_object(key, val)

    cpdef object get_object(self, object key):
        k = kh_get_pyobjectmap(self.table, <pyobject_t>key)
        if k != self.table.n_buckets:
            return <object>self.table.vals[k]
        else:
            raise KeyError("No such key: "+str(key))

    def __getitem__(self, key):
        return self.get_object(key)

    
    cpdef void discard(self, object key) except *:
        cdef khint_t k
        k = kh_get_pyobjectmap(self.table, <pyobject_t>key)
        if k != self.table.n_buckets:
            Py_DECREF(<object>(self.table.keys[k]))
            Py_DECREF(<object>(self.table.vals[k]))
            kh_del_pyobjectmap(self.table, k)


    cdef PyObjectMapIterator get_iter(self, int view_type):
        return PyObjectMapIterator(self, view_type)

    def clear(self):
        cdef PyObjectMap tmp=PyObjectMap()
        swap_pyobjectmap(self, tmp)

    def keys(self):
        return PyObjectMapView(self, 0)

    def values(self):
        return PyObjectMapView(self, 1)

    def items(self):
        return PyObjectMapView(self, 2)


### Iterator:
cdef class PyObjectMapIterator:

    cdef void __move(self) except *:
        while self.it<self.size and not kh_exist_pyobjectmap(self.parent.table, self.it):
              self.it+=1       

    cdef bint has_next(self) except *:
        return self.it < self.parent.table.n_buckets
        
    cdef pyobject_key_val_pair next(self) except *:
        cdef pyobject_key_val_pair result 
        result.key = self.parent.table.keys[self.it]
        result.val = self.parent.table.vals[self.it]
        self.it+=1#ensure at least one move!
        self.__move()
        return result


    def __cinit__(self, PyObjectMap parent, int view_type):
        self.parent = parent
        self.size = parent.table.n_buckets
        self.view_type = view_type
        #search the start:
        self.it = 0
        self.__move()

    def __next__(self):
        cdef pyobject_key_val_pair pair
        if self.has_next():
            pair = self.next()
            if self.view_type == 0:           # keys
                return <object>pair.key
            if self.view_type == 1:           # vals
                return <object>pair.val
            else:                            # items
                return (<object>pair.key, <object>pair.val)
        else:
            raise StopIteration


cdef class PyObjectMapView:
    cdef PyObjectMapIterator get_iter(self):
        return PyObjectMapIterator(self.parent, self.view_type)  

    def __cinit__(self, PyObjectMap parent, view_type):
        self.parent = parent
        self.view_type = view_type

    def __iter__(self):
        return self.get_iter()

### Utils:

def PyObjectMap_from_object_buffer(object[:] keys, object[:] vals, double size_hint=0.0):
    cdef Py_ssize_t n = len(keys)
    cdef Py_ssize_t b = len(vals)
    if b < n:
        n = b
    cdef Py_ssize_t at_least_needed = element_n_from_size_hint(<khint_t>n, size_hint)
    res=PyObjectMap(number_of_elements_hint=at_least_needed)
    cdef Py_ssize_t i
    for i in range(n):
        res.put_object(keys[i], vals[i])
    return res

cpdef void swap_pyobjectmap(PyObjectMap a, PyObjectMap b) except *:
    if a is None or b is None:
        raise TypeError("'NoneType' object is not iterable")

    cdef kh_pyobjectmap_t *tmp=a.table
    a.table=b.table
    b.table=tmp


    


