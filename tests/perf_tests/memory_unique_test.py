import numpy as np
import pandas as pd
import sys

import resource
import psutil

from cykhash import unique_int64, unique_int32

fun_name = sys.argv[1]
N=int(sys.argv[2])

a=np.arange(N, dtype=np.int64)


process = psutil.Process()
old = process.memory_info().rss
old_max = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024

if fun_name == "pandas":
    b=pd.unique(a)
else: 
    b=np.frombuffer(memoryview(unique_int64(a)))

new_max = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024

if new_max>old_max:
    overhead_in_bytes = new_max - old
    print(len(b),  overhead_in_bytes/float(N*8) )
else:
    print(len(b),   "too small")


