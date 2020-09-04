
include "init_pyobjectmap.pxi"
cdef extern from *:

    ctypedef struct kh_pyobjectmap_t:
        khint_t n_buckets, size, n_occupied, upper_bound
        uint32_t *flags
        pyobject_t *keys
        pyobject_t *vals  

    kh_pyobjectmap_t* kh_init_pyobjectmap() nogil
    void kh_destroy_pyobjectmap(kh_pyobjectmap_t*) nogil
    void kh_clear_pyobjectmap(kh_pyobjectmap_t*) nogil
    khint_t kh_get_pyobjectmap(kh_pyobjectmap_t*, pyobject_t) nogil
    void kh_resize_pyobjectmap(kh_pyobjectmap_t*, khint_t) nogil
    khint_t kh_put_pyobjectmap(kh_pyobjectmap_t*, pyobject_t, int* result) nogil
    void kh_del_pyobjectmap(kh_pyobjectmap_t*, khint_t) nogil

    #specializing "kh_exist"-macro 
    bint kh_exist_pyobjectmap "kh_exist" (kh_pyobjectmap_t*, khint_t) nogil


cdef class PyObjectMap:
    cdef kh_pyobjectmap_t *table

    cdef bint contains(self, object key) except *
    cdef PyObjectMapIterator get_iter(self, int view_type)
    cdef khint_t size(self) 
    cpdef void put_object(self, object key, object value) except *
    cpdef object get_object(self, object key)
    cpdef void discard(self, object key) except *
    

cdef struct pyobject_key_val_pair:
    pyobject_t key
    pyobject_t val


cdef class PyObjectMapIterator:
    cdef khint_t   it
    cdef khint_t   size
    cdef int       view_type
    cdef PyObjectMap  parent

    cdef bint has_next(self) except *
    cdef pyobject_key_val_pair next(self) except *
    cdef void __move(self) except *

cdef class PyObjectMapView:
    cdef PyObjectMap  parent
    cdef int       view_type

    cdef PyObjectMapIterator get_iter(self)

# other help functions:
cpdef void swap_pyobjectmap(PyObjectMap a, PyObjectMap b) except *


