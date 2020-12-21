
include "murmurhash.pxi"


# hash functions from khash.h:
cdef extern from *:
    """
        #ifndef CYKHASH_INTEGRAL_HASH_FUNS_PXI
        #define CYKHASH_INTEGRAL_HASH_FUNS_PXI
            inline uint32_t kh_int32_hash_func(uint32_t key){return key;}
            inline int      kh_int32_hash_equal(uint32_t a, uint32_t b) {return a==b;}

            inline uint32_t kh_int64_hash_func(uint64_t key){
                    return (uint32_t)((key)>>33^(key)^(key)<<11);
            }
            inline int      kh_int64_hash_equal(uint64_t a, uint64_t b) {return a==b;}
        #endif
    """
    pass



# handling floats
cdef extern from *:
    """
        #ifndef CYKHASH_FLOATING_HASH_FUNS_PXI
        #define CYKHASH_FLOATING_HASH_FUNS_PXI
            // correct handling for float64/32 <-> int64/32
            #include <string.h>

            typedef double float64_t;
            typedef float float32_t;

            //don't pun and alias:

            inline uint64_t f64_to_ui64(float64_t val){
                  uint64_t res; 
                  memcpy(&res, &val, sizeof(float64_t)); 
                  return res;
            } 

            inline float64_t ui64_to_f64(uint64_t val){
                  float64_t res; 
                  memcpy(&res, &val, sizeof(float64_t)); 
                  return res;
            }

            inline uint32_t f32_to_ui32(float32_t val){
                  uint32_t res; 
                  memcpy(&res, &val, sizeof(float32_t)); 
                  return res;
            } 

            inline float32_t ui32_to_f32(uint32_t val){
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

            inline uint32_t kh_float64_hash_func(float64_t val){
                  if(val==0.0){
                    return ZERO_HASH;
                  }
                  if(val!=val){
                   return NAN_HASH;
                  }
                  int64_t as_int = f64_to_ui64(val);
                  return murmur2_64to32(as_int);
            }

            //                                                       take care of nans:
            #define kh_float64_hash_equal(a, b) ((a) == (b) || ((b) != (b) && (a) != (a)))

            // 32bit
            typedef float float32_t;
            typedef float32_t khfloat32_t;


            inline uint32_t kh_float32_hash_func(float32_t val){ 
                  if(val==0.0){
                    return ZERO_HASH;
                  }
                  if(val!=val){
                   return NAN_HASH;
                  }    
                  int32_t as_int = f32_to_ui32(val);
                  return murmur2_32to32(as_int);
            }


            //                                                       take care of nans:
            #define kh_float32_hash_equal(a, b) ((a) == (b) || ((b) != (b) && (a) != (a)))
        #endif
    """  
    pass


cdef extern from *:
    """
        #ifndef CYKHASH_DEFINE_HASH_FUNS_PXI
        #define CYKHASH_DEFINE_HASH_FUNS_PXI


            // used hash-functions
            #define cykh_int32_hash_func murmur2_32to32
            #define cykh_int64_hash_func murmur2_64to32

            #define cykh_float32_hash_func kh_float32_hash_func
            #define cykh_float64_hash_func kh_float64_hash_func

            
            // used equality-functions
            #define cykh_int32_hash_equal kh_int32_hash_equal
            #define cykh_int64_hash_equal kh_int64_hash_equal

            #define cykh_float32_hash_equal kh_float32_hash_equal
            #define cykh_float64_hash_equal kh_float64_hash_equal

        #endif
    """
    pass
