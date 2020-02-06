
include "init_float32to32map.pxi"
cdef extern from *:

    ctypedef struct kh_float32to32map_t:
        khint_t n_buckets, size, n_occupied, upper_bound
        uint32_t *flags
        float32_t *keys
        int32_t *vals  

    kh_float32to32map_t* kh_init_float32to32map() nogil
    void kh_destroy_float32to32map(kh_float32to32map_t*) nogil
    void kh_clear_float32to32map(kh_float32to32map_t*) nogil
    khint_t kh_get_float32to32map(kh_float32to32map_t*, float32_t) nogil
    void kh_resize_float32to32map(kh_float32to32map_t*, khint_t) nogil
    khint_t kh_put_float32to32map(kh_float32to32map_t*, float32_t, int* result) nogil
    void kh_del_float32to32map(kh_float32to32map_t*, khint_t) nogil

    #specializing "kh_exist"-macro 
    bint kh_exist_float32to32map "kh_exist" (kh_float32to32map_t*, khint_t) nogil


cdef class Float32to32Map:
    cdef kh_float32to32map_t *table
    cdef bint for_int32

    cdef bint contains(self, float32_t key) except *
    cdef Float32to32MapIterator get_iter(self)
    cdef khint_t size(self) 
    cpdef void put_int32(self, float32_t key, int32_t value) except *
    cpdef int32_t get_int32(self, float32_t key) except *
    cpdef void put_float32(self, float32_t key, float32_t value) except *
    cpdef float32_t get_float32(self, float32_t key) except *
    cpdef void discard(self, float32_t key) except *
    

cdef struct float32to32_key_val_pair:
    float32_t key
    int32_t val


cdef class Float32to32MapIterator:
    cdef khint_t   it
    cdef khint_t   size
    cdef Float32to32Map  parent

    cdef bint has_next(self) except *
    cdef float32to32_key_val_pair next(self) except *
    cdef void __move(self) except *

