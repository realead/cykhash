import perfplot

from cykhash import PyObjectMap

def setmeup(n):
    print(n)
    s = dict()
    p = PyObjectMap()

    for i in range(n):
        s[i] = i
        p[i] = i
    return (s,p)

def contains_dict(maps):
    s = maps[0]
    n = len(s)//2
    for i in range(n, 3*n):
        i in s

def contains_pyobjectmap(maps):
    p = maps[1]
    n = len(p)//2
    for i in range(n, 3*n):
        i in p

def discard_insert_dict(maps):
    s = maps[0]
    n = len(s)
    for i in range(n):
        del s[i]
    for i in range(n):
        s[i] = i

def discard_insert_pyobjectmap(maps):
    p = maps[1]
    n = len(p)
    for i in range(n):
        p.discard(i)
    for i in range(n):
        p[i] = i

def insert_dict(maps):
    n = len(maps[1])
    s = dict()
    for i in range(n):
        s[i] = i

def insert_pyobjectmap(maps):
    p = PyObjectMap()
    n = len(maps[0])
    for i in range(n):
        p[i] = i
  
def insert_pyobjectmap_preallocated(maps):
    n = len(maps[1])
    p = PyObjectMap(int(1.3*n))   
    for i in range(n):
        p[i] = i

if True:  
    perfplot.show(
        setup = setmeup,
        n_range=[2**k for k in range(18)],
        kernels=[
            #insert_set,
            #insert_pyobjectset,
            contains_dict,
            contains_pyobjectmap,
            discard_insert_dict,
            discard_insert_pyobjectmap,
            ],
        logx=False,
        logy=False,
        xlabel='number of operations',
        title = "pyobject_map vs dict",
        equality_check = None,
        )

if True:
    perfplot.show(
        setup = setmeup,
        n_range=[2**k for k in range(18)],
        kernels=[
            insert_dict,
            insert_pyobjectmap,
            insert_pyobjectmap_preallocated,
            #contains_set,
            #contains_pyobjectset,
            #discard_insert_set,
            #discard_insert_pyobjectset,
            ],
        logx=False,
        logy=False,
        xlabel='number of operations',
        title = "pyobject_map vs dict",
        equality_check = None,
        )
