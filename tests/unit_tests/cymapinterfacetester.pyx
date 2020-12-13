

############# int64 - test

from cykhash.khashmaps cimport Int64toInt64Map, Int64toFloat64Map, Int64toInt64MapIterator, int64toint64_key_val_pair

def use_int64(keys, values, query):
    s=Int64toInt64Map()
    for x,y in zip(keys, values):
        s.cput(x,y)
    assert s.size() == len(s) #to check size() exists
    res=[]
    for i in query:
        res.append(s.cget(i))
    return res

def use_float64(keys, values, query):
    s=Int64toFloat64Map()
    for x,y in zip(keys, values):
        s.cput(x,y)
    assert s.size() == len(s) #to check size() exists
    res=[]
    for i in query:
        res.append(s.cget(i))
    return res


def as_py_list_int64(Int64toInt64Map db):
    cdef Int64toInt64MapIterator it = db.get_iter(2)
    cdef int64toint64_key_val_pair p
    res=[]
    while it.has_next():
        p = it.next()
        res+= [p.key, p.val]
    return res

############# int32 - test


from cykhash.khashmaps cimport Int32toInt32Map, Int32toFloat32Map, Int32toInt32MapIterator, int32toint32_key_val_pair

def use_int32(keys, values, query):
    s=Int32toInt32Map()
    for x,y in zip(keys, values):
        s.cput(x,y)
    assert s.size() == len(s) #to check size() exists
    res=[]
    for i in query:
        res.append(s.cget(i))
    return res

def use_float32(keys, values, query):
    s=Int32toFloat32Map()
    for x,y in zip(keys, values):
        s.cput(x,y)
    assert s.size() == len(s) #to check size() exists
    res=[]
    for i in query:
        res.append(s.cget(i))
    return res


def as_py_list_int32(Int32toInt32Map db):
    cdef Int32toInt32MapIterator it = db.get_iter(2)
    cdef int32toint32_key_val_pair p
    res=[]
    while it.has_next():
        p = it.next()
        res+= [p.key, p.val]
    return res


############# float64 - test

from cykhash.khashmaps cimport Float64toInt64Map, Float64toFloat64Map, Float64toInt64MapIterator, float64toint64_key_val_pair

def use_int64_float64(keys, values, query):
    s=Float64toInt64Map()
    for x,y in zip(keys, values):
        s.cput(x,y)
    assert s.size() == len(s) #to check size() exists
    res=[]
    for i in query:
        res.append(s.cget(i))
    return res

def use_float64_float64(keys, values, query):
    s=Float64toFloat64Map()
    for x,y in zip(keys, values):
        s.cput(x,y)
    assert s.size() == len(s) #to check size() exists
    res=[]
    for i in query:
        res.append(s.cget(i))
    return res


def as_py_list_int64_float64(Float64toInt64Map db):
    cdef Float64toInt64MapIterator it = db.get_iter(2)
    cdef float64toint64_key_val_pair p
    res=[]
    while it.has_next():
        p = it.next()
        res+= [int(p.key), p.val]
    return res

############# float32 - test

from cykhash.khashmaps cimport Float32toInt32Map, Float32toFloat32Map, Float32toInt32MapIterator, float32toint32_key_val_pair

def use_int32_float32(keys, values, query):
    s=Float32toInt32Map()
    for x,y in zip(keys, values):
        s.cput(x,y)
    assert s.size() == len(s) #to check size() exists
    res=[]
    for i in query:
        res.append(s.cget(i))
    return res

def use_float32_float32(keys, values, query):
    s=Float32toFloat32Map()
    for x,y in zip(keys, values):
        s.cput(x,y)
    assert s.size() == len(s) #to check size() exists
    res=[]
    for i in query:
        res.append(s.cget(i))
    return res


def as_py_list_int32_float32(Float32toInt32Map db):
    cdef Float32toInt32MapIterator it = db.get_iter(2)
    cdef float32toint32_key_val_pair p
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
        s.cput(x,y)
    assert s.size() == len(s) #to check size() exists
    res=[]
    for i in query:
        res.append(s.cget(i))
    return res

def as_py_list_pyobject(PyObjectMap db):
    cdef PyObjectMapIterator it = db.get_iter(2)
    cdef pyobject_key_val_pair p
    res=[]
    while it.has_next():
        p = it.next()
        res+= [int(<object>(p.key)), <object>(p.val)]
    return res




