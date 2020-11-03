import numpy as np

from cykhash import unique_int64, unique_int32, unique_float64, unique_float32
from cykhash import unique_stable_int64, unique_stable_int32, unique_stable_float64, unique_stable_float32

UNIQUE={
            np.float64 : unique_float64,
            np.float32 : unique_float32,
            np.int64 :   unique_int64,
            np.int32 :   unique_int32,
           }

UNIQUE_STABLE = {
            np.float64 : unique_stable_float64,
            np.float32 : unique_stable_float32,
            np.int64 : unique_stable_int64,
            np.int32 : unique_stable_int32,
           }


class  UniqueArange:
    params = [ 
        [np.float64, np.float32, np.int64, np.int32],
        [1_000, 2_000, 8_000, 10_000, 100_000, 1_000_000, 10_000_000, 100_000_000],
    ]
    param_names = ["dtype", "M"]

    def setup(self, dtype, M):
        self.array = np.arange(M, dtype=dtype)

    def time_unique(self, dtype, M):
        UNIQUE[dtype](self.array)

    def time_unique_stable(self, dtype, M):
        UNIQUE_STABLE[dtype](self.array)

    def peakmem_unique(self, dtype, M):
        UNIQUE[dtype](self.array)

    def peakmem_unique_stable(self, dtype, M):
        UNIQUE_STABLE[dtype](self.array)


class  UniqueRandomDivFactor10:
    params = [ 
        [np.float64, np.float32, np.int64, np.int32],
        [1_000, 2_000, 8_000, 10_000, 100_000, 1_000_000, 10_000_000, 100_000_000],
    ]
    param_names = ["dtype", "M"]

    def setup(self, dtype, M):
        np.random.seed(42)
        self.array = np.random.randint(0, M//10, M).astype(dtype)

    def time_unique(self, dtype, M):
        UNIQUE[dtype](self.array)

    def time_unique_stable(self, dtype, M):
        UNIQUE_STABLE[dtype](self.array)

    def peakmem_unique(self, dtype, M):
        UNIQUE[dtype](self.array)

    def peakmem_unique_stable(self, dtype, M):
        UNIQUE_STABLE[dtype](self.array)


class  UniqueRandomDivFactor10Add220:
    params = [ 
        [np.float64, np.float32, np.int64, np.int32],
        [1_000, 2_000, 8_000, 10_000, 100_000, 1_000_000, 10_000_000, 100_000_000],
    ]
    param_names = ["dtype", "M"]

    def setup(self, dtype, M):
        np.random.seed(42)
        self.array = (np.random.randint(0, M//10, M)+2**26).astype(dtype)

    def time_unique(self, dtype, M):
        UNIQUE[dtype](self.array)

    def time_unique_stable(self, dtype, M):
        UNIQUE_STABLE[dtype](self.array)


class  UniqueRandomMulFactor10:
    params = [ 
        [np.float64, np.float32, np.int64, np.int32],
        [1_000, 2_000, 8_000, 10_000, 100_000, 1_000_000, 10_000_000, 100_000_000],
    ]
    param_names = ["dtype", "M"]

    def setup(self, dtype, M):
        np.random.seed(42)
        self.array = np.random.randint(0, M*10, M).astype(dtype)

    def time_unique(self, dtype, M):
        UNIQUE[dtype](self.array)

    def time_unique_stable(self, dtype, M):
        UNIQUE_STABLE[dtype](self.array)


class  UniqueSingle:
    params = [ 
        [np.float64, np.float32, np.int64, np.int32],
        [10_000_000, 100_000_000],
    ]
    param_names = ["dtype", "M"]

    def setup(self, dtype, M):
        self.array = np.ones(M, dtype=dtype)

    def peakmem_unique(self, dtype, M):
        UNIQUE[dtype](self.array)

    def peakmem_unique_stable(self, dtype, M):
        UNIQUE_STABLE[dtype](self.array)


