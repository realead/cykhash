

cdef extern from *:
    """
    //khash has nothing predefined for float/double
    //      in the first stet we add needed functionality
    #include <string.h>

    typedef float float32_t;
    typedef float32_t khfloat32_t;
    //don't pun and alias!
    //i.e. not static khint32_t f32_to_i32(khfloat32_t val){return *((khint32_t *)&val);} 
    //but:
    static khint32_t f32_to_i32(khfloat32_t val){
          khint32_t res; 
          memcpy(&res, &val, sizeof(khfloat32_t)); 
          return res;
    } 
    #define kh_float32_hash_func(key) (khint32_t)(f32_to_i32(key))

    //                                                       take care of nans:
    #define kh_float32_hash_equal(a, b) ((a) == (b) || ((b) != (b) && (a) != (a)))

    /*! @function
      @abstract     Instantiate a hash set containing 32-bit integer keys
      @param  name  Name of the hash table [symbol]
     */
    #define KHASH_SET_INIT_FLOAT32(name)										\
	    KHASH_INIT(name, khfloat32_t, char, 0, kh_float32_hash_func, kh_float32_hash_equal)

    //preprocessor creates needed struct-type and all function definitions 
    //set with keys of type float32 -> resulting typename: kh_float32set_t;
    KHASH_SET_INIT_FLOAT32(float32set)

    //TODO: add generated code:
    """
    pass

