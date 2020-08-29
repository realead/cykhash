#
#
# Don't edit it, unless this is I_n_t_6_4_S_e_t implementation
#
# run sh all_from_XXX.sh to create it from blueprint - I_n_t_6_4_S_e_t
#
#

cpdef PyObjectSet PyObjectSet_from_buffer(object[:] buf, double size_hint=0.0):
    cdef Py_ssize_t n = len(buf)
    cdef Py_ssize_t at_least_needed = element_n_from_size_hint(<khint_t>n, size_hint)
    res=PyObjectSet(number_of_elements_hint=at_least_needed)
    cdef Py_ssize_t i
    for i in range(n):
        res.add(buf[i])
    return res
    

cpdef void isin_pyobject(object[:] query, PyObjectSet db, uint8_t[:] result) except *:
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

cpdef bint aredisjoint_pyobject(PyObjectSet a, PyObjectSet b) except *:
    if a is None or b is None:
        raise TypeError("'NoneType' object is not iterable")

    cdef PyObjectSetIterator it
    cdef PyObjectSet s
    cdef object el
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

cpdef bint issubset_pyobject(PyObjectSet s, PyObjectSet sub) except *:
    if s is None or sub is None:
        raise TypeError("'NoneType' object is not iterable")

    if s.size() < sub.size():
        return False

    cdef PyObjectSetIterator it=sub.get_iter()
    cdef object el
    while it.has_next():
        el = it.next()
        if not s.contains(el):
            return False
    return True

cpdef PyObjectSet copy_pyobject(PyObjectSet s):
    if s is None:
        return None
    cdef PyObjectSet result = PyObjectSet(number_of_elements_hint=s.size())
    cdef PyObjectSetIterator it=s.get_iter()
    cdef object el
    while it.has_next():
        el = it.next()
        result.add(el)
    return result

cpdef void update_pyobject(PyObjectSet s, PyObjectSet other) except *:
    if s is None or other is None:
        raise TypeError("'NoneType' object is not iterable")
    cdef PyObjectSetIterator it=other.get_iter()
    cdef object el
    while it.has_next():
        el = it.next()
        s.add(el)  
   

