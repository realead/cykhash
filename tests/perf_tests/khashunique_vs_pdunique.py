import perfplot
import numpy as np
import pandas as pd

from cykhash import unique_int64, unique_int32


def pandas_unique64(bufs):
    pd.unique(bufs[0])

def pandas_unique32(bufs):
    pd.unique(bufs[1])

def cykhash_unique64(bufs):
    unique_int64(bufs[0])

def cykhash_unique32(bufs):
    unique_int32(bufs[1])


if True:  
    perfplot.show(
        setup = lambda n : (np.arange(n, dtype=np.int64), np.arange(n, dtype=np.int32)),
        n_range=[2**k for k in range(5,20)],
        kernels=[
            pandas_unique64,
            pandas_unique32,
            cykhash_unique64,
            cykhash_unique32,
            ],
        logx=False,
        logy=False,
        xlabel='number of elements',
        title = "pd.unique vs cykhash.unique",
        equality_check = None,
        )
