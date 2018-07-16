import pyximport; 
import numpy as np
pyximport.install(setup_args={'include_dirs': np.get_include()})

import cyunique


import sys
N=int(sys.argv[1])

a=np.arange(N, dtype=np.int64)
b=cyunique.unique_int64(a)

print("cyunique LEN:", len(b))

