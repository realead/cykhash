

# see float_utils.pxi for definitions

cdef extern from *:
    """
    /*! @function
      @abstract     Instantiate a hash set containing 32-bit integer keys
      @param  name  Name of the hash table [symbol]
     */
    #define KHASH_SET_INIT_FLOAT32(name)										\
	    KHASH_INIT(name, khfloat32_t, char, 0, kh_float32_hash_func_0_NAN, kh_float32_hash_equal)

    //preprocessor creates needed struct-type and all function definitions 
    //set with keys of type float32 -> resulting typename: kh_float32set_t;
    KHASH_SET_INIT_FLOAT32(float32set)

    //TODO: add generated code:
    """
    pass

