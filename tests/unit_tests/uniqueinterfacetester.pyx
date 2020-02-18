

############# int64 - test

from cykhash.unique cimport unique_int64, unique_int32, unique_float64

def use_unique_int64(vals):
    return unique_int64(vals, .2)

def use_unique_int32(vals):
    return unique_int32(vals, .2)

def use_unique_float64(vals):
    return unique_float64(vals, .2)

