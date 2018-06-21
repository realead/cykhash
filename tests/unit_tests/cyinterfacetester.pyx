
from cykhash.khashsets cimport Int64Set, Int64SetIterator

def isin(query, db):
    s=Int64Set()
    for d in db:
        s.add(d)
    res=[]
    for i in query:
        res.append(False if s.contains(i)==0 else True)
    return res


def as_py_set(Int64Set db):
    cdef Int64SetIterator it = db.get_iter()
    res=set()
    while it.has_next():
        res.add(it.next())
    return res
