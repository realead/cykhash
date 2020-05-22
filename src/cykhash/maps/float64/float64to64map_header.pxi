
include "init_float64to64map.pxi"
cdef extern from *:

    ctypedef struct kh_float64to64map_t:
        khint_t n_buckets, size, n_occupied, upper_bound
        uint32_t *flags
        float64_t *keys
        int64_t *vals  

    kh_float64to64map_t* kh_init_float64to64map() nogil
    void kh_destroy_float64to64map(kh_float64to64map_t*) nogil
    void kh_clear_float64to64map(kh_float64to64map_t*) nogil
    khint_t kh_get_float64to64map(kh_float64to64map_t*, float64_t) nogil
    void kh_resize_float64to64map(kh_float64to64map_t*, khint_t) nogil
    khint_t kh_put_float64to64map(kh_float64to64map_t*, float64_t, int* result) nogil
    void kh_del_float64to64map(kh_float64to64map_t*, khint_t) nogil

    #specializing "kh_exist"-macro 
    bint kh_exist_float64to64map "kh_exist" (kh_float64to64map_t*, khint_t) nogil


cdef class Float64to64Map:
    cdef kh_float64to64map_t *table
    cdef bint for_int

    cdef bint contains(self, float64_t key) except *
    cdef Float64to64MapIterator get_iter(self)
    cdef khint_t size(self) 
    cpdef void put_int64(self, float64_t key, int64_t value) except *
    cpdef int64_t get_int64(self, float64_t key) except *
    cpdef void put_float64(self, float64_t key, float64_t value) except *
    cpdef float64_t get_float64(self, float64_t key) except *
    cpdef void discard(self, float64_t key) except *
    

cdef struct float64to64_key_val_pair:
    float64_t key
    int64_t val


cdef class Float64to64MapIterator:
    cdef khint_t   it
    cdef khint_t   size
    cdef Float64to64Map  parent

    cdef bint has_next(self) except *
    cdef float64to64_key_val_pair next(self) except *
    cdef void __move(self) except *

