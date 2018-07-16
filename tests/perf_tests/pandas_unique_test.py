import numpy as np
import pandas as pd
import sys

N=int(sys.argv[1])

a=np.arange(N, dtype=np.int64)
b=pd.unique(a)


print("pandas LEN:", len(b))

