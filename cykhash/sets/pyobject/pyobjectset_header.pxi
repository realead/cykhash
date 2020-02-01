

include "init_pyobjectset.pxi"
cdef extern from *:
    ctypedef struct kh_pyobjectset_t:
        khint_t n_buckets, size, n_occupied, upper_bound
        uint32_t *flags
        pyobject_t *keys
        #size_t *vals  //dummy

    kh_pyobjectset_t* kh_init_pyobjectset() nogil
    void kh_destroy_pyobjectset(kh_pyobjectset_t*) nogil
    void kh_clear_pyobjectset(kh_pyobjectset_t*) nogil
    khint_t kh_get_pyobjectset(kh_pyobjectset_t*, pyobject_t) nogil
    void kh_resize_pyobjectset(kh_pyobjectset_t*, khint_t) nogil
    khint_t kh_put_pyobjectset(kh_pyobjectset_t*, pyobject_t, int*) nogil
    void kh_del_pyobjectset(kh_pyobjectset_t*, khint_t) nogil

    #specializing "kh_exist"-macro 
    bint kh_exist_pyobjectset "kh_exist" (kh_pyobjectset_t*, khint_t) nogil


cdef class PyObjectSet:
    cdef kh_pyobjectset_t *table

    cdef bint contains(self, object key) except *
    cdef PyObjectSetIterator get_iter(self)
    cdef khint_t size(self) 
    cpdef void add(self, object key) except *
    cpdef void discard(self, object key) except *
    


cdef class PyObjectSetIterator:
    cdef khint_t   it
    cdef khint_t   size
    cdef PyObjectSet  parent

    cdef bint has_next(self) except *
    cdef object next(self)
    cdef void __move(self) except *

