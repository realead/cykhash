import numpy as np

import cykhash as cyk


MAP_TO_INT            = {np.int32: cyk.Int32toInt32Map_to,
                         np.int64: cyk.Int64toInt64Map_to,
                         np.float64 : cyk.Float64toInt64Map_to,
                         np.float32 : cyk.Float32toInt32Map_to,
                         np.object_ : cyk.PyObjectMap_to,
}

CREATOR_FROM_INT      = {np.int32: cyk.Int32toInt32Map_from_buffers,
                         np.int64: cyk.Int64toInt64Map_from_buffers,
                         np.float64 : cyk.Float64toInt64Map_from_buffers,
                         np.float32 : cyk.Float32toInt32Map_from_buffers,
                         np.object_ : cyk.PyObjectMap_from_buffers,
}


INT_DTYPE      = {np.int32: np.int32,
                 np.int64: np.int64,
                 np.float64 : np.int64,
                 np.float32 : np.int32,
                 np.object_ : np.object_,
}





class MapToWithArange:

    params = [ 
        [np.float64, np.float32, np.int64, np.int32, np.object_],  #
        [1_000, 2_000, 8_000, 10_000, 100_000, 1_000_000], #problem when quadratic behavior is triggered: [10, 100, 1000, 2_000, 8_000, 10_000, 100_000, 256_000, 1_000_000, 10_000_000],
    ]
    param_names = ["dtype", "M"]

    def setup(self, dtype, M):
        keys = np.arange(M).astype(dtype)
        vals = np.zeros_like(keys, dtype=INT_DTYPE[dtype])
        self.map = CREATOR_FROM_INT[dtype](keys, vals)
        self.query = np.repeat(keys, 5)
        self.result = np.ones_like(self.query, dtype=INT_DTYPE[dtype])

    def time_mapto(self, dtype, M):
        MAP_TO_INT[dtype](self.map, self.query, self.result, False)


class MapToWithRandom:

    params = [ 
        [np.float64, np.float32, np.int64, np.int32, np.object_],  #
        [1_000, 2_000, 8_000, 10_000, 100_000, 1_000_000], #problem when quadratic behavior is triggered: [10, 100, 1000, 2_000, 8_000, 10_000, 100_000, 256_000, 1_000_000, 10_000_000],
    ]
    param_names = ["dtype", "M"]

    def setup(self, dtype, M):
        keys = np.arange(M).astype(dtype)
        vals = np.zeros_like(keys, dtype=INT_DTYPE[dtype])
        self.map = CREATOR_FROM_INT[dtype](keys, vals)
        np.random.seed(42)
        self.query = np.random.randint(0, M, 5*M).astype(dtype)
        self.result = np.ones_like(self.query, dtype=INT_DTYPE[dtype])

    def time_mapto(self, dtype, M):
        MAP_TO_INT[dtype](self.map, self.query, self.result, False)


class MapToWithRandomFloat:

    params = [ 
        [np.float64, np.float32],  #
        [1_000, 2_000, 8_000, 10_000, 100_000, 1_000_000], #problem when quadratic behavior is triggered: [10, 100, 1000, 2_000, 8_000, 10_000, 100_000, 256_000, 1_000_000, 10_000_000],
    ]
    param_names = ["dtype", "M"]

    def setup(self, dtype, M):
        np.random.seed(42)
        keys = np.arange(M).astype(dtype)
        vals = np.zeros_like(keys, dtype=INT_DTYPE[dtype])
        self.map = CREATOR_FROM_INT[dtype](keys, vals)
        self.query = np.repeat(keys, 5)
        self.result = np.ones_like(self.query, dtype=INT_DTYPE[dtype])

    def time_mapto(self, dtype, M):
        MAP_TO_INT[dtype](self.map, self.query, self.result, False)


class MapWithRandomScaledFloat:

    params = [ 
        [np.float64, np.float32],  #
        [1_000, 2_000, 8_000, 10_000, 100_000, 1_000_000], #problem when quadratic behavior is triggered: [10, 100, 1000, 2_000, 8_000, 10_000, 100_000, 256_000, 1_000_000, 10_000_000],
    ]
    param_names = ["dtype", "M"]

    def setup(self, dtype, M):
        np.random.seed(42)
        keys = (np.random.rand(M) * 100*M).astype(dtype)
        vals = np.zeros_like(keys, dtype=INT_DTYPE[dtype])
        self.map = CREATOR_FROM_INT[dtype](keys, vals)
        self.query = np.repeat(keys, 5)
        self.result = np.ones_like(self.query, dtype=INT_DTYPE[dtype])

    def time_mapto(self, dtype, M):
        MAP_TO_INT[dtype](self.map, self.query, self.result, False)


