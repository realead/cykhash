#
#
# Don't edit it, unless this is I_n_t_6_4_S_e_t header
#
# run sh all_from_XXX.sh to create it from bluepring - I_n_t_6_4_S_e_t

include "init_float64set.pxi"
cdef extern from *:

    ctypedef struct kh_float64set_t:
        khint_t n_buckets, size, n_occupied, upper_bound
        uint32_t *flags
        float64_t *keys
        #size_t *vals  //dummy

    kh_float64set_t* kh_init_float64set() nogil
    void kh_destroy_float64set(kh_float64set_t*) nogil
    void kh_clear_float64set(kh_float64set_t*) nogil
    khint_t kh_get_float64set(kh_float64set_t*, float64_t) nogil
    void kh_resize_float64set(kh_float64set_t*, khint_t) nogil
    khint_t kh_put_float64set(kh_float64set_t*, float64_t, int*) nogil
    void kh_del_float64set(kh_float64set_t*, khint_t) nogil

    #specializing "kh_exist"-macro 
    bint kh_exist_float64set "kh_exist" (kh_float64set_t*, khint_t) nogil


cdef class Float64Set:
    cdef kh_float64set_t *table

    cdef bint contains(self, float64_t key) except *
    cdef Float64SetIterator get_iter(self)
    cdef khint_t size(self) 
    cpdef void add(self, float64_t key) except *
    cpdef void discard(self, float64_t key) except *
    


cdef class Float64SetIterator:
    cdef khint_t   it
    cdef khint_t   size
    cdef Float64Set  parent

    cdef bint has_next(self) except *
    cdef float64_t next(self) except *
    cdef void __move(self) except *


cpdef Float64Set Float64Set_from_buffer(float64_t[:] buf, double size_hint=*)


from libc.stdint cimport  uint8_t
cpdef void isin_float64(float64_t[:] query, Float64Set db, uint8_t[:] result) except *

cpdef bint all_float64(float64_t[:] query, Float64Set db) except *
cpdef bint all_float64_from_iter(object query, Float64Set db) except *

