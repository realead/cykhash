

cdef extern from *:
    """
    // preprocessor creates needed struct-type and all function definitions

    // map with keys of type int64 -> und result int64
    // resulting typename: kh_int64to64map_t;
    KHASH_INIT(int64to64map, int64_t, int64_t, 1, kh_int64_hash_func, kh_int64_hash_equal)
  

    """
    pass


