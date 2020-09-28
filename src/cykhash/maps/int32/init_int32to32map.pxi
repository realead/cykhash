

cdef extern from *:
    """
    // preprocessor creates needed struct-type and all function definitions

    // map with keys of type int32 -> und result int32
    // resulting typename: kh_int32to32map_t;
    KHASH_INIT(int32to32map, int32_t, int32_t, 1, murmur2_32to32, kh_int_hash_equal)
  

    """
    pass


