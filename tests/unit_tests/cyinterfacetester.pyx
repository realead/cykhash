
from cykhash.khashsets cimport Int64Set

def isin(query, db):
    s=Int64Set()
    for d in db:
        s.add(d)
    res=[]
    for i in query:
        res.append(s.contains(i))
    return res
