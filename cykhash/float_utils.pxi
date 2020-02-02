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

    """  
    pass
