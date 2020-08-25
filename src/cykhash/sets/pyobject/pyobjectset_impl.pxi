#
#
# Don't edit it, unless this is I_n_t_6_4_S_e_t implementation
#
# run sh all_from_XXX.sh to create it from bluepring - I_n_t_6_4_S_e_t
#
#
from cpython.ref cimport Py_INCREF,Py_DECREF

cdef class PyObjectSet:

    def __cinit__(self,  *, number_of_elements_hint=None):
        """
        number_of_elements_hint - number of elements without the need of reallocation.
        """
        self.table = kh_init_pyobjectset()
        if number_of_elements_hint is not None:
            kh_resize_pyobjectset(self.table, element_n_to_bucket_n(number_of_elements_hint))

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
    
cpdef PyObjectSet PyObjectSet_from_buffer(object[:] buf, double size_hint=0.0):
    cdef Py_ssize_t n = len(buf)
    cdef Py_ssize_t at_least_needed = element_n_from_size_hint(<khint_t>n, size_hint)
    res=PyObjectSet(number_of_elements_hint=at_least_needed)
    cdef Py_ssize_t i
    for i in range(n):
        res.add(buf[i])
    return res


cpdef void  isin_pyobject(object[:] query, PyObjectSet db, uint8_t[:] result) except *:
    cdef size_t i
    cdef size_t n=len(query)
    if n!=len(result):
        raise ValueError("Different sizes for query({n}) and result({m})".format(n=n, m=len(result)))
    for i in range(n):
        result[i]=db is not None and db.contains(query[i])

cpdef bint all_pyobject(object[:] query, PyObjectSet db) except *:
    if query is None:
        return True
    cdef size_t i
    cdef size_t n=len(query)
    if db is None:
        return n==0
    for i in range(n):
        if not db.contains(query[i]):
            return False
    return True

cpdef bint all_pyobject_from_iter(object query, PyObjectSet db) except *:
    if query is None:
        return True
    cdef object el
    for el in query:
        if db is None or not db.contains(el):
            return False
    return True

cpdef bint none_pyobject(object[:] query, PyObjectSet db) except *:
    if query is None or db is None:
        return True
    cdef size_t i
    cdef size_t n=len(query)
    for i in range(n):
        if db.contains(query[i]):
            return False
    return True

cpdef bint none_pyobject_from_iter(object query, PyObjectSet db) except *:
    if query is None or db is None:
        return True
    cdef object el
    for el in query:
        if db.contains(el):
            return False
    return True


cpdef bint any_pyobject(object[:] query, PyObjectSet db) except *:
    return not none_pyobject(query, db)

cpdef bint any_pyobject_from_iter(object query, PyObjectSet db) except *:
    return not none_pyobject_from_iter(query, db)

cpdef size_t count_if_pyobject(object[:] query, PyObjectSet db) except *:
    if query is None or db is None:
        return 0
    cdef size_t i
    cdef size_t n=len(query)
    cdef size_t res=0
    for i in range(n):
        if db.contains(query[i]):
            res+=1
    return res

cpdef size_t count_if_pyobject_from_iter(object query, PyObjectSet db) except *:
    if query is None or db is None:
        return 0
    cdef object el
    cdef size_t res=0
    for el in query:
        if db.contains(el):
            res+=1
    return res
