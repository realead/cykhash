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


class CreateArange:

    params = [ 
        [np.float64, np.float32, np.int64, np.int32],  #
        [1_000, 2_000, 8_000, 10_000, 100_000, 1_000_000], #problem when quadratic behavior is triggered: [10, 100, 1000, 2_000, 8_000, 10_000, 100_000, 256_000, 1_000_000, 10_000_000],
    ]
    param_names = ["dtype", "M"]

    def setup(self, dtype, M):
        self.keys = np.arange(M).astype(dtype)

    def time_create(self, dtype, M):
        CREATE_SET[dtype](self.keys)


class CreateRandom:

    params = [ 
        [np.float64, np.float32],  #
        [1_000, 2_000, 8_000, 10_000, 100_000, 1_000_000], #problem when quadratic behavior is triggered: [10, 100, 1000, 2_000, 8_000, 10_000, 100_000, 256_000, 1_000_000, 10_000_000],
    ]
    param_names = ["dtype", "M"]

    def setup(self, dtype, M):
        np.random.seed(42)
        self.keys = np.random.rand(M).astype(dtype)

    def time_create(self, dtype, M):
        CREATE_SET[dtype](self.keys)


class CreateRandomScaled:

    params = [ 
        [np.float64, np.float32, np.int64, np.int32],  #
        [1_000, 2_000, 8_000, 10_000, 100_000, 1_000_000], #problem when quadratic behavior is triggered: [10, 100, 1000, 2_000, 8_000, 10_000, 100_000, 256_000, 1_000_000, 10_000_000],
    ]
    param_names = ["dtype", "M"]

    def setup(self, dtype, M):
        np.random.seed(42)
        self.keys = (np.random.rand(M) * 100*M).astype(dtype)

    def time_create(self, dtype, M):
        CREATE_SET[dtype](self.keys)


