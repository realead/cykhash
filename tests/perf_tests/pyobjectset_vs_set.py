import perfplot

from cykhash import PyObjectSet

def setmeup(n):
    print(n)
    s = set()
    p = PyObjectSet()

    for i in range(n):
        s.add(i)
        p.add(i)
    return (s,p)

def contains_set(sets):
    s = sets[0]
    n = len(s)//2
    for i in range(n, 3*n):
        i in s

def contains_pyobjectset(sets):
    p = sets[1]
    n = len(p)//2
    for i in range(n, 3*n):
        i in p

def discard_insert_set(sets):
    s = sets[0]
    n = len(s)
    for i in range(n):
        s.discard(i)
    for i in range(n):
        s.add(i)

def discard_insert_pyobjectset(sets):
    p = sets[1]
    n = len(p)
    for i in range(n):
        p.discard(i)
    for i in range(n):
        p.add(i)

def insert_set(sets):
    n = len(sets[1])
    s = set()
    for i in range(n):
        s.add(i)

def insert_pyobjectset(sets):
    p = PyObjectSet()
    n = len(sets[0])
    for i in range(n):
        p.add(i)
   
def insert_pyobjectset_preallocated(sets):
    n = len(sets[1])
    p = PyObjectSet(int(1.3*n))   
    for i in range(n):
        p.add(i)

if True:  
    perfplot.show(
        setup = setmeup,
        n_range=[2**k for k in range(18)],
        kernels=[
            #insert_set,
            #insert_pyobjectset,
            contains_set,
            contains_pyobjectset,
            discard_insert_set,
            discard_insert_pyobjectset,
            ],
        logx=False,
        logy=False,
        xlabel='number of operations',
        title = "pyobject_set vs set",
        equality_check = None,
        )

if True:
    perfplot.show(
        setup = setmeup,
        n_range=[2**k for k in range(18)],
        kernels=[
            insert_set,
            insert_pyobjectset,
            insert_pyobjectset_preallocated,
            #contains_set,
            #contains_pyobjectset,
            #discard_insert_set,
            #discard_insert_pyobjectset,
            ],
        logx=False,
        logy=False,
        xlabel='number of operations',
        title = "pyobject_set vs set",
        equality_check = None,
        )
