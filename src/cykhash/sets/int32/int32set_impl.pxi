#
#
# Don't edit it, unless this is I_n_t_6_4_S_e_t implementation
#
# run sh all_from_XXX.sh to create it from blueprint - I_n_t_6_4_S_e_t
#
#

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
        if self.table is not NULL:
            kh_destroy_int32set(self.table)
            self.table = NULL

    def __contains__(self, int32_t key):
        return self.contains(key)


    cdef bint contains(self, int32_t key) except *:
        cdef khint_t k
        k = kh_get_int32set(self.table, key)
        return k != self.table.n_buckets


    cpdef void add(self, int32_t key) except *:
        cdef:
            khint_t k
            int ret = 0

        k = kh_put_int32set(self.table, key, &ret)
        self.table.keys[k] = key

    
    cpdef void discard(self, int32_t key) except *:
        cdef khint_t k
        k = kh_get_int32set(self.table, key)
        if k != self.table.n_buckets:
            kh_del_int32set(self.table, k)


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



### Iterator:
cdef class Int32SetIterator:

    cdef void __move(self) except *:
        while self.it<self.size and not kh_exist_int32set(self.parent.table, self.it):
              self.it+=1       

    cdef bint has_next(self) except *:
        return self.it != self.parent.table.n_buckets
        
    cdef int32_t next(self) except *:
        cdef int32_t result = self.parent.table.keys[self.it]
        self.it+=1#ensure at least one move!
        self.__move()
        return result


    def __cinit__(self, Int32Set parent):
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

def Int32Set_from(it):
    res=Int32Set()
    for i in it:
        res.add(i)
    return res

cpdef Int32Set Int32Set_from_buffer(int32_t[:] buf, double size_hint=0.0):
    cdef Py_ssize_t n = len(buf)
    cdef Py_ssize_t at_least_needed = element_n_from_size_hint(<khint_t>n, size_hint)
    res=Int32Set(number_of_elements_hint=at_least_needed)
    cdef Py_ssize_t i
    for i in range(n):
        res.add(buf[i])
    return res
    

cpdef void isin_int32(int32_t[:] query, Int32Set db, uint8_t[:] result) except *:
    cdef size_t i
    cdef size_t n=len(query)
    if n!=len(result):
        raise ValueError("Different sizes for query({n}) and result({m})".format(n=n, m=len(result)))
    for i in range(n):
        result[i]=db is not None and db.contains(query[i])

cpdef bint all_int32(int32_t[:] query, Int32Set db) except *:
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

cpdef bint all_int32_from_iter(object query, Int32Set db) except *:
    if query is None:
        return True
    cdef int32_t el
    for el in query:
        if db is None or not db.contains(el):
            return False
    return True

cpdef bint none_int32(int32_t[:] query, Int32Set db) except *:
    if query is None or db is None:
        return True
    cdef size_t i
    cdef size_t n=len(query)
    for i in range(n):
        if db.contains(query[i]):
            return False
    return True

cpdef bint none_int32_from_iter(object query, Int32Set db) except *:
    if query is None or db is None:
        return True
    cdef int32_t el
    for el in query:
        if db.contains(el):
            return False
    return True

cpdef bint any_int32(int32_t[:] query, Int32Set db) except *:
    return not none_int32(query, db)

cpdef bint any_int32_from_iter(object query, Int32Set db) except *:
    return not none_int32_from_iter(query, db)

cpdef size_t count_if_int32(int32_t[:] query, Int32Set db) except *:
    if query is None or db is None:
        return 0
    cdef size_t i
    cdef size_t n=len(query)
    cdef size_t res=0
    for i in range(n):
        if db.contains(query[i]):
            res+=1
    return res

cpdef size_t count_if_int32_from_iter(object query, Int32Set db) except *:
    if query is None or db is None:
        return 0
    cdef int32_t el
    cdef size_t res=0
    for el in query:
        if db.contains(el):
            res+=1
    return res

cpdef bint aredisjoint_int32(Int32Set a, Int32Set b) except *:
    if a is None or b is None:
        raise TypeError("'NoneType' object is not iterable")

    cdef Int32SetIterator it
    cdef Int32Set s
    cdef int32_t el
    if a.size()<b.size():
        it=a.get_iter()
        s =b
    else:
        it=b.get_iter()
        s =a
    while it.has_next():
        el = it.next()
        if s.contains(el):
            return False
    return True
    
   

