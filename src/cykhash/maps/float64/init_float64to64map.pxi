
# see float_utils.pxi for definitions

cdef extern from *:
    """
    // preprocessor creates needed struct-type and all function definitions

    // map with keys of type float64 -> und result int64

    #define KHASH_MAP_INIT_FLOAT64(name, khval_t)								\
	    KHASH_INIT(name, khfloat64_t, khval_t, 1, kh_float64_hash_func_0_NAN, kh_float64_hash_equal)

    KHASH_MAP_INIT_FLOAT64(float64to64map, int64_t)

    """
    pass


