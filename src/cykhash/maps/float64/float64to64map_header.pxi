#
#
# Don't edit it, unless this is I_n_t_6_4_to_6_4_m_a_p header
#
# run sh all_from_XXX.sh to create it from blueprint -  I_n_t_6_4_to_6_4_m_a_p

include "init_float64to64map.pxi"

ctypedef float64_t key_float64_t

cdef extern from *:

    ctypedef struct kh_float64to64map_t:
        khint_t n_buckets, size, n_occupied, upper_bound
        uint32_t *flags
        key_float64_t *keys
        int64_t *vals  

    kh_float64to64map_t* kh_init_float64to64map() nogil
    void kh_destroy_float64to64map(kh_float64to64map_t*) nogil
    void kh_clear_float64to64map(kh_float64to64map_t*) nogil
    khint_t kh_get_float64to64map(kh_float64to64map_t*, key_float64_t) nogil
    void kh_resize_float64to64map(kh_float64to64map_t*, khint_t) nogil
    khint_t kh_put_float64to64map(kh_float64to64map_t*, key_float64_t, int* result) nogil
    void kh_del_float64to64map(kh_float64to64map_t*, khint_t) nogil

    #specializing "kh_exist"-macro 
    bint kh_exist_float64to64map "kh_exist" (kh_float64to64map_t*, khint_t) nogil


cdef class Float64to64Map:
    cdef kh_float64to64map_t *table
    cdef bint for_int

    cdef bint contains(self, key_float64_t key) except *
    cdef Float64to64MapIterator get_iter(self, int view_type)
    cdef khint_t size(self) 
    cpdef void put_int64(self, key_float64_t key, int64_t value) except *
    cpdef int64_t get_int64(self, key_float64_t key) except *
    cpdef void put_float64(self, key_float64_t key, float64_t value) except *
    cpdef float64_t get_float64(self, key_float64_t key) except *
    cpdef void discard(self, key_float64_t key) except *
    

cdef struct float64to64_key_val_pair:
    key_float64_t key
    int64_t val


cdef class Float64to64MapIterator:
    cdef khint_t   it
    cdef int       view_type
    cdef Float64to64Map  parent

    cdef bint has_next(self) except *
    cdef float64to64_key_val_pair next(self) except *
    cdef void __move(self) except *


cdef class Float64to64MapView:
    cdef Float64to64Map  parent
    cdef int       view_type

    cdef Float64to64MapIterator get_iter(self)


cpdef Float64to64Map Float64to64Map_from_int64_buffer(key_float64_t[:] keys, int64_t[:] vals, double size_hint=*)
cpdef Float64to64Map Float64to64Map_from_float64_buffer(key_float64_t[:] keys, float64_t[:] vals,double size_hint=*)

cpdef size_t Float64to64Map_to_int64(Float64to64Map map, key_float64_t[:] keys, int64_t[:] vals, bint stop_at_unknown=*, int64_t default_value=*) except *
cpdef size_t Float64to64Map_to_float64(Float64to64Map map, key_float64_t[:] keys, float64_t[:] vals, bint stop_at_unknown=*, float64_t default_value=*) except *


# other help functions:
cpdef void swap_float64map(Float64to64Map a, Float64to64Map b) except *
cpdef Float64to64Map copy_float64map(Float64to64Map s)
cpdef bint are_equal_float64map(Float64to64Map a, Float64to64Map b) except *
cpdef void update_float64map(Float64to64Map a, Float64to64Map b) except *
