#
#
# Don't edit it, unless this is I_n_t_6_4_to_6_4_m_a_p implementation
#
# run sh all_from_XXX.sh to create it from blueprint - I_n_t_6_4_to_6_4_m_a_p
#
#

cdef class Int64to64Map:
    @classmethod
    def fromkeys(cls, iterable, value, for_int=True):
        return Int64to64Map(((key, value) for key in iterable), for_int=for_int)

    def __cinit__(self, iterable=None, *, number_of_elements_hint=None, for_int=True):
        """
        number_of_elements_hint - number of elements without the need of reallocation.
        for_int  if True, __setitem__/__getitem__ sets/gets a in64-object, otherwise a float64-object
        """
        self.for_int = for_int
        self.table = kh_init_int64to64map()
        if number_of_elements_hint is not None:
            kh_resize_int64to64map(self.table, element_n_to_bucket_n(number_of_elements_hint))
        cdef key_int64_t key
        cdef int64_t val_as_int
        cdef float64_t val_as_float
        if iterable is not None:
            if for_int:
                for key, val_as_int in iterable:
                    self.put_int64(key, val_as_int)
            else:
                for key, val_as_float in iterable:
                    self.put_float64(key, val_as_float)

    def __len__(self):
        return self.size()
  
    cdef khint_t size(self):
        return self.table.size
        

    def __dealloc__(self):
        if self.table is not NULL:
            kh_destroy_int64to64map(self.table)
            self.table = NULL

    def __contains__(self, key_int64_t key):
        return self.contains(key)


    cdef bint contains(self, key_int64_t key) except *:
        cdef khint_t k
        k = kh_get_int64to64map(self.table, key)
        return k != self.table.n_buckets


    cpdef void put_int64(self, key_int64_t key, int64_t val) except *:
        cdef:
            khint_t k
            int ret = 0

        k = kh_put_int64to64map(self.table, key, &ret)
        self.table.keys[k] = key
        self.table.vals[k] = val

    cpdef void put_float64(self, key_int64_t key, float64_t val) except *:
        self.put_int64(key, f64_to_i64(val));

    
    def __setitem__(self, key, val):
        if self.for_int:
            self.put_int64(key, val)
        else:
            self.put_float64(key, val)

    cpdef int64_t get_int64(self, key_int64_t key) except *:
        k = kh_get_int64to64map(self.table, key)
        if k != self.table.n_buckets:
            return self.table.vals[k]
        else:
            raise KeyError(key)

    cpdef float64_t get_float64(self, key_int64_t key) except *:
        return i64_to_f64(self.get_int64(key))
  
    cpdef void discard(self, key_int64_t key) except *:
        cdef khint_t k
        k = kh_get_int64to64map(self.table, key)
        if k != self.table.n_buckets:
            kh_del_int64to64map(self.table, k)

    cdef Int64to64MapIterator get_iter(self, int view_type):
        return Int64to64MapIterator(self, view_type)

    def clear(self):
        cdef Int64to64Map tmp=Int64to64Map()
        swap_int64map(self, tmp)

    def copy(self):
        return copy_int64map(self)

    def update(self, other):
        if isinstance(other, Int64to64Map):
            update_int64map(self, other)
            return
        for key,val in other:
            self[key]=val

    def setdefault(self, key, default):
        try:
            return self[key]
        except KeyError:
            self[key]=default
            return default

    def get(self, *args, **kwargs):
        if len(args)==0:
            raise TypeError("get() expected at least 1 arguments, got 0")
        if len(args)>2:
            raise TypeError("get() expected at most 2 arguments, got {0}".format(len(args)))
        if kwargs:
            raise TypeError("get() takes no keyword arguments")
        key = args[0]
        try:
            return self[key]
        except KeyError:
            if len(args)==1:
                return None
            return args[1]

    def pop(self, *args, **kwargs):
        if len(args)==0:
            raise TypeError("pop() expected at least 1 arguments, got 0")
        if len(args)>2:
            raise TypeError("pop() expected at most 2 arguments, got {0}".format(len(args)))
        if kwargs:
            raise TypeError("pop() takes no keyword arguments")
        key = args[0]
        try:
            val = self[key]
        except KeyError as e:
            if len(args)==1:
                raise e from None
            return args[1]
        del self[key]
        return val

    def popitem(self):
        if self.size()== 0:
            raise KeyError("popitem(): dictionary is empty")
        key = next(iter(self))
        val = self.pop(key)
        return (key, val)

    def keys(self):
        return Int64to64MapView(self, 0)

    def values(self):
        return Int64to64MapView(self, 1)

    def items(self):
        return Int64to64MapView(self, 2)

    def __iter__(self):
        return iter(self.keys())

    def __getitem__(self, key):
        if self.for_int:
            return self.get_int64(key)
        else:
            return self.get_float64(key)

    def __delitem__(self, key):
        cdef size_t old=self.size()
        self.discard(key)
        if old==self.size():
            raise KeyError(key)

    def __eq__(self, other):
        return are_equal_int64map(self,other)


### Iterator:
cdef class Int64to64MapIterator:

    cdef void __move(self) except *:
        while self.it<self.parent.table.n_buckets and not kh_exist_int64to64map(self.parent.table, self.it):
              self.it+=1       

    cdef bint has_next(self) except *:
        self.__move()
        return self.it < self.parent.table.n_buckets
      
    # doesn't work if there was change between last has_next() and next()       
    cdef int64to64_key_val_pair next(self) except *:
        cdef int64to64_key_val_pair result 
        result.key = self.parent.table.keys[self.it]
        result.val = self.parent.table.vals[self.it]
        self.it+=1#ensure at least one move!
        return result

    def __cinit__(self, Int64to64Map parent, view_type):
        self.parent = parent
        self.view_type = view_type
        #search the start:
        self.it = 0
        self.__move()

    def __next__(self):
        cdef int64to64_key_val_pair pair
        if self.has_next():
            pair=self.next()
            if self.view_type == 0:           # keys
                return pair.key
            if self.view_type == 1:           # vals
                if self.parent.for_int:
                    return pair.val
                else:
                    i64_to_f64(pair.val)
            else:                        # items
                if self.parent.for_int:
                    return (pair.key, pair.val)
                else:
                    return (pair.key, i64_to_f64(pair.val))
        else:
            raise StopIteration


cdef class Int64to64MapView:
    cdef Int64to64MapIterator get_iter(self):
        return Int64to64MapIterator(self.parent, self.view_type)  

    def __cinit__(self, Int64to64Map parent, view_type):
        self.parent = parent
        self.view_type = view_type

    def __iter__(self):
        return self.get_iter()

    def __len__(self):
        return self.parent.size()

    def __contains__(self, x):
        for y in self:
            if x==y:
                return True
        return False



### Utils:

cpdef Int64to64Map Int64to64Map_from_int64_buffer(key_int64_t[:] keys, int64_t[:] vals, double size_hint=0.0):
    cdef Py_ssize_t n = len(keys)
    cdef Py_ssize_t b = len(vals)
    if b < n:
        n = b
    cdef Py_ssize_t at_least_needed = element_n_from_size_hint(<khint_t>n, size_hint)
    res=Int64to64Map(number_of_elements_hint=at_least_needed, for_int=True)
    cdef Py_ssize_t i
    for i in range(n):
        res.put_int64(keys[i], vals[i])
    return res

cpdef Int64to64Map Int64to64Map_from_float64_buffer(key_int64_t[:] keys, float64_t[:] vals,double size_hint=0.0):
    cdef Py_ssize_t n = len(keys)
    cdef Py_ssize_t b = len(vals)
    if b < n:
        n = b
    cdef Py_ssize_t at_least_needed = element_n_from_size_hint(<khint_t>n, size_hint)
    res=Int64to64Map(number_of_elements_hint=at_least_needed, for_int=False)
    cdef Py_ssize_t i
    for i in range(n):
        res.put_float64(keys[i], vals[i])
    return res


cpdef size_t Int64to64Map_to_int64(Int64to64Map map, key_int64_t[:] keys, int64_t[:] vals, bint stop_at_unknown=True, int64_t default_value=0) except *:
    """returns number of found keys"""
    if map is None:
        raise TypeError("'NoneType' is not a map")
    if not map.for_int:
        raise TypeError("Map is not for ints")
    cdef size_t n = len(keys)
    if n != len(vals):
        raise ValueError("Different lengths of keys and vals arrays")
    cdef size_t i
    cdef khint_t k
    cdef size_t res = 0
    for i in range(n):
        k = kh_get_int64to64map(map.table, keys[i])
        if k != map.table.n_buckets:
            vals[i] = map.table.vals[k]
            res += 1
        else:
            vals[i] = default_value
            if stop_at_unknown:
                return res
    return res


cpdef size_t Int64to64Map_to_float64(Int64to64Map map, key_int64_t[:] keys, float64_t[:] vals, bint stop_at_unknown=True, float64_t default_value=float("nan")) except *:
    """returns number of found keys"""
    if map is None:
        raise TypeError("'NoneType' is not a map")
    if map.for_int:
        raise TypeError("Map is not for floats")
    cdef size_t n = len(keys)
    if n != len(vals):
        raise ValueError("Different lengths of keys and vals arrays")
    cdef size_t i
    cdef khint_t k
    cdef size_t res = 0
    for i in range(n):
        k = kh_get_int64to64map(map.table, keys[i])
        if k != map.table.n_buckets:
            vals[i] = i64_to_f64(map.table.vals[k])
            res += 1
        else:
            vals[i] = default_value
            if stop_at_unknown:
                return res
    return res
   

cpdef void swap_int64map(Int64to64Map a, Int64to64Map b) except *:
    if a is None or b is None:
        raise TypeError("'NoneType' object is not iterable")

    cdef kh_int64to64map_t *tmp=a.table
    a.table=b.table
    b.table=tmp

    cdef bint tmp_for_int=a.for_int
    a.for_int=b.for_int
    b.for_int=tmp_for_int


cpdef Int64to64Map copy_int64map(Int64to64Map s):
    if s is None:
        return None
    cdef Int64to64Map result = Int64to64Map(number_of_elements_hint=s.size(), for_int=s.for_int)
    cdef Int64to64MapIterator it=s.get_iter(2)
    cdef int64to64_key_val_pair p
    while it.has_next():
        p = it.next()
        result.put_int64(p.key, p.val)
    return result

cpdef bint are_equal_int64map(Int64to64Map a, Int64to64Map b) except *:
    if a is None or b is None:
        raise TypeError("'NoneType' object is not iterable")
    if a.for_int!=b.for_int:
        return False
    if a.size()!=b.size():
        return False
    cdef Int64to64MapIterator it=a.get_iter(2)
    cdef int64to64_key_val_pair p
    while it.has_next():
        p = it.next()
        if not b.contains(p.key):
            return False
    return True

cpdef void update_int64map(Int64to64Map a, Int64to64Map b) except *:
    if a is None or b is None:
        raise TypeError("'NoneType' object is not iterable")
    cdef Int64to64MapIterator it=b.get_iter(2)
    cdef int64to64_key_val_pair p
    while it.has_next():
        p = it.next()
        a.put_int64(p.key, p.val)



