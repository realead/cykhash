
from cykhash.khashsets cimport Int64Set

def isin(query, db):
    s=Int64Set()
    for d in db:
        s.add(d)
    res=[]
    for i in query:
        res.append(False if s.contains(i)==0 else True)
    return res
