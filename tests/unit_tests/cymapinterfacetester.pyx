

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

# ToDo
