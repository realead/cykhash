

cdef extern from *:
    """
    //khash has nothing predefined for float/double
    //      in the first stet we add needed functionality
    #include <math.h>

    typedef double float64_t;
    typedef float64_t khfloat64_t;

    //right for all but not -0.0 and NAN
    #define kh_float64_hash_func(key) (khint32_t)((f64_to_i64(key))>>33^(f64_to_i64(key))^(f64_to_i64(key))<<11)

    //right for all except NAN
    #define kh_float64_hash_func_0(key) ((key)==0.0 ? kh_float64_hash_func(0.0) : kh_float64_hash_func(key))

    //right for all, also 0.0 and NAN
    #define kh_float64_hash_func_0_NAN(key) ((key) != (key) ? kh_float64_hash_func_0(NAN) : kh_float64_hash_func(key))

    //                                                       take care of nans:
    #define kh_float64_hash_equal(a, b) ((a) == (b) || ((b) != (b) && (a) != (a)))

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

