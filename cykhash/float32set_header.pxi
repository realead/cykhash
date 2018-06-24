#
#
#
#Set of float32: 

include "init_float32set.pxi"
cdef extern from *:

    ctypedef struct kh_float32set_t:
        khint_t n_buckets, size, n_occupied, upper_bound
        uint32_t *flags
        float32_t *keys
        #size_t *vals  //dummy

    kh_float32set_t* kh_init_float32set() nogil
    void kh_destroy_float32set(kh_float32set_t*) nogil
    void kh_clear_float32set(kh_float32set_t*) nogil
    khint_t kh_get_float32set(kh_float32set_t*, float32_t) nogil
    void kh_resize_float32set(kh_float32set_t*, khint_t) nogil
    khint_t kh_put_float32set(kh_float32set_t*, float32_t, int*) nogil
    void kh_del_float32set(kh_float32set_t*, khint_t) nogil

    #specializing "kh_exist"-macro 
    bint kh_exist_float32set "kh_exist" (kh_float32set_t*, khint_t) nogil


cdef class Float32Set:
    cdef kh_float32set_t *table

    cdef bint contains(self, float32_t key) except *
    cdef Float32SetIterator get_iter(self)
    cpdef void add(self, float32_t key) except *
    cpdef void discard(self, float32_t key) except *
    


cdef class Float32SetIterator:
    cdef khint_t   it
    cdef khint_t   size
    cdef Float32Set  parent

    cdef bint has_next(self) except *
    cdef float32_t next(self) except *
    cdef void __move(self) except *

