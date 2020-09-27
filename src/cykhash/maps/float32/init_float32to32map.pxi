
# see float_utils.pxi for definitions

cdef extern from *:
    """
    // preprocessor creates needed struct-type and all function definitions

    // map with keys of type float32 -> und result int32

    #define KHASH_MAP_INIT_FLOAT32(name, khval_t)								\
	    KHASH_INIT(name, khfloat32_t, khval_t, 1, kh_float32_hash_func_0_NAN, kh_float32_hash_equal)

    KHASH_MAP_INIT_FLOAT64(float32to32map, int32_t)

    """
    pass


