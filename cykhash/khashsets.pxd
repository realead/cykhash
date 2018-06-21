from libc.stdint cimport  uint32_t,  int64_t



### Common definitions:

include "khash.pxi"
cdef extern from *:
    ctypedef uint32_t khint_t

### Set of int64: 

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

    #specializing "kh_exist"-macro - not needed (yet?)
    #bint kh_exist_int64set "kh_exist" (kh_int64set_t*, khiter_t) nogil

cdef class Int64Set:
    cdef kh_int64set_t *table

    cdef bint contains(self, int64_t key)
    cpdef add(self, int64_t key)
    cpdef discard(self, int64_t key)
