

cdef extern from *:
    """
    /*! @function
      @abstract     Instantiate a hash set containing 64-bit integer keys
      @param  name  Name of the hash table [symbol]
     */
    #define KHASH_SET_INIT_FLOAT64(name)										\
	    KHASH_INIT(name, khfloat64_t, char, 0, kh_float64_hash_func_0_NAN, kh_float64_hash_equal)

    //preprocessor creates needed struct-type and all function definitions 
    //set with keys of type float64 -> resulting typename: kh_float64set_t;
    KHASH_SET_INIT_FLOAT64(float64set)

    //TODO: add generated code:
    """
    pass

