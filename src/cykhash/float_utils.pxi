cdef extern from *:
    """
    // correct handling for float64/32 <-> int64/32
    #include <string.h>

    typedef double float64_t;
    typedef float float32_t;

    //don't pun and alias:

    inline int64_t f64_to_i64(float64_t val){
          int64_t res; 
          memcpy(&res, &val, sizeof(float64_t)); 
          return res;
    } 

    inline float64_t i64_to_f64(int64_t val){
          float64_t res; 
          memcpy(&res, &val, sizeof(float64_t)); 
          return res;
    }

    inline int32_t f32_to_i32(float32_t val){
          int32_t res; 
          memcpy(&res, &val, sizeof(float32_t)); 
          return res;
    } 

    inline float32_t i32_to_f32(int32_t val){
          float32_t res; 
          memcpy(&res, &val, sizeof(float32_t)); 
          return res;
    }

    // HASH AND EQUAL FUNCTIONS:
    // 64bit
    //khash has nothing predefined for float/double
    //      in the first stet we add needed functionality
    typedef float64_t khfloat64_t;

    #define ZERO_HASH 0
    #define NAN_HASH  0

    inline khint32_t kh_float64_hash_func(float64_t val){
          if(val==0.0){
            return ZERO_HASH;
          }
          if(val!=val){
           return NAN_HASH;
          }
          Py_hash_t hash = _Py_HashDouble(val);
          return (khint32_t)((hash)>>33^(hash)^(hash)<<11);
    }

    //                                                       take care of nans:
    #define kh_float64_hash_equal(a, b) ((a) == (b) || ((b) != (b) && (a) != (a)))

    // 32bit
    typedef float float32_t;
    typedef float32_t khfloat32_t;


    inline khint32_t kh_float32_hash_func(float32_t val){
          return kh_float64_hash_func(val);
    }


    //                                                       take care of nans:
    #define kh_float32_hash_equal(a, b) ((a) == (b) || ((b) != (b) && (a) != (a)))

    """  
    pass
