

cdef extern from *:
    """
    //khash has nothing predefined for float/double
    //      in the first stet we add needed functionality
    #include <string.h>

    typedef double float64_t;
    typedef float64_t khfloat64_t;
    //don't pun and alias!
    //i.e. not static khint64_t f64_to_i64(khfloat64_t val){return *((khint64_t *)&val);} 
    //but:
    static khint64_t f64_to_i64(khfloat64_t val){
          khint64_t res; 
          memcpy(&res, &val, sizeof(khfloat64_t)); 
          return res;
    } 
    #define kh_float64_hash_func(key) (khint32_t)((f64_to_i64(key))>>33^(f64_to_i64(key))^(f64_to_i64(key))<<11)

    //                                                       take care of nans:
    #define kh_float64_hash_equal(a, b) ((a) == (b) || ((b) != (b) && (a) != (a)))

    /*! @function
      @abstract     Instantiate a hash set containing 64-bit integer keys
      @param  name  Name of the hash table [symbol]
     */
    #define KHASH_SET_INIT_FLOAT64(name)										\
	    KHASH_INIT(name, khfloat64_t, char, 0, kh_float64_hash_func, kh_float64_hash_equal)

    //preprocessor creates needed struct-type and all function definitions 
    //set with keys of type float64 -> resulting typename: kh_float64set_t;
    KHASH_SET_INIT_FLOAT64(float64set)

    //TODO: add generated code:
    """
    pass

