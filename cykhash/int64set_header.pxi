#
# This is a blueprint for other implementations
#
#Set of int64: 

include "init_int64set.pxi"
cdef extern from *:

    ctypedef struct kh_int64set_t:
        khint_t n_buckets, size, n_occupied, upper_bound
        uint32_t *flags
        int64_t *keys
        #size_t *vals  //dummy

    kh_int64set_t* kh_init_int64set() nogil
    void kh_destroy_int64set(kh_int64set_t*) nogil
    void kh_clear_int64set(kh_int64set_t*) nogil
    khint_t kh_get_int64set(kh_int64set_t*, int64_t) nogil
    void kh_resize_int64set(kh_int64set_t*, khint_t) nogil
    khint_t kh_put_int64set(kh_int64set_t*, int64_t, int*) nogil
    void kh_del_int64set(kh_int64set_t*, khint_t) nogil

    #specializing "kh_exist"-macro 
    bint kh_exist_int64set "kh_exist" (kh_int64set_t*, khint_t) nogil


cdef class Int64Set:
    cdef kh_int64set_t *table

    cdef bint contains(self, int64_t key) except *
    cdef Int64SetIterator get_iter(self)
    cpdef void add(self, int64_t key) except *
    cpdef void discard(self, int64_t key) except *
    


cdef class Int64SetIterator:
    cdef khint_t   it
    cdef khint_t   size
    cdef Int64Set  parent

    cdef bint has_next(self) except *
    cdef int64_t next(self) except *
    cdef void __move(self) except *

