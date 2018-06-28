import numpy as np
import pandas as pd
import timeit

from cykhash import isin_int64, Int64Set_from

np.random.seed(0)
arr = np.random.randint(0, 20000, 10000)
res = np.zeros(arr.shape, np.uint8)
ser = pd.Series(arr)

NUMBER=100

print("n\tpandas(#look-up=10^n)\tcykhash(#look-up=10^n)")
for i in range(2,8):
    x_arr = np.array(range(10**i))
    int64set = Int64Set_from(range(10**i))  
    t1 = timeit.timeit("ser.isin(x_arr)", setup="from __main__ import ser, x_arr", number=NUMBER)/NUMBER
    t2 = timeit.timeit("isin_int64(ser.values, int64set, res)", setup = "from __main__ import isin_int64, ser, int64set, res", number=NUMBER)/NUMBER
    print(i,"\t",t1,"\t",t2)


