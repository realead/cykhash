#
#
# Don't edit it, unless this is I_n_t_6_4_to_6_4_m_a_p header
#
# run sh all_from_XXX.sh to create it from blueprint -  I_n_t_6_4_to_6_4_m_a_p

include "init_int32to32map.pxi"

ctypedef int32_t key_int32_t

cdef extern from *:

    ctypedef struct kh_int32to32map_t:
        khint_t n_buckets, size, n_occupied, upper_bound
        uint32_t *flags
        key_int32_t *keys
        int32_t *vals  

    kh_int32to32map_t* kh_init_int32to32map() nogil
    void kh_destroy_int32to32map(kh_int32to32map_t*) nogil
    void kh_clear_int32to32map(kh_int32to32map_t*) nogil
    khint_t kh_get_int32to32map(kh_int32to32map_t*, key_int32_t) nogil
    void kh_resize_int32to32map(kh_int32to32map_t*, khint_t) nogil
    khint_t kh_put_int32to32map(kh_int32to32map_t*, key_int32_t, int* result) nogil
    void kh_del_int32to32map(kh_int32to32map_t*, khint_t) nogil

    #specializing "kh_exist"-macro 
    bint kh_exist_int32to32map "kh_exist" (kh_int32to32map_t*, khint_t) nogil


cdef class Int32to32Map:
    cdef kh_int32to32map_t *table
    cdef bint for_int

    cdef bint contains(self, key_int32_t key) except *
    cdef Int32to32MapIterator get_iter(self, int view_type)
    cdef khint_t size(self) 
    cpdef void put_int32(self, key_int32_t key, int32_t value) except *
    cpdef int32_t get_int32(self, key_int32_t key) except *
    cpdef void put_float32(self, key_int32_t key, float32_t value) except *
    cpdef float32_t get_float32(self, key_int32_t key) except *
    cpdef void discard(self, key_int32_t key) except *
    

cdef struct int32to32_key_val_pair:
    key_int32_t key
    int32_t val


cdef class Int32to32MapIterator:
    cdef khint_t   it
    cdef int       view_type
    cdef Int32to32Map  parent

    cdef bint has_next(self) except *
    cdef int32to32_key_val_pair next(self) except *
    cdef void __move(self) except *


cdef class Int32to32MapView:
    cdef Int32to32Map  parent
    cdef int       view_type

    cdef Int32to32MapIterator get_iter(self)

# other help functions:
cpdef void swap_int32map(Int32to32Map a, Int32to32Map b) except *
cpdef Int32to32Map copy_int32map(Int32to32Map s)
cpdef bint are_equal_int32map(Int32to32Map a, Int32to32Map b) except *
