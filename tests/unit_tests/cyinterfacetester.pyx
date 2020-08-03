

############# int64 - test

from cykhash.khashsets cimport Int64Set, Int64SetIterator, isin_int64, Int64Set_from_buffer

def py_isin_int64(query, db):
    s=Int64Set()
    for d in db:
        s.add(d)
    assert s.size() == len(s) #to check size() exists
    res=[]
    for i in query:
        res.append(False if s.contains(i)==0 else True)
    return res


def as_py_set_int64(Int64Set db):
    cdef Int64SetIterator it = db.get_iter()
    res=set()
    while it.has_next():
        res.add(it.next())
    return res

############# int32 - test

from cykhash.khashsets cimport Int32Set, Int32SetIterator, isin_int32, Int32Set_from_buffer

def py_isin_int32(query, db):
    s=Int32Set()
    for d in db:
        s.add(d)
    assert s.size() == len(s) #to check size() exists
    res=[]
    for i in query:
        res.append(False if s.contains(i)==0 else True)
    return res


def as_py_set_int32(Int32Set db):
    cdef Int32SetIterator it = db.get_iter()
    res=set()
    while it.has_next():
        res.add(it.next())
    return res


############# float64 - test

from cykhash.khashsets cimport Float64Set, Float64SetIterator, isin_float64, Float64Set_from_buffer

def py_isin_float64(query, db):
    s=Float64Set()
    for d in db:
        s.add(d)
    assert s.size() == len(s) #to check size() exists
    res=[]
    for i in query:
        res.append(False if s.contains(i)==0 else True)
    return res


def as_py_set_float64(Float64Set db):
    cdef Float64SetIterator it = db.get_iter()
    res=set()
    while it.has_next():
        res.add(it.next())
    return res



############# float32 - test

from cykhash.khashsets cimport Float32Set, Float32SetIterator, isin_float32, Float32Set_from_buffer

def py_isin_float32(query, db):
    s=Float32Set()
    for d in db:
        s.add(d)
    assert s.size() == len(s) #to check size() exists
    res=[]
    for i in query:
        res.append(False if s.contains(i)==0 else True)
    return res


def as_py_set_float32(Float32Set db):
    cdef Float32SetIterator it = db.get_iter()
    res=set()
    while it.has_next():
        res.add(it.next())
    return res


############# PyObject - test

from cykhash.khashsets cimport PyObjectSet, PyObjectSetIterator, isin_pyobject, PyObjectSet_from_buffer

def py_isin_pyobject(query, db):
    s=PyObjectSet()
    for d in db:
        s.add(d)
    assert s.size() == len(s) #to check size() exists
    res=[]
    for i in query:
        res.append(False if s.contains(i)==0 else True)
    return res


def as_py_set_pyobject(PyObjectSet db):
    cdef PyObjectSetIterator it = db.get_iter()
    res=set()
    while it.has_next():
        res.add(it.next())
    return res


