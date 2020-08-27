#
#
# Don't edit it, unless this is I_n_t_6_4_S_e_t implementation
#
# run sh all_from_XXX.sh to create it from blueprint - I_n_t_6_4_S_e_t
#
#

cpdef Int64Set Int64Set_from_buffer(int64_t[:] buf, double size_hint=0.0):
    cdef Py_ssize_t n = len(buf)
    cdef Py_ssize_t at_least_needed = element_n_from_size_hint(<khint_t>n, size_hint)
    res=Int64Set(number_of_elements_hint=at_least_needed)
    cdef Py_ssize_t i
    for i in range(n):
        res.add(buf[i])
    return res
    

cpdef void isin_int64(int64_t[:] query, Int64Set db, uint8_t[:] result) except *:
    cdef size_t i
    cdef size_t n=len(query)
    if n!=len(result):
        raise ValueError("Different sizes for query({n}) and result({m})".format(n=n, m=len(result)))
    for i in range(n):
        result[i]=db is not None and db.contains(query[i])

cpdef bint all_int64(int64_t[:] query, Int64Set db) except *:
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

cpdef bint all_int64_from_iter(object query, Int64Set db) except *:
    if query is None:
        return True
    cdef int64_t el
    for el in query:
        if db is None or not db.contains(el):
            return False
    return True

cpdef bint none_int64(int64_t[:] query, Int64Set db) except *:
    if query is None or db is None:
        return True
    cdef size_t i
    cdef size_t n=len(query)
    for i in range(n):
        if db.contains(query[i]):
            return False
    return True

cpdef bint none_int64_from_iter(object query, Int64Set db) except *:
    if query is None or db is None:
        return True
    cdef int64_t el
    for el in query:
        if db.contains(el):
            return False
    return True

cpdef bint any_int64(int64_t[:] query, Int64Set db) except *:
    return not none_int64(query, db)

cpdef bint any_int64_from_iter(object query, Int64Set db) except *:
    return not none_int64_from_iter(query, db)

cpdef size_t count_if_int64(int64_t[:] query, Int64Set db) except *:
    if query is None or db is None:
        return 0
    cdef size_t i
    cdef size_t n=len(query)
    cdef size_t res=0
    for i in range(n):
        if db.contains(query[i]):
            res+=1
    return res

cpdef size_t count_if_int64_from_iter(object query, Int64Set db) except *:
    if query is None or db is None:
        return 0
    cdef int64_t el
    cdef size_t res=0
    for el in query:
        if db.contains(el):
            res+=1
    return res

cpdef bint aredisjoint_int64(Int64Set a, Int64Set b) except *:
    if a is None or b is None:
        raise TypeError("'NoneType' object is not iterable")

    cdef Int64SetIterator it
    cdef Int64Set s
    cdef int64_t el
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

cpdef bint issubset_int64(Int64Set s, Int64Set sub) except *:
    if s is None or sub is None:
        raise TypeError("'NoneType' object is not iterable")

    if s.size() < sub.size():
        return False

    cdef Int64SetIterator it=sub.get_iter()
    cdef int64_t el
    while it.has_next():
        el = it.next()
        if not s.contains(el):
            return False
    return True

cpdef Int64Set copy_int64(Int64Set s):
    if s is None:
        return None
    cdef Int64Set result = Int64Set(number_of_elements_hint=s.size())
    cdef Int64SetIterator it=s.get_iter()
    cdef int64_t el
    while it.has_next():
        el = it.next()
        result.add(el)
    return result
    
    
   

