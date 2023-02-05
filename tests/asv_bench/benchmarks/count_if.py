import numpy as np

from cykhash import count_if_int64, count_if_int64_from_iter, Int64Set_from, Int64Set_from_buffer
from cykhash import count_if_int32, count_if_int32_from_iter, Int32Set_from, Int32Set_from_buffer
from cykhash import count_if_float64, count_if_float64_from_iter, Float64Set_from, Float64Set_from_buffer
from cykhash import count_if_float32, count_if_float32_from_iter, Float32Set_from, Float32Set_from_buffer
from cykhash import count_if_pyobject, count_if_pyobject_from_iter,  PyObjectSet_from, PyObjectSet_from_buffer


CREATE_SET={
            np.float64 : Float64Set_from_buffer,
            np.float32 : Float32Set_from_buffer,
            np.int64 :   Int64Set_from_buffer,
            np.int32 :   Int32Set_from_buffer,
           }

COUNT_IF = {
            np.float64 : count_if_float64,
            np.float32 : count_if_float32,
            np.int64 : count_if_int64,
            np.int32 : count_if_int32,
           }


class CountIfObject:

    def setup(self):
        N=100_000
        self.set = PyObjectSet_from(x<<32 for x in range(N))
        np.random.seed(42)
        self.query = np.random.randint(0,N,N).astype(np.object_)

    def time_countif(self):
        count_if_pyobject(self.query, self.set)


class CountIfSameLongTuple:

    def setup(self):
        t = tuple(range(1000))
        self.set = PyObjectSet_from([t])
        self.query = np.array(["a"] + [t]*1000)

    def time_countif(self):
        count_if_pyobject(self.query, self.set)


class CountIfArange:
    params = [ 
        [np.float64, np.float32, np.int64, np.int32],
        [1_000, 2_000, 8_000, 10_000, 100_000, 1_000_000, 10_000_000, 100_000_000],
        [-2, 0, 2]
    ]
    param_names = ["dtype", "M", "offset_factor"]

    def setup(self, dtype, M, offset_factor):
        self.set = CREATE_SET[dtype](np.arange(M).astype(dtype))
        offset = int(M*offset_factor)
        N=10**6
        np.random.seed(42)
        self.query = np.random.randint(offset,M+offset,N).astype(dtype)

    def time_countif(self, dtype, M, offset_factor):
        COUNT_IF[dtype](self.query, self.set)


class CountIfRandomYes:
    params = [ 
        [np.float64, np.float32, np.int64, np.int32],  #
        [1_000, 2_000, 8_000, 10_000, 100_000, 1_000_000, 10_000_000, 100_000_000],
    ]
    param_names = ["dtype", "M"]

    def setup(self, dtype, M):
        np.random.seed(42)
        keys = (np.random.rand(M)*M).astype(dtype)
        self.set = CREATE_SET[dtype](keys)
        N=10**6
        self.query = (np.random.rand(N)*M).astype(dtype)

    def time_countif(self, dtype, M):
        COUNT_IF[dtype](self.query, self.set)


class CountIfRandomNo:
    params = [ 
        [np.float64, np.float32, np.int64, np.int32],  #
        [1_000, 2_000, 8_000, 10_000, 100_000, 1_000_000, 10_000_000, 100_000_000],
    ]
    param_names = ["dtype", "M"]

    def setup(self, dtype, M):
        np.random.seed(42)
        keys = (np.random.rand(M)*M).astype(dtype)
        self.set = CREATE_SET[dtype](keys)
        N=10**6
        self.query = (np.random.rand(N)*M+2*M).astype(dtype)

    def time_countif(self, dtype, M):
        COUNT_IF[dtype](self.query, self.set)


