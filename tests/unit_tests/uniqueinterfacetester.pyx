

############# int64 - test

from cykhash.unique cimport unique_int64

def use_unique_int64(vals):
    return unique_int64(vals, .2)

