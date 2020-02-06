

############# int64 - test

from cykhash.khashmaps cimport Int64to64Map, Int64to64MapIterator, int64to64_key_val_pair

def use_int64(keys, values, query):
    s=Int64to64Map()
    for x,y in zip(keys, values):
        s.put_int64(x,y)
    assert s.size() == len(s) #to check size() exists
    res=[]
    for i in query:
        res.append(s.get_int64(i))
    return res

def use_float64(keys, values, query):
    s=Int64to64Map()
    for x,y in zip(keys, values):
        s.put_float64(x,y)
    assert s.size() == len(s) #to check size() exists
    res=[]
    for i in query:
        res.append(s.get_float64(i))
    return res


def as_py_list_int64(Int64to64Map db):
    cdef Int64to64MapIterator it = db.get_iter()
    cdef int64to64_key_val_pair p
    res=[]
    while it.has_next():
        p = it.next()
        res+= [p.key, p.val]
    return res

############# int32 - test


from cykhash.khashmaps cimport Int32to32Map, Int32to32MapIterator, int32to32_key_val_pair

def use_int32(keys, values, query):
    s=Int32to32Map()
    for x,y in zip(keys, values):
        s.put_int32(x,y)
    assert s.size() == len(s) #to check size() exists
    res=[]
    for i in query:
        res.append(s.get_int32(i))
    return res

def use_float32(keys, values, query):
    s=Int32to32Map()
    for x,y in zip(keys, values):
        s.put_float32(x,y)
    assert s.size() == len(s) #to check size() exists
    res=[]
    for i in query:
        res.append(s.get_float32(i))
    return res


def as_py_list_int32(Int32to32Map db):
    cdef Int32to32MapIterator it = db.get_iter()
    cdef int32to32_key_val_pair p
    res=[]
    while it.has_next():
        p = it.next()
        res+= [p.key, p.val]
    return res


############# float64 - test

from cykhash.khashmaps cimport Float64to64Map, Float64to64MapIterator, float64to64_key_val_pair

def use_int64_float64(keys, values, query):
    s=Float64to64Map()
    for x,y in zip(keys, values):
        s.put_int64(x,y)
    assert s.size() == len(s) #to check size() exists
    res=[]
    for i in query:
        res.append(s.get_int64(i))
    return res

def use_float64_float64(keys, values, query):
    s=Float64to64Map()
    for x,y in zip(keys, values):
        s.put_float64(x,y)
    assert s.size() == len(s) #to check size() exists
    res=[]
    for i in query:
        res.append(s.get_float64(i))
    return res


def as_py_list_int64_float64(Float64to64Map db):
    cdef Float64to64MapIterator it = db.get_iter()
    cdef float64to64_key_val_pair p
    res=[]
    while it.has_next():
        p = it.next()
        res+= [int(p.key), p.val]
    return res

############# float32 - test

from cykhash.khashmaps cimport Float32to32Map, Float32to32MapIterator, float32to32_key_val_pair

def use_int32_float32(keys, values, query):
    s=Float32to32Map()
    for x,y in zip(keys, values):
        s.put_int32(x,y)
    assert s.size() == len(s) #to check size() exists
    res=[]
    for i in query:
        res.append(s.get_int32(i))
    return res

def use_float32_float32(keys, values, query):
    s=Float32to32Map()
    for x,y in zip(keys, values):
        s.put_float32(x,y)
    assert s.size() == len(s) #to check size() exists
    res=[]
    for i in query:
        res.append(s.get_float32(i))
    return res


def as_py_list_int32_float32(Float32to32Map db):
    cdef Float32to32MapIterator it = db.get_iter()
    cdef float32to32_key_val_pair p
    res=[]
    while it.has_next():
        p = it.next()
        res+= [int(p.key), p.val]
    return res


############# float32 - test

from cykhash.khashmaps cimport PyObjectMap, PyObjectMapIterator, pyobject_key_val_pair

def use_pyobject(keys, values, query):
    s=PyObjectMap()
    for x,y in zip(keys, values):
        s.put_object(x,y)
    assert s.size() == len(s) #to check size() exists
    res=[]
    for i in query:
        res.append(s.get_object(i))
    return res

def as_py_list_pyobject(PyObjectMap db):
    cdef PyObjectMapIterator it = db.get_iter()
    cdef pyobject_key_val_pair p
    res=[]
    while it.has_next():
        p = it.next()
        res+= [int(<object>(p.key)), <object>(p.val)]
    return res




