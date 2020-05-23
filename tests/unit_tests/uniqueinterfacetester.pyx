

############# int64 - test

from cykhash.unique cimport unique_int64, unique_int32, unique_float64, unique_float32
from cykhash.unique cimport unique_stable_int64, unique_stable_int32, unique_stable_float64, unique_stable_float32 

def use_unique_int64(vals):
    return unique_int64(vals, .2)

def use_unique_stable_int64(vals):
    return unique_stable_int64(vals, .2)

def use_unique_int32(vals):
    return unique_int32(vals, .2)

def use_unique_stable_int32(vals):
    return unique_stable_int32(vals, .2)

def use_unique_float64(vals):
    return unique_float64(vals, .2)

def use_unique_stable_float64(vals):
    return unique_stable_float64(vals, .2)

def use_unique_float32(vals):
    return unique_float32(vals, .2)

def use_unique_stable_float32(vals):
    return unique_stable_float32(vals, .2)

